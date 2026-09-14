"""Game state machine with explicit transitions. Illegal transitions raise.

Main line: DISCOVER → APPLY → SEATED → ROSTER_PENDING → ROSTER_READY → WRITING ⇄ RECOVERING → LANDING → COMPLETE
           → PUBLISH_PENDING → SUBMITTED → ACCEPTED.  ABANDONED is reachable from every state before COMPLETE.
Backward edges that production needed (coordination_lessons.md cases 7, 10):
  ROSTER_PENDING → SEATED   (a frame timed out: seats re-open, a new frame will be issued)
  SEATED → ROSTER_PENDING   (re-issue)
  LANDING ⇄ RECOVERING      (a writer drops out during the last line)
  RECOVERING → LANDING      (recovery lands directly in the last line)
"""
from __future__ import annotations

from datetime import datetime
from typing import Callable, Optional

from ..models import GameState

S = GameState

TRANSITIONS: dict[GameState, frozenset[GameState]] = {
    S.DISCOVER: frozenset({S.APPLY}),
    S.APPLY: frozenset({S.SEATED}),
    S.SEATED: frozenset({S.ROSTER_PENDING}),
    S.ROSTER_PENDING: frozenset({S.ROSTER_READY, S.SEATED}),
    S.ROSTER_READY: frozenset({S.WRITING}),
    S.WRITING: frozenset({S.RECOVERING, S.LANDING, S.COMPLETE}),
    S.RECOVERING: frozenset({S.WRITING, S.LANDING}),
    S.LANDING: frozenset({S.COMPLETE, S.RECOVERING}),
    S.COMPLETE: frozenset({S.PUBLISH_PENDING}),
    S.PUBLISH_PENDING: frozenset({S.SUBMITTED}),
    S.SUBMITTED: frozenset({S.ACCEPTED}),
    S.ACCEPTED: frozenset(),
    S.ABANDONED: frozenset(),
}

PRE_COMPLETE: frozenset[GameState] = frozenset({
    S.DISCOVER, S.APPLY, S.SEATED, S.ROSTER_PENDING, S.ROSTER_READY, S.WRITING, S.RECOVERING, S.LANDING,
})

TERMINAL: frozenset[GameState] = frozenset({S.ACCEPTED, S.ABANDONED})


class IllegalTransition(RuntimeError):
    pass


class GameStateMachine:
    def __init__(self, initial: GameState = GameState.DISCOVER,
                 on_transition: Optional[Callable[[GameState, GameState, str], None]] = None):
        self._state = GameState(initial)
        self.history: list[tuple[GameState, GameState, str, Optional[datetime]]] = []
        self._on_transition = on_transition

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def terminal(self) -> bool:
        return self._state in TERMINAL

    @property
    def writing(self) -> bool:
        return self._state in (S.WRITING, S.RECOVERING, S.LANDING)

    def allowed(self) -> frozenset[GameState]:
        out = set(TRANSITIONS[self._state])
        if self._state in PRE_COMPLETE:
            out.add(S.ABANDONED)
        return frozenset(out)

    def can(self, to: GameState) -> bool:
        return GameState(to) in self.allowed()

    def transition(self, to: GameState, reason: str = "", at: Optional[datetime] = None) -> GameState:
        to = GameState(to)
        if not self.can(to):
            raise IllegalTransition(f"{self._state.value} -> {to.value} is not allowed ({reason or 'no reason'})")
        frm = self._state
        self._state = to
        self.history.append((frm, to, reason, at))
        if self._on_transition:
            self._on_transition(frm, to, reason)
        return to

    def ensure(self, to: GameState, reason: str = "", at: Optional[datetime] = None) -> GameState:
        """Transition only if not already there (idempotent helper for the controller)."""
        if self._state == GameState(to):
            return self._state
        return self.transition(to, reason, at)
