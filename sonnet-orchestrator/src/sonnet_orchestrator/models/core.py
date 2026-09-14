"""Pydantic v2 domain models shared by every layer.

Everything here is deterministic data; no I/O and no creativity.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------- enums
class GameState(str, Enum):
    DISCOVER = "DISCOVER"
    APPLY = "APPLY"
    SEATED = "SEATED"
    ROSTER_PENDING = "ROSTER_PENDING"
    ROSTER_READY = "ROSTER_READY"
    WRITING = "WRITING"
    RECOVERING = "RECOVERING"
    LANDING = "LANDING"
    COMPLETE = "COMPLETE"
    PUBLISH_PENDING = "PUBLISH_PENDING"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    ABANDONED = "ABANDONED"


class WriterHealth(str, Enum):
    HEALTHY = "HEALTHY"
    SLOW = "SLOW"
    SUSPECT = "SUSPECT"
    DOWN = "DOWN"
    SILENT = "SILENT"  # addendum: seated/signed but no accepted word or post


class ConsentState(str, Enum):
    NONE = "NONE"
    APPLIED = "APPLIED"
    SEATED = "SEATED"
    SIGNED = "SIGNED"
    CONFLICTED = "CONFLICTED"  # live consent elsewhere
    WITHDRAWN = "WITHDRAWN"
    FROZEN = "FROZEN"


class FrameState(str, Enum):
    DRAFT = "DRAFT"
    SIGNING = "SIGNING"
    READY = "READY"
    SUPERSEDED = "SUPERSEDED"
    FROZEN = "FROZEN"


class AvailabilityState(str, Enum):
    """Referee-lag aware view of another writer's roster status."""
    KNOWN_ACTIVE = "KNOWN_ACTIVE"
    KNOWN_FREE = "KNOWN_FREE"
    UNKNOWN = "UNKNOWN"


class ProposalStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    TIMED_OUT = "TIMED_OUT"


class Role(str, Enum):
    LEAD = "Lead"
    AUTHOR = "Author"
    SOLVER = "Solver"
    PUBLISHER = "Publisher"


class Decision(str, Enum):
    AUTONOMOUS = "AUTONOMOUS"
    OPERATOR_APPROVAL = "OPERATOR_APPROVAL"


# ---------------------------------------------------------------- DID / letters
def did_letters(did: str) -> frozenset[str]:
    """Letters a DID may spell: every ASCII letter present in the DID, lowercased."""
    return frozenset(ch for ch in did.lower() if "a" <= ch <= "z")


def word_letters(word: str) -> frozenset[str]:
    return frozenset(ch for ch in word.lower() if "a" <= ch <= "z")


# ---------------------------------------------------------------- writers
class WriterProfile(BaseModel):
    did: str
    handle: Optional[str] = None
    x_account: Optional[str] = None
    letters: frozenset[str] = Field(default_factory=frozenset)
    health: WriterHealth = WriterHealth.HEALTHY
    consent: ConsentState = ConsentState.NONE
    is_self: bool = False
    is_lead: bool = False
    # reliability inputs (addendum: from accepted words / signs, not from "yes")
    poems_completed: int = 0
    games_joined: int = 0
    words_accepted: int = 0
    words_rejected: int = 0
    signs: int = 0
    seat_no_sign_count: int = 0
    consent_conflict_count: int = 0
    stale_offer_count: int = 0
    published_entry_count: int = 0
    sign_latency_median_ms: Optional[float] = None
    word_latency_median_ms: Optional[float] = None
    last_activity_at: Optional[datetime] = None
    mass_application_score: float = 0.0
    reliability: float = 0.5

    @model_validator(mode="after")
    def _fill_letters(self):
        if not self.letters:
            object.__setattr__(self, "letters", did_letters(self.did))
        return self

    @property
    def missing_letters(self) -> str:
        return "".join(c for c in LETTERS if c not in self.letters)

    def can_spell(self, word: str) -> bool:
        return word_letters(word) <= self.letters


# ---------------------------------------------------------------- words / poem
class WordEntry(BaseModel):
    """One canonical word placement in a plan (position 0-based over the whole poem)."""
    index: int
    text: str  # token as it appears (may carry trailing punctuation)
    line: int
    syllables: int
    stress: tuple[int, ...] = ()
    rhyme_key: Optional[str] = None
    letters: frozenset[str] = Field(default_factory=frozenset)

    @model_validator(mode="after")
    def _fill_letters(self):
        if not self.letters:
            object.__setattr__(self, "letters", word_letters(self.text))
        return self


class AcceptedWord(BaseModel):
    """Referee receipt = the only truth. Immutable once recorded."""
    index: int
    text: str
    contributor: str
    version: int
    receipt_seq: Optional[int] = None
    accepted_at: Optional[datetime] = None
    request_id: Optional[str] = None


class Receipt(BaseModel):
    """Normalized referee response for one proposal."""
    request_id: Optional[str]
    status: ProposalStatus
    index: Optional[int] = None
    text: Optional[str] = None
    contributor: Optional[str] = None
    version: Optional[int] = None
    reason: Optional[str] = None
    seq: Optional[int] = None
    at: datetime = Field(default_factory=utcnow)


class Proposal(BaseModel):
    request_id: str
    index: int
    text: str
    contributor: str
    base_version: int
    status: ProposalStatus = ProposalStatus.PENDING
    sent_at: datetime = Field(default_factory=utcnow)
    resolved_at: Optional[datetime] = None
    reason: Optional[str] = None


class PoemForm(BaseModel):
    lines: int = 14
    syllables_per_line: int = 10
    stanzas: tuple[int, ...] = (4, 4, 4, 2)
    rhyme_scheme: str = "ABABCDCDEFEFGG"


class Assignment(BaseModel):
    index: int
    primary: str
    backup: Optional[str] = None
    keys: int = 0  # number of active writers able to spell the word
    lead_only: bool = False


class Plan(BaseModel):
    plan_id: str
    game_id: str
    version: int
    owner: str
    source: str = "solver"
    is_active: bool = True
    words: list[WordEntry]
    assignments: list[Assignment] = Field(default_factory=list)
    accepted_prefix_len: int = 0
    created_at: datetime = Field(default_factory=utcnow)
    lines: list[str] = Field(default_factory=list)

    @property
    def text(self) -> str:
        return canonical_text(self.lines)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    @property
    def hash_prefix(self) -> str:
        return self.sha256[:8]


class PoemState(BaseModel):
    """Referee-accepted prefix (immutable) + expected version."""
    game_id: str
    accepted: list[AcceptedWord] = Field(default_factory=list)
    version: int = 0
    complete: bool = False

    @property
    def next_index(self) -> int:
        return len(self.accepted)

    @property
    def last_contributor(self) -> Optional[str]:
        return self.accepted[-1].contributor if self.accepted else None

    def accepted_texts(self) -> list[str]:
        return [w.text for w in self.accepted]


# ---------------------------------------------------------------- roster / frames
class Frame(BaseModel):
    """A roster frame: exact members[] order + poem_room + room_generation."""
    frame_id: str
    game_id: str
    members: list[str]
    poem_room: str
    room_generation: int = 1
    state: FrameState = FrameState.DRAFT
    signed_by: set[str] = Field(default_factory=set)
    issued_at: datetime = Field(default_factory=utcnow)
    superseded_by: Optional[str] = None

    @property
    def signature(self) -> str:
        return hashlib.sha256(("|".join(self.members) + "#" + self.poem_room + "#" + str(self.room_generation)).encode()).hexdigest()[:12]

    def same_as(self, other: "Frame") -> bool:
        return self.signature == other.signature


class Offer(BaseModel):
    """A recruitment offer/application seen in discovery."""
    seq: int
    at: datetime
    sender: str
    game_id: Optional[str]
    kind: str  # application | recruit | personal_offer | note
    text: str = ""
    to_did: Optional[str] = None


# ---------------------------------------------------------------- health / events
class WriterEvent(BaseModel):
    did: str
    kind: str  # word_accepted | word_rejected | sign | seat | post | consent_conflict | timeout | ...
    at: datetime = Field(default_factory=utcnow)
    latency_ms: Optional[float] = None
    game_id: Optional[str] = None
    detail: Optional[str] = None


class HealthSnapshot(BaseModel):
    did: str
    health: WriterHealth
    expected_ms: float
    last_seen_at: Optional[datetime] = None
    reason: str = ""


# ---------------------------------------------------------------- canonical text
def canonical_text(lines: list[str]) -> str:
    """Words space-joined, LF lines, blank line between 4/4/4/2 stanzas, no trailing newline."""
    lines = [" ".join(l.split()) for l in lines]
    out: list[str] = []
    for i, line in enumerate(lines):
        out.append(line)
        if i in (3, 7, 11) and i != len(lines) - 1:
            out.append("")
    return "\n".join(out)


def poem_sha256(lines: list[str]) -> str:
    return hashlib.sha256(canonical_text(lines).encode("utf-8")).hexdigest()
