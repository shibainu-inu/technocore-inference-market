"""End-to-end games through Controller.tick() with the mock world (FakeClock, MockReferee, ScriptedWriters).

Poem: data/fixtures/nohitori-2/final_poem.txt (131 words, every word in the frozen dictionary).
Writers: A = our all-letter DID; B, C, D = synthetic DIDs (B spells every word, C lacks p/w, D lacks c/v).
Planner/solver are stubbed: a fixed text and a round-robin assignment (see ``round_robin_assign``).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from sonnet_orchestrator.adapters.mock import (FakeClock, MockDiscovery, MockPublication, MockReferee, MockTeamRoom,
                                               ScriptedWriters, WriterScript, synthetic_did)
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.db import Store
from sonnet_orchestrator.lexicon.core import load_lexicon
from sonnet_orchestrator.models import Assignment, GameState, ProposalStatus, WriterHealth, WriterProfile, word_letters
from sonnet_orchestrator.orchestration import Controller

ROOT = Path(__file__).resolve().parents[2]
POEM_PATH = ROOT / "data" / "fixtures" / "nohitori-2" / "final_poem.txt"
SELF = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
B = synthetic_did("abcfghlnoprstuvw")   # every word of the fixture
C = synthetic_did("abcfghlnorstuv")     # lacks p, w
D = synthetic_did("abfghlnoprstuw")     # lacks c, v
GAME = "mock-1"


@pytest.fixture(scope="session")
def lexicon():
    return load_lexicon(str(ROOT / "data" / "cmudict" / "cmudict.dict"))


@pytest.fixture(scope="session")
def poem_lines() -> list[str]:
    return [l for l in POEM_PATH.read_text(encoding="utf-8").split("\n") if l.strip()]


def settings_for_test():
    s = load_settings()
    s.scheduler.tick_seconds = 10          # fast ticks for the simulation
    return s


def fixed_planner(lines: list[str]):
    """Planner stub: the fixed text; an accepted prefix must be a prefix of it (hybrid text is not simulated)."""
    def planner_fn(prefix, writers, settings):
        words = [w for l in lines for w in l.split()]
        assert list(prefix) == words[: len(prefix)], "stub planner cannot absorb a diverging prefix"
        return list(lines)
    return planner_fn


@dataclass
class StubResult:
    assignments: list[Assignment]
    cost: float = 0.0
    feasible: bool = True
    dead_ends: list[int] = field(default_factory=list)
    explanation: list[str] = field(default_factory=list)


def round_robin_assign(words, writers, *, settings, lead_did, start_index=0, last_contributor=None, unavailable=set()):
    """Rotate over the writers (in given order); a writer must spell the word, differ from the previous contributor
    and not be unavailable. Backup = next spelling writer in rotation."""
    order = [w for w in writers if w.did not in unavailable]
    letters = {w.did: w.letters for w in order}
    out, dead = [], []
    last = last_contributor
    pos = 0
    for w in words:
        if w.index < start_index:
            continue
        cands = [d for d in [order[(pos + k) % len(order)].did for k in range(len(order))]
                 if d != last and word_letters(w.text) <= letters[d]]
        if not cands:
            dead.append(w.index)
            out.append(Assignment(index=w.index, primary=lead_did if lead_did != last else order[0].did, keys=0))
            continue
        primary = cands[0]
        out.append(Assignment(index=w.index, primary=primary, backup=cands[1] if len(cands) > 1 else None,
                              keys=sum(1 for d in letters if word_letters(w.text) <= letters[d])))
        last = primary
        pos = [o.did for o in order].index(primary) + 1
    return StubResult(out, feasible=not dead, dead_ends=dead)


def make_world(lexicon, poem_lines, *, scripts: dict[str, WriterScript] | None = None, referee_kwargs=None,
               publishers=None, step_seconds=5.0):
    settings = settings_for_test()
    clock = FakeClock(step_seconds=step_seconds)
    referee = MockReferee(lexicon, clock, **(referee_kwargs or {}))
    discovery = MockDiscovery(clock, SELF)
    room = MockTeamRoom(clock, SELF, referee=referee, char_limit=settings.room.post_char_limit)
    publication = MockPublication(clock, publishers=set(publishers if publishers is not None else {SELF, D}))
    store = Store(":memory:")
    store.upsert_writer(WriterProfile(did=SELF, handle="nohitori", x_account="https://x.com/0xnohitori", is_self=True, is_lead=True))
    store.upsert_writer(WriterProfile(did=B, handle="b"))
    store.upsert_writer(WriterProfile(did=C, handle="c"))
    store.upsert_writer(WriterProfile(did=D, handle="d", x_account="https://x.com/d"))
    scripts = scripts or {}
    ws = [scripts.get(d) or WriterScript(did=d) for d in (B, C, D)]
    writers = ScriptedWriters(referee, room, publication, clock, lexicon, settings, GAME, SELF, ws).attach()
    ctl = Controller(settings, store, lexicon, referee, discovery, room, publication, engine=None, clock=clock,
                     self_did=SELF, game_id=GAME, planner_fn=fixed_planner(poem_lines), assign_fn=round_robin_assign,
                     members=[B, C, D], poem_room="d-mock-team")
    return ctl, referee, writers, room, discovery, publication, store, clock


def contributors(ctl) -> list[str]:
    return [w.contributor for w in ctl.poem.accepted]


# ---------------------------------------------------------------- (a) full game
def test_full_game_completes_and_is_submitted(lexicon, poem_lines):
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(lexicon, poem_lines)
    final = ctl.run_until_complete(max_ticks=600)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED), ctl.events[-10:]
    truth = referee.truth(GAME)
    assert truth.complete and len(truth.accepted) == 131
    assert ctl.poem.accepted_texts() == [w.text for w in truth.accepted]
    assert ctl.final_lines == poem_lines
    # every contributor alternates; every member wrote at least once
    cs = contributors(ctl)
    assert all(cs[i] != cs[i + 1] for i in range(len(cs) - 1))
    assert set(cs) == {SELF, B, C, D}
    # the 403 fallback before roster_ready was exercised (draft went to discovery)
    assert any(e["kind"] == "team_room_403" for e in ctl.events)
    assert any(p.kind == "draft" for p in discovery.posts)
    # tables in the team room are ≤ 2000 chars and from us only
    tables = [p for p in room.posts[GAME] if p.kind == "table"]
    assert tables and all(len(p.text) <= 2000 for p in tables)
    assert all(p.sender == SELF for p in tables)
    # publication + submission by the final contributor
    assert publication.submitted(GAME)
    snap = ctl.snapshot()
    json.dumps(snap)   # JSON-serialisable
    assert snap["state"] == final.value and snap["final_sha256"]
    # store holds the same immutable prefix
    assert [w.text for w in store.accepted(GAME)] == ctl.poem.accepted_texts()


# ---------------------------------------------------------------- (b) C goes DOWN at word 40
def test_writer_down_mid_poem_recovers(lexicon, poem_lines):
    base, referee0, *_ = make_world(lexicon, poem_lines)
    base.run_until_complete(max_ticks=600)
    baseline = base.poem.accepted_texts()

    scripts = {C: WriterScript(did=C, down_after_index=40)}
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(lexicon, poem_lines, scripts=scripts)
    final = ctl.run_until_complete(max_ticks=900)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED), ctl.events[-10:]
    texts = ctl.poem.accepted_texts()
    assert len(texts) == 131
    assert texts[:40] == baseline[:40]           # accepted prefix identical up to the fault
    assert texts == baseline                      # the text itself never changed (cover posts the planned word)
    # C is detected as inactive and never assigned or accepted afterwards
    down_events = [e for e in ctl.events if e["kind"] == "writer_inactive" and C[-8:] in e["detail"]]
    assert down_events, "C was never classified inactive"
    assert C in ctl.unavailable
    cs = contributors(ctl)
    assert C not in cs[40:]
    assert all(a.primary != C for a in ctl.plan.assignments if a.index >= ctl.plan.accepted_prefix_len)
    assert any(e["kind"] == "state" and "RECOVERING" in e["detail"] for e in ctl.events)
    # plan version bumped and the table re-posted
    assert ctl.plan.version > 1 and len(ctl.table_posts) > 1
    assert all(cs[i] != cs[i + 1] for i in range(len(cs) - 1))
    assert publication.submitted(GAME)


# ---------------------------------------------------------------- (c) race: two proposals, one index
def test_race_two_proposals_same_index(lexicon, poem_lines):
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(lexicon, poem_lines)
    # drive to WRITING
    for _ in range(20):
        if ctl.tick() == GameState.WRITING:
            break
        clock.sleep(ctl.settings.scheduler.tick_seconds)
    assert ctl.state == GameState.WRITING
    truth = referee.truth(GAME)
    idx, ver = len(truth.accepted), truth.version
    word = ctl.plan.words[idx].text
    # two members race for the same index at the same instant: first wins, second is STALE
    receipts = referee.race(GAME, [(f"race-{B[-6:]}", idx, word, B, ver), (f"race-{C[-6:]}", idx, word, C, ver)])
    assert [r.status for r in receipts] == [ProposalStatus.ACCEPTED, ProposalStatus.STALE]
    assert receipts[1].reason == "version: stale"
    assert len(truth.accepted) == idx + 1 and truth.accepted[idx].contributor == B
    # the controller ingests exactly one accepted word for that index
    ctl.tick()
    assert ctl.poem.accepted_texts()[idx] == word
    assert [w.index for w in ctl.poem.accepted] == list(range(idx + 1))
    # now race our own proposal against a member for the next slot
    idx2, ver2 = len(truth.accepted), truth.version
    word2 = ctl.plan.words[idx2].text
    rival = next(d for d in (B, C, D) if d != truth.accepted[-1].contributor and word_letters(word2) <= word_letters(d))
    referee.propose_word(GAME, f"race2-{rival[-6:]}", idx2, word2, rival, ver2)
    p = ctl.dispatcher.propose(idx2, word2, SELF, ver2)
    ctl.tick()
    assert p.status == ProposalStatus.STALE
    assert truth.accepted[idx2].contributor == rival
    assert ctl.poem.accepted_texts()[: idx2 + 1] == [w.text for w in truth.accepted[: idx2 + 1]]
    assert len({w.index for w in ctl.poem.accepted}) == len(ctl.poem.accepted)
    # and the game still completes
    final = ctl.run_until_complete(max_ticks=600)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED)
    assert len(referee.truth(GAME).accepted) == 131


# ---------------------------------------------------------------- (d) delayed receipt after a replan
def test_delayed_receipt_after_replan_is_idempotent(lexicon, poem_lines):
    # D's receipts arrive 100 s late (past the 6x15 s DOWN threshold) and the referee offers no resync channel,
    # so the controller is blind meanwhile: its cover of D's slot comes back "version: stale", D is classified
    # DOWN and the plan is re-versioned; when the late receipt finally arrives it is applied once, buffered
    # followers drain, and nothing is duplicated. (D follows C in the rotation, so we may cover D's slot;
    # B always follows us, so the alternation rule would forbid covering B.)
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(
        lexicon, poem_lines, referee_kwargs={"delayed_receipt": {D: 100000}, "expose_accepted": False})
    final = ctl.run_until_complete(max_ticks=1500)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED), ctl.events[-10:]
    truth = referee.truth(GAME)
    assert ctl.poem.accepted_texts() == [w.text for w in truth.accepted] == [w for l in poem_lines for w in l.split()]
    assert [w.index for w in ctl.poem.accepted] == list(range(131))
    kinds = [e["kind"] for e in ctl.events]
    assert "cover" in kinds and "receipt_stale" in kinds and "resync_unavailable" in kinds
    assert any(e["kind"] == "writer_inactive" and D[-8:] in e["detail"] for e in ctl.events)
    assert ctl.plan.version > 1
    # late receipts were matched to D's words and applied exactly once (store is append-only, no conflicts)
    assert not any("conflict" in line for line in ctl.dispatcher.log)
    assert any(o == "buffered" for o in ctl.dispatcher_outcome_kinds)
    assert store.accepted(GAME) == ctl.poem.accepted
    cs = contributors(ctl)
    assert all(cs[i] != cs[i + 1] for i in range(len(cs) - 1))


# ---------------------------------------------------------------- single-owner table rule
def test_foreign_table_is_reported_not_adopted(lexicon, poem_lines):
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(lexicon, poem_lines)
    for _ in range(20):
        if ctl.tick() == GameState.WRITING:
            break
        clock.sleep(ctl.settings.scheduler.tick_seconds)
    v = ctl.plan.version
    # a member posts its own table for the same text
    room.post_as(B, GAME, f"PLAN v99 {ctl.plan.hash_prefix} next=0 (1/1)\n0 My {B[-8:]}/-", "table")
    ctl.tick()
    conflicts = [e for e in ctl.events if e["kind"] == "table_conflict"]
    assert conflicts and conflicts[0]["sender"] == B and conflicts[0]["version"] == 99
    assert ctl.plan.owner == SELF and ctl.plan.version == v   # never adopted


# ---------------------------------------------------------------- (e) a member signs but never writes
def test_silent_member_is_excluded_and_poem_completes(lexicon, poem_lines):
    scripts = {D: WriterScript(did=D, profile="silent")}
    ctl, referee, writers, room, discovery, publication, store, clock = make_world(lexicon, poem_lines, scripts=scripts, publishers={SELF})
    final = ctl.run_until_complete(max_ticks=900)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED), ctl.events[-10:]
    assert len(ctl.poem.accepted) == 131 and D not in contributors(ctl)
    assert D in ctl.unavailable
    assert any(e["kind"] == "cover" for e in ctl.events)          # D's first slot was covered by us
    assert all(a.primary != D for a in ctl.plan.assignments if a.index >= ctl.plan.accepted_prefix_len)
