"""Mock discovery room, team room (403 before roster_ready, 2000-char refusal) and publication/submit."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ...adapters.protocols import PostResult, RoomPost
from ...models import Offer

TOO_LONG = "forbidden content or too long"


class MockDiscovery:
    def __init__(self, clock, self_did: str, char_limit: int = 2000):
        self.clock = clock
        self.self_did = self_did
        self.char_limit = char_limit
        self.offers: list[Offer] = []
        self.posts: list[RoomPost] = []
        self._seq = 0

    def _next(self) -> int:
        self._seq += 1
        return self._seq

    def add_offer(self, sender: str, game_id: Optional[str], kind: str = "recruit", text: str = "",
                  to_did: Optional[str] = None, at: Optional[datetime] = None) -> Offer:
        o = Offer(seq=self._next(), at=at or self.clock.now(), sender=sender, game_id=game_id, kind=kind, text=text, to_did=to_did)
        self.offers.append(o)
        return o

    def fetch_offers(self, since_seq: int = 0) -> list[Offer]:
        return [o for o in self.offers if o.seq > since_seq]

    def post(self, text: str, kind: str = "note", to_did: Optional[str] = None) -> PostResult:
        return self.post_as(self.self_did, text, kind, to_did)

    def post_as(self, sender: str, text: str, kind: str = "note", to_did: Optional[str] = None) -> PostResult:
        if len(text) > self.char_limit:
            return PostResult(ok=False, error=TOO_LONG, http_status=400)
        seq = self._next()
        self.posts.append(RoomPost(seq=seq, at=self.clock.now(), sender=sender, text=text, kind=kind, meta={"to_did": to_did}))
        return PostResult(ok=True, seq=seq)


class MockTeamRoom:
    def __init__(self, clock, self_did: str, referee=None, char_limit: int = 2000, pre_roster_403: bool = True):
        self.clock = clock
        self.self_did = self_did
        self.referee = referee
        self.char_limit = char_limit
        self.pre_roster_403 = pre_roster_403
        self.posts: dict[str, list[RoomPost]] = {}
        self.refusals: list[tuple[str, int, str]] = []   # (game_id, http_status, error)
        self._seq = 0

    def _ready(self, game_id: str) -> bool:
        if self.referee is None:
            return True
        return bool(self.referee.roster_status(game_id).get("ready"))

    def post(self, game_id: str, text: str, kind: str = "note") -> PostResult:
        return self.post_as(self.self_did, game_id, text, kind)

    def post_as(self, sender: str, game_id: str, text: str, kind: str = "note") -> PostResult:
        if self.pre_roster_403 and not self._ready(game_id):
            self.refusals.append((game_id, 403, "forbidden: roster not ready"))
            return PostResult(ok=False, error="forbidden: roster not ready", http_status=403)
        if len(text) > self.char_limit:
            self.refusals.append((game_id, 400, TOO_LONG))
            return PostResult(ok=False, error=TOO_LONG, http_status=400)
        self._seq += 1
        p = RoomPost(seq=self._seq, at=self.clock.now(), sender=sender, text=text, kind=kind)
        self.posts.setdefault(game_id, []).append(p)
        return PostResult(ok=True, seq=self._seq)

    def fetch(self, game_id: str, since_seq: int = 0) -> list[RoomPost]:
        return [p for p in self.posts.get(game_id, []) if p.seq > since_seq]


@dataclass
class Submission:
    game_id: str
    did: str
    post_url: str
    sha256: str
    at: datetime
    accepted: bool = True


class MockPublication:
    def __init__(self, clock, publishers: Optional[set[str]] = None, auto_accept: bool = True):
        self.clock = clock
        self.publishers: set[str] = set(publishers or ())
        self.auto_accept = auto_accept
        self.published: list[tuple[str, str, str]] = []   # (did, text, url)
        self.submissions: list[Submission] = []
        self._seq = 0

    def can_publish(self, did: str) -> bool:
        return did in self.publishers

    def publish(self, did: str, text: str) -> PostResult:
        if not self.can_publish(did):
            return PostResult(ok=False, error="publication: no X account for this DID", http_status=403)
        self._seq += 1
        url = f"https://x.com/mock/status/{self._seq}"
        self.published.append((did, text, url))
        return PostResult(ok=True, seq=self._seq, error=url)   # error field carries the URL for the caller

    def post_url(self, seq: int) -> str:
        return f"https://x.com/mock/status/{seq}"

    def submit(self, game_id: str, did: str, post_url: str, sha256: str) -> PostResult:
        self._seq += 1
        self.submissions.append(Submission(game_id, did, post_url, sha256, self.clock.now(), accepted=self.auto_accept))
        return PostResult(ok=True, seq=self._seq)

    def submitted(self, game_id: str) -> bool:
        return any(s.game_id == game_id for s in self.submissions)

    def submission_accepted(self, game_id: str) -> bool:
        return any(s.game_id == game_id and s.accepted for s in self.submissions)
