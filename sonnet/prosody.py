#!/usr/bin/env python3
"""Prosody helpers on top of the official sonnet validator.

Contest gates (syllable count = max over pronunciations, token grammar, DID-letter
check, 14-line / 4-4-4-2 / exact-ten) are delegated to ``pkg/sonnet_validate.py``.
This module adds stress, rhyme, iambic fit, canonical text/hash and candidate
search, parsed from the same frozen ``pkg/cmudict.dict``.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_PKG = _HERE / "pkg"
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

import sonnet_validate as sv  # noqa: E402  (vendored official validator)

TOKEN = sv.TOKEN
WORD = sv.WORD
VOWELS = sv.VOWELS
DICT_PATH = _PKG / "cmudict.dict"
IAMBIC = (0, 1, 0, 1, 0, 1, 0, 1, 0, 1)

_STRESS = re.compile(r"\d$")


# ---------- dictionary ----------
def read_lexicon(path: Path = DICT_PATH) -> dict[str, int]:
    """Official syllable lexicon (word -> max syllable count)."""
    return sv.read_lexicon(Path(path))


def load_prons(path: Path = DICT_PATH) -> dict[str, list[list[str]]]:
    """Lowercase word -> list of pronunciations (phones with stress digits)."""
    prons: dict[str, list[list[str]]] = {}
    for entry in Path(path).read_text(encoding="utf-8").splitlines():
        fields = entry.split("#", 1)[0].split()
        if not fields or fields[0].startswith(";;;"):
            continue
        word = re.sub(r"\(\d+\)$", "", fields[0]).lower()
        if not WORD.fullmatch(word):
            continue
        phones = fields[1:]
        if any(p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"} for p in phones):
            prons.setdefault(word, []).append(phones)
    if not prons:
        raise ValueError("dictionary: no usable pronunciations")
    return prons


_PRONS: dict[str, list[list[str]]] | None = None
_LEX: dict[str, int] | None = None


def prons() -> dict[str, list[list[str]]]:
    """Module-level cached pronunciations."""
    global _PRONS
    if _PRONS is None:
        _PRONS = load_prons()
    return _PRONS


def lexicon() -> dict[str, int]:
    """Module-level cached official lexicon."""
    global _LEX
    if _LEX is None:
        _LEX = read_lexicon()
    return _LEX


# ---------- tokens ----------
def bare(token: str) -> str:
    """Strip one trailing punctuation mark and lowercase; ValueError on bad grammar."""
    m = TOKEN.fullmatch(token)
    if not m:
        raise ValueError(f"word: bad token {token!r}")
    return m[1].lower()


def did_letters(did: str) -> set[str]:
    """Lowercase a-z letters in the full DID string, ``did:key:`` prefix included."""
    return {c for c in did.lower() if "a" <= c <= "z"}


def word_letters(word: str) -> set[str]:
    return {c for c in word.lower() if "a" <= c <= "z"}


# ---------- stress and rhyme ----------
def _vowel_stresses(phones: list[str]) -> tuple[int, ...]:
    return tuple(int(p[-1]) for p in phones if p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"})


def stress_patterns(word: str, prons_: dict | None = None) -> list[tuple[int, ...]]:
    """Per pronunciation: 0/1/2 per vowel phone. Unknown word -> ValueError."""
    p = (prons_ or prons()).get(bare(word))
    if not p:
        raise ValueError(f"word: {word!r} is not in the frozen dictionary")
    out: list[tuple[int, ...]] = []
    for ph in p:
        s = _vowel_stresses(ph)
        if s not in out:
            out.append(s)
    return out


def _rhyme_key_of(phones: list[str]) -> str:
    idx = [i for i, p in enumerate(phones) if p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"}]
    primary = [i for i in idx if phones[i].endswith("1")]
    start = primary[-1] if primary else idx[-1]
    return " ".join(_STRESS.sub("", p) for p in phones[start:])


def rhyme_key(word: str, prons_: dict | None = None) -> set[str]:
    """Set of rhyme keys (phones from last primary-stressed vowel, stress stripped)."""
    p = (prons_ or prons()).get(bare(word))
    if not p:
        raise ValueError(f"word: {word!r} is not in the frozen dictionary")
    return {_rhyme_key_of(ph) for ph in p}


def rhymes(a: str, b: str, prons_: dict | None = None) -> bool:
    """True when the two words share a rhyme key and are not the same word."""
    wa, wb = bare(a), bare(b)
    if wa == wb:
        return False
    return bool(rhyme_key(wa, prons_) & rhyme_key(wb, prons_))


# ---------- lines ----------
def line_syllables(words: list[str], lex: dict | None = None) -> int:
    """Official syllable total of a word list (ValueError on unknown words)."""
    lex = lex or lexicon()
    return sum(sv.word_syllables(w, lex) for w in words)


def iambic_fit(words: list[str], prons_: dict | None = None) -> float:
    """Fraction of positions matching weak-strong 0101010101, best per-word pronunciation.

    Monosyllables and secondary stress match either target. Scored on the
    positions available when the line is not exactly 10 syllables.
    """
    prons_ = prons_ or prons()
    matched = 0
    pos = 0
    for w in words:
        pats = stress_patterns(w, prons_)
        best = -1
        best_len = 0
        for pat in pats:
            score = 0
            for j, s in enumerate(pat):
                k = pos + j
                if k >= len(IAMBIC):
                    break
                if len(pat) == 1 or s == 2 or s == IAMBIC[k]:
                    score += 1
            if score > best:
                best, best_len = score, len(pat)
        matched += best
        pos += best_len
    total = min(pos, len(IAMBIC))
    return matched / total if total else 0.0


def split_words(line: str) -> list[str]:
    return [w for w in line.strip().split(" ") if w]


def end_word(line: str) -> str:
    """Last token of a line with trailing punctuation stripped, lowercased."""
    words = split_words(line)
    if not words:
        raise ValueError("line: empty")
    return bare(words[-1])


# ---------- poem ----------
def canonical_text(lines: list[str]) -> str:
    """Rules form: one space between words, LF between lines, blank line between 4/4/4/2, no final LF."""
    if len(lines) != 14:
        raise ValueError(f"lines: expected 14, got {len(lines)}")
    norm = [" ".join(split_words(l)) for l in lines]
    stanzas = [norm[0:4], norm[4:8], norm[8:12], norm[12:14]]
    return "\n\n".join("\n".join(s) for s in stanzas)


def poem_sha256(lines: list[str]) -> str:
    return hashlib.sha256(canonical_text(lines).encode("utf-8")).hexdigest()


RHYME_PAIRS = [(1, 3), (2, 4), (5, 7), (6, 8), (9, 11), (10, 12), (13, 14)]
FAMILY_LETTERS = "ABCDEFG"


def rhyme_report(lines: list[str], prons_: dict | None = None) -> dict:
    """ABAB CDCD EFEF GG check: each pair rhymes? seven families mutually distinct?"""
    prons_ = prons_ or prons()
    if len(lines) != 14:
        raise ValueError(f"lines: expected 14, got {len(lines)}")
    ends = [end_word(l) for l in lines]
    pairs = {}
    for a, b in RHYME_PAIRS:
        try:
            pairs[f"{a}-{b}"] = rhymes(ends[a - 1], ends[b - 1], prons_)
        except ValueError:
            pairs[f"{a}-{b}"] = False
    families = {}
    for letter, (a, _) in zip(FAMILY_LETTERS, RHYME_PAIRS, strict=False):
        try:
            families[letter] = rhyme_key(ends[a - 1], prons_)
        except ValueError:
            families[letter] = set()
    clashes = []
    letters = list(families)
    for i in range(len(letters)):
        for j in range(i + 1, len(letters)):
            if families[letters[i]] & families[letters[j]]:
                clashes.append(letters[i] + letters[j])
    return {
        "end_words": ends,
        "pairs": pairs,
        "all_pairs_rhyme": all(pairs.values()),
        "families_distinct": not clashes,
        "clashes": clashes,
    }


# ---------- candidate search ----------
class CandidateIndex:
    """Per-word letter sets and syllable counts, built once."""

    def __init__(self, lex: dict | None = None, prons_: dict | None = None):
        self.lex = lex or lexicon()
        self.prons = prons_ or prons()
        self.letters = {w: word_letters(w) for w in self.lex}

    def search(self, allowed_letters: set[str], max_syllables: int,
               need_stress: tuple | None = None, rhyme_with: str | None = None) -> list[str]:
        target_keys = rhyme_key(rhyme_with, self.prons) if rhyme_with else None
        rw = bare(rhyme_with) if rhyme_with else None
        out = []
        for w, n in self.lex.items():
            if n > max_syllables or not self.letters[w] <= allowed_letters:
                continue
            p = self.prons.get(w)
            if not p:
                continue
            if need_stress is not None and need_stress not in {_vowel_stresses(ph) for ph in p}:
                continue
            if target_keys is not None:
                if w == rw or not ({_rhyme_key_of(ph) for ph in p} & target_keys):
                    continue
            out.append(w)
        return out


_INDEX: CandidateIndex | None = None


def candidates(lex: dict | None, allowed_letters: set[str], max_syllables: int,
               prons_: dict | None = None, need_stress: tuple | None = None,
               rhyme_with: str | None = None) -> list[str]:
    """Words with letters ⊆ allowed, syllables ≤ max, optional stress pattern and rhyme."""
    global _INDEX
    if lex is None and prons_ is None:
        if _INDEX is None:
            _INDEX = CandidateIndex()
        idx = _INDEX
    else:
        idx = CandidateIndex(lex, prons_)
    return idx.search(set(allowed_letters), max_syllables, need_stress, rhyme_with)


__all__ = [
    "read_lexicon", "load_prons", "prons", "lexicon", "bare", "did_letters", "word_letters",
    "stress_patterns", "rhyme_key", "rhymes", "line_syllables", "iambic_fit", "split_words",
    "end_word", "canonical_text", "poem_sha256", "rhyme_report", "CandidateIndex", "candidates",
    "DICT_PATH", "IAMBIC", "RHYME_PAIRS",
]
