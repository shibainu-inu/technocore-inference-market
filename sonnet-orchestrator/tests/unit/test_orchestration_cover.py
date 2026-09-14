"""Cover / hand-off rules, including the 58→59 and 96→97 'beg' traps from nohitori-2 (coordination_lessons.md 8, 11)."""
from sonnet_orchestrator.adapters.mock import FakeClock
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models import AcceptedWord, Assignment, Plan, PoemState, WordEntry, WriterHealth as H, WriterProfile
from sonnet_orchestrator.orchestration.cover import chain_feasible, hand_off_next, should_cover, spellers
from sonnet_orchestrator.orchestration.health import HealthManager

ME, X, Y = "did:me", "did:x", "did:y"
ALL = frozenset("abcdefghijklmnopqrstuvwxyz")
# X and Y cannot spell 'g' (beg / begin), Y cannot spell 'w'
W_ME = WriterProfile(did=ME, letters=ALL, is_self=True)
W_X = WriterProfile(did=X, letters=ALL - {"g"})
W_Y = WriterProfile(did=Y, letters=ALL - {"g", "w"})
WRITERS = [W_ME, W_X, W_Y]


def mk_plan(words: list[str], primaries: list[str]) -> Plan:
    ws = [WordEntry(index=i, text=t, line=0, syllables=1) for i, t in enumerate(words)]
    return Plan(plan_id="p", game_id="g", version=1, owner=ME, words=ws, lines=[" ".join(words)],
                assignments=[Assignment(index=i, primary=p) for i, p in enumerate(primaries)])


def poem(texts: list[str], contributors: list[str], clock) -> PoemState:
    acc = [AcceptedWord(index=i, text=t, contributor=c, version=i + 1, accepted_at=clock.now())
           for i, (t, c) in enumerate(zip(texts, contributors))]
    return PoemState(game_id="g", accepted=acc, version=len(acc))


def mk():
    settings = load_settings()
    clock = FakeClock()
    hm = HealthManager(settings, clock)
    for w in WRITERS:
        hm.register(w.did)
    return settings, clock, hm


def test_no_cover_before_expected_ms_then_cover_with_hand_off():
    settings, clock, hm = mk()
    plan = mk_plan(["the", "sea", "and", "sky"], [Y, X, ME, X])
    pm = poem(["the"], [Y], clock)
    since = clock.now()
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=WRITERS, waiting_since=since)
    assert not dec.cover and "within expected" in dec.reason
    clock.advance(settings.health.minimum_timeout_ms / 1000.0)
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=WRITERS, waiting_since=since)
    assert dec.cover and dec.who == ME and dec.index == 1
    assert dec.hand_off == (2, Y)          # word 2 was ours; handed to the active member with the fewest slots


def test_never_cover_after_our_own_word_or_when_we_cannot_spell():
    settings, clock, hm = mk()
    plan = mk_plan(["the", "sea", "and"], [ME, X, Y])
    pm = poem(["the"], [ME], clock)
    clock.advance(settings.health.minimum_timeout_ms)
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=WRITERS, waiting_since=pm.accepted[0].accepted_at)
    assert not dec.cover and "twice in a row" in dec.reason
    narrow = [WriterProfile(did=ME, letters=frozenset("dik"), is_self=True), W_X, W_Y]
    pm2 = poem(["the"], [Y], clock)
    dec = should_cover(plan, pm2, hm, settings, clock.now(), self_did=ME, writers=narrow, waiting_since=pm2.accepted[0].accepted_at)
    assert not dec.cover and "cannot spell" in dec.reason
    own = should_cover(mk_plan(["the", "sea"], [Y, ME]), pm2, hm, settings, clock.now(), self_did=ME, writers=WRITERS)
    assert not own.cover and "own slot" in own.reason


def test_beg_trap_58_59_next_word_only_we_can_spell():
    """Word 58 is X's and overdue; word 59 'beg' is spellable only by us -> taking 58 deadlocks the room."""
    settings, clock, hm = mk()
    plan = mk_plan(["the", "tide", "beg", "for"], [ME, X, ME, X])
    pm = poem(["the"], [ME], clock)
    pm.accepted[0].contributor = Y          # Y wrote word 0 so that we are allowed to post
    clock.advance(settings.health.down_multiplier * settings.health.minimum_timeout_ms / 1000.0)
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=WRITERS, waiting_since=pm.accepted[0].accepted_at)
    assert not dec.cover and "beg trap" in dec.reason and "'beg'" in dec.reason


def test_beg_trap_96_97_absent_or_slow_members_do_not_count():
    """Word 97 is spellable by us and by Y, but Y is DOWN (or SILENT): treat Y as absent -> no cover."""
    settings, clock, hm = mk()
    plan = mk_plan(["the", "tide", "wag", "for"], [Y, X, Y, X])     # 'wag' needs g: only ME and (not X, not Y)...
    # make Y able to spell 'wag' but DOWN
    writers = [W_ME, W_X, WriterProfile(did=Y, letters=ALL)]
    pm = poem(["the"], [Y], clock)
    clock.advance(settings.health.down_multiplier * settings.health.minimum_timeout_ms / 1000.0)
    ok = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=writers, waiting_since=pm.accepted[0].accepted_at)
    assert ok.cover                                  # Y healthy: Y can take 'wag' after us
    hm.set_health(Y, H.DOWN, "test")
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=writers, waiting_since=pm.accepted[0].accepted_at)
    assert not dec.cover and "beg trap" in dec.reason
    hm.set_health(Y, H.SILENT, "test")
    assert not should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=writers, waiting_since=pm.accepted[0].accepted_at).cover
    hm.set_health(Y, H.SLOW, "test")                 # SLOW is still active: cover allowed, Y keeps word 2
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=writers, waiting_since=pm.accepted[0].accepted_at)
    assert dec.cover and dec.hand_off is None


def test_lookahead_depth_two_chain():
    """Word i+1 has an active speller, but word i+2 then has nobody legal -> lookahead 2 refuses the cover."""
    settings, clock, hm = mk()
    # only ME and X spell 'sea': after we take word 1 the chain is 2 -> X, 3 -> ME (feasible at depth 2)
    writers = [W_ME, WriterProfile(did=X, letters=frozenset("seadik")), WriterProfile(did=Y, letters=frozenset("dikey"))]
    plan = mk_plan(["the", "tide", "sea", "sea", "sea"], [Y, X, X, X, X])
    pm = poem(["the"], [Y], clock)
    clock.advance(settings.health.minimum_timeout_ms / 1000.0)
    # chain after ME: 2 -> X (only X or ME can spell 'sea'; ME just posted), 3 -> ME, fine at depth 2
    dec = should_cover(plan, pm, hm, settings, clock.now(), self_did=ME, writers=writers, waiting_since=pm.accepted[0].accepted_at)
    assert dec.cover
    letters = {ME: ALL, X: frozenset("seadik")}
    assert chain_feasible(["sea", "sea"], letters, ME, 2)
    assert not chain_feasible(["sea", "sea"], {ME: ALL, X: frozenset("dik")}, ME, 2)


def test_hand_off_prefers_fewest_assignments_and_active_spellers():
    plan = mk_plan(["the", "sea", "the", "the"], [ME, X, X, X])
    letters = {X: ALL, Y: ALL}
    assert hand_off_next(plan, 1, letters, ME) == Y                  # Y has 0 slots, X has 3
    assert hand_off_next(plan, 1, {X: ALL}, ME, exclude={X}) is None
    assert spellers("beg", {ME: ALL, X: ALL - {"g"}}) == [ME]
