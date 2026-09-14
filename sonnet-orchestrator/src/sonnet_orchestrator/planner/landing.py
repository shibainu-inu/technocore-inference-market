"""Landing routes: who posts the final word, and the alternating path that gets there.

A route is a full assignment of the remaining words (``poem.next_index`` .. end) that respects
spelling and alternation and ends with a chosen final contributor. Writers with an ``x_account``
can publish, so they are preferred as the final contributor; routes are ordered publishers first,
then by reliability. At least ``settings.planner.landing_routes`` routes are produced when the
alternation graph allows it (alternative paths for the same final contributor count).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..config import Settings
from ..models.core import Plan, PoemState, WriterProfile
from .feasible import available_writers, reachable_sets


@dataclass
class LandingRoute:
    final_contributor: str
    path: list[tuple[int, str]]          # (word index, did) for every remaining word, in order
    can_publish: bool
    explanation: str = ""
    handles: dict = field(default_factory=dict)


def _backtrack(reach: list[frozenset], start: int, final: str, prefer: dict[int, str],
               order: list[str]) -> list[tuple[int, str]]:
    """Walk ``reach`` backwards from ``final``; ``prefer`` (index -> did) wins when legal, else ``order``."""
    chosen: list[str] = [final]
    for i in range(len(reach) - 2, -1, -1):
        nxt = chosen[-1]
        options = [d for d in reach[i] if d != nxt]
        want = prefer.get(start + i)
        if want in options:
            pick = want
        else:
            pick = next(d for d in order if d in options)
        chosen.append(pick)
    chosen.reverse()
    return [(start + i, d) for i, d in enumerate(chosen)]


def landing_routes(plan: Plan, poem: PoemState, writers: Sequence[WriterProfile], settings: Settings, *,
                   unavailable: Sequence[str] | set = ()) -> list[LandingRoute]:
    start = poem.next_index
    remaining = plan.words[start:]
    if not remaining:
        return []
    active = available_writers(writers, unavailable)
    if not active:
        return []
    by_did = {w.did: w for w in active}
    reach, dead = reachable_sets(remaining, active, last_contributor=poem.last_contributor)
    if dead is not None:
        return []
    # writer preference order: publishers first, then reliability, then DID for determinism
    order = [w.did for w in sorted(active, key=lambda w: (not bool(w.x_account), -w.reliability, w.did))]
    primary = {a.index: a.primary for a in plan.assignments}
    backup = {a.index: a.backup for a in plan.assignments if a.backup}

    want = settings.planner.landing_routes
    routes: list[LandingRoute] = []
    seen: set[tuple[tuple[int, str], ...]] = set()

    def add(final: str, prefer: dict[int, str], variant: str) -> None:
        path = _backtrack(reach, start, final, prefer, order)
        key = tuple(path)
        if key in seen:
            return
        seen.add(key)
        w = by_did[final]
        contributors = sorted({d for _, d in path})
        routes.append(LandingRoute(
            final_contributor=final, path=path, can_publish=bool(w.x_account),
            explanation=f"final word {plan.words[-1].text!r} by {w.handle or final[-8:]} "
                        f"({'can publish' if w.x_account else 'no x_account'}); {len(path)} words via "
                        f"{len(contributors)} writers; {variant}",
            handles={d: (by_did[d].handle or d[-8:]) for d in contributors}))

    finals = [d for d in order if d in reach[-1]]
    for d in finals:                     # one route per possible final contributor, publishers first
        add(d, primary, "plan primaries where legal")
    for d in finals:                     # then alternative paths until the required count is met
        if len(routes) >= want:
            break
        add(d, backup, "plan backups where legal")
    for d in finals:
        if len(routes) >= want:
            break
        add(d, {}, "reliability order")
    routes.sort(key=lambda r: (not r.can_publish, order.index(r.final_contributor)))
    return routes


__all__ = ["LandingRoute", "landing_routes"]
