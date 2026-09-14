"""Adapter Protocols. The deterministic core only ever talks to these interfaces.

Phase 1-6: mocks in adapters/mock. Phase 7: real Technocore / X adapters implement the same Protocols.
Nothing here signs anything: signing keys stay with the operator's live agent.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Protocol, runtime_checkable

from ..models import Frame, Offer, Receipt


@dataclass
class RoomPost:
    seq: int
    at: datetime
    sender: str
    text: str
    kind: str = "note"          # note | word | receipt | roster | setup | application | recruit | submit | ...
    meta: dict = field(default_factory=dict)


@dataclass
class PostResult:
    ok: bool
    seq: Optional[int] = None
    error: Optional[str] = None
    http_status: int = 200


@runtime_checkable
class Clock(Protocol):
    def now(self) -> datetime: ...
    def sleep(self, seconds: float) -> None: ...


@runtime_checkable
class RefereeAdapter(Protocol):
    """Word proposals and roster frames. Every call is tagged with a request_id so late receipts can be matched."""

    def propose_word(self, game_id: str, request_id: str, index: int, text: str, contributor: str, base_version: int) -> PostResult: ...
    def poll_receipts(self, game_id: str) -> list[Receipt]: ...
    def issue_frame(self, frame: Frame) -> PostResult: ...
    def withdraw(self, game_id: str, did: str) -> PostResult: ...
    def sign_frame(self, frame: Frame, did: str) -> PostResult: ...
    def roster_status(self, game_id: str) -> dict: ...   # {ready: bool, frozen: bool, members: [...], version: int}


@runtime_checkable
class DiscoveryAdapter(Protocol):
    def fetch_offers(self, since_seq: int = 0) -> list[Offer]: ...
    def post(self, text: str, kind: str = "note", to_did: Optional[str] = None) -> PostResult: ...


@runtime_checkable
class TeamRoomAdapter(Protocol):
    def post(self, game_id: str, text: str, kind: str = "note") -> PostResult: ...
    def fetch(self, game_id: str, since_seq: int = 0) -> list[RoomPost]: ...


@runtime_checkable
class PublicationAdapter(Protocol):
    """X publication + submit. Real implementation is operator-mediated (the bot cannot post on X itself)."""

    def can_publish(self, did: str) -> bool: ...
    def publish(self, did: str, text: str) -> PostResult: ...
    def submit(self, game_id: str, did: str, post_url: str, sha256: str) -> PostResult: ...
