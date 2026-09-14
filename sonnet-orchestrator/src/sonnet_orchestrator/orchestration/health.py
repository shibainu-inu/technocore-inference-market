"""Per-writer health from measured latencies (never from promises).

expected_ms(did)  = max(minimum_timeout_ms, median of that writer's accepted-word latencies)
While a writer holds the next slot ("waiting"), overdue/expected ≥ slow/suspect/down multipliers escalates
HEALTHY → SLOW → SUSPECT → DOWN.  A seated/signed writer with no accepted word or post for silent_after_ms is SILENT.
Recovery: any new post/sign while DOWN/SILENT/SUSPECT/SLOW → settings.health.recover_to; the next accepted word → HEALTHY.
Escalated states are sticky until the writer shows activity (a covered writer stays SLOW/SUSPECT/DOWN).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from statistics import median
from typing import Iterable, Optional

from ..models import HealthSnapshot, WriterHealth

ACTIVE_STATES = frozenset({WriterHealth.HEALTHY, WriterHealth.SLOW, WriterHealth.SUSPECT})
INACTIVE_STATES = frozenset({WriterHealth.DOWN, WriterHealth.SILENT})
RANK = {WriterHealth.HEALTHY: 0, WriterHealth.SLOW: 1, WriterHealth.SUSPECT: 2, WriterHealth.SILENT: 3, WriterHealth.DOWN: 4}


def _ms(a: datetime, b: datetime) -> float:
    return (a - b).total_seconds() * 1000.0


@dataclass
class WriterTrack:
    did: str
    health: WriterHealth = WriterHealth.HEALTHY
    seated_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None
    last_word_at: Optional[datetime] = None
    waiting_since: Optional[datetime] = None
    latencies_ms: list[float] = field(default_factory=list)
    prior_median_ms: Optional[float] = None
    reason: str = ""


class HealthManager:
    def __init__(self, settings, clock):
        self.settings = settings
        self.clock = clock
        self.tracks: dict[str, WriterTrack] = {}

    # ------------------------------------------------------------ registration / inputs
    def register(self, did: str, seated_at: Optional[datetime] = None, latency_median_ms: Optional[float] = None,
                 health: WriterHealth = WriterHealth.HEALTHY) -> WriterTrack:
        t = self.tracks.get(did)
        if t is None:
            t = WriterTrack(did=did, seated_at=seated_at or self.clock.now(), prior_median_ms=latency_median_ms, health=health)
            self.tracks[did] = t
        else:
            if seated_at is not None:
                t.seated_at = seated_at
            if latency_median_ms is not None:
                t.prior_median_ms = latency_median_ms
        return t

    def _track(self, did: str) -> WriterTrack:
        return self.tracks.get(did) or self.register(did)

    def record_latency(self, did: str, ms: float) -> None:
        if ms >= 0:
            self._track(did).latencies_ms.append(float(ms))

    def record_activity(self, did: str, at: Optional[datetime] = None, kind: str = "post") -> WriterHealth:
        t = self._track(did)
        at = at or self.clock.now()
        t.last_activity_at = at
        if kind == "word_accepted":
            t.last_word_at = at
            t.waiting_since = None
            t.health = WriterHealth.HEALTHY
            t.reason = "accepted a word"
        elif t.health != WriterHealth.HEALTHY:
            t.health = WriterHealth(self.settings.health.recover_to)
            t.reason = f"{kind} seen while degraded -> {t.health.value}"
        return t.health

    def mark_waiting(self, did: str, since: datetime) -> None:
        t = self._track(did)
        if t.waiting_since is None or since > t.waiting_since:
            t.waiting_since = since

    def clear_waiting(self, did: Optional[str] = None) -> None:
        for t in (self.tracks.values() if did is None else [self._track(did)]):
            t.waiting_since = None

    # ------------------------------------------------------------ outputs
    def expected_ms(self, did: str) -> float:
        floor = float(self.settings.health.minimum_timeout_ms)
        t = self.tracks.get(did)
        if t is None:
            return floor
        if t.latencies_ms:
            return max(floor, float(median(t.latencies_ms)))
        if t.prior_median_ms is not None:
            return max(floor, float(t.prior_median_ms))
        return floor

    def update(self, now: Optional[datetime] = None) -> dict[str, WriterHealth]:
        now = now or self.clock.now()
        h = self.settings.health
        for t in self.tracks.values():
            if t.waiting_since is not None:
                ratio = _ms(now, t.waiting_since) / self.expected_ms(t.did)
                if ratio >= h.down_multiplier:
                    esc, why = WriterHealth.DOWN, f"overdue x{ratio:.1f} on the next slot"
                elif ratio >= h.suspect_multiplier:
                    esc, why = WriterHealth.SUSPECT, f"overdue x{ratio:.1f} on the next slot"
                elif ratio >= h.slow_multiplier:
                    esc, why = WriterHealth.SLOW, f"overdue x{ratio:.1f} on the next slot"
                else:
                    esc, why = None, ""
                if esc is not None and RANK[esc] > RANK[t.health]:
                    t.health, t.reason = esc, why
            last = t.last_activity_at or t.seated_at
            if last is not None and t.health in ACTIVE_STATES and _ms(now, last) >= h.silent_after_ms:
                t.health = WriterHealth.SILENT
                t.reason = f"no accepted word or post for {_ms(now, last) / 1000:.0f} s"
        return {d: t.health for d, t in self.tracks.items()}

    def health(self, did: str) -> WriterHealth:
        t = self.tracks.get(did)
        return t.health if t else WriterHealth.HEALTHY

    def set_health(self, did: str, health: WriterHealth, reason: str = "") -> None:
        t = self._track(did)
        t.health, t.reason = health, reason

    def is_active(self, did: str) -> bool:
        return self.health(did) in ACTIVE_STATES

    def active(self, dids: Optional[Iterable[str]] = None) -> list[str]:
        pool = list(dids) if dids is not None else list(self.tracks)
        return [d for d in pool if self.is_active(d)]

    def snapshot(self) -> list[HealthSnapshot]:
        return [HealthSnapshot(did=t.did, health=t.health, expected_ms=self.expected_ms(t.did),
                               last_seen_at=t.last_activity_at, reason=t.reason) for t in self.tracks.values()]
