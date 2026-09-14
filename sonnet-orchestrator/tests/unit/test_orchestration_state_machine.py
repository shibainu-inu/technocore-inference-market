import pytest

from sonnet_orchestrator.models import GameState as S
from sonnet_orchestrator.orchestration.state_machine import GameStateMachine, IllegalTransition, TRANSITIONS

MAIN_LINE = [S.APPLY, S.SEATED, S.ROSTER_PENDING, S.ROSTER_READY, S.WRITING, S.LANDING, S.COMPLETE,
             S.PUBLISH_PENDING, S.SUBMITTED, S.ACCEPTED]


def test_main_line_is_legal_and_recorded():
    seen = []
    sm = GameStateMachine(on_transition=lambda a, b, r: seen.append((a, b)))
    assert sm.state == S.DISCOVER
    for st in MAIN_LINE:
        sm.transition(st, "ok")
    assert sm.state == S.ACCEPTED and sm.terminal
    assert [b for _, b in seen] == MAIN_LINE
    assert len(sm.history) == len(MAIN_LINE)


def test_writing_recovering_loop_and_landing():
    sm = GameStateMachine(S.WRITING)
    sm.transition(S.RECOVERING)
    sm.transition(S.WRITING)
    sm.transition(S.RECOVERING)
    sm.transition(S.LANDING)
    sm.transition(S.RECOVERING)
    sm.transition(S.LANDING)
    sm.transition(S.COMPLETE)
    assert sm.state == S.COMPLETE


@pytest.mark.parametrize("frm,to", [
    (S.DISCOVER, S.WRITING), (S.APPLY, S.ROSTER_READY), (S.WRITING, S.SUBMITTED), (S.COMPLETE, S.WRITING),
    (S.SUBMITTED, S.WRITING), (S.ACCEPTED, S.DISCOVER), (S.ROSTER_READY, S.ROSTER_PENDING),
])
def test_illegal_transitions_raise(frm, to):
    sm = GameStateMachine(frm)
    assert not sm.can(to)
    with pytest.raises(IllegalTransition):
        sm.transition(to)
    assert sm.state == frm


def test_abandoned_only_before_complete():
    for st in [S.DISCOVER, S.APPLY, S.SEATED, S.ROSTER_PENDING, S.ROSTER_READY, S.WRITING, S.RECOVERING, S.LANDING]:
        sm = GameStateMachine(st)
        assert sm.can(S.ABANDONED)
        sm.transition(S.ABANDONED)
        assert sm.terminal
    for st in [S.COMPLETE, S.PUBLISH_PENDING, S.SUBMITTED, S.ACCEPTED]:
        sm = GameStateMachine(st)
        assert not sm.can(S.ABANDONED)
        with pytest.raises(IllegalTransition):
            sm.transition(S.ABANDONED)


def test_frame_timeout_reopens_seats():
    sm = GameStateMachine(S.ROSTER_PENDING)
    sm.transition(S.SEATED, "timeout")
    sm.transition(S.ROSTER_PENDING, "re-issued")
    assert sm.state == S.ROSTER_PENDING


def test_ensure_is_idempotent_and_every_state_has_a_row():
    sm = GameStateMachine(S.WRITING)
    assert sm.ensure(S.WRITING) == S.WRITING and not sm.history
    assert sm.ensure(S.LANDING) == S.LANDING and len(sm.history) == 1
    assert set(TRANSITIONS) == set(S)
