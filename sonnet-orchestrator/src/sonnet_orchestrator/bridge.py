"""Phase 7 file-bridge, orchestrator side (see docs/BRIDGE.md).

Reads the live bot's ``state-sonnet-2.json`` and ``policy.json`` (read-only), writes
``<out_dir>/<game_id>.json`` (plan: lines + turn script) and ``<out_dir>/roster-<game_id>.json`` (advice).
Never signs, never posts, never writes anywhere but ``out_dir``.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

from .config import Settings
from .creative.heuristic import HeuristicCreativeEngine
from .did.analyzer import LETTERS, coverage
from .lexicon.core import Lexicon
from .models.core import WordEntry, WriterHealth, WriterProfile, canonical_text, word_letters
from .planner.beam import PlanError, plan_poem
from .planner.validator import words_of_poem
from .solver import feasibility as solver_feasibility
from .solver.assignment import assign
from .solver.roster import roster_tolerance

POEM_LINES = 14
SOURCE = "orchestrator"
ADVICE_MAX_CHARS = 200


# ------------------------------------------------------------------ live view
@dataclass
class LiveView:
    self_did: str
    game_id: Optional[str]
    members: list[str]                         # lead first
    team_ready: bool
    poem_complete: bool
    accepted_words: list[str]
    last_contributor: Optional[str]
    existing_plan_lines: Optional[list[str]]
    existing_script: Optional[tuple[list[str], list[str]]]   # (words, who)
    candidates: list[tuple[str, str]]          # (did, source) source in waitlist|application|invite
    slow_members: list[str]
    absent_members: list[str]
    lead_max_members: int
    lead_did: str = ""
    x_account: Optional[str] = None
    frozen: bool = False

    @property
    def unavailable(self) -> set[str]:
        return set(self.slow_members) | set(self.absent_members)


def _words_of_lines(lines: Sequence[str]) -> list[str]:
    return [w for line in lines for w in str(line).split(" ") if w]


def _read_json(path: str | os.PathLike) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {}


def load_live(state_path: str | os.PathLike, policy_path: str | os.PathLike) -> LiveView:
    state = _read_json(state_path)
    policy = _read_json(policy_path)
    self_did = str(policy.get("did") or "")
    team = state.get("team") if isinstance(state.get("team"), dict) else None
    lead = state.get("lead") if isinstance(state.get("lead"), dict) else None
    poem = state.get("poem") if isinstance(state.get("poem"), dict) else {}

    game_id: Optional[str] = None
    if team and team.get("game_id"):
        game_id = str(team["game_id"])
    elif lead and lead.get("game_id"):
        game_id = str(lead["game_id"])

    lead_did = str((team or {}).get("lead") or self_did)
    if team and isinstance(team.get("members"), list) and team["members"]:
        raw = [str(m) for m in team["members"]]
    else:
        raw = [self_did] + [str(m) for m in (lead or {}).get("members", []) or []]
    members: list[str] = []
    for m in [lead_did] + raw:
        if m and m not in members:
            members.append(m)

    lines = [str(l) for l in poem.get("lines", []) or []]
    current = [str(w) for w in poem.get("current", []) or []]
    frozen = bool(poem.get("frozen"))
    accepted = _words_of_lines(lines) + current
    poem_complete = frozen and len(lines) >= POEM_LINES

    plan = state.get("plan")
    existing_plan = [str(l) for l in plan] if isinstance(plan, list) and len(plan) == POEM_LINES else None
    script = state.get("script")
    existing_script = None
    if isinstance(script, dict) and isinstance(script.get("words"), list) and isinstance(script.get("who"), list):
        existing_script = ([str(w) for w in script["words"]], [str(w) for w in script["who"]])

    member_set = set(members)
    candidates: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add(dids, source: str) -> None:
        for d in dids or []:
            d = str(d)
            if d and d not in member_set and d not in seen:
                seen.add(d)
                candidates.append((d, source))

    add((lead or {}).get("waitlist", []), "waitlist")
    apps = state.get("applications")
    add(list(apps.keys()) if isinstance(apps, dict) else [], "application")
    add(policy.get("lead_invites", []), "invite")

    slow = [str(d) for d in policy.get("slow_members", []) or [] ]
    absent = [str(d) for d in policy.get("absent_members", []) or []]
    return LiveView(
        self_did=self_did, game_id=game_id, members=members, team_ready=bool((team or {}).get("ready")),
        poem_complete=poem_complete, accepted_words=accepted,
        last_contributor=(str(poem["last_contributor"]) if poem.get("last_contributor") else None),
        existing_plan_lines=existing_plan, existing_script=existing_script, candidates=candidates,
        slow_members=slow, absent_members=absent, lead_max_members=int(policy.get("lead_max_members") or 0),
        lead_did=lead_did, x_account=policy.get("x_account_url"), frozen=frozen,
    )


# ------------------------------------------------------------------ writers
def _scores_map(scores_path: Optional[str | os.PathLike]) -> dict[str, WriterProfile]:
    if not scores_path or not Path(scores_path).exists():
        return {}
    from .diagnostics.metrics import load_writer_scores
    return {w.did: w for w in load_writer_scores(scores_path)}


def _profile(did: str, scores: dict[str, WriterProfile], **update) -> WriterProfile:
    base = scores.get(did)
    if base is None:
        return WriterProfile(did=did, **update)
    return base.model_copy(update=update)


def build_writers(view: LiveView, scores_path: Optional[str | os.PathLike] = None,
                  lead_latency_ms: Optional[float] = None) -> list[WriterProfile]:
    """One WriterProfile per member (lead first). Letters come from the DID; latency/mass_application from scores.
    ``lead_latency_ms`` (config bridge.lead_word_latency_ms) makes the solver treat the lead as slow, so the lead is a
    controller + emergency cover and gets words only where nobody else can spell them."""
    scores = _scores_map(scores_path)
    out: list[WriterProfile] = []
    for did in view.members:
        upd: dict = {"is_lead": did == view.lead_did, "is_self": did == view.self_did}
        if did == view.self_did and view.x_account:
            upd["x_account"] = view.x_account
        if did == view.lead_did and lead_latency_ms:
            upd["word_latency_median_ms"] = float(lead_latency_ms)
        if did in view.absent_members:
            upd["health"] = WriterHealth.DOWN
        elif did in view.slow_members:
            upd["health"] = WriterHealth.SLOW
        out.append(_profile(did, scores, **upd))
    return out


# ------------------------------------------------------------------ plan file
def plan_id(lines: Sequence[str], who: Sequence[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "|" + ",".join(who)).encode("utf-8")).hexdigest()[:12]


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def keys_and_problems(words: Sequence[str], members: Sequence[str], lead_did: str) -> tuple[list[int], list[str]]:
    """Mirror of the live bot's ``key_fits_plan``: keys per word, two-key and adjacent-lead-only problems."""
    letters = {m: frozenset(c for c in m.lower() if "a" <= c <= "z") for m in members}
    can = [[m for m in members if word_letters(w) <= letters[m]] for w in words]
    keys = [len(c) for c in can]
    problems: list[str] = []
    single = [words[i] for i in range(len(words)) if keys[i] < 2]
    if single:
        problems.append(f"{len(single)} word(s) spellable by fewer than two keys (e.g. {', '.join(single[:4])})")
    adj = [(words[i], words[i + 1]) for i in range(len(words) - 1) if can[i] == [lead_did] and can[i + 1] == [lead_did]]
    if adj:
        problems.append(f"{len(adj)} adjacent pair(s) only the lead could spell (e.g. {' '.join(adj[0])})")
    return keys, problems


def _prefix_who(view: LiveView, members: Sequence[str], prefix_len: int) -> list[str]:
    """Contributors for the accepted prefix: the existing script when it lines up, else a lead-first alternation.

    Always alternates and ends on ``last_contributor`` when known (the real constraint for the next word).
    """
    if prefix_len == 0:
        return []
    lead = view.lead_did
    other = next((m for m in members if m != lead), lead)
    who: Optional[list[str]] = None
    if view.existing_script is not None:
        s_words, s_who = view.existing_script
        if len(s_who) >= prefix_len and s_words[:prefix_len] == list(view.accepted_words[:prefix_len]) \
                and all(w in members for w in s_who[:prefix_len]):
            who = list(s_who[:prefix_len])
    if who is None:
        who = [lead if i % 2 == (prefix_len - 1) % 2 else other for i in range(prefix_len)]
    last = view.last_contributor
    if last and last in members and who[-1] != last:
        who[-1] = last
    # repair any consecutive duplicates backwards (prefix positions are informational; the words are accepted)
    for i in range(len(who) - 2, -1, -1):
        if who[i] == who[i + 1]:
            prev = who[i - 1] if i > 0 else None
            who[i] = next(m for m in members if m != who[i + 1] and m != prev) if len(members) > 2 \
                else next(m for m in members if m != who[i + 1])
    return who


def _previous_valid(previous: Optional[dict], view: LiveView, writers: Sequence[WriterProfile], lexicon: Lexicon) -> bool:
    if not isinstance(previous, dict):
        return False
    lines = previous.get("lines")
    who = previous.get("who")
    if previous.get("game_id") != view.game_id or set(previous.get("members") or []) != set(view.members):
        return False
    if not (isinstance(lines, list) and len(lines) == POEM_LINES and isinstance(who, list)):
        return False
    words = _words_of_lines(lines)
    n = len(view.accepted_words)
    if words[:n] != list(view.accepted_words) or len(who) != len(words):
        return False
    if any(who[i] == who[i + 1] for i in range(len(who) - 1)) or any(w not in view.members for w in who):
        return False
    try:
        entries = words_of_poem(lines, lexicon)
    except Exception:  # noqa: BLE001 - unknown token in an old file
        return False
    last = view.last_contributor or (who[n - 1] if n else None)
    fz = solver_feasibility.check(entries, list(writers), lead_did=view.lead_did, last_contributor=last,
                                  start_index=n, unavailable=view.unavailable)
    return bool(fz.feasible)


def _assign_suffix(entries: list[WordEntry], writers: Sequence[WriterProfile], settings: Settings, view: LiveView,
                   prefix_len: int, last: Optional[str]) -> tuple[list[str], bool]:
    """Suffix assignment: every available member contributes; members nobody can seat are dropped (feasible stays)."""
    unavailable = set(view.absent_members)
    res = assign(entries, list(writers), settings=settings, lead_did=view.lead_did, start_index=prefix_len,
                 last_contributor=last, unavailable=unavailable, every_member_must_contribute=True)
    if res.missing_contributors and not res.dead_ends:
        res = assign(entries, list(writers), settings=settings, lead_did=view.lead_did, start_index=prefix_len,
                     last_contributor=last, unavailable=unavailable | set(res.missing_contributors),
                     every_member_must_contribute=True)
    who = [a.primary for a in res.assignments]
    return who, bool(res.feasible)


def plan_for(view: LiveView, writers: Sequence[WriterProfile], settings: Settings, lexicon: Lexicon, *,
             previous: Optional[dict], seed: int, max_seeds: Optional[int] = None,
             time_budget_s: Optional[float] = None) -> dict:
    """The plan file content (BRIDGE.md output 1). Returns ``previous`` untouched when it is still valid."""
    if _previous_valid(previous, view, writers, lexicon):
        return previous  # type: ignore[return-value]
    max_seeds = int(max_seeds if max_seeds is not None else settings.bridge.max_seeds)
    budget = float(time_budget_s if time_budget_s is not None else settings.bridge.seed_budget_s)
    prefix = list(view.accepted_words)
    prefix_len = len(prefix)
    members = list(view.members)
    prefix_who = _prefix_who(view, members, prefix_len)
    last = prefix_who[-1] if prefix_who else None
    engine = HeuristicCreativeEngine(lexicon, seed=seed)

    best: Optional[dict] = None
    errors: list[str] = []
    t0 = time.perf_counter()
    for k in range(max(1, max_seeds)):
        s = seed + k
        try:
            plan = plan_poem(engine, lexicon, writers, settings, accepted_prefix=prefix, lead_did=view.lead_did,
                             last_contributor=last, unavailable=view.unavailable, seed=s, game_id=view.game_id or "game",
                             owner=view.lead_did, source=SOURCE)
        except PlanError as e:
            errors.append(f"seed {s}: {e}")
            if time.perf_counter() - t0 > budget:
                break
            continue
        lines = list(plan.lines)
        words = _words_of_lines(lines)
        lexicon.validate_poem(canonical_text(lines), exact_ten=True)     # official validator, raises on failure
        suffix_who, feasible = _assign_suffix(plan.words, writers, settings, view, prefix_len, last)
        who = prefix_who + suffix_who
        keys, problems = keys_and_problems(words, members, view.lead_did)
        cand = {
            "id": plan_id(lines, who), "game_id": view.game_id, "generated_at": _iso_now(), "members": members,
            "prefix_len": prefix_len, "lines": lines, "who": who, "keys": keys, "fit_problems": problems,
            "source": SOURCE, "feasible": bool(feasible and len(who) == len(words)), "seed": s,
        }
        rank = (0 if cand["feasible"] else 1, len(problems))
        if best is None or rank < best["_rank"]:
            cand["_rank"] = rank
            best = cand
        if rank == (0, 0) or time.perf_counter() - t0 > budget:
            break
    if best is None:
        raise PlanError("no plan for any seed: " + "; ".join(errors[:3]))
    best.pop("_rank", None)
    return best


# ------------------------------------------------------------------ roster report
def plan_from_bot_text(view: LiveView, writers: Sequence[WriterProfile], settings: Settings, lexicon: Lexicon) -> Optional[dict]:
    """text_source == "bot": the live bot's plan (LLM-written, operator-reviewable) is the text; the bridge only assigns.

    Returns None when the bot has no plan yet (nothing to assign). When the remaining words cannot be alternated by the
    available members, returns a ``request: replan`` file so the bot clears its plan and lets the LLM rewrite the suffix
    from the accepted words. Ids are stable per (lines, prefix) so the bot never loops on the same request.
    """
    lines = view.existing_plan_lines
    if not (isinstance(lines, list) and len(lines) == POEM_LINES and all(isinstance(x, str) for x in lines)):
        return None
    members = list(view.members)
    prefix = list(view.accepted_words)
    prefix_len = len(prefix)
    words = _words_of_lines(lines)
    base = {"game_id": view.game_id, "generated_at": _iso_now(), "members": members, "prefix_len": prefix_len, "lines": list(lines)}
    try:
        lexicon.validate_poem(canonical_text(lines), exact_ten=True)
        entries = words_of_poem(lines, lexicon)
    except ValueError as e:
        return dict(base, id=plan_id(lines, ["replan", "invalid", str(prefix_len)]), request="replan", who=[], keys=[], fit_problems=[],
                    source="orchestrator-replan", feasible=False, reason=f"bot text fails the official validator: {e}")
    if words[:prefix_len] != prefix:
        div = next((i for i in range(min(len(words), prefix_len)) if words[i] != prefix[i]), prefix_len)
        return dict(base, id=plan_id(lines, ["replan", "prefix", str(prefix_len)]), request="replan", who=[], keys=[], fit_problems=[],
                    source="orchestrator-replan", feasible=False, reason=f"accepted words diverge from the bot text at index {div}")
    prefix_who = _prefix_who(view, members, prefix_len)
    last = prefix_who[-1] if prefix_who else None
    suffix_who, feasible = _assign_suffix(entries, writers, settings, view, prefix_len, last)
    who = prefix_who + suffix_who
    keys, problems = keys_and_problems(words, members, view.lead_did)
    if not feasible or len(who) != len(words) or any(not w for w in who):
        dead = [i for i in range(prefix_len, len(words)) if keys[i] == 0 or (i < len(who) and not who[i])]
        return dict(base, id=plan_id(lines, ["replan", "infeasible", str(prefix_len)]), request="replan", who=[], keys=keys,
                    fit_problems=problems, source="orchestrator-replan", feasible=False,
                    reason=f"remaining words cannot be alternated by the available members (dead ends near {dead[:4]})")
    return dict(base, id=plan_id(lines, who), who=who, keys=keys, fit_problems=problems, source="bot-text+orchestrator-assign", feasible=True)


def _nonlead_counts(members: Sequence[str], lead_did: str) -> dict[str, int]:
    return {c: sum(1 for m in members if m != lead_did and c in m.lower()) for c in LETTERS}


def roster_report(view: LiveView, writers: Sequence[WriterProfile], settings: Settings,
                  plan_lines: Optional[Sequence[str]] = None, scores_path: Optional[str | os.PathLike] = None,
                  lexicon: Optional[Lexicon] = None) -> dict:
    """BRIDGE.md output 2: coverage of the current roster and what each candidate would add."""
    members = list(view.members)
    lead = view.lead_did
    cov = coverage(members, lead=lead)
    before = _nonlead_counts(members, lead)
    target = max(1, settings.roster.coverage_excluding_lead_target)
    survivability: Optional[float] = None
    if plan_lines and lexicon is not None:
        try:
            entries = words_of_poem(plan_lines, lexicon)
            n = len(view.accepted_words)
            ft = solver_feasibility.failure_tolerance(entries, list(writers), lead_did=lead, start_index=n,
                                                      last_contributor=view.last_contributor if n else None,
                                                      unavailable=set(view.absent_members))
            survivability = ft.survivability
        except Exception:  # noqa: BLE001
            survivability = None
    if survivability is None:
        survivability = roster_tolerance(list(writers), lead, settings)

    scores = _scores_map(scores_path)
    rows: list[dict] = []
    for did, source in view.candidates:
        after_members = members + [did]
        c2 = coverage(after_members, lead=lead)
        after = _nonlead_counts(after_members, lead)
        adds = "".join(c for c in LETTERS if before[c] < target <= after[c])
        prof = scores.get(did)
        note_bits = [f"lacks {''.join(c for c in LETTERS if c not in did.lower()) or '-'}"]
        if prof is not None:
            note_bits.append(f"{prof.words_accepted} accepted words")
            if prof.word_latency_median_ms is not None:
                note_bits.append(f"median {prof.word_latency_median_ms / 1000:.0f}s")
            if prof.mass_application_score:
                note_bits.append(f"spam {prof.mass_application_score:.2f}")
        else:
            note_bits.append("no score history")
        rows.append({
            "did": did, "source": source, "adds_letters": adds, "lead_only_after": c2.lead_only_letters,
            "fragility_after": round(c2.fragility, 4), "rank": 0, "note": "; ".join(note_bits),
            "_sort": (len(c2.lead_only_letters), round(c2.fragility, 4), -len(adds),
                      -(prof.words_accepted if prof else 0), (prof.mass_application_score if prof else 1.0), did),
        })
    rows.sort(key=lambda r: r["_sort"])
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r.pop("_sort")

    size = len(members)
    cap = view.lead_max_members
    head = f"roster {size}/{cap}" if cap else f"roster {size}"
    if cov.missing_from_union:
        body = f"nobody spells '{cov.missing_from_union}'"
    elif cov.lead_only_letters:
        body = f"lead-only letters '{cov.lead_only_letters}'"
    elif cov.single_key_letters:
        body = f"single-key letters '{cov.single_key_letters}'"
    else:
        body = "every letter has two keys"
    if cap and size >= cap:
        advice = f"{head}: full; {body}"
    elif rows and (cov.lead_only_letters or cov.missing_from_union or cov.single_key_letters):
        want = cov.lead_only_letters or cov.missing_from_union or cov.single_key_letters
        picks = ", ".join(f"{r['did'][-8:]} (rank {r['rank']})" if r['rank'] == 1 else r['did'][-8:] for r in rows[:3])
        advice = f"{head}: {body} — prefer candidates with {','.join(want)}: {picks}"
    elif rows:
        advice = f"{head}: {body}; best next: " + ", ".join(r['did'][-8:] for r in rows[:3])
    else:
        advice = f"{head}: {body}; no candidates"
    if len(advice) > ADVICE_MAX_CHARS:
        advice = advice[:ADVICE_MAX_CHARS - 1] + "…"

    report = {
        "game_id": view.game_id, "members": members, "missing_from_union": cov.missing_from_union,
        "single_key_letters": cov.single_key_letters, "lead_only_letters": cov.lead_only_letters,
        "fragility": round(cov.fragility, 4), "survivability": round(survivability, 4),
        "candidates": rows, "advice": advice,
    }
    report["id"] = hashlib.sha256(json.dumps(report, sort_keys=True).encode("utf-8")).hexdigest()[:12]
    report["generated_at"] = _iso_now()
    return report


# ------------------------------------------------------------------ tick
@dataclass
class TickResult:
    wrote_plan: bool
    wrote_roster: bool
    reason: str
    plan_id: Optional[str] = None
    game_id: Optional[str] = None
    roster_id: Optional[str] = None
    elapsed_s: float = 0.0
    fit_problems: list[str] = field(default_factory=list)


def _load_existing(path: Path) -> Optional[dict]:
    try:
        return _read_json(path)
    except (OSError, ValueError):
        return None


def write_atomic(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


_LEXICON_CACHE: dict[str, Lexicon] = {}


def _lexicon_for(settings: Settings) -> Lexicon:
    key = str(settings.cmudict_path)
    if key not in _LEXICON_CACHE:
        _LEXICON_CACHE[key] = Lexicon(Path(key))
    return _LEXICON_CACHE[key]


def tick(state_path: str | os.PathLike, policy_path: str | os.PathLike, out_dir: str | os.PathLike, settings: Settings, *,
         scores_path: Optional[str | os.PathLike] = None, seed: int = 0, lexicon: Optional[Lexicon] = None) -> TickResult:
    t0 = time.perf_counter()
    view = load_live(state_path, policy_path)
    if not view.game_id:
        return TickResult(False, False, "no game", elapsed_s=time.perf_counter() - t0)
    if view.poem_complete:
        return TickResult(False, False, "poem complete", game_id=view.game_id, elapsed_s=time.perf_counter() - t0)
    if view.lead_did and view.lead_did != view.self_did:
        # One plan, one table, one owner: in another lead's team the text and the table are theirs. Write nothing.
        return TickResult(False, False, f"not our team (lead {view.lead_did[-8:]}); nothing written", game_id=view.game_id,
                          elapsed_s=time.perf_counter() - t0)
    out = Path(out_dir)
    lexicon = lexicon or _lexicon_for(settings)
    writers = build_writers(view, scores_path, lead_latency_ms=getattr(settings.bridge, "lead_word_latency_ms", None))

    plan_path = out / f"{view.game_id}.json"
    previous = _load_existing(plan_path)
    wrote_plan = False
    reasons: list[str] = []
    plan: Optional[dict] = None
    if getattr(settings.bridge, "text_source", "bot") == "bot":
        try:
            plan = plan_from_bot_text(view, writers, settings, lexicon)
        except (PlanError, ValueError) as e:
            reasons.append(f"assign failed: {e}")
        if plan is None and not reasons:
            reasons.append("waiting for the bot's text (LLM plan); roster advice only")
    else:
        try:
            plan = plan_for(view, writers, settings, lexicon, previous=previous, seed=seed)
        except (PlanError, ValueError) as e:
            reasons.append(f"plan failed: {e}")
    if plan is not None:
        if previous is not None and previous.get("id") == plan["id"]:
            reasons.append(f"plan {plan['id']} unchanged")
        else:
            write_atomic(plan_path, plan)
            wrote_plan = True
            reasons.append(f"plan {plan['id']} written (prefix {plan['prefix_len']}, problems {len(plan['fit_problems'])})")

    roster_path = out / f"roster-{view.game_id}.json"
    report = roster_report(view, writers, settings, plan_lines=(plan or {}).get("lines") or view.existing_plan_lines,
                           scores_path=scores_path, lexicon=lexicon)
    prev_r = _load_existing(roster_path)
    wrote_roster = False
    if prev_r is not None and prev_r.get("id") == report["id"]:
        reasons.append(f"roster {report['id']} unchanged")
    else:
        write_atomic(roster_path, report)
        wrote_roster = True
        reasons.append(f"roster {report['id']} written ({len(report['candidates'])} candidates)")
    return TickResult(wrote_plan, wrote_roster, "; ".join(reasons), plan_id=(plan or {}).get("id"), game_id=view.game_id,
                      roster_id=report["id"], elapsed_s=time.perf_counter() - t0,
                      fit_problems=list((plan or {}).get("fit_problems") or []))


__all__ = ["LiveView", "TickResult", "load_live", "build_writers", "plan_for", "plan_from_bot_text", "roster_report", "tick",
           "keys_and_problems", "plan_id", "write_atomic"]
