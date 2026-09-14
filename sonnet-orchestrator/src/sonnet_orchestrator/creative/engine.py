"""CreativeEngine protocol: the only seam through which an LLM may enter.

The deterministic core never trusts candidates blindly: every candidate is re-validated
by lexicon/validator and the solver before it can be placed in a plan.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable


@dataclass
class LineContext:
    line_index: int                 # 0..13
    previous_lines: list[str]
    rhyme_key: Optional[str]        # required end-rhyme key, or None if this line sets the key
    allowed_letters: frozenset      # union of letters over available writers (hard)
    per_writer_letters: dict        # did -> frozenset (used to prefer two-key words)
    theme: str = ""
    syllables: int = 10
    max_candidates: int = 24
    forbidden_end_words: set = field(default_factory=set)


@dataclass
class LineCandidate:
    words: list[str]                # tokens, may carry trailing punctuation
    score: float = 0.0
    source: str = "heuristic"
    notes: str = ""


@runtime_checkable
class CreativeEngine(Protocol):
    def propose_lines(self, ctx: LineContext) -> list[LineCandidate]: ...
    def propose_word_alternatives(self, word: str, ctx: LineContext, needed_syllables: int) -> list[str]: ...
