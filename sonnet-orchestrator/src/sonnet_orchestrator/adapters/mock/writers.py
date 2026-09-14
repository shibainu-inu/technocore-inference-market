"""Scripted members: they sign frames after a latency and post their own table slots, like real drivers do
(coordination_lessons.md case 11: "members' drivers post only on their own table slots").

Profiles: healthy | slow | down_after_index | silent (signs, never writes) | never_signs.
``race_index`` makes a writer also propose for that index even when it is not its slot (two proposals, one index).
``synthetic_did(letters)`` builds a DID that passes the official validator's shape check and spells exactly ``letters``
(plus d,i,k,e,y,z,m from the ``did:key:z6Mk`` prefix).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ...models import canonical_text, poem_sha256
from ...orchestration.table import TableHeader, lines_from_words, parse_table

BASE58_FORBIDDEN = set("0OIl")
DID_PREFIX = "did:key:z6Mk"
DID_BODY_LEN = 44
DID_SUFFIX_LEN = 8


def synthetic_did(letters: str, salt: str = "") -> str:
    """A well-formed did:key whose letters are exactly {d,i,k,e,y,z,m} ∪ letters (case-insensitive).
    base58 forbids 0, O, I, l: 'l' is written as 'L'; 'o' and 'i' stay lowercase. The last 8 characters are a
    digit-only tail derived from (letters, salt) so that DID suffixes (used in tables) never collide."""
    body = "".join(("L" if ch == "l" else ch) for ch in letters.lower() if "a" <= ch <= "z")
    tail_int = int(hashlib.sha256((letters + "|" + salt).encode()).hexdigest(), 16)
    tail = ""
    for _ in range(DID_SUFFIX_LEN):
        tail += "123456789"[tail_int % 9]
        tail_int //= 9
    body = (body + "123456789" * 8)[: DID_BODY_LEN - DID_SUFFIX_LEN] + tail
    did = DID_PREFIX + body
    assert len(did) == len(DID_PREFIX) + DID_BODY_LEN and not (set(did[len(DID_PREFIX):]) & BASE58_FORBIDDEN)
    return did


@dataclass
class WriterScript:
    did: str
    profile: str = "healthy"
    latency_s: float = 10.0
    sign_latency_s: float = 5.0
    down_after_index: Optional[int] = None
    race_index: Optional[int] = None
    withdraw_first: bool = True
    proposed_indexes: set[int] = field(default_factory=set)
    sign_attempted: set[str] = field(default_factory=set)
    sign_results: list[tuple[str, bool, Optional[str]]] = field(default_factory=list)
    proposals: list[str] = field(default_factory=list)
    published: bool = False

    def writes(self) -> bool:
        return self.profile not in ("silent", "never_signs")

    def signs(self) -> bool:
        return self.profile != "never_signs"


class ScriptedWriters:
    def __init__(self, referee, team_room, publication, clock, lexicon, settings, game_id: str, lead_did: str,
                 scripts: list[WriterScript]):
        self.referee = referee
        self.team_room = team_room
        self.publication = publication
        self.clock = clock
        self.lexicon = lexicon
        self.settings = settings
        self.game_id = game_id
        self.lead_did = lead_did
        self.scripts = {s.did: s for s in scripts}
        self.log: list[str] = []
        self._room_cursor = 0
        self._tables: list[TableHeader] = []          # the lead's table chunks, parsed once per post
        self._rows: dict[int, object] = {}
        self._rows_version = -1

    def _current_rows(self) -> dict:
        """index -> TableRow of the lead's latest table version (posts parsed once, cached)."""
        posts = self.team_room.fetch(self.game_id, self._room_cursor)
        for p in posts:
            self._room_cursor = max(self._room_cursor, p.seq)
            if p.sender != self.lead_did:
                continue
            th = parse_table(p.text, self.settings.room.table_prefix)
            if th:
                th.sender, th.seq = p.sender, p.seq
                self._tables.append(th)
        if not self._tables:
            return {}
        best = max(th.version for th in self._tables)
        if best != self._rows_version:
            self._rows = {r.index: r for th in self._tables if th.version == best for r in th.rows}
            self._rows_version = best
        return self._rows

    def attach(self, clock=None) -> "ScriptedWriters":
        (clock or self.clock).subscribe(self.step)
        return self

    # ------------------------------------------------------------ one world step
    def step(self, now: datetime) -> None:
        g = self.referee.truth(self.game_id)
        table_cache = None
        for s in self.scripts.values():
            if s.did not in g.members:
                continue
            self._maybe_sign(s, g, now)
            if not g.ready or not s.writes():
                continue
            if g.complete:
                self._maybe_publish(s, g)
                continue
            idx = len(g.accepted)
            if s.down_after_index is not None and idx >= s.down_after_index:
                continue
            if g.accepted and g.accepted[-1].contributor == s.did:
                continue
            if idx in s.proposed_indexes:
                continue
            last_at = g.accepted[-1].accepted_at if g.accepted else g.ready_at
            if last_at is None or (now - last_at).total_seconds() < s.latency_s:
                continue
            if table_cache is None:
                table_cache = self._current_rows()
            row = table_cache.get(idx)
            if row is None or not (row.primary == s.did[-8:] or s.race_index == idx):
                continue
            rid = f"w{idx}-{s.did[-6:]}-{int(now.timestamp())}"
            self.referee.propose_word(self.game_id, rid, idx, row.word, s.did, g.version)
            s.proposed_indexes.add(idx)
            s.proposals.append(rid)
            self.log.append(f"{now.isoformat()} {s.did[-8:]} proposed {idx} {row.word!r}")

    def _maybe_sign(self, s: WriterScript, g, now: datetime) -> None:
        f = g.frame
        if f is None or g.ready or not s.signs() or s.did in g.signed or s.did not in f.members:
            return
        if f.signature in s.sign_attempted or g.frame_at is None or (now - g.frame_at).total_seconds() < s.sign_latency_s:
            return
        held = self.referee.live_consent.get(s.did)
        if held and held != (self.game_id, f.signature) and s.withdraw_first:
            self.referee.withdraw(held[0], s.did)
        res = self.referee.sign_frame(f, s.did)
        s.sign_attempted.add(f.signature)
        s.sign_results.append((f.signature, res.ok, res.error))
        self.log.append(f"{now.isoformat()} {s.did[-8:]} sign {f.signature}: {'ok' if res.ok else res.error}")

    def _maybe_publish(self, s: WriterScript, g) -> None:
        if s.published or not g.accepted or g.accepted[-1].contributor != s.did:
            return
        if not self.publication.can_publish(s.did):
            return
        lines = lines_from_words([w.text for w in g.accepted], self.lexicon, self.referee.form)
        text = canonical_text(lines)
        res = self.publication.publish(s.did, text)
        if res.ok:
            self.publication.submit(self.game_id, s.did, self.publication.post_url(res.seq), poem_sha256(lines))
        s.published = True
