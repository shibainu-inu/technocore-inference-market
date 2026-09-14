"""Word -> writer assignment by dynamic programming.

State: ``dp[pos][last_writer][used_mask]`` where ``pos`` runs over the words to assign (index >= start_index),
``last_writer`` is the index of the writer who took the previous word (sentinel NO_LAST when unconstrained) and
``used_mask`` is the bitmask of writers who contributed at least once (only tracked when
``every_member_must_contribute``; otherwise the mask stays 0 and the state space collapses).

Transition cost for giving word ``p`` to writer ``i``::

    w_latency * latency_norm(i) + w_reliability * (1 - reliability(i)) + w_fragility * (1 / keys(p))
    + w_health * health_penalty(i)

with weights from ``settings.solver.weights``.  Rules:

* a writer may take a word iff ``word.letters <= writer.letters``, the writer is not in ``unavailable`` and its
  health is neither DOWN nor SILENT (those are treated as absent for the lookahead too);
* no consecutive words from the same writer (``last_contributor`` constrains the first word);
* lookahead: before extending a path with writer ``i`` at ``p`` the solver checks that words ``p+1 .. p+L`` can
  still be alternated by the active writers (``L = max(settings.solver.lookahead_words,
  settings.solver.minimum_lookahead)``); paths failing that check are refused whenever any alternative survives.
  Because the DP is exhaustive over the whole horizon the lookahead is exact for feasible inputs; for infeasible
  inputs it is a pruning heuristic that keeps the dead-end count small;
* when no writer can take a word the DP pays ``settings.solver.dead_end_penalty``, records the index in
  ``dead_ends`` and continues with an unconstrained ``last_writer`` (the planner must replace that word);
* ``every_member_must_contribute``: the final state must have every active writer in ``used_mask``; each missing
  writer costs one ``dead_end_penalty`` and makes the result infeasible.

Deterministic: ties are broken by writer input order.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

from ..config import Settings
from ..models.core import Assignment, WordEntry, WriterHealth, WriterProfile
from . import reliability as _rel

NO_LAST = -1          # "previous writer unconstrained"
DEAD = -2             # path choice marker: nobody could take the word

# Health penalty per class (DOWN / SILENT never get a word; they are listed for completeness).
HEALTH_PENALTY: dict[WriterHealth, float] = {
    WriterHealth.HEALTHY: 0.0,
    WriterHealth.SLOW: 0.5,
    WriterHealth.SUSPECT: 0.8,
    WriterHealth.DOWN: 1.0,
    WriterHealth.SILENT: 1.0,
}
INACTIVE_HEALTH = frozenset({WriterHealth.DOWN, WriterHealth.SILENT})


@dataclass
class AssignmentResult:
    assignments: list[Assignment]
    cost: float
    feasible: bool
    dead_ends: list[int]
    explanation: list[str]
    start_index: int = 0
    lookahead: int = 0
    missing_contributors: list[str] = field(default_factory=list)   # every_member_must_contribute misses
    per_index_cost: dict[int, float] = field(default_factory=dict)

    def primary_of(self, index: int) -> Optional[str]:
        for a in self.assignments:
            if a.index == index:
                return a.primary or None
        return None


# ------------------------------------------------------------------ helpers
def writer_label(writer: WriterProfile) -> str:
    return writer.handle or writer.did[-8:]


def is_active(writer: WriterProfile, unavailable: Iterable[str] = ()) -> bool:
    return writer.did not in set(unavailable) and writer.health not in INACTIVE_HEALTH


def active_writers(writers: Sequence[WriterProfile], unavailable: Iterable[str] = ()) -> list[WriterProfile]:
    """Writers allowed to take a turn, in input order."""
    unav = set(unavailable)
    return [w for w in writers if w.did not in unav and w.health not in INACTIVE_HEALTH]


def health_penalty(writer: WriterProfile, settings: Optional[Settings] = None) -> float:
    table = HEALTH_PENALTY
    if settings is not None:
        override = getattr(settings.solver, "health_penalty", None)
        if isinstance(override, dict):
            table = {**HEALTH_PENALTY, **{WriterHealth(k): float(v) for k, v in override.items()}}
    return table.get(writer.health, 1.0)


def latency_norm(writers: Sequence[WriterProfile]) -> dict[str, float]:
    """word_latency_median_ms / max over writers; missing -> 1.0 (assume the worst)."""
    known = [w.word_latency_median_ms for w in writers if w.word_latency_median_ms is not None]
    mx = max(known) if known else 0.0
    out: dict[str, float] = {}
    for w in writers:
        if w.word_latency_median_ms is None or mx <= 0:
            out[w.did] = 1.0
        else:
            out[w.did] = max(0.0, min(1.0, float(w.word_latency_median_ms) / float(mx)))
    return out


def eligible_writers(word: WordEntry, active: Sequence[WriterProfile]) -> list[int]:
    """Indices (into ``active``) of writers who can spell ``word``."""
    need = word.letters
    return [i for i, w in enumerate(active) if need <= w.letters]


def every_member_flag(settings: Settings, override: Optional[bool]) -> bool:
    if override is not None:
        return bool(override)
    return bool(getattr(settings.solver, "every_member_must_contribute", False))


def effective_lookahead(settings: Settings, override: Optional[int] = None) -> int:
    la = settings.solver.lookahead_words if override is None else int(override)
    return max(int(la), int(settings.solver.minimum_lookahead), 0)


def _popcount(x: int) -> int:
    return bin(x).count("1")


# ------------------------------------------------------------------ main entry
def assign(words: Sequence[WordEntry], writers: Sequence[WriterProfile], *, settings: Settings, lead_did: str,
           start_index: int = 0, last_contributor: Optional[str] = None, unavailable: Iterable[str] = (),
           every_member_must_contribute: Optional[bool] = None, lookahead: Optional[int] = None) -> AssignmentResult:
    unavailable = set(unavailable)
    slice_words = sorted((w for w in words if w.index >= start_index), key=lambda w: w.index)
    active = active_writers(writers, unavailable)
    n, m = len(slice_words), len(active)
    L = effective_lookahead(settings, lookahead)
    emmc = every_member_flag(settings, every_member_must_contribute)
    weights = settings.solver.weights
    penalty = float(settings.solver.dead_end_penalty)

    explanation: list[str] = [
        f"writers active={m}/{len(writers)} (unavailable={sorted(unavailable) or '-'}, DOWN/SILENT excluded)",
        f"lookahead={L} (lookahead_words={settings.solver.lookahead_words}, minimum={settings.solver.minimum_lookahead})",
        f"every_member_must_contribute={'on' if emmc else 'off'}",
    ]
    if n == 0:
        return AssignmentResult([], 0.0, True, [], explanation + ["nothing to assign"], start_index, L)

    # ---- static per-writer cost and per-word data
    lat = latency_norm(active)
    rel = {w.did: _rel.effective_reliability(w, settings) for w in active}
    hp = {w.did: health_penalty(w, settings) for w in active}
    static_cost = [weights.latency * lat[w.did] + weights.reliability * (1.0 - rel[w.did]) + weights.health * hp[w.did]
                   for w in active]
    eligible = [eligible_writers(w, active) for w in slice_words]
    keys = [len(e) for e in eligible]
    frag = [weights.fragility * (1.0 / k) if k > 0 else weights.fragility for k in keys]

    did_index = {w.did: i for i, w in enumerate(active)}
    last0 = did_index.get(last_contributor, NO_LAST) if last_contributor else NO_LAST
    full_mask = (1 << m) - 1 if emmc else 0

    # ---- lookahead: chain_ok(q, last, end) = words q..end-1 can be alternated given previous writer `last`
    memo: dict[tuple[int, int, int], bool] = {}

    def chain_ok(q: int, last: int, end: int) -> bool:
        if q >= end:
            return True
        key = (q, last, end)
        hit = memo.get(key)
        if hit is not None:
            return hit
        el = eligible[q]
        if not el:                       # hard dead end: nobody spells it; the DP handles it as a reset
            res = chain_ok(q + 1, NO_LAST, end)
        else:
            res = any(chain_ok(q + 1, i, end) for i in el if i != last)
        memo[key] = res
        return res

    ok_next = [[chain_ok(p + 1, i, min(p + 1 + L, n)) for i in range(m)] for p in range(n)]

    # ---- DP
    # states: dict[(last, mask)] -> cost ; back[p][(last, mask)] -> (prev_last, prev_mask, choice)
    cur: dict[tuple[int, int], float] = {(last0, 0): 0.0}
    back: list[dict[tuple[int, int], tuple[int, int, int]]] = []
    for p in range(n):
        nxt: dict[tuple[int, int], float] = {}
        bk: dict[tuple[int, int], tuple[int, int, int]] = {}
        el = eligible[p]
        for (last, mask), cost in cur.items():
            cands = [i for i in el if i != last]
            good = [i for i in cands if ok_next[p][i]]
            use = good if good else cands
            if not use:
                key = (NO_LAST, mask)
                c = cost + penalty
                if key not in nxt or c < nxt[key]:
                    nxt[key] = c
                    bk[key] = (last, mask, DEAD)
                continue
            for i in use:
                nm = (mask | (1 << i)) if emmc else 0
                key = (i, nm)
                c = cost + static_cost[i] + frag[p]
                if key not in nxt or c < nxt[key]:
                    nxt[key] = c
                    bk[key] = (last, mask, i)
        # deterministic iteration order for the next round
        cur = dict(sorted(nxt.items(), key=lambda kv: (kv[0][0], kv[0][1])))
        back.append(bk)

    # ---- choose the best final state (every-member misses cost one penalty each)
    best_key, best_total = None, float("inf")
    for key, cost in cur.items():
        missing = _popcount(full_mask & ~key[1]) if emmc else 0
        total = cost + penalty * missing
        if total < best_total:
            best_key, best_total = key, total
    assert best_key is not None

    # ---- backtrack
    choices: list[int] = [DEAD] * n
    key = best_key
    for p in range(n - 1, -1, -1):
        prev_last, prev_mask, choice = back[p][key]
        choices[p] = choice
        key = (prev_last, prev_mask)

    missing_dids = [active[i].did for i in range(m) if emmc and not (best_key[1] >> i) & 1]

    # ---- build assignments, backups, explanation
    assignments: list[Assignment] = []
    dead_ends: list[int] = []
    per_index_cost: dict[int, float] = {}
    for p, word in enumerate(slice_words):
        choice = choices[p]
        prev = choices[p - 1] if p > 0 else last0
        if prev == DEAD:
            prev = NO_LAST
        nxt_choice = choices[p + 1] if p + 1 < n else NO_LAST
        if nxt_choice == DEAD:
            nxt_choice = NO_LAST
        lead_only = keys[p] == 1 and active[eligible[p][0]].did == lead_did
        if choice == DEAD:
            dead_ends.append(word.index)
            per_index_cost[word.index] = penalty
            if keys[p] == 0:
                union = frozenset().union(*(w.letters for w in active)) if active else frozenset()
                missing = "".join(sorted(word.letters - union))
                reason = f"no active writer spells it (letters nobody has: {missing or '-'})"
            else:
                owners = ", ".join(writer_label(active[i]) for i in eligible[p])
                prev_label = writer_label(active[prev]) if prev >= 0 else "-"
                reason = f"only [{owners}] spell it but the previous word is by {prev_label} (no consecutive words)"
            assignments.append(Assignment(index=word.index, primary="", backup=None, keys=keys[p], lead_only=lead_only))
            explanation.append(f"#{word.index} {word.text!r}: DEAD END - {reason}")
            continue
        primary = active[choice]
        strict = [b for b in eligible[p] if b not in (choice, prev, nxt_choice)]
        relaxed = [b for b in eligible[p] if b not in (choice, prev)]
        backup_note = ""
        if strict:
            b = min(strict, key=lambda i: (static_cost[i], i))
        elif relaxed:
            b = min(relaxed, key=lambda i: (static_cost[i], i))
            backup_note = " (backup would also need the next slot re-covered)"
        else:
            b = None
        backup = active[b].did if b is not None else None
        c = static_cost[choice] + frag[p]
        per_index_cost[word.index] = c
        assignments.append(Assignment(index=word.index, primary=primary.did, backup=backup, keys=keys[p], lead_only=lead_only))
        explanation.append(
            f"#{word.index} {word.text!r} -> {writer_label(primary)} (keys={keys[p]}{', lead-only' if lead_only else ''};"
            f" backup={writer_label(active[b]) if b is not None else '-'}{backup_note});"
            f" cost {c:.3f} = lat {weights.latency * lat[primary.did]:.3f}"
            f" + rel {weights.reliability * (1.0 - rel[primary.did]):.3f}"
            f" + frag {frag[p]:.3f} + health {weights.health * hp[primary.did]:.3f} [{primary.health.value}]"
        )

    if missing_dids:
        explanation.append("every_member_must_contribute violated; never assigned: "
                           + ", ".join(writer_label(active[did_index[d]]) for d in missing_dids))
    feasible = not dead_ends and not missing_dids
    explanation.append(f"total cost {best_total:.3f}; dead ends {dead_ends or '-'}; feasible={feasible}")
    return AssignmentResult(assignments, best_total, feasible, dead_ends, explanation, start_index, L,
                            missing_dids, per_index_cost)
