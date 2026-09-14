"""Operator boundary: which actions the bot may take on its own (settings.operator).

Lesson (coordination_lessons.md §3): strategy pivots made by the agent without asking eroded trust.
Unknown actions default to OPERATOR_APPROVAL (fail closed).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..models import Decision


@dataclass
class OperatorRequest:
    action: str
    detail: str
    decision: Decision
    at: Optional[datetime]
    approved: Optional[bool] = None


@dataclass
class OperatorBoundary:
    settings: object
    store: object = None
    requests: list[OperatorRequest] = field(default_factory=list)
    _approved_actions: set[str] = field(default_factory=set)

    def classify(self, action: str) -> Decision:
        op = self.settings.operator
        if action in op.approval_required:
            return Decision.OPERATOR_APPROVAL
        if action in op.autonomous:
            return Decision.AUTONOMOUS
        return Decision.OPERATOR_APPROVAL

    def approve(self, action: str) -> None:
        """Operator grants a standing approval for ``action`` (recorded on the next request)."""
        self._approved_actions.add(action)

    def request(self, action: str, detail: str = "", at: Optional[datetime] = None) -> bool:
        """Record the request and return True iff the bot may proceed autonomously (or was approved)."""
        decision = self.classify(action)
        approved: Optional[bool] = None
        if decision == Decision.OPERATOR_APPROVAL:
            approved = action in self._approved_actions
        req = OperatorRequest(action=action, detail=detail, decision=decision, at=at, approved=approved)
        self.requests.append(req)
        if self.store is not None:
            self.store.record_decision(action, decision.value, detail, at=at, approved=approved)
        return decision == Decision.AUTONOMOUS or bool(approved)

    def pending(self) -> list[OperatorRequest]:
        return [r for r in self.requests if r.decision == Decision.OPERATOR_APPROVAL and not r.approved]
