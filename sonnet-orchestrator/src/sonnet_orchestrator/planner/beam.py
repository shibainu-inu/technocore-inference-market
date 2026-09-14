"""Line-by-line beam search that turns a ``CreativeEngine`` into a validated ``Plan``.

* The accepted prefix is laid into lines by official 10-syllable boundaries and fixed verbatim; a
  partially filled line is completed by asking the engine for a fragment of the remaining budget.
* Each line's candidates are filtered hard (exact syllables, required rhyme, distinct families,
  no repeated end word, alternation feasibility via ``planner.feasible.check``) and ranked by the
  engine score (meter + two-key redundancy) plus a rhyme-partner bonus.
* The final poem must pass ``planner.validator`` strictly (official form + all rhyme pairs +
  distinct families) or ``PlanError`` is raised.
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..config import Settings
from ..creative.engine import CreativeEngine, LineContext
from ..lexicon.core import Lexicon, bare
from ..models.core import Assignment, Plan, PoemForm, WordEntry, WriterProfile
from .feasible import available_writers, check, extend_reach
from .meter import best_stress
from .validator import ValidationReport, rhyme_pairs_for, validate_poem_lines

STANZA_END_PUNCT = "."
LINE_END_PUNCT = ","
REDUNDANCY_BONUS = 0.25   # per line: fraction of words spellable by >= 2 available writers


class PlanError(RuntimeError):
    """No valid poem could be produced (reason in ``args[0]``, partial state in ``.state``)."""

    def __init__(self, msg: str, state: Optional["BeamState"] = None):
        super().__init__(msg)
        self.state = state


@dataclass
class BeamState:
    lines: list[list[str]] = field(default_factory=list)   # completed lines (tokens)
    partial: list[str] = field(default_factory=list)       # tokens of the current, unfinished line
    score: float = 0.0
    reach: Optional[frozenset] = None                      # writers who may have posted the last token (None = any)

    def all_tokens(self) -> list[str]:
        return [t for l in self.lines for t in l] + list(self.partial)

    def end_words(self) -> list[str]:
        return [bare(l[-1]) for l in self.lines]


# ------------------------------------------------------------------ prefix layout
def lay_prefix(prefix: Sequence[str], lexicon: Lexicon, form: PoemForm) -> tuple[list[list[str]], list[str]]:
    """Split accepted tokens into full lines by exact 10-syllable boundaries; return (lines, partial)."""
    lines: list[list[str]] = []
    cur: list[str] = []
    used = 0
    for i, tok in enumerate(prefix):
        n = lexicon.word_syllables(tok)          # raises on bad token / unknown word
        if used + n > form.syllables_per_line:
            raise PlanError(f"accepted prefix: word {i} {tok!r} crosses the line boundary ({used}+{n} > {form.syllables_per_line})")
        cur.append(tok)
        used += n
        if used == form.syllables_per_line:
            lines.append(cur)
            cur, used = [], 0
    if len(lines) > form.lines or (len(lines) == form.lines and cur):
        raise PlanError("accepted prefix: longer than the poem")
    return lines, cur


def partner_index(line: int, form: PoemForm) -> Optional[int]:
    """Earlier line that ``line`` must rhyme with, or None when the line opens a family."""
    for a, b in rhyme_pairs_for(form):
        if b - 1 == line:
            return a - 1
    return None


def _family_openers(form: PoemForm) -> list[int]:
    return [a - 1 for a, _ in rhyme_pairs_for(form)]


# ------------------------------------------------------------------ helpers
def _decorate(tokens: list[str], line: int, fresh_line: bool, form: PoemForm) -> list[str]:
    out = list(tokens)
    if fresh_line and out and out[0][0].islower():
        out[0] = out[0][0].upper() + out[0][1:]
    if out:
        last = out[-1]
        if last[-1].isalpha():
            stanza_ends = set()
            acc = 0
            for n in form.stanzas:
                acc += n
                stanza_ends.add(acc - 1)
            out[-1] = last + (STANZA_END_PUNCT if line in stanza_ends else LINE_END_PUNCT)
    return out


def _families_ok(end_words: list[str], lexicon: Lexicon, form: PoemForm) -> bool:
    keys = []
    for li in _family_openers(form):
        if li < len(end_words):
            keys.append(lexicon.rhyme_keys(end_words[li]))
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if keys[i] & keys[j]:
                return False
    return True


def _pick_lead(writers: Sequence[WriterProfile], lead_did: Optional[str]) -> str:
    if lead_did:
        return lead_did
    for w in writers:
        if w.is_lead:
            return w.did
    for w in writers:
        if w.is_self:
            return w.did
    return writers[0].did if writers else ""


def _rhyme_key_for(word: str, partner: Optional[str], lexicon: Lexicon) -> Optional[str]:
    keys = lexicon.rhyme_keys(word)
    if partner:
        shared = keys & lexicon.rhyme_keys(partner)
        if shared:
            return sorted(shared)[0]
    return sorted(keys)[0] if keys else None


def build_word_entries(lines: list[list[str]], lexicon: Lexicon, form: PoemForm) -> list[WordEntry]:
    entries: list[WordEntry] = []
    idx = 0
    for li, toks in enumerate(lines):
        pos = 0
        p = partner_index(li, form)
        partner_end = bare(lines[p][-1]) if p is not None and p < len(lines) else None
        for k, tok in enumerate(toks):
            w = bare(tok)
            n = lexicon.info(w).syllables
            is_end = k == len(toks) - 1
            entries.append(WordEntry(index=idx, text=tok, line=li, syllables=n, stress=best_stress(w, lexicon, pos),
                                     rhyme_key=_rhyme_key_for(w, partner_end if is_end else None, lexicon)))
            idx += 1
            pos += n
    return entries


def try_assign(words: list[WordEntry], writers: Sequence[WriterProfile], settings: Settings, lead_did: str,
               *, start_index: int = 0, last_contributor: Optional[str] = None) -> list[Assignment]:
    """``solver.assignment.assign`` when available; empty list otherwise (the solver fills them later)."""
    try:
        from ..solver import assignment as solver_assignment  # lazy: written concurrently by agent A
        res = solver_assignment.assign(words, list(writers), settings=settings, lead_did=lead_did,
                                       start_index=start_index, last_contributor=last_contributor)
        return list(res.assignments)
    except Exception:  # noqa: BLE001
        return []


# ------------------------------------------------------------------ main entry
def plan_poem(engine: CreativeEngine, lexicon: Lexicon, writers: Sequence[WriterProfile], settings: Settings, *,
              accepted_prefix: Sequence[str] = (), theme: str = "", seed: Optional[int] = None,
              game_id: str = "game", lead_did: Optional[str] = None, owner: Optional[str] = None,
              version: int = 1, source: str = "solver", unavailable: Sequence[str] | set = (),
              last_contributor: Optional[str] = None, form: Optional[PoemForm] = None) -> Plan:
    """Beam-search a complete, validated sonnet plan whose first words equal ``accepted_prefix`` verbatim.

    Raises ``PlanError`` when the prefix is invalid, infeasible, or no rhyme/feasible completion exists.
    """
    form = form or PoemForm()
    writers = list(writers)
    if not writers:
        raise PlanError("no writers")
    lead = _pick_lead(writers, lead_did)
    active = available_writers(writers, unavailable)
    if not active:
        raise PlanError("no available writers")
    per_writer = {w.did: frozenset(w.letters) for w in active}
    allowed = frozenset().union(*per_writer.values())
    if seed is not None and hasattr(engine, "reseed"):
        engine.reseed(seed)
    beam_width = settings.planner.beam_width
    expansions = settings.planner.expansion_count

    prefix = [str(t) for t in accepted_prefix]
    fixed_lines, partial = lay_prefix(prefix, lexicon, form)
    fz = check(prefix, active, lead_did=lead, last_contributor=last_contributor)
    if prefix and not fz.feasible:
        raise PlanError(f"accepted prefix is infeasible for the available writers: {'; '.join(fz.reasons)}")

    reach0 = extend_reach(frozenset([last_contributor]) if last_contributor else None, prefix, active)
    beam: list[BeamState] = [BeamState(lines=[list(l) for l in fixed_lines], partial=list(partial), reach=reach0)]
    for line_no in range(len(fixed_lines), form.lines):
        p_idx = partner_index(line_no, form)
        new_states: list[BeamState] = []
        seen: set[tuple[str, ...]] = set()
        for st in beam:
            used = lexicon.line_syllables(st.partial) if st.partial else 0
            budget = form.syllables_per_line - used
            ends = st.end_words()
            partner_end = ends[p_idx] if p_idx is not None else None
            ctx = LineContext(line_index=line_no, previous_lines=[" ".join(l) for l in st.lines],
                              rhyme_key=partner_end, allowed_letters=allowed, per_writer_letters=per_writer,
                              theme=theme, syllables=budget, max_candidates=expansions,
                              forbidden_end_words=set(ends))
            for cand in engine.propose_lines(ctx):
                toks = _decorate(cand.words, line_no, fresh_line=not st.partial, form=form)
                full = list(st.partial) + toks
                try:
                    if lexicon.line_syllables(full) != form.syllables_per_line:
                        continue
                    end = bare(full[-1])
                    if end in ends:
                        continue
                    if partner_end is not None and not lexicon.rhymes(end, partner_end):
                        continue
                    if not _families_ok(ends + [end], lexicon, form):
                        continue
                    if any(not (lexicon.info(t).letters <= allowed) for t in toks):
                        continue
                except ValueError:
                    continue
                key = tuple(bare(t) for l in st.lines for t in l) + tuple(bare(t) for t in full)
                if key in seen:
                    continue
                reach = extend_reach(st.reach, toks, active)     # exact alternation + spelling, incremental
                if reach is None:
                    continue
                seen.add(key)
                redundancy = sum(1 for t in toks if sum(1 for ls in per_writer.values() if lexicon.info(t).letters <= ls) >= 2)
                score = st.score + cand.score + REDUNDANCY_BONUS * redundancy / max(1, len(toks))
                new_states.append(BeamState(lines=[list(l) for l in st.lines] + [full], partial=[], score=score, reach=reach))
        if not new_states:
            why = f"line {line_no + 1}: no candidate satisfied"
            why += f" rhyme with {partner_end!r}" if p_idx is not None else " the constraints"
            raise PlanError(why, beam[0] if beam else None)
        # deterministic, non-alphabetical tie-break (alphabetical would favour lines starting with "A")
        new_states.sort(key=lambda s: (-s.score, zlib.crc32("\n".join(" ".join(l) for l in s.lines).encode())))
        beam = []
        for st in new_states:                                     # solver feasibility on the survivors only
            fz = check(st.all_tokens(), active, lead_did=lead, last_contributor=last_contributor)
            if fz.feasible:
                beam.append(st)
                if len(beam) >= beam_width:
                    break
        if not beam:
            raise PlanError(f"line {line_no + 1}: solver rejected every candidate: {fz.reasons}", new_states[0])

    report: Optional[ValidationReport] = None
    for st in beam:
        line_strs = [" ".join(l) for l in st.lines]
        report = validate_poem_lines(line_strs, lexicon, form)
        if report.strict_ok:
            return _make_plan(st.lines, lexicon, form, active, settings, lead, prefix, game_id, owner or lead,
                              version, source, last_contributor)
    raise PlanError(f"no beam state passed validation: {report.errors if report else 'empty beam'}", beam[0] if beam else None)


def _make_plan(lines: list[list[str]], lexicon: Lexicon, form: PoemForm, writers: Sequence[WriterProfile],
               settings: Settings, lead: str, prefix: Sequence[str], game_id: str, owner: str, version: int,
               source: str, last_contributor: Optional[str]) -> Plan:
    words = build_word_entries(lines, lexicon, form)
    line_strs = [" ".join(l) for l in lines]
    plan = Plan(plan_id="pending", game_id=game_id, version=version, owner=owner, source=source, words=words,
                accepted_prefix_len=len(prefix), lines=line_strs)
    plan.plan_id = f"{game_id}-v{version}-{plan.hash_prefix}"
    plan.assignments = try_assign(words, writers, settings, lead, last_contributor=last_contributor)
    return plan


__all__ = ["plan_poem", "PlanError", "BeamState", "lay_prefix", "partner_index", "build_word_entries", "try_assign"]
