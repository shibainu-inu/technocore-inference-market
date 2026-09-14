"""Consent + roster frame lifecycle (coordination_lessons.md cases 7 and 10).

Member consent: NONE → APPLIED → SEATED → SIGNED / CONFLICTED / WITHDRAWN / FROZEN.
Frame:          DRAFT → SIGNING → READY → FROZEN;  SUPERSEDED when re-issued.
Rules:
- waitlist while SIGNING: never seat into a frame that is out for signature (case 7 fault 1);
- signatures are recorded per frame signature and carried over to an identical re-issue (fault 2);
- timeouts are checked on every tick (fault 3); a member who signed an earlier frame gets a REMINDER, not the door (fault 4);
- "consent: withdraw before changing": a rejected consent un-marks the signature and yields a withdraw-first note (case 10);
- tri-state availability of other DIDs with referee lag (§2 "referee lag as a hidden variable");
- offer filters: dedupe by (sender, game_id), drop self-offers, drop stale offers, personal offers first (case 6).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Optional

from ..models import AvailabilityState, ConsentState, Frame, FrameState, Offer

WITHDRAW_BEFORE_CHANGING = "consent: withdraw before changing"


@dataclass
class MemberConsent:
    did: str
    state: ConsentState = ConsentState.NONE
    frame_signature: Optional[str] = None
    signed_at: Optional[datetime] = None
    seated_at: Optional[datetime] = None
    reminders: int = 0
    last_reminder_at: Optional[datetime] = None
    rejections: int = 0


@dataclass
class ConsentAction:
    kind: str            # remind | drop | reissue | withdraw_first | ready | seat
    did: Optional[str]
    detail: str = ""


class FrameManager:
    def __init__(self, settings, clock, game_id: str, poem_room: str, lead_did: str, room_generation: int = 1):
        self.settings = settings
        self.clock = clock
        self.game_id = game_id
        self.poem_room = poem_room
        self.lead_did = lead_did
        self.room_generation = room_generation
        self.members: list[str] = [lead_did]
        self.waitlist: list[str] = []
        self.declined: list[str] = []
        self.frame: Optional[Frame] = None
        self.frames: list[Frame] = []
        self.sigs: dict[str, dict[str, datetime]] = {}   # did -> {frame_signature: at}  (every signature ever seen)
        self.consents: dict[str, MemberConsent] = {lead_did: MemberConsent(lead_did, ConsentState.SEATED, seated_at=clock.now())}
        self._counter = 0

    # ------------------------------------------------------------ members
    def consent(self, did: str) -> MemberConsent:
        c = self.consents.get(did)
        if c is None:
            c = MemberConsent(did)
            self.consents[did] = c
        return c

    def apply(self, did: str) -> MemberConsent:
        c = self.consent(did)
        if c.state == ConsentState.NONE:
            c.state = ConsentState.APPLIED
        return c

    @property
    def signing(self) -> bool:
        return self.frame is not None and self.frame.state == FrameState.SIGNING

    def seat(self, did: str, at: Optional[datetime] = None) -> ConsentAction:
        """Seat a member, or waitlist while a frame is out for signature."""
        at = at or self.clock.now()
        if did in self.members:
            return ConsentAction("seat", did, "already seated")
        if self.frame is not None and self.frame.state in (FrameState.READY, FrameState.FROZEN):
            return ConsentAction("waitlist", did, "roster is ready/frozen; cannot seat")
        if self.signing:
            if did not in self.waitlist:
                self.waitlist.append(did)
            return ConsentAction("waitlist", did, "frame out for signature; waitlisted")
        self.members.append(did)
        c = self.consent(did)
        c.state, c.seated_at = ConsentState.SEATED, at
        return ConsentAction("seat", did, "seated")

    def unseat(self, did: str, reason: str = "") -> None:
        if did in self.members and did != self.lead_did:
            self.members.remove(did)
            self.declined.append(did)
        c = self.consent(did)
        if c.state != ConsentState.WITHDRAWN:
            c.state = ConsentState.NONE
        c.frame_signature = None

    def seat_from_waitlist(self, ok: Optional[callable] = None, capacity: Optional[int] = None) -> list[ConsentAction]:
        """Seat waitlisted candidates in order; ``ok(did) -> str`` returns a reason to skip (or "")."""
        cap = capacity or self.settings.roster.preferred_size
        out = []
        for d in list(self.waitlist):
            if len(self.members) >= cap:
                break
            self.waitlist.remove(d)
            if d in self.members or d in self.declined:
                continue
            why = ok(d) if ok else ""
            if why:
                out.append(ConsentAction("skip", d, why))
                continue
            out.append(self.seat(d))
        return out

    # ------------------------------------------------------------ frame
    def issue(self, at: Optional[datetime] = None) -> Frame:
        at = at or self.clock.now()
        self._counter += 1
        frame = Frame(frame_id=f"{self.game_id}-f{self._counter}", game_id=self.game_id, members=list(self.members),
                      poem_room=self.poem_room, room_generation=self.room_generation, state=FrameState.SIGNING, issued_at=at)
        if self.frame is not None and self.frame.state not in (FrameState.FROZEN,):
            self.frame.state = FrameState.SUPERSEDED
            self.frame.superseded_by = frame.frame_id
        # the lead's roster post is the lead's consent
        self.sigs.setdefault(self.lead_did, {})[frame.signature] = at
        # carry over every earlier signature on the identical frame
        for did in frame.members:
            when = self.sigs.get(did, {}).get(frame.signature)
            if when is not None:
                frame.signed_by.add(did)
                c = self.consent(did)
                c.state, c.frame_signature, c.signed_at = ConsentState.SIGNED, frame.signature, when
            else:
                c = self.consent(did)
                if c.state in (ConsentState.SIGNED, ConsentState.CONFLICTED):
                    c.state = ConsentState.SEATED
                c.frame_signature = None
        self.frame = frame
        self.frames.append(frame)
        return frame

    def record_signature(self, did: str, frame_signature: str, at: Optional[datetime] = None) -> bool:
        """A consent accepted by the referee. True iff it is on the current frame."""
        at = at or self.clock.now()
        self.sigs.setdefault(did, {})[frame_signature] = at
        f = self.frame
        if f is None or frame_signature != f.signature or did not in f.members:
            return False
        f.signed_by.add(did)
        c = self.consent(did)
        c.state, c.frame_signature, c.signed_at = ConsentState.SIGNED, frame_signature, at
        if f.state == FrameState.SIGNING and self.all_signed():
            f.state = FrameState.READY
        return True

    def record_rejection(self, did: str, reason: str, at: Optional[datetime] = None) -> Optional[ConsentAction]:
        """A consent rejected by the referee un-marks the signature; 'withdraw before changing' → CONFLICTED + note."""
        c = self.consent(did)
        c.rejections += 1
        if self.frame and did in self.frame.signed_by and c.frame_signature == self.frame.signature:
            self.frame.signed_by.discard(did)
        c.frame_signature = None
        if reason.startswith(WITHDRAW_BEFORE_CHANGING):
            c.state = ConsentState.CONFLICTED
            return ConsentAction("withdraw_first", did, f"post sonnet.withdraw.v1 for {self.game_id}, then mirror the current frame")
        if c.state == ConsentState.SIGNED:
            c.state = ConsentState.SEATED
        return ConsentAction("rejected", did, reason)

    def record_withdraw(self, did: str, at: Optional[datetime] = None) -> None:
        c = self.consent(did)
        if self.frame and did in self.frame.signed_by:
            self.frame.signed_by.discard(did)
        c.frame_signature = None
        c.state = ConsentState.WITHDRAWN if did not in self.members else ConsentState.SEATED

    def all_signed(self) -> bool:
        return self.frame is not None and set(self.frame.members) <= self.frame.signed_by

    def missing(self) -> list[str]:
        if self.frame is None:
            return []
        return [d for d in self.frame.members if d not in self.frame.signed_by]

    def change_plan(self, did: str, target: Frame) -> list[str]:
        """Ordering for a member moving to ``target``: withdraw first if a different consent is live."""
        c = self.consent(did)
        if c.frame_signature and c.frame_signature != target.signature:
            return ["withdraw", "sign"]
        return ["sign"]

    def freeze(self, at: Optional[datetime] = None) -> None:
        if self.frame is None:
            return
        self.frame.state = FrameState.FROZEN
        for d in self.frame.members:
            self.consent(d).state = ConsentState.FROZEN

    # ------------------------------------------------------------ tick
    def check(self, now: Optional[datetime] = None) -> list[ConsentAction]:
        """Timeouts: never-signers are dropped, previous-frame signers are reminded. Returns the actions taken."""
        now = now or self.clock.now()
        f = self.frame
        out: list[ConsentAction] = []
        if f is None or f.state != FrameState.SIGNING:
            return out
        missing = self.missing()
        if not missing:
            f.state = FrameState.READY
            out.append(ConsentAction("ready", None, f"frame {f.signature} fully signed"))
            return out
        cs = self.settings.consent
        elapsed = (now - f.issued_at).total_seconds()
        if elapsed < cs.signature_timeout_s:
            return out
        keep = [d for d in missing if self.sigs.get(d)]
        drop = [d for d in missing if not self.sigs.get(d)]
        for d in keep:
            c = self.consent(d)
            if c.last_reminder_at is None or (now - c.last_reminder_at).total_seconds() >= cs.reminder_interval_s:
                c.reminders += 1
                c.last_reminder_at = now
                out.append(ConsentAction("remind", d, "your consent is on an earlier frame: withdraw, then mirror the current frame"))
        for d in drop:
            self.unseat(d, "no signature within the window")
            out.append(ConsentAction("drop", d, f"no signature on any frame within {cs.signature_timeout_s} s"))
        if drop:
            f.state = FrameState.SUPERSEDED      # membership changed: this frame is void, seats may be refilled
            out.append(ConsentAction("reissue", None, "seats re-opened; refill from the waitlist and re-issue the frame"))
        return out


# ---------------------------------------------------------------- availability (referee lag)
@dataclass
class Observation:
    state: AvailabilityState
    at: datetime
    detail: str = ""


class AvailabilityTracker:
    """What we know about another DID's live consent, decaying to UNKNOWN after referee_lag_unknown_after_s."""

    def __init__(self, settings, clock):
        self.settings = settings
        self.clock = clock
        self.obs: dict[str, Observation] = {}

    def observe(self, did: str, state: AvailabilityState, at: Optional[datetime] = None, detail: str = "") -> None:
        self.obs[did] = Observation(AvailabilityState(state), at or self.clock.now(), detail)

    def mark_pending(self, did: str, at: Optional[datetime] = None, detail: str = "withdraw posted, no receipt") -> None:
        """A withdraw/sign is in flight without a receipt: neither free nor active is known."""
        self.obs[did] = Observation(AvailabilityState.UNKNOWN, at or self.clock.now(), detail)

    def state(self, did: str, now: Optional[datetime] = None) -> AvailabilityState:
        o = self.obs.get(did)
        if o is None:
            return AvailabilityState.UNKNOWN
        now = now or self.clock.now()
        if (now - o.at).total_seconds() > self.settings.consent.referee_lag_unknown_after_s:
            return AvailabilityState.UNKNOWN
        return o.state

    def seatable(self, did: str, now: Optional[datetime] = None) -> bool:
        return self.state(did, now) == AvailabilityState.KNOWN_FREE


# ---------------------------------------------------------------- offer filters
def filter_offers(offers: Iterable[Offer], self_did: str, own_game_ids: Iterable[str] = (),
                  closed_game_ids: Iterable[str] = ()) -> list[Offer]:
    """Dedupe by (sender, game_id) keeping the latest; drop self-offers; drop stale (frozen/complete) games;
    personal offers (to_did == self) first, then newest first."""
    own = set(own_game_ids)
    closed = set(closed_game_ids)
    latest: dict[tuple[str, Optional[str]], Offer] = {}
    for o in offers:
        if o.sender == self_did or (o.game_id and o.game_id in own):
            continue
        if o.game_id and o.game_id in closed:
            continue
        key = (o.sender, o.game_id)
        if key not in latest or o.seq > latest[key].seq:
            latest[key] = o
    out = list(latest.values())
    out.sort(key=lambda o: (0 if o.to_did == self_did else 1, -o.seq))
    return out
