"""DID letter analysis and roster coverage.

Rule: a contributor may only post words whose letters all occur in its DID string (``did:key:`` prefix included,
case-insensitive). Every DID therefore spells d,i,k,e,y,z,m and usually 't','h' etc.; scarce letters vary.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

LETTERS = "abcdefghijklmnopqrstuvwxyz"
# English letter frequency (share of running text); used to weight the coverage score.
LETTER_FREQ = {
    "e": .127, "t": .091, "a": .082, "o": .075, "i": .070, "n": .067, "s": .063, "h": .061, "r": .060, "d": .043,
    "l": .040, "c": .028, "u": .028, "m": .024, "w": .024, "f": .022, "g": .020, "y": .020, "p": .019, "b": .015,
    "v": .010, "k": .008, "j": .002, "x": .002, "q": .001, "z": .001,
}
ROSTER_BOTTLENECK_LETTERS = "anost"


def did_letters(did: str) -> frozenset[str]:
    return frozenset(c for c in did.lower() if "a" <= c <= "z")


@dataclass
class CoverageReport:
    members: list[str]
    letters_per_member: dict[str, frozenset]
    union: frozenset
    missing_from_union: str                       # letters nobody can spell
    counts: dict[str, int]                        # letter -> how many members spell it
    single_key_letters: str                       # letters only one member spells (fragile)
    lead_only_letters: str                        # letters only the lead spells (parity trap)
    weighted_coverage: float                      # frequency-weighted share of letters covered ≥1
    weighted_redundancy: float                    # frequency-weighted share of letters covered ≥2
    fragility: float                              # 1 - weighted_redundancy
    explanation: list[str] = field(default_factory=list)


def coverage(members: Iterable[str], lead: str | None = None, letters_of=None) -> CoverageReport:
    members = list(members)
    letters_of = letters_of or did_letters
    per = {m: frozenset(letters_of(m)) for m in members}
    union = frozenset().union(*per.values()) if per else frozenset()
    counts = {c: sum(1 for m in members if c in per[m]) for c in LETTERS}
    single = "".join(c for c in LETTERS if counts[c] == 1)
    lead_only = "".join(c for c in LETTERS if counts[c] == 1 and lead and c in per.get(lead, frozenset()))
    wc = sum(LETTER_FREQ[c] for c in LETTERS if counts[c] >= 1)
    wr = sum(LETTER_FREQ[c] for c in LETTERS if counts[c] >= 2)
    total = sum(LETTER_FREQ.values())
    rep = CoverageReport(members, per, union, "".join(c for c in LETTERS if c not in union), counts, single, lead_only,
                         wc / total, wr / total, 1 - wr / total)
    for m in members:
        miss = "".join(c for c in LETTERS if c not in per[m])
        rep.explanation.append(f"{m[-8:]}: lacks {miss or '-'}")
    if rep.missing_from_union:
        rep.explanation.append(f"nobody spells: {rep.missing_from_union}")
    if single:
        rep.explanation.append(f"single-key letters (one writer only): {single}")
    if lead_only:
        rep.explanation.append(f"lead-only letters (parity trap under alternation): {lead_only}")
    return rep


def keys_for_word(word: str, per_member: dict[str, frozenset]) -> list[str]:
    """Members able to spell ``word``."""
    need = frozenset(c for c in word.lower() if "a" <= c <= "z")
    return [m for m, ls in per_member.items() if need <= ls]
