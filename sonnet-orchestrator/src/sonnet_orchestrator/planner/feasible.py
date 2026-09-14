"""Bridge to ``solver.feasibility.check`` with a local fallback.

The solver package is developed concurrently; the planner must not hard-depend on it. The local
check is exact for the two rules the planner cares about at plan time: every word must be
spellable by an available writer, and no two consecutive words may come from the same writer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..models.core import WordEntry, WriterHealth, WriterProfile, word_letters

UNAVAILABLE_HEALTH = (WriterHealth.DOWN, WriterHealth.SILENT)


@dataclass
class Feasibility:
    feasible: bool
    first_dead_end: Optional[int] = None
    reasons: list[str] = field(default_factory=list)


def available_writers(writers: Sequence[WriterProfile], unavailable: Sequence[str] | set = ()) -> list[WriterProfile]:
    """Writers a plan may rely on: not explicitly excluded and not DOWN/SILENT."""
    ex = set(unavailable)
    return [w for w in writers if w.did not in ex and w.health not in UNAVAILABLE_HEALTH]


def _texts(words: Sequence[WordEntry] | Sequence[str]) -> list[str]:
    return [w.text if isinstance(w, WordEntry) else w for w in words]


def reachable_sets(words: Sequence[WordEntry] | Sequence[str], writers: Sequence[WriterProfile], *,
                   last_contributor: Optional[str] = None) -> tuple[list[frozenset], Optional[int]]:
    """Forward alternation DP.

    ``R[i]`` = writers who can post word ``i`` such that words ``0..i`` all have a valid, alternating
    assignment. Returns ``(R, first_dead_end)``; ``R`` stops at the dead end.
    """
    letters = {w.did: w.letters for w in writers}
    prev: Optional[frozenset] = frozenset([last_contributor]) if last_contributor else None
    out: list[frozenset] = []
    for i, text in enumerate(_texts(words)):
        need = word_letters(text)
        spellers = [d for d, ls in letters.items() if need <= ls]
        if prev is None:
            cur = frozenset(spellers)
        else:
            cur = frozenset(d for d in spellers if any(p != d for p in prev))
        if not cur:
            return out, i
        out.append(cur)
        prev = cur
    return out, None


def extend_reach(reach: Optional[frozenset], tokens: Sequence[str], writers: Sequence[WriterProfile]) -> Optional[frozenset]:
    """One DP step per token: new reachable set, or None at the first dead end. ``reach=None`` means no constraint."""
    letters = [(w.did, w.letters) for w in writers]
    for text in tokens:
        need = word_letters(text)
        if reach is None:
            cur = frozenset(d for d, ls in letters if need <= ls)
        else:
            cur = frozenset(d for d, ls in letters if need <= ls and any(p != d for p in reach))
        if not cur:
            return None
        reach = cur
    return reach if reach is not None else frozenset(d for d, _ in letters)


def local_check(words: Sequence[WordEntry] | Sequence[str], writers: Sequence[WriterProfile], *,
                lead_did: Optional[str] = None, last_contributor: Optional[str] = None,
                start_index: int = 0) -> Feasibility:
    """Exact feasibility under spelling + alternation (no cost model)."""
    _, dead = reachable_sets(words, writers, last_contributor=last_contributor)
    if dead is None:
        return Feasibility(True, None, [])
    text = _texts(words)[dead]
    spellers = [w.did for w in writers if w.can_spell(text)]
    if not spellers:
        reason = f"word {start_index + dead} {text!r}: no available writer can spell it"
    else:
        reason = f"word {start_index + dead} {text!r}: only {spellers[0][-6:]} spells it and they hold the previous turn"
    return Feasibility(False, start_index + dead, [reason])


def check(words: Sequence[WordEntry] | Sequence[str], writers: Sequence[WriterProfile], *,
          lead_did: Optional[str] = None, last_contributor: Optional[str] = None,
          start_index: int = 0) -> Feasibility:
    """``solver.feasibility.check`` when importable and healthy, else the local exact check."""
    entries = [w if isinstance(w, WordEntry) else WordEntry(index=start_index + i, text=w, line=0, syllables=0)
               for i, w in enumerate(words)]
    try:
        from ..solver import feasibility as solver_feasibility  # lazy: written concurrently by agent A
        res = solver_feasibility.check(entries, list(writers), lead_did=lead_did,
                                       last_contributor=last_contributor, start_index=start_index)
        return Feasibility(bool(res.feasible), getattr(res, "first_dead_end", None), list(getattr(res, "reasons", [])))
    except Exception:  # noqa: BLE001 - any solver problem falls back to the exact local rule
        return local_check(words, writers, lead_did=lead_did, last_contributor=last_contributor, start_index=start_index)


__all__ = ["Feasibility", "available_writers", "reachable_sets", "extend_reach", "local_check", "check", "UNAVAILABLE_HEALTH"]
