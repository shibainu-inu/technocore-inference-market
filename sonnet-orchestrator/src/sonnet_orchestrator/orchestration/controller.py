"""The control loop. Deterministic given adapters + clock; every tick:

    receipts → reconcile prefix → health → cover / hand-off → replan → repost table on version change
    → landing → complete → publish / submit

Planner and solver are injected (``planner_fn``, ``assign_fn``) and default to lazy imports of
``planner.beam.plan_poem`` and ``solver.assignment.assign`` so this module never hard-depends on them.

planner_fn(accepted_prefix: list[str], writers: list[WriterProfile], settings) -> list[str]   # 14 lines
assign_fn(words, writers, *, settings, lead_did, start_index, last_contributor, unavailable) -> obj with
          .assignments (list[Assignment]), .feasible (bool), .dead_ends (list[int])
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Optional

from ..models import (AcceptedWord, Assignment, ConsentState, GameState, Plan, PoemForm, PoemState, WordEntry,
                      WriterEvent, WriterHealth, WriterProfile, canonical_text, word_letters)
from .consent import AvailabilityTracker, FrameManager
from .cover import active_letters, hand_off_next, should_cover, spellers
from .dispatcher import Dispatcher
from .health import HealthManager, INACTIVE_STATES
from .operator import OperatorBoundary
from .state_machine import GameStateMachine
from .table import detect_table_conflicts, lines_from_words, render_table

S = GameState


class Controller:
    def __init__(self, settings, store, lexicon, referee, discovery, team_room, publication, engine, clock,
                 self_did: str, game_id: str, planner_fn: Optional[Callable] = None, assign_fn: Optional[Callable] = None,
                 *, members: Optional[list[str]] = None, poem_room: Optional[str] = None, room_generation: int = 1,
                 theme: str = "", seed: Optional[int] = None, form: Optional[PoemForm] = None):
        self.settings = settings
        self.store = store
        self.lexicon = lexicon
        self.referee = referee
        self.discovery = discovery
        self.team_room = team_room
        self.publication = publication
        self.engine = engine
        self.clock = clock
        self.self_did = self_did
        self.game_id = game_id
        self.theme = theme
        self.seed = seed if seed is not None else settings.simulation.seed
        self.form = form or PoemForm()
        self._planner_fn = planner_fn
        self._assign_fn = assign_fn
        self.poem_room = poem_room or settings.contest.get("team_room_pattern", "d-team-{game_id}").format(game_id=game_id)

        self.sm = GameStateMachine(on_transition=self._on_transition)
        self.frames = FrameManager(settings, clock, game_id, self.poem_room, self_did, room_generation)
        self.health = HealthManager(settings, clock)
        self.operator = OperatorBoundary(settings, store)
        self.availability = AvailabilityTracker(settings, clock)
        self.dispatcher = Dispatcher(referee, store, clock, game_id,
                                     timeout_ms=settings.health.minimum_timeout_ms * settings.health.down_multiplier)

        self.pending_members: list[str] = list(members or [])
        self.writers: list[WriterProfile] = []
        self.plan: Optional[Plan] = None
        self.poem = PoemState(game_id=game_id)
        self.events: list[dict] = []
        self.tick_count = 0
        self.waiting_since: Optional[datetime] = None
        self.unavailable: set[str] = set()
        self.last_table_version_posted: int = 0
        self.table_posts: list[int] = []
        self.team_room_cursor = 0
        self.landing_route: Optional[dict] = None
        self.publish_url: Optional[str] = None
        self.final_lines: list[str] = []
        self._stale_index: Optional[int] = None
        self._slot: Optional[tuple[int, str, datetime]] = None   # (index, assignee, since) of the open slot
        self.dispatcher_outcome_kinds: list[str] = []
        self._seen_accepted = 0
        self._draft_posted = False
        self._plan_counter = 0
        store.upsert_game(game_id, lead_did=self_did, poem_room=self.poem_room, room_generation=room_generation)
        self.health.register(self_did, seated_at=clock.now())

    # ================================================================ helpers
    def _on_transition(self, frm: GameState, to: GameState, reason: str) -> None:
        self.event("state", f"{frm.value} -> {to.value}: {reason}")
        self.store.upsert_game(self.game_id, state=to.value)

    def event(self, kind: str, detail: str = "", **extra: Any) -> None:
        e = {"kind": kind, "at": self.clock.now().isoformat(), "detail": detail}
        e.update(extra)
        self.events.append(e)

    def _profile(self, did: str) -> WriterProfile:
        w = self.store.get_writer(did)
        if w is None:
            w = WriterProfile(did=did)
        return w.model_copy(update={"is_self": did == self.self_did, "is_lead": did == self.self_did})

    def _writers_now(self) -> list[WriterProfile]:
        """Member profiles with current health applied (what the solver sees)."""
        return [w.model_copy(update={"health": self.health.health(w.did),
                                     "consent": self.frames.consent(w.did).state}) for w in self.writers]

    def members(self) -> list[str]:
        return list(self.frames.members)

    @property
    def state(self) -> GameState:
        return self.sm.state

    # ---------------------------------------------------------------- planner / solver seams
    def _plan_lines(self, prefix: list[str]) -> list[str]:
        """Text for the whole poem with the accepted prefix verbatim; only currently available writers are planned for."""
        writers = [w for w in self._writers_now() if w.did not in self.unavailable]
        if self._planner_fn is not None:
            return list(self._planner_fn(prefix, writers, self.settings))
        from ..planner.beam import plan_poem  # lazy: planner is another agent's package
        plan = plan_poem(self.engine, self.lexicon, writers, self.settings, accepted_prefix=list(prefix),
                         theme=self.theme, seed=self.seed, lead_did=self.self_did, game_id=self.game_id,
                         last_contributor=self.poem.last_contributor, unavailable=set(self.unavailable))
        return list(plan.lines)

    def _assign(self, words: list[WordEntry], start_index: int, last_contributor: Optional[str]):
        writers = [w for w in self._writers_now() if w.did not in self.unavailable]
        kwargs = dict(settings=self.settings, lead_did=self.self_did, start_index=start_index,
                      last_contributor=last_contributor, unavailable=set(self.unavailable))
        if self._assign_fn is not None:
            return self._assign_fn(words, writers, **kwargs)
        from ..solver.assignment import assign  # lazy: solver is another agent's package
        rules = (self.settings.contest or {}).get("rules", {}) if isinstance(self.settings.contest, dict) else {}
        return assign(words, writers, every_member_must_contribute=bool(rules.get("every_member_must_contribute", False)), **kwargs)

    def _words_from_lines(self, lines: list[str]) -> list[WordEntry]:
        out: list[WordEntry] = []
        i = 0
        for li, line in enumerate(lines):
            for tok in line.split():
                out.append(WordEntry(index=i, text=tok, line=li, syllables=self.lexicon.word_syllables(tok)))
                i += 1
        return out

    def _new_plan(self, lines: list[str], source: str, prefix_len: int) -> Plan:
        self._plan_counter += 1
        version = (self.plan.version + 1) if self.plan else 1
        text = canonical_text(lines)
        try:
            self.lexicon.validate_poem(text, exact_ten=True)   # official validator: final say on form
        except ValueError as e:
            self.event("plan_invalid", str(e))
            raise
        plan = Plan(plan_id=f"{self.game_id}-v{version}", game_id=self.game_id, version=version, owner=self.self_did,
                    source=source, words=self._words_from_lines(lines), accepted_prefix_len=prefix_len, lines=list(lines),
                    created_at=self.clock.now())
        return plan

    def _apply_assignments(self, plan: Plan, start_index: int, last_contributor: Optional[str]) -> bool:
        res = self._assign(plan.words, start_index, last_contributor)
        keep = [a for a in (self.plan.assignments if self.plan else []) if a.index < start_index]
        new = [a for a in res.assignments if a.index >= start_index]
        plan.assignments = sorted(keep + new, key=lambda a: a.index)
        feasible = bool(getattr(res, "feasible", True))
        if not feasible:
            self.event("assignment_infeasible", f"dead ends at {list(getattr(res, 'dead_ends', []))[:5]}")
        return feasible

    def _adopt(self, plan: Plan, reason: str) -> None:
        self.plan = plan
        self.store.save_plan(plan)
        self.event("plan", f"v{plan.version} {plan.hash_prefix} ({plan.source}): {reason}")

    def _replan_text(self, reason: str) -> None:
        prefix = self.poem.accepted_texts()
        lines = self._plan_lines(prefix)
        plan = self._new_plan(lines, "hybrid" if prefix else "solver", len(prefix))
        self._apply_assignments(plan, self.poem.next_index, self.poem.last_contributor)
        self._adopt(plan, reason)

    def _replan_assignments(self, start_index: int, last_contributor: Optional[str], reason: str,
                            fixed: Optional[dict[int, str]] = None) -> None:
        assert self.plan is not None
        plan = self._new_plan(self.plan.lines, "solver", self.poem.next_index)
        plan.assignments = list(self.plan.assignments)
        by_index = {a.index: a for a in plan.assignments}
        for idx, did in (fixed or {}).items():
            a = by_index.get(idx)
            if a:
                a.primary, a.backup = did, (a.backup if a.backup != did else None)
        feasible = self._apply_assignments(plan, start_index, last_contributor)
        if not feasible and not fixed:
            # Roster freeze != text freeze: the accepted prefix stays, the suffix is regenerated around the dead ends.
            try:
                self._replan_text(f"{reason}; suffix regenerated around dead ends")
                return
            except Exception as e:  # planner could not find a text either: keep the best-effort assignment
                self.event("replan_text_failed", str(e)[:200])
        for idx, did in (fixed or {}).items():   # the solver may not override a fixed hand-off
            for a in plan.assignments:
                if a.index == idx:
                    a.primary = did
        self._adopt(plan, reason)

    # ---------------------------------------------------------------- posting
    def _post_team_or_discovery(self, text: str, kind: str) -> bool:
        res = self.team_room.post(self.game_id, text, kind)
        if res.ok:
            return True
        if res.http_status == 403:
            self.event("team_room_403", "posted to discovery instead")
            res2 = self.discovery.post(text, kind)
            return res2.ok
        self.event("post_failed", f"{kind}: {res.error}")
        return False

    def _post_table(self) -> None:
        assert self.plan is not None
        chunks = render_table(self.plan, self.poem, self.writers, self.settings)
        ok = True
        for c in chunks:
            ok = self._post_team_or_discovery(c, "table") and ok
        if ok:
            self.last_table_version_posted = self.plan.version
            self.table_posts.append(self.plan.version)
            self.event("table", f"v{self.plan.version} next={self.poem.next_index} in {len(chunks)} chunk(s)")

    # ================================================================ tick
    def tick(self) -> GameState:
        self.tick_count += 1
        now = self.clock.now()
        if self.sm.terminal:
            return self.sm.state
        # setup phases cascade within one tick until the state settles (a frame re-issue after a timeout
        # must not wait for the next tick: coordination_lessons.md case 7 fault 3)
        prev = None
        while self.sm.state != prev and not self.sm.writing and not self.sm.terminal:
            prev = self.sm.state
            if self.sm.state == S.DISCOVER:
                self.sm.transition(S.APPLY, "leading own game", now)
            elif self.sm.state == S.APPLY:
                self._seat_members(now)
            elif self.sm.state == S.SEATED:
                self._issue_frame(now)
            elif self.sm.state == S.ROSTER_PENDING:
                self._roster_pending(now)
            elif self.sm.state == S.ROSTER_READY:
                self._start_writing(now)
            else:
                break
        if self.sm.writing:
            self._writing_tick(now)
        if self.sm.state == S.COMPLETE:
            self._complete_tick(now)
        if self.sm.state == S.PUBLISH_PENDING:
            self._publish_pending_tick(now)
        if self.sm.state == S.SUBMITTED:
            self._submitted_tick(now)
        return self.sm.state

    def run_until_complete(self, max_ticks: int = 1000, until: GameState = GameState.SUBMITTED) -> GameState:
        stop = {GameState(until), S.ABANDONED, S.ACCEPTED}
        for _ in range(max_ticks):
            st = self.tick()
            if st in stop or (st == S.ACCEPTED):
                return st
            self.clock.sleep(self.settings.scheduler.tick_seconds)
        return self.sm.state

    # ---------------------------------------------------------------- roster phases
    def _seat_members(self, now: datetime) -> None:
        for did in self.pending_members:
            self.frames.apply(did)
            act = self.frames.seat(did, now)
            self.event("seat", f"{did[-8:]}: {act.detail}")
            self.health.register(did, seated_at=now, latency_median_ms=self._profile(did).word_latency_median_ms)
        self.pending_members = []
        self.writers = [self._profile(d) for d in self.frames.members]
        self.store.set_members(self.game_id, self.frames.members)
        self.sm.transition(S.SEATED, f"{len(self.frames.members)} seated", now)

    def _issue_frame(self, now: datetime) -> None:
        if self.plan is None:
            try:
                lines = self._plan_lines([])
                plan = self._new_plan(lines, "solver", 0)
                self._apply_assignments(plan, 0, None)
                self._adopt(plan, "draft before the frame")
            except Exception as e:  # noqa: BLE001 - planner failure is reported, not fatal before the frame
                self.event("plan_failed", repr(e))
        if self.plan is not None and not self._draft_posted:
            self._post_team_or_discovery(f"DRAFT {self.plan.hash_prefix}\n{self.plan.text}", "draft")
            self._draft_posted = True
        if self.frames.frame is not None:
            # our consent on the previous frame is still live: withdraw first or the referee answers
            # "consent: withdraw before changing" (live bot lead_check_roster does the same)
            wd = self.referee.withdraw(self.game_id, self.self_did)
            self.event("withdraw", f"before re-issue: {'ok' if wd.ok else wd.error}")
            self.availability.mark_pending(self.self_did, now)
        frame = self.frames.issue(now)
        res = self.referee.issue_frame(frame)
        if not res.ok:
            self.event("frame_rejected", res.error or "")
            return
        self.event("frame", f"{frame.frame_id} {frame.signature} members={len(frame.members)} signed={sorted(d[-8:] for d in frame.signed_by)}")
        self.sm.transition(S.ROSTER_PENDING, f"frame {frame.signature} issued", now)

    def _roster_pending(self, now: datetime) -> None:
        status = self.referee.roster_status(self.game_id)
        frame = self.frames.frame
        assert frame is not None
        sig = status.get("frame_signature") or frame.signature
        for did in status.get("signed", []):
            if did not in frame.signed_by:
                if self.frames.record_signature(did, sig, now):
                    self.event("signature", did[-8:])
                    self.health.record_activity(did, now, "sign")
        for did, reason in (status.get("rejected") or {}).items():
            act = self.frames.record_rejection(did, reason, now)
            if act and act.kind == "withdraw_first":
                self.discovery.post(f"@{did[-8:]} {self.game_id}: {act.detail}", "note", to_did=did)
                self.event("withdraw_first_note", did[-8:])
        for act in self.frames.check(now):
            self.event(f"consent_{act.kind}", f"{(act.did or '')[-8:]} {act.detail}".strip())
            if act.kind == "remind":
                self.discovery.post(f"@{act.did[-8:]} {self.game_id}: {act.detail}", "note", to_did=act.did)
            elif act.kind == "drop":
                self.writers = [w for w in self.writers if w.did != act.did]
            elif act.kind == "reissue":
                self.frames.seat_from_waitlist(ok=self._seat_gate)
                self.writers = [self._profile(d) for d in self.frames.members]
                for d in self.frames.members:
                    self.health.register(d, seated_at=now)
                self.store.set_members(self.game_id, self.frames.members)
                self.sm.transition(S.SEATED, "frame re-issue after timeout", now)
                return
        if status.get("ready") or self.frames.all_signed():
            self.frames.freeze(now)
            self.writers = [self._profile(d) for d in self.frames.members]
            self.store.set_members(self.game_id, self.frames.members)
            self.store.upsert_game(self.game_id, frame_state="FROZEN")
            self.sm.transition(S.ROSTER_READY, "all consents on the frame", now)

    def _seat_gate(self, did: str) -> str:
        """Reason to skip a waitlisted candidate (key must fit the plan: no single-key words added)."""
        if self.plan is None:
            return ""
        letters = {w.did: w.letters for w in self.writers}
        letters[did] = self._profile(did).letters
        single = [w.text for w in self.plan.words if len(spellers(w.text, letters)) < 2]
        return f"{len(single)} word(s) spellable by one key only" if single else ""

    def _start_writing(self, now: datetime) -> None:
        if self.plan is None:
            self._replan_text("first plan after roster_ready")
        else:
            self._replan_assignments(0, None, "assignments for the frozen roster")
        self._post_table()
        self.waiting_since = now
        self.sm.transition(S.WRITING, "table posted", now)

    # ---------------------------------------------------------------- writing
    def _refresh_poem(self) -> list[AcceptedWord]:
        acc = self.store.accepted(self.game_id)
        new = acc[self._seen_accepted:]
        self.poem = PoemState(game_id=self.game_id, accepted=acc, version=acc[-1].version if acc else 0)
        if new:
            total = sum(self.lexicon.word_syllables(w.text) for w in acc)
            self.poem.complete = total >= self.form.lines * self.form.syllables_per_line
        self._seen_accepted = len(acc)
        return new

    def _ingest_accepted(self, new: list[AcceptedWord]) -> None:
        for w in new:
            prev_at = self.poem.accepted[w.index - 1].accepted_at if w.index > 0 else self.waiting_since
            at = w.accepted_at or self.clock.now()
            latency = (at - prev_at).total_seconds() * 1000.0 if prev_at else None
            self.health.record_activity(w.contributor, at, "word_accepted")
            if latency is not None and w.contributor != self.self_did:
                self.health.record_latency(w.contributor, latency)
            self.store.add_event(WriterEvent(did=w.contributor, kind="word_accepted", at=at, latency_ms=latency,
                                             game_id=self.game_id, detail=w.text))
            self.waiting_since = at
            self._stale_index = None
        if new:
            self.health.clear_waiting()

    def _writing_tick(self, now: datetime) -> None:
        # 1. receipts
        outcomes = self.dispatcher.process_receipts()
        self.dispatcher_outcome_kinds.extend(o.kind for o in outcomes)
        for o in outcomes:
            if o.kind in ("stale", "rejected", "conflict", "timed_out_late"):
                self.event(f"receipt_{o.kind}", f"{o.receipt.request_id} {o.receipt.reason or ''}".strip())
            elif o.kind == "buffered" and o.receipt.contributor and o.receipt.contributor != self.self_did:
                # the referee accepted this writer's word ahead of our prefix: the writer is demonstrably alive
                self.health.record_activity(o.receipt.contributor, o.receipt.at, "word_accepted")
        if self.dispatcher.needs_resync:
            self._resync()
        for p in self.dispatcher.expire(now):
            self.event("proposal_timeout", p.request_id)
        new = self._refresh_poem()
        self._ingest_accepted(new)
        if self.poem.complete:
            self._on_complete(now)
            return
        # 2. reconcile the accepted prefix with the plan
        assert self.plan is not None
        div = self._divergence()
        if div is not None:
            self.event("divergence", f"index {div}: plan {self.plan.words[div].text!r} vs accepted {self.poem.accepted[div].text!r}")
            self._replan_text(f"hybrid text from index {div}")
        # 3. health: the open slot's assignee is "waiting" since the slot was given to them
        #    (the last accepted word, or a later re-assignment), never since an older word
        slot_since = self._slot_since(now)
        idx = self.poem.next_index
        by_index = {a.index: a for a in self.plan.assignments}
        a = by_index.get(idx)
        if a and a.primary != self.self_did:
            self.health.mark_waiting(a.primary, slot_since)
        self.health.update(now)
        self._update_unavailable(now)
        # 4. landing (before our move: the route decides who must post the last word)
        self._landing(now)
        # 5. our move: own slot, or cover
        if not self.poem.complete:
            self._maybe_propose(now, self._slot_since(now))
        # 6. repost the table when the plan version changed
        if self.plan.version != self.last_table_version_posted:
            self._post_table()
        # 7. team room: foreign tables, member activity
        self._scan_team_room(now)

    def _resync(self) -> None:
        reader = getattr(self.referee, "accepted_words", None)
        if reader is None:
            self.event("resync_unavailable", "waiting for receipts")
            return
        try:
            added = self.dispatcher.resync(reader(self.game_id))
        except AttributeError:
            self.event("resync_unavailable", "waiting for receipts")
            return
        self.event("resync", f"{added} word(s) adopted from the referee")

    def _divergence(self) -> Optional[int]:
        assert self.plan is not None
        for w in self.poem.accepted:
            if w.index >= len(self.plan.words) or self.plan.words[w.index].text != w.text:
                return w.index
        return None

    def _update_unavailable(self, now: datetime) -> None:
        assert self.plan is not None
        idx = self.poem.next_index
        newly = set()
        for w in self.writers:
            if w.did == self.self_did:
                continue
            h = self.health.health(w.did)
            if h in INACTIVE_STATES and w.did not in self.unavailable:
                newly.add(w.did)
            elif h not in INACTIVE_STATES and w.did in self.unavailable:
                self.unavailable.discard(w.did)
                self.event("writer_back", f"{w.did[-8:]} {h.value}")
        if not newly:
            if self.sm.state == S.RECOVERING:
                self.sm.transition(S.WRITING, "plan feasible again", now)
            return
        self.unavailable |= newly
        for d in newly:
            self.event("writer_inactive", f"{d[-8:]} {self.health.health(d).value}: {self.health.tracks[d].reason}")
        affected = any(a.index >= idx and a.primary in self.unavailable for a in self.plan.assignments)
        if affected:
            if self.sm.state != S.RECOVERING:
                self.sm.transition(S.RECOVERING, f"{', '.join(d[-8:] for d in sorted(newly))} inactive", now)
            if self.operator.request("same_plan_assignment_recovery", f"exclude {sorted(newly)}", now):
                self._replan_assignments(idx, self.poem.last_contributor, f"exclude inactive {sorted(d[-8:] for d in newly)}")
                if self.sm.state == S.RECOVERING:
                    self.sm.transition(S.WRITING, "reassigned around inactive writers", now)

    def _slot_since(self, now: datetime) -> datetime:
        """When the current assignee of the next slot was given it (used for overdue / cover timing)."""
        assert self.plan is not None
        idx = self.poem.next_index
        by_index = {a.index: a for a in self.plan.assignments}
        a = by_index.get(idx)
        did = a.primary if a else ""
        base = self.waiting_since or now
        if self._slot is None or self._slot[0] != idx:
            self._slot = (idx, did, base)
        elif self._slot[1] != did:
            self._slot = (idx, did, max(base, now))
        return self._slot[2]

    def _maybe_propose(self, now: datetime, slot_since: Optional[datetime] = None) -> None:
        assert self.plan is not None
        idx = self.poem.next_index
        if idx >= len(self.plan.words):
            return
        if self.dispatcher.pending(idx):
            return
        if self._stale_index == idx:
            return   # somebody else took this index; wait for the receipt / resync
        by_index = {a.index: a for a in self.plan.assignments}
        a = by_index.get(idx)
        word = self.plan.words[idx].text
        last = self.poem.last_contributor
        if a is not None and a.primary == self.self_did:
            if last == self.self_did:
                letters = active_letters(self.writers, self.health)
                letters.pop(self.self_did, None)
                who = hand_off_next(self.plan, idx, letters, self.self_did)
                if who:
                    self._replan_assignments(idx + 1, who, f"parity: we posted {idx - 1}; hand word {idx} to {who[-8:]}", fixed={idx: who})
                return
            self._propose(idx, word, now, "own slot")
            return
        route = self.landing_route
        if route and route.get("final_contributor") == self.self_did and idx == len(self.plan.words) - 2:
            return   # the landing route needs us for the last word: never take the one before it
        dec = should_cover(self.plan, self.poem, self.health, self.settings, now, self_did=self.self_did,
                           writers=self.writers, waiting_since=slot_since or self.waiting_since)
        if not dec.cover:
            return
        self.event("cover", f"word {idx} {word!r}: {dec.reason}")
        self._propose(idx, word, now, "cover")
        if dec.hand_off:
            ho_idx, who = dec.hand_off
            self._replan_assignments(ho_idx + 1, who, f"hand-off: word {ho_idx} to {who[-8:]}", fixed={ho_idx: who})

    def _propose(self, idx: int, word: str, now: datetime, why: str) -> None:
        p = self.dispatcher.propose(idx, word, self.self_did, self.poem.version)
        self.event("propose", f"{p.request_id} {word!r} ({why})")

    def _landing(self, now: datetime) -> None:
        assert self.plan is not None
        idx = self.poem.next_index
        last_line = self.form.lines - 1
        first_of_last = next((w.index for w in self.plan.words if w.line == last_line), None)
        if first_of_last is None or idx < first_of_last:
            return
        if self.sm.state == S.WRITING:
            self.sm.transition(S.LANDING, "last line", now)
        final = self.plan.words[-1]
        by_index = {a.index: a for a in self.plan.assignments}
        fa = by_index.get(final.index)
        routes = self._landing_routes()
        self.landing_route = routes[0] if routes else None
        if not routes or not routes[0]["can_publish"] or fa is None:
            return
        path = {i: d for i, d in routes[0]["path"] if i >= idx}
        needs_fix = not self.publication.can_publish(fa.primary) or self._suffix_broken(idx)
        if needs_fix and path and any(by_index[i].primary != d for i, d in path.items() if i in by_index):
            target = routes[0]["final_contributor"]
            self._replan_assignments(idx, self.poem.last_contributor,
                                     f"landing: route to publisher {target[-8:]} ({len(path)} words)", fixed=path)

    def _suffix_broken(self, idx: int) -> bool:
        """Consecutive same primary or a primary that cannot spell its word in the remaining assignments."""
        assert self.plan is not None
        letters = {w.did: w.letters for w in self.writers}
        prev = self.poem.last_contributor
        for a in sorted((a for a in self.plan.assignments if a.index >= idx), key=lambda a: a.index):
            if a.primary == prev or not (word_letters(self.plan.words[a.index].text) <= letters.get(a.primary, frozenset())):
                return True
            prev = a.primary
        return False

    def _landing_routes(self) -> list[dict]:
        """Routes as dicts {final_contributor, path: [(index, did)...], can_publish}; planner.landing when available."""
        assert self.plan is not None
        try:
            from ..planner.landing import landing_routes  # lazy: planner is another agent's package
            routes = landing_routes(self.plan, self.poem, self._writers_now(), self.settings, unavailable=self.unavailable)
            out = [{"final_contributor": r.final_contributor, "path": [tuple(p) for p in r.path], "can_publish": bool(r.can_publish)}
                   for r in routes]
            # the planner judges publication by x_account; the PublicationAdapter has the final say
            for r in out:
                r["can_publish"] = bool(self.publication.can_publish(r["final_contributor"]))
            out.sort(key=lambda r: not r["can_publish"])
            if out:
                return out
        except Exception as e:  # noqa: BLE001 - fall back to the built-in route builder
            self.event("landing_fallback", repr(e))
        return self._fallback_routes()

    def _fallback_routes(self) -> list[dict]:
        """Depth-first alternation search over the remaining words, publishers as final contributor first."""
        assert self.plan is not None
        idx = self.poem.next_index
        words = [w.text for w in self.plan.words[idx:]]
        letters = active_letters(self.writers, self.health)
        order = sorted(letters, key=lambda d: (not self.publication.can_publish(d), d))
        out: list[dict] = []

        def walk(i: int, last: Optional[str], path: list[tuple[int, str]]) -> bool:
            if i == len(words):
                final = path[-1][1]
                out.append({"final_contributor": final, "path": list(path), "can_publish": self.publication.can_publish(final)})
                return True
            found = False
            for d in order:
                if d != last and word_letters(words[i]) <= letters[d]:
                    path.append((idx + i, d))
                    if walk(i + 1, d, path):
                        found = True
                    path.pop()
                    if len(out) >= max(self.settings.planner.landing_routes, 1):
                        return True
            return found

        walk(0, self.poem.last_contributor, [])
        out.sort(key=lambda r: not r["can_publish"])
        return out

    def _scan_team_room(self, now: datetime) -> None:
        posts = self.team_room.fetch(self.game_id, self.team_room_cursor)
        if not posts:
            return
        self.team_room_cursor = max(p.seq for p in posts)
        for c in detect_table_conflicts(posts, self.self_did, self.settings):
            self.event("table_conflict", c.describe(), sender=c.sender, seq=c.seq, version=c.header.version)
        for p in posts:
            if p.sender != self.self_did and p.sender in self.health.tracks:
                self.health.record_activity(p.sender, p.at, "post")

    # ---------------------------------------------------------------- completion
    def _on_complete(self, now: datetime) -> None:
        self.final_lines = lines_from_words(self.poem.accepted_texts(), self.lexicon, self.form)
        try:
            self.lexicon.validate_poem(canonical_text(self.final_lines), exact_ten=True)
            self.event("complete", f"{len(self.poem.accepted)} words, sha {self.final_sha()[:12]}, final by {self.poem.last_contributor[-8:]}")
        except ValueError as e:
            self.event("complete_invalid", str(e))
        self.store.upsert_game(self.game_id, version=self.poem.version)
        self.sm.transition(S.COMPLETE, "referee accepted the last word", now)

    def final_sha(self) -> str:
        from ..models import poem_sha256
        return poem_sha256(self.final_lines)

    def _complete_tick(self, now: datetime) -> None:
        final = self.poem.last_contributor
        if final == self.self_did and self.publication.can_publish(self.self_did):
            res = self.publication.publish(self.self_did, canonical_text(self.final_lines))
            if res.ok:
                self.publish_url = getattr(self.publication, "post_url", lambda s: f"seq:{s}")(res.seq)
                self.event("published", self.publish_url)
            else:
                self.event("publish_failed", res.error or "")
        else:
            self.event("publish_by_other", f"final contributor {final[-8:] if final else '?'} must publish")
        self.sm.transition(S.PUBLISH_PENDING, "awaiting submission", now)

    def _publish_pending_tick(self, now: datetime) -> None:
        if self.publish_url and self.poem.last_contributor == self.self_did:
            res = self.publication.submit(self.game_id, self.self_did, self.publish_url, self.final_sha())
            if res.ok:
                self.event("submitted", self.final_sha()[:12])
                self.sm.transition(S.SUBMITTED, "submit posted", now)
            return
        checker = getattr(self.publication, "submitted", None)
        if checker and checker(self.game_id):
            self.sm.transition(S.SUBMITTED, "submitted by the final contributor", now)

    def _submitted_tick(self, now: datetime) -> None:
        checker = getattr(self.publication, "submission_accepted", None)
        if checker and checker(self.game_id):
            self.sm.transition(S.ACCEPTED, "submission accepted", now)

    # ================================================================ snapshot
    def snapshot(self) -> dict:
        idx = self.poem.next_index
        by_index = {a.index: a for a in (self.plan.assignments if self.plan else [])}
        a = by_index.get(idx)
        nxt = self.plan.words[idx].text if self.plan and idx < len(self.plan.words) else None
        hs = {h.did: h for h in self.health.snapshot()}
        letters = {w.did: w.letters for w in self.writers}
        members = []
        for w in self.writers:
            h = hs.get(w.did)
            members.append({
                "did": w.did, "handle": w.handle, "health": h.health.value if h else WriterHealth.HEALTHY.value,
                "expected_ms": h.expected_ms if h else None, "consent": self.frames.consent(w.did).state.value,
                "keys": sum(1 for x in (self.plan.words if self.plan else []) if word_letters(x.text) <= letters[w.did]),
                "latency_ms": self.health.tracks[w.did].latencies_ms[-1] if self.health.tracks.get(w.did) and self.health.tracks[w.did].latencies_ms else None,
                "words": sum(1 for x in self.poem.accepted if x.contributor == w.did),
                "unavailable": w.did in self.unavailable,
            })
        frame = self.frames.frame
        return {
            "game_id": self.game_id, "state": self.sm.state.value, "tick": self.tick_count, "now": self.clock.now().isoformat(),
            "self_did": self.self_did, "members": members,
            "accepted": self.poem.accepted_texts(), "next_index": idx, "next_word": nxt,
            "primary": a.primary if a else None, "backup": a.backup if a else None,
            "plan": {"version": self.plan.version, "hash": self.plan.hash_prefix, "source": self.plan.source,
                     "words": len(self.plan.words), "table_posted_version": self.last_table_version_posted} if self.plan else None,
            "pending_proposals": [p.request_id for p in self.dispatcher.pending()],
            "landing_route": self.landing_route,
            "operator_pending": [{"action": r.action, "detail": r.detail} for r in self.operator.pending()],
            "frame": {"signature": frame.signature, "state": frame.state.value, "signed_by": sorted(frame.signed_by),
                      "members": list(frame.members)} if frame else None,
            "waitlist": list(self.frames.waitlist),
            "events": self.events[-20:],
            "final_sha256": self.final_sha() if self.final_lines else None,
        }
