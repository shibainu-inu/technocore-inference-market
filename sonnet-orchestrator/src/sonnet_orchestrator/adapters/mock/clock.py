"""Deterministic clock. ``sleep``/``advance`` move time in fixed sub-steps and notify subscribers
(the simulated world — scripted writers, referee delivery) at every sub-step."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Callable, Optional


class FakeClock:
    def __init__(self, start: Optional[datetime] = None, step_seconds: float = 5.0):
        self._now = start or datetime(2026, 9, 14, 0, 0, tzinfo=timezone.utc)
        if self._now.tzinfo is None:
            self._now = self._now.replace(tzinfo=timezone.utc)
        self.step_seconds = float(step_seconds)
        self._subscribers: list[Callable[[datetime], None]] = []
        self.sleeps: list[float] = []

    def now(self) -> datetime:
        return self._now

    def subscribe(self, fn: Callable[[datetime], None]) -> None:
        self._subscribers.append(fn)

    def advance(self, seconds: float) -> datetime:
        remaining = float(seconds)
        while remaining > 0:
            step = min(self.step_seconds, remaining)
            self._now = self._now + timedelta(seconds=step)
            remaining -= step
            for fn in list(self._subscribers):
                fn(self._now)
        return self._now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(float(seconds))
        self.advance(seconds)
