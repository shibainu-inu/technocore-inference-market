"""Human-readable explanation of an assignment (why this writer, how many keys, which backup)."""
from __future__ import annotations

from typing import Sequence

from ..models.core import WordEntry, WriterProfile
from .assignment import AssignmentResult, writer_label


def explain_assignment(result: AssignmentResult, words: Sequence[WordEntry], writers: Sequence[WriterProfile]) -> str:
    by_did = {w.did: w for w in writers}
    by_index = {w.index: w for w in words}

    def label(did: str | None) -> str:
        if not did:
            return "-"
        w = by_did.get(did)
        return writer_label(w) if w else did[-8:]

    lines = [
        f"assignment from index {result.start_index}: {len(result.assignments)} words, cost {result.cost:.3f},"
        f" feasible={result.feasible}, dead ends {result.dead_ends or '-'}, lookahead {result.lookahead}",
    ]
    if result.missing_contributors:
        lines.append("members never assigned: " + ", ".join(label(d) for d in result.missing_contributors))
    lines.append("")
    for a in result.assignments:
        word = by_index.get(a.index)
        text = word.text if word else "?"
        if not a.primary:
            lines.append(f"#{a.index:>3} {text:<14} DEAD END (keys={a.keys})")
            continue
        flags = " lead-only" if a.lead_only else ""
        cost = result.per_index_cost.get(a.index)
        cost_s = f" cost {cost:.3f}" if cost is not None else ""
        lines.append(f"#{a.index:>3} {text:<14} {label(a.primary):<12} keys={a.keys}{flags} backup={label(a.backup)}{cost_s}")
    lines.append("")
    lines.append("reasons:")
    lines.extend(f"  {e}" for e in result.explanation)
    return "\n".join(lines)


def explain_index(result: AssignmentResult, words: Sequence[WordEntry], writers: Sequence[WriterProfile], index: int) -> str:
    """Explanation for a single word index (subset of explain_assignment)."""
    full = explain_assignment(result, words, writers)
    lines = [l for l in full.splitlines() if l.strip().startswith(f"{index} ") or l.strip().startswith(f"#{index} ")
             or l.strip().startswith(f"{index:3d} ") or f"[{index}]" in l or l.strip().startswith(f"{index}:")]
    return "\n".join(lines) if lines else full
