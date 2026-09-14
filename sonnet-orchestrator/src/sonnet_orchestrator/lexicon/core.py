"""CMUdict compiler: syllables (official rule: max over pronunciations), stress patterns, rhyme keys, letter masks.

Adapted from the live bot's sonnet/prosody.py (audited, not rewritten). Frozen dictionary = data/cmudict/cmudict.dict.
``official_validator.py`` is a verbatim copy of the referee's sonnet_validate.py and has the final say on form.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional

from . import official_validator as ov

TOKEN = ov.TOKEN
WORD = ov.WORD
VOWELS = ov.VOWELS
IAMBIC = (0, 1, 0, 1, 0, 1, 0, 1, 0, 1)
RHYME_PAIRS = [(1, 3), (2, 4), (5, 7), (6, 8), (9, 11), (10, 12), (13, 14)]
_STRESS = re.compile(r"\d$")
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def bare(token: str) -> str:
    m = TOKEN.fullmatch(token)
    if not m:
        raise ValueError(f"word: bad token {token!r}")
    return m[1].lower()


def letter_mask(letters: Iterable[str]) -> int:
    m = 0
    for c in letters:
        if "a" <= c <= "z":
            m |= 1 << (ord(c) - 97)
    return m


def _vowel_stresses(phones: list[str]) -> tuple[int, ...]:
    return tuple(int(p[-1]) for p in phones if p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"})


def _rhyme_key_of(phones: list[str]) -> str:
    idx = [i for i, p in enumerate(phones) if p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"}]
    primary = [i for i in idx if phones[i].endswith("1")]
    start = primary[-1] if primary else idx[-1]
    return " ".join(_STRESS.sub("", p) for p in phones[start:])


@dataclass(frozen=True)
class WordInfo:
    word: str
    syllables: int                      # official (max over pronunciations)
    letters: frozenset
    mask: int
    stresses: tuple[tuple[int, ...], ...]
    rhyme_keys: frozenset


class Lexicon:
    """Compiled frozen dictionary. Build once per process; cheap lookups afterwards."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.syllables: dict[str, int] = ov.read_lexicon(self.path)
        self.prons: dict[str, list[list[str]]] = {}
        for entry in self.path.read_text(encoding="utf-8").splitlines():
            fields = entry.split("#", 1)[0].split()
            if not fields or fields[0].startswith(";;;"):
                continue
            word = re.sub(r"\(\d+\)$", "", fields[0]).lower()
            if not WORD.fullmatch(word):
                continue
            phones = fields[1:]
            if any(p[:-1] in VOWELS and p[-1:] in {"0", "1", "2"} for p in phones):
                self.prons.setdefault(word, []).append(phones)
        self._info: dict[str, WordInfo] = {}
        self._by_rhyme: dict[str, list[str]] | None = None

    # ------------------------------------------------------------ lookups
    def __contains__(self, token: str) -> bool:
        try:
            return bare(token) in self.syllables
        except ValueError:
            return False

    def __len__(self) -> int:
        return len(self.syllables)

    def info(self, token: str) -> WordInfo:
        w = bare(token)
        wi = self._info.get(w)
        if wi is None:
            if w not in self.syllables:
                raise ValueError(f"word: {w!r} is not in the frozen dictionary")
            prons = self.prons.get(w, [])
            stresses: list[tuple[int, ...]] = []
            for ph in prons:
                s = _vowel_stresses(ph)
                if s not in stresses:
                    stresses.append(s)
            letters = frozenset(c for c in w if "a" <= c <= "z")
            wi = WordInfo(w, self.syllables[w], letters, letter_mask(letters), tuple(stresses),
                          frozenset(_rhyme_key_of(ph) for ph in prons))
            self._info[w] = wi
        return wi

    def word_syllables(self, token: str) -> int:
        """Official token validation + syllable count (raises ValueError on grammar / unknown word)."""
        return ov.word_syllables(token, self.syllables)

    def validate_word(self, token: str, did: str) -> int:
        """Official per-word check including DID letters."""
        return ov.validate_word(token, did, self.syllables)

    def validate_poem(self, text: str, exact_ten: bool = True) -> list[int]:
        return ov.validate_poem(text, self.syllables, exact_ten=exact_ten)

    def line_syllables(self, words: list[str]) -> int:
        return sum(self.word_syllables(w) for w in words)

    def stress_patterns(self, token: str) -> list[tuple[int, ...]]:
        return list(self.info(token).stresses)

    def rhyme_keys(self, token: str) -> frozenset:
        return self.info(token).rhyme_keys

    def rhymes(self, a: str, b: str) -> bool:
        wa, wb = bare(a), bare(b)
        if wa == wb:
            return False
        return bool(self.rhyme_keys(wa) & self.rhyme_keys(wb))

    def can_spell(self, token: str, letters: frozenset | set) -> bool:
        return self.info(token).letters <= frozenset(letters)

    # ------------------------------------------------------------ search
    def by_rhyme(self, key: str) -> list[str]:
        if self._by_rhyme is None:
            self._by_rhyme = {}
            for w in self.syllables:
                for k in self.info(w).rhyme_keys:
                    self._by_rhyme.setdefault(k, []).append(w)
        return self._by_rhyme.get(key, [])

    def candidates(self, allowed_letters: Iterable[str], max_syllables: int, *, min_syllables: int = 1,
                   need_stress: Optional[tuple[int, ...]] = None, rhyme_with: Optional[str] = None,
                   exclude: Iterable[str] = ()) -> list[str]:
        allowed = frozenset(allowed_letters)
        amask = letter_mask(allowed)
        ex = set(exclude)
        pool: Iterable[str]
        if rhyme_with:
            rw = bare(rhyme_with)
            ex.add(rw)
            pool = {w for k in self.rhyme_keys(rw) for w in self.by_rhyme(k)}
        else:
            pool = self.syllables
        out = []
        for w in pool:
            n = self.syllables[w]
            if n > max_syllables or n < min_syllables or w in ex:
                continue
            wi = self.info(w)
            if wi.mask & ~amask:
                continue
            if need_stress is not None and need_stress not in wi.stresses:
                continue
            out.append(w)
        out.sort()
        return out

    # ------------------------------------------------------------ export rows for SQLite
    def rows(self):
        for w, n in self.syllables.items():
            wi = self.info(w)
            yield (w, n, "".join(sorted(wi.letters)), wi.mask)

    def pron_rows(self):
        for w in self.syllables:
            for i, ph in enumerate(self.prons.get(w, [])):
                yield (w, i, " ".join(ph), "".join(str(s) for s in _vowel_stresses(ph)), _rhyme_key_of(ph))


@lru_cache(maxsize=4)
def load_lexicon(path: str) -> Lexicon:
    return Lexicon(Path(path))
