"""Line-level prosody: syllable totals and distance from the iambic template.

The stress logic is a port of ``sonnet/prosody.py::iambic_fit`` (audited, not reinvented):
per word the best pronunciation is used, positions advance by the *official* syllable count
(max over pronunciations), and monosyllables / secondary stress match either target.
"""
from __future__ import annotations

from typing import Optional, Sequence

from ..lexicon.core import IAMBIC, Lexicon, bare
from ..models.core import PoemForm


def split_words(line: str) -> list[str]:
    return [w for w in line.strip().split(" ") if w]


def end_word(words: Sequence[str]) -> str:
    """Last token of a line, punctuation stripped, lowercased."""
    if not words:
        raise ValueError("line: empty")
    return bare(words[-1])


def line_syllables(words: Sequence[str], lexicon: Lexicon) -> int:
    """Official syllable total (ValueError on bad token / unknown word)."""
    return lexicon.line_syllables(list(words))


def word_fit(word: str, lexicon: Lexicon, pos: int, template: Sequence[int] = IAMBIC) -> tuple[int, tuple[int, ...]]:
    """Best (matched_positions, stress_pattern) for ``word`` starting at metrical position ``pos``.

    Only positions inside the template are scored; a word running past the end scores its
    in-range positions only.
    """
    info = lexicon.info(word)
    n = info.syllables
    pats = [p for p in info.stresses if len(p) == n] or list(info.stresses) or [(1,) * n]
    best = -1
    best_pat: tuple[int, ...] = pats[0]
    for pat in pats:
        score = 0
        for j, st in enumerate(pat):
            k = pos + j
            if k >= len(template):
                break
            if len(pat) == 1 or st == 2 or st == template[k]:
                score += 1
        if score > best:
            best, best_pat = score, pat
    return max(best, 0), best_pat


def stress_distance(words: Sequence[str], lexicon: Lexicon, template: Sequence[int] = IAMBIC,
                    start_pos: int = 0) -> float:
    """Number of metrical positions that do NOT match ``template`` (0.0 = perfect iambic).

    ``start_pos`` lets a fragment be scored at its real position inside a partially filled line.
    Positions beyond the template are counted as mismatches (an over-long line is never "fit").
    """
    matched = 0
    pos = start_pos
    for w in words:
        m, _ = word_fit(w, lexicon, pos, template)
        matched += m
        pos += lexicon.info(w).syllables
    scored = min(pos, len(template)) - min(start_pos, len(template))
    overflow = max(0, pos - len(template))
    return float(scored - matched + overflow)


def best_stress(word: str, lexicon: Lexicon, pos: int = 0) -> tuple[int, ...]:
    """Stress pattern of the pronunciation that best fits the template at ``pos``."""
    return word_fit(word, lexicon, pos)[1]


def line_ok(words: Sequence[str], lexicon: Lexicon, form: Optional[PoemForm] = None) -> bool:
    """True when every token is valid and the official syllable total equals the form's line length."""
    form = form or PoemForm()
    try:
        return line_syllables(words, lexicon) == form.syllables_per_line
    except ValueError:
        return False


__all__ = ["split_words", "end_word", "line_syllables", "word_fit", "stress_distance", "best_stress", "line_ok"]
