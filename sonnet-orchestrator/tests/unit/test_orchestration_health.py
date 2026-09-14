from datetime import timedelta

from sonnet_orchestrator.adapters.mock import FakeClock
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models import WriterHealth as H
from sonnet_orchestrator.orchestration.health import HealthManager

A, B = "did:a", "did:b"


def mk():
    settings = load_settings()
    clock = FakeClock()
    return settings, clock, HealthManager(settings, clock)


def test_expected_ms_floor_prior_and_median():
    settings, clock, hm = mk()
    floor = settings.health.minimum_timeout_ms
    assert hm.expected_ms("unknown") == floor
    hm.register(A, latency_median_ms=floor * 3)
    assert hm.expected_ms(A) == floor * 3            # prior from writer_scores until we measure
    for ms in (1000, 2000, 3000):
        hm.record_latency(A, ms)
    assert hm.expected_ms(A) == floor                 # measured median below the floor -> floor
    hm.record_latency(B, floor * 4); hm.record_latency(B, floor * 2); hm.record_latency(B, floor * 8)
    assert hm.expected_ms(B) == floor * 4             # median of measurements


def test_waiting_escalates_by_multipliers_and_is_sticky_until_activity():
    settings, clock, hm = mk()
    h = settings.health
    hm.register(A)
    t0 = clock.now()
    hm.mark_waiting(A, t0)
    exp = hm.expected_ms(A) / 1000.0
    clock.advance(exp * h.slow_multiplier)
    assert hm.update()[A] == H.SLOW
    clock.advance(exp * (h.suspect_multiplier - h.slow_multiplier))
    assert hm.update()[A] == H.SUSPECT
    clock.advance(exp * (h.down_multiplier - h.suspect_multiplier))
    assert hm.update()[A] == H.DOWN and not hm.is_active(A)
    hm.clear_waiting(A)                                # somebody covered the slot: state stays DOWN
    assert hm.update()[A] == H.DOWN
    hm.record_activity(A, kind="post")                 # a post -> recover_to
    assert hm.health(A) == H(h.recover_to)
    assert hm.is_active(A)
    hm.record_activity(A, kind="word_accepted")        # accepted word -> HEALTHY
    assert hm.health(A) == H.HEALTHY


def test_silent_after_no_activity_and_recovery():
    settings, clock, hm = mk()
    hm.register(A)
    hm.register(B)
    clock.advance(settings.health.silent_after_ms / 1000.0 - 1)
    hm.record_activity(B, kind="post")
    clock.advance(2)
    st = hm.update()
    assert st[A] == H.SILENT and st[B] == H.HEALTHY
    assert hm.active([A, B]) == [B]
    hm.record_activity(A, kind="sign")
    assert hm.health(A) == H(settings.health.recover_to)
    snaps = {s.did: s for s in hm.snapshot()}
    assert snaps[A].health == H.SUSPECT and snaps[A].expected_ms == settings.health.minimum_timeout_ms
    assert snaps[B].last_seen_at is not None


def test_mark_waiting_keeps_the_earliest_since():
    settings, clock, hm = mk()
    hm.register(A)
    t0 = clock.now()
    hm.mark_waiting(A, t0)
    hm.mark_waiting(A, t0 - timedelta(seconds=5))     # older 'since' does not move the timer back
    assert hm.tracks[A].waiting_since == t0
    hm.mark_waiting(A, t0 + timedelta(seconds=5))     # a later re-assignment restarts it
    assert hm.tracks[A].waiting_since == t0 + timedelta(seconds=5)
