"""Replay of team-room exports (``data/fixtures/<game>/team_room_export.ndjson``).

The referee receipt is the only truth: the accepted stream is every ``sonnet.receipt.v1`` with
``status == accepted`` whose ``request_id`` matches a ``sonnet.word.v1`` post, in seq order.  The word
text, version and contributor come from that word post.  Everything here is read-only parsing; no
policy numbers live in this module.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from ..adapters.protocols import RoomPost
from ..did.analyzer import did_letters
from ..models.core import AcceptedWord, ProposalStatus, Receipt, canonical_text

REFEREE_DID = "did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte"
SELF_DID = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"

# Handles used as signer labels in tables posted by other members (contest handle -> DID suffix).
HANDLE_ALIASES: dict[str, str] = {
    "leidream": "MWV4RmAQ", "sifat": "3sLzg7ws", "halftongue": "kc46mJuz", "stein": "kc46mJuz",
    "nohitori": "W4TAejK6", "KIMI": "F6jvabi2", "weather-prophet": "f9vthSUn", "Jingdu": "VxSdDkhu",
}

WORD_TYPE = "sonnet.word.v1"
RECEIPT_TYPE = "sonnet.receipt.v1"
BATCH_TYPE = "sonnet.receipts.v1"
ROOM_TYPE = "sonnet.room.v1"

# "51:then:VxSdDkhu" / "98:this::VxSdDkhu" (word may carry a trailing ':') / "3:the:sifat"
_TABLE_ROW = re.compile(r"(?<!\S)(\d+):(\S+?):([A-Za-z0-9_-]+)(?=\s|$)")
_TABLE_MARK = re.compile(r"\bTABLE\b")
_TURN_SCRIPT_MARK = re.compile(r"TURN SCRIPT|Stanza \d:")


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


@dataclass
class WordProposal:
    seq: int
    at: datetime
    sender: str
    text: str
    version: int
    request_id: str
    previous_state_hash: Optional[str] = None
    room_generation: Optional[int] = None


@dataclass
class RosterReceipt:
    seq: int
    at: datetime
    sender_did: str
    request_id: str
    status: str
    roster_ready: Optional[bool]
    reason: str = ""


@dataclass
class Rejection:
    seq: int
    at: datetime
    sender: str
    word: Optional[str]
    version: Optional[int]
    reason: str
    request_id: Optional[str]
    batch: bool = False


@dataclass
class TablePost:
    seq: int
    at: datetime
    sender: str
    rows: dict[int, str]          # 1-based index -> signer label as written (DID suffix or handle)
    words: dict[int, str]         # 1-based index -> planned word
    version_label: str = ""       # e.g. "v2", "1/5"
    kind: str = "table"           # table | turn_script


@dataclass
class ReplayLog:
    game_id: str
    path: Path
    lead: str
    posts: list[RoomPost] = field(default_factory=list)
    words: list[WordProposal] = field(default_factory=list)
    receipts: list[Receipt] = field(default_factory=list)
    accepted: list[AcceptedWord] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    timeline: list[RoomPost] = field(default_factory=list)
    roster_receipts: list[RosterReceipt] = field(default_factory=list)
    rejections: list[Rejection] = field(default_factory=list)
    tables: list[TablePost] = field(default_factory=list)
    room_created_at: Optional[datetime] = None
    roster_ready_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    final_version: Optional[int] = None
    final_contributor: Optional[str] = None
    complete: bool = False

    # ------------------------------------------------------------ views
    @property
    def letters(self) -> dict[str, frozenset]:
        return {m: did_letters(m) for m in self.members}

    def accepted_texts(self) -> list[str]:
        return [w.text for w in self.accepted]

    def contributions(self) -> dict[str, int]:
        out: dict[str, int] = {m: 0 for m in self.members}
        for w in self.accepted:
            out[w.contributor] = out.get(w.contributor, 0) + 1
        return out

    def spellers(self, word: str) -> list[str]:
        return word_spellers(word, self.members)

    def suffix(self, did: str, n: int = 8) -> str:
        return did[-n:]

    def resolve_label(self, label: str) -> Optional[str]:
        """Map a table label (DID suffix 'VxSdDkhu' / 'TAejK6', or a known handle) to a member DID; None if unknown."""
        label = HANDLE_ALIASES.get(label, label)
        for m in self.members:
            if m.endswith(label):
                return m
        return None

    def table_for(self, index_1based: int, before_seq: int) -> Optional[TablePost]:
        """Newest table posted before ``before_seq`` that assigns ``index_1based``."""
        best = None
        for t in self.tables:
            if t.seq < before_seq and index_1based in t.rows:
                best = t
        return best


# ---------------------------------------------------------------- parsing
def _load_rows(path: Path) -> list[dict]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    rows.sort(key=lambda r: r["seq"])
    return rows


def _json_or_none(text: str):
    try:
        j = json.loads(text)
    except (ValueError, TypeError):
        return None
    return j if isinstance(j, dict) else None


def _parse_table(post: RoomPost) -> Optional[TablePost]:
    text = post.text
    found = _TABLE_ROW.findall(text)
    rows = {int(i): signer for i, _w, signer in found}
    # A planned word "this:" is written "98:this::VxSdDkhu"; the non-greedy word group keeps "this:".
    words = {int(i): w for i, w, _s in found}
    if rows and _TABLE_MARK.search(text):
        m = re.search(r"TABLE\s+(v\d+|\d+/\d+)", text)
        return TablePost(post.seq, post.at, post.sender, rows, words, m.group(1) if m else "", "table")
    if _TURN_SCRIPT_MARK.search(text) and "[" in text:
        return TablePost(post.seq, post.at, post.sender, {}, {}, "", "turn_script")
    return None


def parse_export(path: str | Path, *, lead: str = SELF_DID, referee: str = REFEREE_DID) -> ReplayLog:
    path = Path(path)
    rows = _load_rows(path)
    game_id = path.parent.name
    log = ReplayLog(game_id=game_id, path=path, lead=lead)
    proposals: dict[str, WordProposal] = {}
    members: list[str] = []

    def seen(did: Optional[str]) -> None:
        if did and did != referee and did not in members:
            members.append(did)

    for r in rows:
        at = parse_ts(r["ts"])
        sender = r["from"]
        j = _json_or_none(r["text"])
        kind = "note"
        meta: dict = {}
        if j is None:
            seen(sender)
            post = RoomPost(r["seq"], at, sender, r["text"], "note", {})
            log.posts.append(post)
            log.timeline.append(post)
            t = _parse_table(post)
            if t is not None:
                log.tables.append(t)
            continue
        typ = j.get("type")
        if typ == WORD_TYPE:
            kind = "word"
            seen(sender)
            wp = WordProposal(r["seq"], at, sender, str(j.get("word")), int(j.get("version", 0)),
                              str(j.get("request_id")), j.get("previous_state_hash"), j.get("room_generation"))
            proposals[wp.request_id] = wp
            log.words.append(wp)
            meta = {"request_id": wp.request_id, "version": wp.version, "word": wp.text}
        elif typ == RECEIPT_TYPE:
            kind = "receipt"
            rid = j.get("request_id")
            status = j.get("status")
            reason = j.get("reason") or ""
            wp = proposals.get(rid)
            if wp is None and "roster_ready" not in j:
                # room setup / other administrative receipt (e.g. request_id "resetup-<game>")
                log.room_created_at = log.room_created_at or at
                log.receipts.append(Receipt(request_id=rid, status=ProposalStatus.ACCEPTED if status == "accepted" else ProposalStatus.REJECTED,
                                            reason=reason or None, seq=r["seq"], at=at))
            elif wp is None:
                sd = j.get("sender_did")
                seen(sd)
                rr = RosterReceipt(r["seq"], at, sd, str(rid), status, j.get("roster_ready"), reason)
                log.roster_receipts.append(rr)
                if rr.roster_ready and status == "accepted" and log.roster_ready_at is None:
                    log.roster_ready_at = at
                log.receipts.append(Receipt(request_id=rid, status=ProposalStatus.ACCEPTED if status == "accepted" else ProposalStatus.REJECTED,
                                            contributor=sd, reason=reason or None, seq=r["seq"], at=at))
            else:
                if status == "accepted":
                    idx = len(log.accepted)
                    version = int(j.get("version", wp.version + 1))
                    aw = AcceptedWord(index=idx, text=wp.text, contributor=wp.sender, version=wp.version,
                                      receipt_seq=r["seq"], accepted_at=at, request_id=wp.request_id)
                    log.accepted.append(aw)
                    log.receipts.append(Receipt(request_id=rid, status=ProposalStatus.ACCEPTED, index=idx, text=wp.text,
                                                contributor=wp.sender, version=version, seq=r["seq"], at=at))
                    if j.get("complete"):
                        log.complete = True
                        log.completed_at = at
                        log.final_version = version
                        log.final_contributor = wp.sender
                else:
                    st = ProposalStatus.STALE if reason.startswith("version: stale") else ProposalStatus.REJECTED
                    log.rejections.append(Rejection(r["seq"], at, wp.sender, wp.text, wp.version, reason, rid, False))
                    log.receipts.append(Receipt(request_id=rid, status=st, text=wp.text, contributor=wp.sender,
                                                version=wp.version, reason=reason, seq=r["seq"], at=at))
            meta = {"request_id": rid, "status": status, "reason": reason}
        elif typ == BATCH_TYPE:
            kind = "receipts"
            reason = j.get("reason") or ""
            status = j.get("status")
            for item in j.get("receipts", []):
                rid = item.get("request_id")
                wp = proposals.get(rid)
                st = ProposalStatus.STALE if reason.startswith("version: stale") else ProposalStatus.REJECTED
                if status == "accepted":
                    st = ProposalStatus.ACCEPTED
                log.rejections.append(Rejection(r["seq"], at, item.get("sender_did") or (wp.sender if wp else ""),
                                                wp.text if wp else None, wp.version if wp else None, reason, rid, True))
                log.receipts.append(Receipt(request_id=rid, status=st, text=wp.text if wp else None,
                                            contributor=item.get("sender_did") or (wp.sender if wp else None),
                                            version=wp.version if wp else None, reason=reason, seq=r["seq"], at=at))
            meta = {"status": status, "reason": reason, "count": len(j.get("receipts", []))}
        elif typ == ROOM_TYPE:
            kind = "room"
            log.room_created_at = log.room_created_at or at
            game_id = j.get("game_id") or game_id
            meta = {"game_id": game_id}
        else:
            kind = typ or "note"
            seen(sender)
        log.posts.append(RoomPost(r["seq"], at, sender, r["text"], kind, meta))
    log.game_id = game_id
    log.members = members
    if lead not in members and members:
        log.lead = members[0]
    return log


# ---------------------------------------------------------------- helpers
def accepted_from_export(path: str | Path) -> list[AcceptedWord]:
    return parse_export(path).accepted


def lines_from_words(words: Iterable[str], lexicon, *, per_line: int = 10) -> list[str]:
    """Lay words into lines at cumulative ``per_line``-syllable boundaries (official syllable counts)."""
    lines: list[list[str]] = [[]]
    total = 0
    for w in words:
        n = lexicon.word_syllables(w)
        if total + n > per_line:
            raise ValueError(f"word {w!r} crosses the {per_line}-syllable boundary at {total}+{n}")
        lines[-1].append(w)
        total += n
        if total == per_line:
            lines.append([])
            total = 0
    if lines and not lines[-1]:
        lines.pop()
    if total not in (0,):
        raise ValueError(f"last line is incomplete: {total} syllables")
    return [" ".join(l) for l in lines]


def canonical_from_export(path: str | Path, lexicon) -> tuple[str, str]:
    """(canonical text, sha256) reconstructed from the accepted stream."""
    text = canonical_text(lines_from_words([w.text for w in accepted_from_export(path)], lexicon))
    return text, hashlib.sha256(text.encode("utf-8")).hexdigest()


def word_spellers(word: str, members: Iterable[str], letters_of=did_letters) -> list[str]:
    need = frozenset(c for c in word.lower() if "a" <= c <= "z")
    return [m for m in members if need <= letters_of(m)]


def load_final_poem(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8").removesuffix("\n")
