"""Deterministic solver: word -> writer assignment, feasibility, reliability, roster optimisation."""
from .assignment import AssignmentResult, assign, active_writers, eligible_writers, latency_norm, health_penalty  # noqa: F401
from .feasibility import Feasibility, FailureTolerance, ParityReport, check, parity_check, failure_tolerance  # noqa: F401
from .reliability import score, effective_reliability, components, has_history  # noqa: F401
from .roster import RosterOption, optimize, evaluate, member_value  # noqa: F401
from .explain import explain_assignment  # noqa: F401
