"""Writer reliability score (addendum rule: counted from accepted words / signs, never from "yes").

score() blends five components with the weights in ``settings.reliability.weights``:

* completion_rate      poems_completed / games_joined                          (unknown -> neutral)
* accepted_rate        words_accepted / (words_accepted + words_rejected)      (unknown -> neutral)
* response_score       ref / (ref + median latency), ref = health.minimum_timeout_ms (unknown -> neutral)
* recent_activity      window / (window + age), window = health.silent_after_ms  (unknown -> neutral)
* stale_conflict_score 1 - mass-application penalty normalised against real evidence (accepted words + signs)

The mass-application penalty is ``seat_no_sign_weight * seat_no_sign_count + consent_conflict_weight *
consent_conflict_count`` (+ stale offers, weight 1), normalised as ``penalty / (penalty + evidence)`` so that a
writer with plenty of accepted words is forgiven one conflict while a writer with no evidence and one conflict is
scored 0 on that component. ``WriterProfile.mass_application_score`` (already in [0,1] when set) scales it further.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from ..config import Settings
from ..models.core import WriterProfile, utcnow

NEUTRAL = 0.5  # value used for a component about which nothing is known


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


def has_history(writer: WriterProfile) -> bool:
    """True when the profile carries any measured evidence (counts or latencies), not just a stored prior."""
    return any((
        writer.games_joined, writer.words_accepted, writer.words_rejected, writer.signs,
        writer.seat_no_sign_count, writer.consent_conflict_count, writer.stale_offer_count,
        writer.poems_completed, writer.published_entry_count,
        writer.word_latency_median_ms is not None, writer.sign_latency_median_ms is not None,
        writer.last_activity_at is not None,
    ))


def completion_rate(writer: WriterProfile) -> float:
    if writer.games_joined <= 0:
        return NEUTRAL
    return _clamp(writer.poems_completed / writer.games_joined)


def accepted_rate(writer: WriterProfile) -> float:
    total = writer.words_accepted + writer.words_rejected
    if total <= 0:
        return NEUTRAL
    return _clamp(writer.words_accepted / total)


def response_score(writer: WriterProfile, settings: Settings) -> float:
    """1.0 for instant, 0.5 at the minimum timeout, -> 0 for very slow. Word latency first, sign latency fallback."""
    ref = float(settings.health.minimum_timeout_ms)
    lat = writer.word_latency_median_ms
    if lat is None:
        lat = writer.sign_latency_median_ms
    if lat is None or ref <= 0:
        return NEUTRAL
    return _clamp(ref / (ref + max(0.0, float(lat))))


def recent_activity(writer: WriterProfile, settings: Settings, now: Optional[datetime] = None) -> float:
    if writer.last_activity_at is None:
        return NEUTRAL
    now = now or utcnow()
    last = writer.last_activity_at
    if last.tzinfo is None and now.tzinfo is not None:
        now = now.replace(tzinfo=None)
    age_ms = max(0.0, (now - last).total_seconds() * 1000.0)
    window = float(settings.health.silent_after_ms)
    if window <= 0:
        return NEUTRAL
    return _clamp(window / (window + age_ms))


def mass_application_penalty(writer: WriterProfile, settings: Settings) -> float:
    """Raw (un-normalised) penalty mass from the addendum counters."""
    ma = settings.reliability.mass_application
    return (ma.seat_no_sign_weight * writer.seat_no_sign_count
            + ma.consent_conflict_weight * writer.consent_conflict_count
            + writer.stale_offer_count)


def stale_conflict_score(writer: WriterProfile, settings: Settings) -> float:
    penalty = float(mass_application_penalty(writer, settings))
    evidence = float(writer.words_accepted + writer.signs)
    if penalty <= 0:
        base = 1.0
    else:
        base = 1.0 - penalty / (penalty + evidence)
    return _clamp(base * (1.0 - _clamp(writer.mass_application_score)))


def components(writer: WriterProfile, settings: Settings, now: Optional[datetime] = None) -> dict[str, float]:
    return {
        "completion_rate": completion_rate(writer),
        "accepted_rate": accepted_rate(writer),
        "response_score": response_score(writer, settings),
        "recent_activity": recent_activity(writer, settings, now),
        "stale_conflict_score": stale_conflict_score(writer, settings),
    }


def score(writer: WriterProfile, settings: Settings, now: Optional[datetime] = None) -> float:
    """Weighted reliability in [0, 1]. Weights come from settings.reliability.weights (normalised by their sum)."""
    w = settings.reliability.weights
    weights = {
        "completion_rate": w.completion_rate,
        "accepted_rate": w.accepted_rate,
        "response_score": w.response_score,
        "recent_activity": w.recent_activity,
        "stale_conflict_score": w.stale_conflict_score,
    }
    total = sum(weights.values())
    if total <= 0:
        return NEUTRAL
    comps = components(writer, settings, now)
    return _clamp(sum(weights[k] * comps[k] for k in weights) / total)


def effective_reliability(writer: WriterProfile, settings: Settings, now: Optional[datetime] = None) -> float:
    """What the solver uses: the measured score when the profile carries evidence, else the stored prior field."""
    if has_history(writer):
        return score(writer, settings, now)
    return _clamp(writer.reliability)
