from datetime import timedelta

from sonnet_orchestrator.adapters.mock import FakeClock
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models import AvailabilityState, ConsentState, FrameState, Offer
from sonnet_orchestrator.orchestration.consent import (WITHDRAW_BEFORE_CHANGING, AvailabilityTracker, FrameManager,
                                                       filter_offers)

LEAD, A, B, C, D, E = "did:lead", "did:a", "did:b", "did:c", "did:d", "did:e"


def mk():
    settings = load_settings()
    clock = FakeClock()
    fm = FrameManager(settings, clock, "g1", "room-1", LEAD)
    return settings, clock, fm


def test_seat_apply_and_issue_frame():
    settings, clock, fm = mk()
    for d in (A, B, C):
        fm.apply(d)
        assert fm.consent(d).state == ConsentState.APPLIED
        assert fm.seat(d).kind == "seat"
    assert fm.members == [LEAD, A, B, C]
    f = fm.issue()
    assert f.state == FrameState.SIGNING and f.members == [LEAD, A, B, C]
    assert f.signed_by == {LEAD}          # the lead's roster post is its consent
    assert fm.missing() == [A, B, C]


def test_waitlist_while_signing_never_changes_members():
    settings, clock, fm = mk()
    for d in (A, B, C):
        fm.seat(d)
    f = fm.issue()
    act = fm.seat(D)
    assert act.kind == "waitlist" and D not in fm.members and fm.waitlist == [D]
    assert fm.frame.signature == f.signature     # frame identity untouched


def test_signatures_carry_over_to_identical_frame_and_ready():
    settings, clock, fm = mk()
    for d in (A, B):
        fm.seat(d)
    f1 = fm.issue()
    assert fm.record_signature(A, f1.signature)
    assert fm.consent(A).state == ConsentState.SIGNED
    f2 = fm.issue()                               # re-issue of the identical frame
    assert f2.same_as(f1) and f1.state == FrameState.SUPERSEDED and f1.superseded_by == f2.frame_id
    assert A in f2.signed_by and fm.consent(A).state == ConsentState.SIGNED
    assert not fm.record_signature(B, "not-this-frame")
    assert fm.record_signature(B, f2.signature)
    assert fm.all_signed() and f2.state == FrameState.READY
    fm.freeze()
    assert f2.state == FrameState.FROZEN and all(fm.consent(d).state == ConsentState.FROZEN for d in f2.members)
    assert fm.seat(E).kind == "waitlist"


def test_changed_frame_resets_signatures_of_the_old_one():
    settings, clock, fm = mk()
    fm.seat(A); fm.seat(B)
    f1 = fm.issue()
    fm.record_signature(A, f1.signature)
    fm.seat(C)                                    # allowed? no: SIGNING -> waitlist
    assert C in fm.waitlist
    fm.frame.state = FrameState.SUPERSEDED         # simulate the lead deciding to re-frame
    fm.seat_from_waitlist()
    f2 = fm.issue()
    assert not f2.same_as(f1) and A not in f2.signed_by
    assert fm.consent(A).state == ConsentState.SEATED
    assert fm.change_plan(A, f2) == ["sign"]      # nothing live on another frame from our records
    fm.consent(A).frame_signature = f1.signature
    assert fm.change_plan(A, f2) == ["withdraw", "sign"]


def test_timeout_reminds_previous_signers_and_drops_never_signers():
    settings, clock, fm = mk()
    fm.seat(A); fm.seat(B); fm.seat(C)
    f1 = fm.issue()
    fm.record_signature(A, f1.signature)
    fm.record_signature(B, f1.signature)
    # B's consent gets rejected later (consent elsewhere): signature un-marked, note issued
    act = fm.record_rejection(B, WITHDRAW_BEFORE_CHANGING + " (live consent on g9)")
    assert act.kind == "withdraw_first" and fm.consent(B).state == ConsentState.CONFLICTED
    assert B not in f1.signed_by
    assert fm.check() == []                        # before the timeout nothing happens
    clock.advance(settings.consent.signature_timeout_s)
    actions = fm.check()
    kinds = {(a.kind, a.did) for a in actions}
    assert ("remind", B) in kinds                  # B signed a frame before -> reminder, not the door
    assert ("drop", C) in kinds                    # C never signed anything -> dropped
    assert ("reissue", None) in kinds
    assert C not in fm.members and C in fm.declined and B in fm.members
    # reminders repeat only every reminder_interval_s
    fm.issue()                                     # new frame [LEAD, A, B]: A and B signed the old one
    clock.advance(settings.consent.signature_timeout_s)
    assert {a.did for a in fm.check() if a.kind == "remind"} == {A, B}
    assert [a for a in fm.check() if a.kind == "remind"] == []     # same instant: interval not elapsed
    clock.advance(settings.consent.reminder_interval_s)
    assert {a.did for a in fm.check() if a.kind == "remind"} == {A, B}
    assert fm.consent(B).reminders == 3 and fm.consent(A).reminders == 2
    assert not any(a.kind == "drop" for a in fm.check())           # previous signers are never dropped


def test_seat_from_waitlist_respects_gate_and_capacity():
    settings, clock, fm = mk()
    fm.seat(A); fm.seat(B)
    fm.issue()
    fm.seat(C); fm.seat(D); fm.seat(E)
    fm.frame.state = FrameState.SUPERSEDED
    acts = fm.seat_from_waitlist(ok=lambda d: "bad key" if d == C else "", capacity=4)
    assert [(a.kind, a.did) for a in acts] == [("skip", C), ("seat", D)]
    assert fm.members == [LEAD, A, B, D] and E in fm.waitlist


def test_withdraw_then_sign_ordering_on_rejection_counts():
    settings, clock, fm = mk()
    fm.seat(A)
    f = fm.issue()
    fm.record_signature(A, f.signature)
    fm.record_withdraw(A)
    assert A not in f.signed_by and fm.consent(A).state == ConsentState.SEATED
    fm.record_signature(A, f.signature)
    assert fm.all_signed()


def test_availability_tri_state_with_referee_lag():
    settings, clock, _ = mk()
    av = AvailabilityTracker(settings, clock)
    assert av.state(A) == AvailabilityState.UNKNOWN
    av.observe(A, AvailabilityState.KNOWN_FREE)
    assert av.seatable(A)
    clock.advance(settings.consent.referee_lag_unknown_after_s + 1)
    assert av.state(A) == AvailabilityState.UNKNOWN and not av.seatable(A)
    av.observe(B, AvailabilityState.KNOWN_ACTIVE, detail="consent on g9 seq 123")
    assert av.state(B) == AvailabilityState.KNOWN_ACTIVE
    av.mark_pending(B)
    assert av.state(B) == AvailabilityState.UNKNOWN


def test_offer_filters():
    clock = FakeClock()
    t = clock.now()
    offers = [
        Offer(seq=1, at=t, sender=A, game_id="g-a", kind="recruit"),
        Offer(seq=2, at=t, sender=A, game_id="g-a", kind="recruit"),              # duplicate (sender, game)
        Offer(seq=3, at=t, sender=LEAD, game_id="g1", kind="recruit"),          # self-offer
        Offer(seq=4, at=t, sender=B, game_id="g1", kind="application"),         # application to our own game
        Offer(seq=5, at=t, sender=C, game_id="g-old", kind="recruit"),          # stale: game frozen
        Offer(seq=6, at=t, sender=D, game_id="g-d", kind="personal_offer", to_did=LEAD),
        Offer(seq=7, at=t, sender=E, game_id="g-e", kind="recruit"),
    ]
    out = filter_offers(offers, LEAD, own_game_ids={"g1"}, closed_game_ids={"g-old"})
    assert [o.seq for o in out] == [6, 7, 2]      # personal first, then newest; dedupe kept seq 2
