"""Reconcile a plan with the referee-accepted prefix and regenerate the mutable suffix.

Hybrid text (accepted words that differ from the plan) is normal: the accepted text is adopted
verbatim and only the suffix is regenerated. The accepted prefix is never edited.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from ..config import Settings
from ..creative.engine import CreativeEngine
from ..lexicon.core import Lexicon
from ..models.core import Plan, PoemForm, PoemState, WriterProfile
from .beam import PlanError, plan_poem
from .feasible import available_writers, check


@dataclass
class ReconcileResult:
    prefix_matches: bool                 # every accepted word equals the plan word at that index
    divergence_index: Optional[int]      # first index where they differ (None if none)
    accepted_len: int
    plan_len: int
    accepted_beyond_plan: bool = False   # the poem has more words than the plan (should not happen)

    @property
    def hybrid(self) -> bool:
        return not self.prefix_matches


def reconcile(plan: Plan, poem: PoemState) -> ReconcileResult:
    """Compare the accepted stream with the plan, token by token (exact, punctuation included)."""
    accepted = poem.accepted_texts()
    n = len(accepted)
    div: Optional[int] = None
    for i, text in enumerate(accepted):
        if i >= len(plan.words) or plan.words[i].text != text:
            div = i
            break
    return ReconcileResult(prefix_matches=div is None, divergence_index=div, accepted_len=n, plan_len=len(plan.words),
                           accepted_beyond_plan=n > len(plan.words))


def first_infeasible_index(plan: Plan, poem: PoemState, writers: Sequence[WriterProfile], *,
                           lead_did: Optional[str] = None, unavailable: Sequence[str] | set = ()) -> Optional[int]:
    """Index of the first planned (not yet accepted) word with no feasible alternating assignment."""
    start = poem.next_index
    rest = plan.words[start:]
    if not rest:
        return None
    fz = check(rest, available_writers(writers, unavailable), lead_did=lead_did,
               last_contributor=poem.last_contributor, start_index=start)
    return None if fz.feasible else fz.first_dead_end


def replan(plan: Plan, poem: PoemState, writers: Sequence[WriterProfile], *, engine: CreativeEngine, lexicon: Lexicon,
           settings: Settings, seed: Optional[int] = None, from_index: Optional[int] = None,
           unavailable: Sequence[str] | set = (), lead_did: Optional[str] = None, theme: str = "",
           minimal_change: bool = True, form: Optional[PoemForm] = None) -> Plan:
    """New plan: accepted prefix verbatim, suffix regenerated, ``version + 1``, ``source="solver"``.

    When the accepted prefix still matches and ``minimal_change`` is set, planned words up to the
    first infeasible index (or ``from_index``) are kept so the execution table changes as little as
    possible; if that kept tail turns out to be unplannable the suffix is regenerated from
    ``poem.next_index`` instead.
    """
    rec = reconcile(plan, poem)
    accepted = poem.accepted_texts()
    keep = list(accepted)
    lead = lead_did or plan.owner
    if rec.prefix_matches and minimal_change and len(plan.words) > len(accepted):
        stop = len(plan.words)
        dead = first_infeasible_index(plan, poem, writers, lead_did=lead, unavailable=unavailable)
        if dead is not None:
            stop = min(stop, dead)
        if from_index is not None:
            stop = min(stop, max(from_index, len(accepted)))
        keep = keep + [w.text for w in plan.words[len(accepted):stop]]
    if seed is None:
        seed = settings.simulation.seed + plan.version + 1
    common = dict(accepted_prefix=None, theme=theme, seed=seed, game_id=plan.game_id, lead_did=lead, owner=plan.owner,
                  version=plan.version + 1, source="solver", unavailable=unavailable,
                  last_contributor=poem.last_contributor, form=form)
    try:
        common["accepted_prefix"] = keep
        new = plan_poem(engine, lexicon, writers, settings, **common)
    except PlanError:
        if keep == accepted:
            raise
        common["accepted_prefix"] = accepted
        new = plan_poem(engine, lexicon, writers, settings, **common)
    new.accepted_prefix_len = len(accepted)
    return new


__all__ = ["ReconcileResult", "reconcile", "replan", "first_infeasible_index"]
