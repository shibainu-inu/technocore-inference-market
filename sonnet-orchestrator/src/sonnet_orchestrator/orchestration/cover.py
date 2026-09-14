"""Cover / hand-off decisions (coordination_lessons.md cases 8 and 11).

Rules encoded here:
- We cover an overdue slot only after the assignee's expected_ms has elapsed (measured, floor from settings).
- We never cover when we posted the previous word (no consecutive contributor).
- Lookahead ≥ settings.solver.minimum_lookahead (≥ 2): after we take word i there must exist a chain of active
  writers (non-SILENT/DOWN, alternating, letters ⊆ DID) for words i+1 .. i+L. The 58→59 and 96→97 "beg" traps are the
  depth-1 case: if word i+1 is spellable only by us, taking word i deadlocks the room.
- After a cover, the next slot is handed off to an active member able to spell it (fewest assignments first).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping, Optional

from ..models import Plan, PoemState, WriterHealth, WriterProfile, word_letters
from .health import ACTIVE_STATES


@dataclass
class CoverDecision:
    cover: bool
    who: Optional[str]
    reason: str
    index: Optional[int] = None
    hand_off: Optional[tuple[int, str]] = None   # (index, did) for the following slot


def letters_of(writers: Iterable[WriterProfile]) -> dict[str, frozenset]:
    return {w.did: w.letters for w in writers}


def spellers(word: str, letters: Mapping[str, frozenset]) -> list[str]:
    need = word_letters(word)
    return [d for d, ls in letters.items() if need <= ls]


def chain_feasible(words: list[str], letters: Mapping[str, frozenset], last: Optional[str], depth: int) -> bool:
    """Does a contributor chain exist for words[0:depth] with no consecutive repeat, starting after ``last``?"""
    if depth <= 0 or not words:
        return True
    cands = [d for d in spellers(words[0], letters) if d != last]
    return any(chain_feasible(words[1:], letters, d, depth - 1) for d in cands)


def _health_of(health, did: str) -> WriterHealth:
    if hasattr(health, "health"):
        return health.health(did)
    return WriterHealth(health.get(did, WriterHealth.HEALTHY))


def _expected_ms(health, did: str, settings) -> float:
    if hasattr(health, "expected_ms"):
        return float(health.expected_ms(did))
    return float(settings.health.minimum_timeout_ms)


def active_letters(writers: Iterable[WriterProfile], health) -> dict[str, frozenset]:
    return {w.did: w.letters for w in writers if _health_of(health, w.did) in ACTIVE_STATES}


def hand_off_next(plan: Plan, next_index: int, letters: Mapping[str, frozenset], self_did: str,
                  exclude: Iterable[str] = ()) -> Optional[str]:
    """Pick an active member (not us, not excluded) able to spell plan.words[next_index]; fewest assignments first."""
    if next_index >= len(plan.words):
        return None
    ex = set(exclude) | {self_did}
    word = plan.words[next_index].text
    cands = [d for d in spellers(word, letters) if d not in ex]
    if not cands:
        return None
    counts = {d: sum(1 for a in plan.assignments if a.primary == d) for d in cands}
    return min(cands, key=lambda d: (counts[d], d))


def should_cover(plan: Plan, poem: PoemState, health, settings, now: datetime, *, self_did: str,
                 writers: Iterable[WriterProfile], waiting_since: Optional[datetime] = None) -> CoverDecision:
    idx = poem.next_index
    if idx >= len(plan.words):
        return CoverDecision(False, None, "poem has no open slot", idx)
    by_index = {a.index: a for a in plan.assignments}
    a = by_index.get(idx)
    if a is None:
        return CoverDecision(False, None, f"no assignment for word {idx}", idx)
    if a.primary == self_did:
        return CoverDecision(False, None, "own slot (not a cover)", idx)
    if poem.last_contributor == self_did:
        return CoverDecision(False, None, "we posted the previous word; cannot post twice in a row", idx)
    writers = list(writers)
    letters = letters_of(writers)
    if self_did not in letters or not (word_letters(plan.words[idx].text) <= letters[self_did]):
        return CoverDecision(False, None, f"we cannot spell {plan.words[idx].text!r}", idx)
    waiting_since = waiting_since or (poem.accepted[-1].accepted_at if poem.accepted and poem.accepted[-1].accepted_at else None)
    waited_ms = (now - waiting_since).total_seconds() * 1000.0 if waiting_since else 0.0
    expected = _expected_ms(health, a.primary, settings)
    assignee_health = _health_of(health, a.primary)
    if waited_ms < expected:
        return CoverDecision(False, None, f"assignee {a.primary[-8:]} within expected {expected:.0f} ms (waited {waited_ms:.0f})", idx)
    act = active_letters(writers, health)
    act.pop(self_did, None)
    depth = max(int(settings.solver.minimum_lookahead), 2)
    following = [w.text for w in plan.words[idx + 1: idx + 1 + depth]]
    if following:
        nxt = following[0]
        if not spellers(nxt, act):
            return CoverDecision(False, None, f"beg trap: next word {nxt!r} is spellable only by us (or by absent members)", idx)
        chain_letters = dict(act)
        chain_letters[self_did] = letters[self_did]
        if not chain_feasible(following, chain_letters, self_did, len(following)):
            return CoverDecision(False, None, f"lookahead {len(following)} infeasible for active writers after we take word {idx}", idx)
    ho = None
    if idx + 1 < len(plan.words):
        nxt_a = by_index.get(idx + 1)
        nxt_primary = nxt_a.primary if nxt_a else None
        if nxt_primary is None or nxt_primary == self_did or nxt_primary not in act:
            who = hand_off_next(plan, idx + 1, act, self_did)
            if who:
                ho = (idx + 1, who)
    return CoverDecision(True, self_did, f"assignee {a.primary[-8:]} ({assignee_health.value}) overdue {waited_ms:.0f} ms ≥ {expected:.0f} ms; lookahead ok", idx, ho)
