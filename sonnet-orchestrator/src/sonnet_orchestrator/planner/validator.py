"""Poem validation: structural (official validator = final say) plus rhyme diagnostics.

``ok`` means the official validator accepted the canonical text (14 lines, 4/4/4/2, exactly ten
official syllables per line, every token in the frozen dictionary). Rhyme is NOT a contest gate,
so it is reported separately (``rhyme_pairs_ok``, ``families_distinct``); ``strict_ok`` folds it in
and is what the planner requires of its own output.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..lexicon.core import RHYME_PAIRS, Lexicon, bare
from ..models.core import PoemForm, canonical_text
from .meter import split_words

FAMILY_LETTERS = "ABCDEFG"


@dataclass
class ValidationReport:
    ok: bool                                   # official validator accepted the canonical text
    errors: list[str] = field(default_factory=list)
    per_line_syllables: list[int] = field(default_factory=list)
    rhyme_pairs_ok: dict[str, bool] = field(default_factory=dict)   # "1-3" -> bool
    families_distinct: bool = True
    clashes: list[str] = field(default_factory=list)                 # e.g. ["AB", "CG"]
    end_words: list[str] = field(default_factory=list)
    official_error: Optional[str] = None
    canonical: str = ""

    @property
    def all_pairs_rhyme(self) -> bool:
        return bool(self.rhyme_pairs_ok) and all(self.rhyme_pairs_ok.values())

    @property
    def strict_ok(self) -> bool:
        return self.ok and self.all_pairs_rhyme and self.families_distinct


def rhyme_pairs_for(form: PoemForm) -> list[tuple[int, int]]:
    """1-based (a, b) line pairs derived from the form's rhyme scheme (ABAB CDCD EFEF GG -> RHYME_PAIRS)."""
    scheme = form.rhyme_scheme
    if len(scheme) != form.lines:
        return list(RHYME_PAIRS)
    first: dict[str, int] = {}
    pairs: list[tuple[int, int]] = []
    for i, letter in enumerate(scheme, 1):
        if letter in first:
            pairs.append((first[letter], i))
        else:
            first[letter] = i
    return pairs


def _rhyme_diagnostics(lines_words: list[list[str]], lexicon: Lexicon, form: PoemForm, rep: ValidationReport) -> None:
    ends: list[str] = []
    for ws in lines_words:
        try:
            ends.append(bare(ws[-1]) if ws else "")
        except ValueError:
            ends.append("")
    rep.end_words = ends
    pairs = rhyme_pairs_for(form)
    for a, b in pairs:
        key = f"{a}-{b}"
        try:
            rep.rhyme_pairs_ok[key] = bool(ends[a - 1] and ends[b - 1] and lexicon.rhymes(ends[a - 1], ends[b - 1]))
        except (ValueError, IndexError):
            rep.rhyme_pairs_ok[key] = False
    families: list[tuple[str, frozenset]] = []
    for letter, (a, _b) in zip(FAMILY_LETTERS, pairs):
        try:
            families.append((letter, lexicon.rhyme_keys(ends[a - 1])))
        except (ValueError, IndexError):
            families.append((letter, frozenset()))
    for i in range(len(families)):
        for j in range(i + 1, len(families)):
            if families[i][1] & families[j][1]:
                rep.clashes.append(families[i][0] + families[j][0])
    rep.families_distinct = not rep.clashes


def validate_poem_lines(lines: Sequence[str] | Sequence[Sequence[str]], lexicon: Lexicon,
                        form: Optional[PoemForm] = None) -> ValidationReport:
    """Validate a full poem given as 14 line strings (or 14 token lists).

    Structural checks are delegated to the official validator on the canonical text; per-line
    diagnostics (syllable counts, rhyme pairs, family distinctness) are added so a caller can see
    *why* something failed.
    """
    form = form or PoemForm()
    lines_words: list[list[str]] = [split_words(l) if isinstance(l, str) else list(l) for l in lines]
    line_strs = [" ".join(ws) for ws in lines_words]
    rep = ValidationReport(ok=False, canonical=canonical_text(line_strs))

    if len(lines_words) != form.lines:
        rep.errors.append(f"lines: expected {form.lines}, got {len(lines_words)}")
    for n, ws in enumerate(lines_words, 1):
        if not ws:
            rep.errors.append(f"line {n}: empty")
            rep.per_line_syllables.append(0)
            continue
        try:
            count = lexicon.line_syllables(ws)
        except ValueError as e:
            rep.errors.append(f"line {n}: {e}")
            rep.per_line_syllables.append(0)
            continue
        rep.per_line_syllables.append(count)
        if count != form.syllables_per_line:
            rep.errors.append(f"line {n}: syllables must be exactly {form.syllables_per_line}, got {count}")

    if len(lines_words) == form.lines:
        _rhyme_diagnostics(lines_words, lexicon, form, rep)

    # Final say: the official validator on the canonical text.
    try:
        counts = lexicon.validate_poem(rep.canonical, exact_ten=(form.syllables_per_line == 10))
        rep.per_line_syllables = list(counts)
        rep.ok = not rep.errors
    except ValueError as e:
        rep.official_error = str(e)
        rep.ok = False
        if str(e) not in rep.errors:
            rep.errors.append(f"official: {e}")
    return rep


def validate_poem_text(text: str, lexicon: Lexicon, form: Optional[PoemForm] = None) -> ValidationReport:
    """Validate canonical text (blank lines between stanzas are ignored for line splitting)."""
    lines = [l for l in text.removesuffix("\n").split("\n") if l.strip()]
    return validate_poem_lines(lines, lexicon, form)


__all__ = ["ValidationReport", "validate_poem_lines", "validate_poem_text", "rhyme_pairs_for", "FAMILY_LETTERS"]


def words_of_poem(lines: Sequence[str], lexicon: Lexicon, form: Optional[PoemForm] = None) -> list[WordEntry]:
    """Flatten poem lines into WordEntry objects (index/line/syllables/stress/rhyme_key) for the solver / CLI."""
    from ..models import WordEntry
    out: list[WordEntry] = []
    idx = 0
    for li, line in enumerate(lines):
        for tok in str(line).split():
            info = lexicon.info(tok)
            out.append(WordEntry(index=idx, text=tok, line=li, syllables=info.syllables,
                                 stress=info.stresses[0] if info.stresses else (), rhyme_key=next(iter(info.rhyme_keys), None)))
            idx += 1
    return out
