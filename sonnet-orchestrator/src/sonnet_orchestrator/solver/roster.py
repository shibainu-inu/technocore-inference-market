"""Roster optimisation: which candidates to seat next to the lead.

Option score (weights from ``settings.roster.weights``)::

    reliability            mean effective reliability of the non-lead members
    lexical_coverage       frequency-weighted share of letters the whole roster spells (did.analyzer.coverage)
    redundant_coverage     mean of (a) frequency-weighted redundancy credit over all letters and (b) mean credit over
                           the bottleneck letters ("anost"); credit = min(non-lead keys, target) / target
    response_speed         mean ref/(ref + word latency), ref = health.minimum_timeout_ms (unknown -> neutral)
    historical_completion  mean poems_completed/games_joined (no history -> 0)
    - size_penalty_per_extra_member * max(0, size - preferred_size)

``tolerance`` = fraction of non-lead members whose loss keeps every bottleneck letter spellable by at least one
remaining non-lead member (single-failure survivability against the parity trap).

When ``require_accepted_word_history`` is on, candidates without any accepted word are dropped from the pool as long
as enough candidates with history remain for the minimum roster size; otherwise they are kept and ranked last.
The pool is capped at ``candidate_pool_limit`` (settings.roster attribute when present, else DEFAULT_POOL_LIMIT)
best individual candidates before exhaustive enumeration, so 196 discovery-room candidates stay tractable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from itertools import combinations
from typing import Optional, Sequence

from ..config import Settings
from ..did.analyzer import LETTERS, LETTER_FREQ, CoverageReport, coverage
from ..models.core import WriterProfile
from . import reliability as _rel

DEFAULT_POOL_LIMIT = 12          # compute budget, not a policy knob: C(12, 7) = 792 evaluations per size


@dataclass
class RosterOption:
    members: list[str]                 # lead first, then the chosen candidates (input order)
    score: float
    coverage: CoverageReport
    tolerance: float
    explanation: list[str] = field(default_factory=list)
    components: dict[str, float] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.members)


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _speed(w: WriterProfile, settings: Settings) -> float:
    return _rel.response_score(w, settings)


def _completion(w: WriterProfile) -> float:
    if w.games_joined <= 0:
        return 0.0
    return max(0.0, min(1.0, w.poems_completed / w.games_joined))


def _weighted_share(letters: set[str] | frozenset[str]) -> float:
    total = sum(LETTER_FREQ.values())
    return sum(LETTER_FREQ[c] for c in letters) / total


def member_value(w: WriterProfile, settings: Settings, now: Optional[datetime] = None) -> float:
    """Individual ranking used to cap the candidate pool (same weights as the option score)."""
    rw = settings.roster.weights
    bottleneck = set(settings.roster.bottleneck_letters)
    own_bottleneck = len(bottleneck & set(w.letters)) / len(bottleneck) if bottleneck else 0.0
    return (rw.reliability * _rel.effective_reliability(w, settings, now)
            + rw.lexical_coverage * _weighted_share(w.letters)
            + rw.redundant_coverage * own_bottleneck
            + rw.response_speed * _speed(w, settings)
            + rw.historical_completion * _completion(w))


def redundant_coverage_excluding_lead(members: Sequence[WriterProfile], lead_did: str, settings: Settings) -> tuple[float, float, dict[str, int]]:
    """(frequency-weighted redundancy credit, bottleneck credit, non-lead key counts).

    Credit per letter = min(non-lead keys, target) / target, so a letter only the lead spells earns 0, one non-lead
    key earns 1/target and >= target keys earn 1 (graded rather than thresholded so a parity trap costs score).
    """
    target = max(1, settings.roster.coverage_excluding_lead_target)
    others = [m for m in members if m.did != lead_did]
    counts = {c: sum(1 for m in others if c in m.letters) for c in LETTERS}
    credit = {c: min(counts[c], target) / target for c in LETTERS}     # graded: 1 key of 2 earns half
    total = sum(LETTER_FREQ.values())
    weighted = sum(LETTER_FREQ[c] * credit[c] for c in LETTERS) / total
    bottleneck = list(settings.roster.bottleneck_letters)
    b_share = (sum(credit[c] for c in bottleneck) / len(bottleneck)) if bottleneck else 0.0
    return weighted, b_share, counts


def roster_tolerance(members: Sequence[WriterProfile], lead_did: str, settings: Settings) -> float:
    others = [m for m in members if m.did != lead_did]
    bottleneck = list(settings.roster.bottleneck_letters)
    if not others or not bottleneck:
        return 0.0
    ok = 0
    for gone in others:
        remaining = [m for m in others if m.did != gone.did]
        if all(any(c in m.letters for m in remaining) for c in bottleneck):
            ok += 1
    return ok / len(others)


def evaluate(members: Sequence[WriterProfile], lead: WriterProfile, settings: Settings,
             now: Optional[datetime] = None) -> RosterOption:
    """Score one roster (lead must be among ``members``; it is moved to the front)."""
    ordered = [lead] + [m for m in members if m.did != lead.did]
    others = ordered[1:]
    letters_map = {m.did: m.letters for m in ordered}
    cov = coverage([m.did for m in ordered], lead=lead.did, letters_of=lambda d: letters_map[d])
    rw = settings.roster.weights
    rel = _mean([_rel.effective_reliability(m, settings, now) for m in others])
    lex = cov.weighted_coverage
    red_w, red_b, _ = redundant_coverage_excluding_lead(ordered, lead.did, settings)
    red = (red_w + red_b) / 2.0
    speed = _mean([_speed(m, settings) for m in others])
    hist = _mean([_completion(m) for m in others])
    extra = max(0, len(ordered) - settings.roster.preferred_size)
    size_pen = settings.roster.size_penalty_per_extra_member * extra
    score = (rw.reliability * rel + rw.lexical_coverage * lex + rw.redundant_coverage * red
             + rw.response_speed * speed + rw.historical_completion * hist - size_pen)
    tol = roster_tolerance(ordered, lead.did, settings)
    comps = {"reliability": rel, "lexical_coverage": lex, "redundant_coverage": red,
             "redundant_weighted": red_w, "redundant_bottleneck": red_b,
             "response_speed": speed, "historical_completion": hist, "size_penalty": size_pen}
    labels = ", ".join((m.handle or m.did[-8:]) for m in others)
    expl = [
        f"members (excl. lead): {labels}",
        f"score {score:.3f} = rel {rw.reliability * rel:.3f} + lex {rw.lexical_coverage * lex:.3f}"
        f" + red {rw.redundant_coverage * red:.3f} + speed {rw.response_speed * speed:.3f}"
        f" + hist {rw.historical_completion * hist:.3f} - size {size_pen:.3f}",
        f"bottleneck '{settings.roster.bottleneck_letters}' covered >= {settings.roster.coverage_excluding_lead_target}x"
        f" excluding lead: {red_b:.0%}; single-failure tolerance {tol:.0%}",
    ]
    if cov.missing_from_union:
        expl.append(f"nobody spells: {cov.missing_from_union}")
    if cov.lead_only_letters:
        expl.append(f"lead-only letters (parity trap): {cov.lead_only_letters}")
    no_hist = [m for m in others if m.words_accepted <= 0]
    if no_hist:
        expl.append("no accepted-word history: " + ", ".join((m.handle or m.did[-8:]) for m in no_hist))
    return RosterOption([m.did for m in ordered], score, cov, tol, expl, comps)


def optimize(candidates: Sequence[WriterProfile], lead: WriterProfile, settings: Settings, size: Optional[int] = None,
             *, now: Optional[datetime] = None, pool_limit: Optional[int] = None,
             max_options: Optional[int] = None) -> list[RosterOption]:
    """Rank rosters built from ``lead`` + candidates. Sizes = [size] or minimum_size..maximum_size."""
    rc = settings.roster
    pool_notes: list[str] = []
    cands = [c for c in candidates if c.did != lead.did]
    # dedupe by DID, keep first occurrence
    seen: set[str] = set()
    cands = [c for c in cands if not (c.did in seen or seen.add(c.did))]
    if rc.require_accepted_word_history:
        with_hist = [c for c in cands if c.words_accepted > 0]
        if len(with_hist) >= rc.minimum_size - 1:
            dropped = len(cands) - len(with_hist)
            cands = with_hist
            if dropped:
                pool_notes.append(f"dropped {dropped} candidate(s) without accepted-word history")
        else:
            pool_notes.append("not enough candidates with accepted-word history; no-history candidates kept")
    limit = pool_limit if pool_limit is not None else int(getattr(rc, "candidate_pool_limit", DEFAULT_POOL_LIMIT))
    ranked = sorted(cands, key=lambda c: (-(c.words_accepted > 0), -member_value(c, settings, now), c.did))
    if len(ranked) > limit:
        pool_notes.append(f"pool capped to the {limit} best of {len(ranked)} candidates")
        ranked = ranked[:limit]
    pool = ranked
    if not pool:
        return []
    sizes = [size] if size is not None else list(range(rc.minimum_size, rc.maximum_size + 1))
    sizes = [s for s in sizes if 2 <= s and s - 1 <= len(pool)]
    if not sizes:
        sizes = [len(pool) + 1]
        pool_notes.append(f"too few candidates for the requested size; using all {len(pool)}")
    options: list[RosterOption] = []
    for s in sizes:
        for combo in combinations(pool, s - 1):
            options.append(evaluate([lead, *combo], lead, settings, now))
    options.sort(key=lambda o: (-o.score, -o.tolerance, o.size, o.members))
    for o in options:
        o.explanation = pool_notes + o.explanation
    if max_options is not None:
        options = options[:max_options]
    return options
