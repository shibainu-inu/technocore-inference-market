"""Word proposals and receipt processing. The referee receipt is the only truth.

request_id = f"w{index}-{hash8}-{did[-6:]}-{ms}" (hash8 = sha256 of the token, ms = clock milliseconds) so every
proposal is unique and a late receipt can still be matched.  Receipts are applied idempotently:
- a receipt for a proposal already resolved is ignored (duplicate / late);
- ACCEPTED → store.append_accepted (contiguous, immutable; a repeat of the same word is a no-op);
- "version: stale" → STALE + needs_resync (the controller re-reads the accepted state);
- receipts for unknown request_ids that carry (index, text, contributor, version) are other members' accepted words:
  they are applied to the accepted stream in index order (out-of-order ones wait in a buffer); anything else is
  logged, never applied;
- pending proposals older than timeout_ms → TIMED_OUT; a receipt arriving later still resolves them.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..models import AcceptedWord, Proposal, ProposalStatus, Receipt

STALE_REASON = "version: stale"


@dataclass
class ReceiptOutcome:
    receipt: Receipt
    kind: str            # applied | duplicate | stale | rejected | timed_out_late | unknown | buffered | conflict
    proposal: Optional[Proposal] = None
    detail: str = ""


@dataclass
class Dispatcher:
    referee: object
    store: object
    clock: object
    game_id: str
    timeout_ms: float
    proposals: dict[str, Proposal] = field(default_factory=dict)
    log: list[str] = field(default_factory=list)
    needs_resync: bool = False
    buffered: dict[int, Receipt] = field(default_factory=dict)
    accepted_count: int = 0

    def __post_init__(self):
        self.accepted_count = len(self.store.accepted(self.game_id))

    # ------------------------------------------------------------ proposals
    def request_id(self, index: int, text: str, contributor: str) -> str:
        ms = int(self.clock.now().timestamp() * 1000)
        h8 = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
        rid = f"w{index}-{h8}-{contributor[-6:]}-{ms}"
        n = 0
        while rid in self.proposals:
            n += 1
            rid = f"w{index}-{h8}-{contributor[-6:]}-{ms + n}"
        return rid

    def pending(self, index: Optional[int] = None) -> list[Proposal]:
        return [p for p in self.proposals.values() if p.status == ProposalStatus.PENDING and (index is None or p.index == index)]

    def propose(self, index: int, text: str, contributor: str, base_version: int) -> Proposal:
        rid = self.request_id(index, text, contributor)
        p = Proposal(request_id=rid, index=index, text=text, contributor=contributor, base_version=base_version, sent_at=self.clock.now())
        self.proposals[rid] = p
        self.store.add_proposal(self.game_id, p)
        res = self.referee.propose_word(self.game_id, rid, index, text, contributor, base_version)
        if not res.ok:
            self._resolve(p, ProposalStatus.REJECTED, res.error or f"http {res.http_status}")
        return p

    def _resolve(self, p: Proposal, status: ProposalStatus, reason: Optional[str]) -> None:
        p.status, p.reason, p.resolved_at = status, reason, self.clock.now()
        self.store.resolve_proposal(p.request_id, status, reason, p.resolved_at)

    # ------------------------------------------------------------ receipts
    def _append(self, w: AcceptedWord) -> str:
        try:
            self.store.append_accepted(self.game_id, w)
        except ValueError as e:
            self.log.append(f"conflict: {e}")
            return "conflict"
        self.accepted_count = len(self.store.accepted(self.game_id))
        return "applied"

    def _drain_buffer(self, outcomes: list[ReceiptOutcome]) -> None:
        while self.accepted_count in self.buffered:
            r = self.buffered.pop(self.accepted_count)
            kind = self._append(AcceptedWord(index=r.index, text=r.text, contributor=r.contributor, version=r.version,
                                             receipt_seq=r.seq, accepted_at=r.at, request_id=r.request_id))
            outcomes.append(ReceiptOutcome(r, kind, None, "from buffer"))

    def process_receipts(self, receipts: Optional[list[Receipt]] = None) -> list[ReceiptOutcome]:
        if receipts is None:
            receipts = self.referee.poll_receipts(self.game_id)
        outcomes: list[ReceiptOutcome] = []
        for r in receipts:
            p = self.proposals.get(r.request_id) if r.request_id else None
            if p is not None:
                outcomes.append(self._apply_own(p, r))
            else:
                outcomes.append(self._apply_foreign(r))
            self._drain_buffer(outcomes)
        return outcomes

    def _apply_own(self, p: Proposal, r: Receipt) -> ReceiptOutcome:
        if p.status not in (ProposalStatus.PENDING, ProposalStatus.TIMED_OUT):
            self.log.append(f"duplicate receipt for {p.request_id} ({r.status.value}); already {p.status.value}")
            return ReceiptOutcome(r, "duplicate", p)
        late = p.status == ProposalStatus.TIMED_OUT
        if r.status == ProposalStatus.ACCEPTED:
            version = r.version if r.version is not None else p.base_version + 1
            self._resolve(p, ProposalStatus.ACCEPTED, r.reason)
            w = AcceptedWord(index=r.index if r.index is not None else p.index, text=r.text or p.text,
                             contributor=r.contributor or p.contributor, version=version, receipt_seq=r.seq,
                             accepted_at=r.at, request_id=p.request_id)
            if w.index > self.accepted_count:
                self.buffered.setdefault(w.index, Receipt(request_id=p.request_id, status=r.status, index=w.index, text=w.text,
                                                          contributor=w.contributor, version=version, seq=r.seq, at=r.at))
                return ReceiptOutcome(r, "buffered", p, "late" if late else "")
            kind = self._append(w)
            return ReceiptOutcome(r, kind if not late else "timed_out_late", p)
        if r.status == ProposalStatus.STALE or (r.reason or "").startswith(STALE_REASON):
            self._resolve(p, ProposalStatus.STALE, r.reason or STALE_REASON)
            self.needs_resync = True
            return ReceiptOutcome(r, "stale", p)
        self._resolve(p, ProposalStatus.REJECTED, r.reason)
        return ReceiptOutcome(r, "rejected", p, r.reason or "")

    def _apply_foreign(self, r: Receipt) -> ReceiptOutcome:
        if r.status == ProposalStatus.ACCEPTED and None not in (r.index, r.text, r.contributor, r.version):
            if r.index < self.accepted_count:
                existing = self.store.accepted(self.game_id)[r.index]
                if existing.text == r.text and existing.contributor == r.contributor:
                    return ReceiptOutcome(r, "duplicate", None, "already recorded")
                self.log.append(f"conflict: receipt seq {r.seq} says index {r.index} is {r.text!r} by {r.contributor[-8:]}, store has {existing.text!r}")
                return ReceiptOutcome(r, "conflict")
            if r.index > self.accepted_count:
                self.buffered.setdefault(r.index, r)
                return ReceiptOutcome(r, "buffered", None, f"waiting for index {self.accepted_count}")
            kind = self._append(AcceptedWord(index=r.index, text=r.text, contributor=r.contributor, version=r.version,
                                             receipt_seq=r.seq, accepted_at=r.at, request_id=r.request_id))
            return ReceiptOutcome(r, kind)
        self.log.append(f"unknown request_id {r.request_id!r} ({r.status.value} {r.reason or ''}) logged, not applied")
        return ReceiptOutcome(r, "unknown")

    # ------------------------------------------------------------ resync / timeouts
    def resync(self, accepted: list[AcceptedWord]) -> int:
        """Adopt the referee's accepted state (e.g. after 'version: stale'). Returns the number of words added."""
        added = 0
        for w in accepted:
            if w.index < self.accepted_count:
                continue
            if self._append(w) == "applied":
                added += 1
        self.needs_resync = False
        return added

    def expire(self, now: Optional[datetime] = None) -> list[Proposal]:
        now = now or self.clock.now()
        out = []
        for p in self.proposals.values():
            if p.status == ProposalStatus.PENDING and (now - p.sent_at).total_seconds() * 1000.0 >= self.timeout_ms:
                self._resolve(p, ProposalStatus.TIMED_OUT, f"no receipt within {self.timeout_ms:.0f} ms")
                out.append(p)
        return out
