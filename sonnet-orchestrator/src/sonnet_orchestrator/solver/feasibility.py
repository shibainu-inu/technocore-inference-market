"""Exact feasibility of a word sequence under the contest rules (letters, no consecutive contributor).

``check``  reachability over "who may have written the previous word"; O(n * writers^2), no costs.
``parity_check``  the two-person special case: alternation is forced, so every lead-only word must land on the
                  lead's turn (and partner-only words on the partner's).
``failure_tolerance``  remove each active writer in turn and re-check; the "single-failure survivability" KPI is
                  the fraction of active writers whose loss keeps the plan feasible.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Optional, Sequence

from ..models.core import WordEntry, WriterProfile
from .assignment import NO_LAST, active_writers, eligible_writers, writer_label


@dataclass
class Feasibility:
    feasible: bool
    first_dead_end: Optional[int]
    reasons: list[str] = field(default_factory=list)
    dead_ends: list[int] = field(default_factory=list)
    keys: dict[int, int] = field(default_factory=dict)      # word index -> number of active writers able to spell it
    lead_only: list[int] = field(default_factory=list)       # indices only the lead can spell


@dataclass
class ParityReport:
    applicable: bool            # exactly two active writers
    ok: bool
    lead_starts: Optional[bool]  # parity chosen for the first word (None when not applicable / no free choice needed)
    violations: list[int] = field(default_factory=list)
    lead_only: list[int] = field(default_factory=list)
    partner_only: list[int] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


def _slice(words: Sequence[WordEntry], start_index: int) -> list[WordEntry]:
    return sorted((w for w in words if w.index >= start_index), key=lambda w: w.index)


def check(words: Sequence[WordEntry], writers: Sequence[WriterProfile], *, lead_did: str,
          last_contributor: Optional[str] = None, start_index: int = 0,
          unavailable: Iterable[str] = ()) -> Feasibility:
    slice_words = _slice(words, start_index)
    active = active_writers(writers, unavailable)
    did_index = {w.did: i for i, w in enumerate(active)}
    union = frozenset().union(*(w.letters for w in active)) if active else frozenset()
    reach: set[int] = {did_index.get(last_contributor, NO_LAST) if last_contributor else NO_LAST}
    reasons: list[str] = []
    dead_ends: list[int] = []
    keys: dict[int, int] = {}
    lead_only: list[int] = []
    if not active:
        reasons.append("no active writer")
    for word in slice_words:
        el = eligible_writers(word, active)
        keys[word.index] = len(el)
        if len(el) == 1 and active[el[0]].did == lead_did:
            lead_only.append(word.index)
        if not el:
            missing = "".join(sorted(word.letters - union))
            reasons.append(f"#{word.index} {word.text!r}: no active writer spells it (missing letters: {missing or '-'})")
            dead_ends.append(word.index)
            reach = {NO_LAST}
            continue
        new = {i for i in el if any(last != i for last in reach)}
        if not new:
            owners = ", ".join(writer_label(active[i]) for i in el)
            reasons.append(f"#{word.index} {word.text!r}: only [{owners}] spell it and the previous word must be theirs"
                           " (no consecutive words)")
            dead_ends.append(word.index)
            reach = {NO_LAST}
            continue
        reach = new
    return Feasibility(not dead_ends, dead_ends[0] if dead_ends else None, reasons, dead_ends, keys, lead_only)


def parity_check(words: Sequence[WordEntry], active_writers_: Sequence[WriterProfile], lead_did: str,
                 start_index: int = 0, last_contributor: Optional[str] = None,
                 unavailable: Iterable[str] = ()) -> ParityReport:
    """Two-person alternation: turns are forced, so lead-only words must land on the lead's turns.

    With more (or fewer) than two active writers the check is not applicable; ``ok`` then falls back to ``check``.
    """
    active = active_writers(active_writers_, unavailable)
    slice_words = _slice(words, start_index)
    if len(active) != 2 or not any(w.did == lead_did for w in active):
        fb = check(words, active_writers_, lead_did=lead_did, last_contributor=last_contributor,
                   start_index=start_index, unavailable=unavailable)
        return ParityReport(False, fb.feasible, None, fb.dead_ends, fb.lead_only, [],
                            [f"not a two-person alternation with the lead ({len(active)} active); used check()"] + fb.reasons)
    lead = next(w for w in active if w.did == lead_did)
    partner = next(w for w in active if w.did != lead_did)
    lead_only = [w.index for w in slice_words if w.letters <= lead.letters and not w.letters <= partner.letters]
    partner_only = [w.index for w in slice_words if w.letters <= partner.letters and not w.letters <= lead.letters]
    nobody = [w.index for w in slice_words if not w.letters <= lead.letters and not w.letters <= partner.letters]

    def violations_for(lead_starts: bool) -> list[int]:
        out: list[int] = []
        for k, w in enumerate(slice_words):
            lead_turn = lead_starts if k % 2 == 0 else not lead_starts
            if w.index in nobody or (w.index in lead_only and not lead_turn) or (w.index in partner_only and lead_turn):
                out.append(w.index)
        return out

    if last_contributor == lead.did:
        options = [False]
    elif last_contributor == partner.did:
        options = [True]
    else:
        options = [True, False]
    best_start, best_viol = None, None
    for opt in options:
        v = violations_for(opt)
        if best_viol is None or len(v) < len(best_viol):
            best_start, best_viol = opt, v
    assert best_viol is not None
    reasons = [f"lead-only words at {lead_only or '-'}; partner-only at {partner_only or '-'}; nobody at {nobody or '-'}",
               f"turn parity: lead {'starts' if best_start else 'goes second'}"
               + (" (forced by last_contributor)" if len(options) == 1 else " (free choice)")]
    for idx in best_viol:
        w = next(x for x in slice_words if x.index == idx)
        who = "nobody" if idx in nobody else ("lead" if idx in lead_only else "partner")
        reasons.append(f"#{idx} {w.text!r}: spellable by {who} only, lands on the other writer's turn"
                       if who != "nobody" else f"#{idx} {w.text!r}: neither writer spells it")
    return ParityReport(True, not best_viol, best_start, best_viol, lead_only, partner_only, reasons)


class FailureTolerance(Mapping):
    """dict-like: ``ft[did] -> Feasibility`` (plan feasibility with that writer removed) plus KPIs."""

    def __init__(self, per_writer: dict[str, Feasibility], baseline: Feasibility):
        self.per_writer = per_writer
        self.baseline = baseline
        self.fatal: list[str] = [d for d, f in per_writer.items() if not f.feasible]
        self.survivors: list[str] = [d for d, f in per_writer.items() if f.feasible]
        self.survivability: float = (len(self.survivors) / len(per_writer)) if per_writer else 0.0

    def __getitem__(self, did: str) -> Feasibility:
        return self.per_writer[did]

    def __iter__(self) -> Iterator[str]:
        return iter(self.per_writer)

    def __len__(self) -> int:
        return len(self.per_writer)

    def __repr__(self) -> str:
        return f"FailureTolerance(survivability={self.survivability:.2f}, fatal={self.fatal})"


def failure_tolerance(words: Sequence[WordEntry], writers: Sequence[WriterProfile], *, lead_did: str,
                      last_contributor: Optional[str] = None, start_index: int = 0,
                      unavailable: Iterable[str] = ()) -> FailureTolerance:
    unavailable = set(unavailable)
    baseline = check(words, writers, lead_did=lead_did, last_contributor=last_contributor,
                     start_index=start_index, unavailable=unavailable)
    per: dict[str, Feasibility] = {}
    for w in active_writers(writers, unavailable):
        per[w.did] = check(words, writers, lead_did=lead_did, last_contributor=last_contributor,
                           start_index=start_index, unavailable=unavailable | {w.did})
    return FailureTolerance(per, baseline)
