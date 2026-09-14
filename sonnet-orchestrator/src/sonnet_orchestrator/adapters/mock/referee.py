"""In-memory referee that enforces the contest rules the real one enforces (INTERFACES.md "Contest facts").

Word rules: roster ready ("roster: incomplete consent" otherwise), contiguous index + version match
("version: stale"), no consecutive contributor, official token/letter/dictionary validation (lexicon.validate_word),
line boundaries (exactly 10 syllables per line), complete when the form is full.  First valid proposal for an index
wins; later ones for the same index get "version: stale".
Roster rules: one live consent per DID ("consent: withdraw before changing"), "roster: frozen",
"roster: member already frozen", frame identity = members[] order + poem_room + room_generation.
Fault injection: per-writer receipt ``delay_ms`` / ``delayed_receipt`` (keyed by DID or request_id), seeded
``drop_prob`` per writer, forced ``rejected`` reasons, ``duplicate_receipts`` re-delivery, ``race`` helper.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable, Optional, Union

from ...adapters.protocols import PostResult
from ...models import AcceptedWord, Frame, PoemForm, ProposalStatus, Receipt

STALE = "version: stale"


@dataclass
class GameTruth:
    game_id: str
    members: list[str] = field(default_factory=list)
    frame: Optional[Frame] = None
    frame_at: Optional[datetime] = None
    signed: set[str] = field(default_factory=set)
    rejected_signs: dict[str, str] = field(default_factory=dict)
    ready: bool = False
    frozen: bool = False
    accepted: list[AcceptedWord] = field(default_factory=list)
    version: int = 0
    syllables: int = 0
    complete: bool = False
    ready_at: Optional[datetime] = None
    seen_requests: dict[str, Receipt] = field(default_factory=dict)
    receipts: list[Receipt] = field(default_factory=list)                # every receipt ever issued (seq order)
    queue: list[tuple[datetime, int, Receipt]] = field(default_factory=list)   # (release_at, seq, receipt)
    delivered: set[int] = field(default_factory=set)
    redelivered: set[int] = field(default_factory=set)


class MockReferee:
    def __init__(self, lexicon, clock, *, form: Optional[PoemForm] = None, seed: int = 0,
                 delay_ms: Optional[dict[str, float]] = None, delayed_receipt: Optional[dict[str, float]] = None,
                 drop_prob: Optional[dict[str, float]] = None,
                 rejected: Optional[Union[dict[str, str], Callable[[str, int, str, str], Optional[str]]]] = None,
                 duplicate_receipts: bool = False, expose_accepted: bool = True):
        self.lexicon = lexicon
        self.clock = clock
        self.form = form or PoemForm()
        self.rng = random.Random(seed)
        self.delay_ms: dict[str, float] = dict(delay_ms or {})
        self.delay_ms.update(delayed_receipt or {})
        self.drop_prob: dict[str, float] = dict(drop_prob or {})
        self.rejected = rejected
        self.duplicate_receipts = duplicate_receipts
        self.expose_accepted = expose_accepted
        self.games: dict[str, GameTruth] = {}
        self.live_consent: dict[str, tuple[str, str]] = {}      # did -> (game_id, frame signature)
        self.frozen_members: dict[str, str] = {}                # did -> game_id
        self._seq = 0
        self.dropped: list[Receipt] = []
        self.log: list[str] = []

    # ------------------------------------------------------------ helpers
    def truth(self, game_id: str) -> GameTruth:
        g = self.games.get(game_id)
        if g is None:
            g = GameTruth(game_id)
            self.games[game_id] = g
        return g

    def accepted_words(self, game_id: str) -> list[AcceptedWord]:
        """Optional resync channel (not part of the Protocol; disabled with expose_accepted=False)."""
        if not self.expose_accepted:
            raise AttributeError("accepted_words is not exposed by this referee")
        return list(self.truth(game_id).accepted)

    def _next_seq(self) -> int:
        self._seq += 1
        return self._seq

    def _delay_for(self, request_id: str, did: str) -> float:
        if request_id in self.delay_ms:
            return float(self.delay_ms[request_id])
        return float(self.delay_ms.get(did, 0.0))

    def _emit(self, g: GameTruth, request_id: str, did: str, status: ProposalStatus, *, index=None, text=None,
              version=None, reason=None) -> Receipt:
        now = self.clock.now()
        r = Receipt(request_id=request_id, status=status, index=index, text=text, contributor=did, version=version,
                    reason=reason, seq=self._next_seq(), at=now)
        g.receipts.append(r)
        g.seen_requests[request_id] = r
        prob = self.drop_prob.get(did, 0.0)
        if prob and self.rng.random() < prob:
            self.dropped.append(r)
            self.log.append(f"dropped receipt seq {r.seq} for {request_id}")
            return r
        g.queue.append((now + timedelta(milliseconds=self._delay_for(request_id, did)), r.seq, r))
        return r

    # ------------------------------------------------------------ RefereeAdapter: words
    def propose_word(self, game_id: str, request_id: str, index: int, text: str, contributor: str, base_version: int) -> PostResult:
        g = self.truth(game_id)
        if request_id in g.seen_requests:
            prev = g.seen_requests[request_id]
            g.queue.append((self.clock.now(), prev.seq, prev))   # re-deliver: duplicate post, same receipt
            return PostResult(ok=True, seq=prev.seq)
        if not g.ready:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason="roster: incomplete consent")
            return PostResult(ok=True, seq=self._seq)
        if g.complete:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason="poem: complete")
            return PostResult(ok=True, seq=self._seq)
        if contributor not in g.members:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason="roster: not a member")
            return PostResult(ok=True, seq=self._seq)
        if index != len(g.accepted) or base_version != g.version:
            self._emit(g, request_id, contributor, ProposalStatus.STALE, index=index, text=text, version=g.version, reason=STALE)
            return PostResult(ok=True, seq=self._seq)
        if g.accepted and g.accepted[-1].contributor == contributor:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason="turn: consecutive contributor")
            return PostResult(ok=True, seq=self._seq)
        try:
            syl = self.lexicon.validate_word(text, contributor)
        except ValueError as e:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason=str(e))
            return PostResult(ok=True, seq=self._seq)
        per_line = self.form.syllables_per_line
        if (g.syllables % per_line) + syl > per_line:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason="syllables: word crosses the line boundary")
            return PostResult(ok=True, seq=self._seq)
        forced = None
        if callable(self.rejected):
            forced = self.rejected(request_id, index, text, contributor)
        elif isinstance(self.rejected, dict):
            forced = self.rejected.get(request_id) or self.rejected.get(contributor)
        if forced:
            self._emit(g, request_id, contributor, ProposalStatus.REJECTED, index=index, text=text, reason=forced)
            return PostResult(ok=True, seq=self._seq)
        g.version += 1
        g.syllables += syl
        w = AcceptedWord(index=index, text=text, contributor=contributor, version=g.version, accepted_at=self.clock.now(), request_id=request_id)
        g.accepted.append(w)
        if g.syllables >= self.form.lines * per_line:
            g.complete = True
        r = self._emit(g, request_id, contributor, ProposalStatus.ACCEPTED, index=index, text=text, version=g.version)
        w.receipt_seq = r.seq
        return PostResult(ok=True, seq=r.seq)

    def race(self, game_id: str, proposals: list[tuple[str, int, str, str, int]]) -> list[Receipt]:
        """Submit several proposals at the same instant (request_id, index, text, contributor, base_version): first wins."""
        out = []
        for rid, idx, text, did, ver in proposals:
            self.propose_word(game_id, rid, idx, text, did, ver)
            out.append(self.truth(game_id).seen_requests[rid])
        return out

    def poll_receipts(self, game_id: str) -> list[Receipt]:
        g = self.truth(game_id)
        now = self.clock.now()
        due = sorted([q for q in g.queue if q[0] <= now], key=lambda q: (q[1], q[0]))
        g.queue = [q for q in g.queue if q[0] > now]
        out: list[Receipt] = []
        for _, seq, r in due:
            out.append(r)
            if self.duplicate_receipts and seq not in g.redelivered:
                g.redelivered.add(seq)
                g.queue.append((now, seq, r))    # once more on the next poll
            g.delivered.add(seq)
        return out

    # ------------------------------------------------------------ RefereeAdapter: roster
    def issue_frame(self, frame: Frame) -> PostResult:
        g = self.truth(frame.game_id)
        if g.frozen:
            return PostResult(ok=False, error="roster: frozen", http_status=409)
        lead = frame.members[0]
        held = self.live_consent.get(lead)
        if held and held != (frame.game_id, frame.signature):
            return PostResult(ok=False, error="consent: withdraw before changing", http_status=409)
        g.members = list(frame.members)
        g.frame = frame.model_copy(deep=True)
        g.frame_at = self.clock.now()
        g.rejected_signs = {}
        # consents on a different frame are no longer live for this game; identical frame keeps them
        g.signed = {d for d in g.signed if self.live_consent.get(d) == (frame.game_id, frame.signature)}
        g.signed.add(lead)
        self.live_consent[lead] = (frame.game_id, frame.signature)
        self._check_ready(g)
        return PostResult(ok=True, seq=self._next_seq())

    def sign_frame(self, frame: Frame, did: str) -> PostResult:
        g = self.truth(frame.game_id)
        if g.frozen:
            return PostResult(ok=False, error="roster: frozen", http_status=409)
        if did in self.frozen_members and self.frozen_members[did] != frame.game_id:
            g.rejected_signs[did] = "roster: member already frozen"
            return PostResult(ok=False, error="roster: member already frozen", http_status=409)
        if g.frame is None or g.frame.signature != frame.signature:
            g.rejected_signs[did] = "roster: frame mismatch"
            return PostResult(ok=False, error="roster: frame mismatch", http_status=409)
        if did not in g.members:
            g.rejected_signs[did] = "roster: not a member"
            return PostResult(ok=False, error="roster: not a member", http_status=409)
        held = self.live_consent.get(did)
        if held and held != (frame.game_id, frame.signature):
            g.rejected_signs[did] = "consent: withdraw before changing"
            return PostResult(ok=False, error="consent: withdraw before changing", http_status=409)
        g.signed.add(did)
        g.rejected_signs.pop(did, None)
        self.live_consent[did] = (frame.game_id, frame.signature)
        self._check_ready(g)
        return PostResult(ok=True, seq=self._next_seq())

    def _check_ready(self, g: GameTruth) -> None:
        if g.frame is not None and set(g.frame.members) <= g.signed and not g.ready:
            g.ready = True
            g.frozen = True
            g.ready_at = self.clock.now()
            for d in g.members:
                self.frozen_members[d] = g.game_id

    def withdraw(self, game_id: str, did: str) -> PostResult:
        g = self.truth(game_id)
        if g.frozen:
            return PostResult(ok=False, error="roster: frozen", http_status=409)
        held = self.live_consent.get(did)
        if not held or held[0] != game_id:
            return PostResult(ok=False, error="consent: missing", http_status=404)
        del self.live_consent[did]
        g.signed.discard(did)
        return PostResult(ok=True, seq=self._next_seq())

    def roster_status(self, game_id: str) -> dict:
        g = self.truth(game_id)
        return {"ready": g.ready, "frozen": g.frozen, "members": list(g.members), "version": g.version,
                "signed": sorted(g.signed), "rejected": dict(g.rejected_signs),
                "frame_signature": g.frame.signature if g.frame else None, "complete": g.complete}
