"""Per-writer metrics and game KPIs derived from a :class:`ReplayLog`.

Metric definitions follow ``sonnet/tools/writer_scores.py`` (the live scoring tool):
- word latency = seconds from the previous accepted word's receipt to this writer's accepted word post
  (the first accepted word of a game has no predecessor and is skipped);
- rejected = referee receipts with status rejected for this writer's word posts (batch receipts included);
- sign latency = seconds from the lead's accepted roster receipt to the member's accepted roster receipt
  (only receipts after the lead's count; None when the export holds no lead roster receipt);
- published entries = poems where the writer posted the final (complete=true) word.
"""
from __future__ import annotations

import json
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models.core import ConsentState, WriterProfile
from .replay import ReplayLog

STALE_REASON = "version: stale"
INCOMPLETE_CONSENT_REASON = "roster: incomplete consent"
LETTERS_ABSENT_PREFIX = "word: letters absent from contributor DID"


@dataclass
class CoverEvent:
    """An accepted word posted by someone other than the planned signer of the newest table."""
    index: int                 # 0-based accepted index
    word: str
    planned: str               # label as written in the table
    planned_did: Optional[str]
    actual: str
    table_seq: int
    at: datetime
    by_lead: bool


@dataclass
class GameKPIs:
    game_id: str
    words: int
    members: list[str]
    roster_ready_at: Optional[datetime]
    completed_at: Optional[datetime]
    complete: bool
    minutes_to_complete: Optional[float]
    words_per_hour: Optional[float]
    longest_gap_s: float
    longest_gap_index: Optional[int]
    gaps_s: list[float]
    contributions: dict[str, int]
    stale_count: int
    stale_batch_count: int
    incomplete_consent_count: int
    letters_absent_count: int
    rejections: int
    cover_events: list[CoverEvent]
    cover_count: int
    table_posts: int
    turn_script_posts: int
    note_posts: int
    final_contributor: Optional[str]
    stalls_over_s: dict[int, int] = field(default_factory=dict)   # threshold -> count of gaps above it

    def as_dict(self) -> dict:
        return {
            "game_id": self.game_id, "words": self.words, "complete": self.complete,
            "roster_ready_at": self.roster_ready_at.isoformat() if self.roster_ready_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "minutes_to_complete": self.minutes_to_complete, "words_per_hour": self.words_per_hour,
            "longest_gap_s": self.longest_gap_s, "longest_gap_index": self.longest_gap_index,
            "contributions": dict(self.contributions), "stale_count": self.stale_count,
            "stale_batch_count": self.stale_batch_count, "incomplete_consent_count": self.incomplete_consent_count,
            "letters_absent_count": self.letters_absent_count, "rejections": self.rejections,
            "cover_count": self.cover_count, "table_posts": self.table_posts,
            "final_contributor": self.final_contributor, "stalls_over_s": dict(self.stalls_over_s),
        }


# ---------------------------------------------------------------- per-writer
def word_latencies(log: ReplayLog) -> dict[str, list[float]]:
    """Seconds from previous accepted receipt to each writer's accepted word post (writer_scores.py definition)."""
    posts = {w.request_id: w for w in log.words}
    out: dict[str, list[float]] = {m: [] for m in log.members}
    prev: Optional[datetime] = None
    for aw in log.accepted:
        wp = posts.get(aw.request_id)
        if wp is None:
            continue
        if prev is not None:
            out.setdefault(aw.contributor, []).append(max(0.0, (wp.at - prev).total_seconds()))
        prev = aw.accepted_at
    return out


def accepted_gaps(log: ReplayLog) -> list[float]:
    """Seconds between consecutive accepted receipts (index i-1 -> i); gaps[0] is roster_ready -> word 0 when known."""
    gaps: list[float] = []
    prev = log.roster_ready_at
    for aw in log.accepted:
        if prev is not None and aw.accepted_at is not None:
            gaps.append((aw.accepted_at - prev).total_seconds())
        prev = aw.accepted_at
    return gaps


def sign_latencies(log: ReplayLog) -> dict[str, list[float]]:
    lead_receipts = [r for r in log.roster_receipts if r.sender_did == log.lead and r.status == "accepted"]
    out: dict[str, list[float]] = {}
    if not lead_receipts:
        return out
    t0 = lead_receipts[0].at
    for r in log.roster_receipts:
        if r.sender_did == log.lead or r.status != "accepted" or r.at < t0:
            continue
        out.setdefault(r.sender_did, []).append((r.at - t0).total_seconds())
    return out


def writer_metrics(log: ReplayLog, *, self_did: Optional[str] = None) -> dict[str, WriterProfile]:
    self_did = self_did or log.lead
    lat = word_latencies(log)
    sig = sign_latencies(log)
    contrib = log.contributions()
    rejected: dict[str, int] = {m: 0 for m in log.members}
    for rj in log.rejections:
        if rj.sender:
            rejected[rj.sender] = rejected.get(rj.sender, 0) + 1
    signs = {m: sum(1 for r in log.roster_receipts if r.sender_did == m and r.status == "accepted") for m in log.members}
    last_seen: dict[str, datetime] = {}
    for p in log.posts:
        if p.sender in log.members:
            last_seen[p.sender] = p.at
    out: dict[str, WriterProfile] = {}
    for m in log.members:
        l = lat.get(m, [])
        s = sig.get(m, [])
        out[m] = WriterProfile(
            did=m,
            is_self=(m == self_did),
            is_lead=(m == log.lead),
            consent=ConsentState.FROZEN if log.roster_ready_at else ConsentState.NONE,
            games_joined=1,
            poems_completed=1 if log.complete else 0,
            words_accepted=contrib.get(m, 0),
            words_rejected=rejected.get(m, 0),
            signs=signs.get(m, 0),
            published_entry_count=1 if (log.complete and log.final_contributor == m) else 0,
            word_latency_median_ms=statistics.median(l) * 1000.0 if l else None,
            sign_latency_median_ms=statistics.median(s) * 1000.0 if s else None,
            last_activity_at=last_seen.get(m),
        )
    return out


# ---------------------------------------------------------------- game KPIs
def cover_events(log: ReplayLog) -> list[CoverEvent]:
    posts = {w.request_id: w for w in log.words}
    events: list[CoverEvent] = []
    for aw in log.accepted:
        wp = posts.get(aw.request_id)
        if wp is None:
            continue
        t = log.table_for(aw.index + 1, wp.seq)
        if t is None:
            continue
        label = t.rows[aw.index + 1]
        planned = log.resolve_label(label)
        if planned is None or planned == aw.contributor:
            continue   # unknown label: not evidence of a cover
        events.append(CoverEvent(aw.index, aw.text, label, planned, aw.contributor, t.seq, aw.accepted_at or wp.at,
                                 aw.contributor == log.lead))
    return events


def game_kpis(log: ReplayLog, *, stall_thresholds_s: tuple[int, ...] = (300, 600, 1800)) -> GameKPIs:
    gaps = accepted_gaps(log)
    # gap i corresponds to accepted index i when roster_ready is known, else i+1
    offset = 0 if log.roster_ready_at is not None else 1
    longest = max(gaps) if gaps else 0.0
    longest_idx = (gaps.index(longest) + offset) if gaps else None
    start = log.roster_ready_at
    end = log.completed_at
    minutes = (end - start).total_seconds() / 60.0 if (start and end) else None
    wph = (len(log.accepted) / (minutes / 60.0)) if minutes else None
    stale_single = sum(1 for r in log.rejections if r.reason.startswith(STALE_REASON) and not r.batch)
    stale_batch = sum(1 for r in log.rejections if r.reason.startswith(STALE_REASON) and r.batch)
    covers = cover_events(log)
    return GameKPIs(
        game_id=log.game_id, words=len(log.accepted), members=list(log.members),
        roster_ready_at=start, completed_at=end, complete=log.complete,
        minutes_to_complete=minutes, words_per_hour=wph,
        longest_gap_s=longest, longest_gap_index=longest_idx, gaps_s=gaps,
        contributions=log.contributions(),
        stale_count=stale_single + stale_batch, stale_batch_count=stale_batch,
        incomplete_consent_count=sum(1 for r in log.rejections if r.reason.startswith(INCOMPLETE_CONSENT_REASON)),
        letters_absent_count=sum(1 for r in log.rejections if r.reason.startswith(LETTERS_ABSENT_PREFIX)),
        rejections=len(log.rejections),
        cover_events=covers, cover_count=len(covers),
        table_posts=sum(1 for t in log.tables if t.kind == "table"),
        turn_script_posts=sum(1 for t in log.tables if t.kind == "turn_script"),
        note_posts=len(log.timeline),
        final_contributor=log.final_contributor,
        stalls_over_s={th: sum(1 for g in gaps if g > th) for th in stall_thresholds_s},
    )


# ---------------------------------------------------------------- writer_scores.json
def load_writer_scores(path: str | Path) -> list[WriterProfile]:
    """``writer_scores_YYYY-MM-DD.json`` rows -> WriterProfile list (mass_application_score = spam share)."""
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    out: list[WriterProfile] = []
    for r in rows:
        consent = r.get("consent")
        out.append(WriterProfile(
            did=r["did"],
            is_lead=bool(r.get("lead")),
            consent=ConsentState.SIGNED if consent else ConsentState.NONE,
            games_joined=int(r.get("poems") or 0),
            poems_completed=int(r.get("poems") or 0),
            words_accepted=int(r.get("words") or 0),
            words_rejected=int(r.get("rej") or 0),
            signs=1 if r.get("sign_med") is not None else 0,
            published_entry_count=int(r.get("final") or 0),
            word_latency_median_ms=(float(r["lat_med"]) * 1000.0) if r.get("lat_med") is not None else None,
            sign_latency_median_ms=(float(r["sign_med"]) * 1000.0) if r.get("sign_med") is not None else None,
            last_activity_at=datetime.fromisoformat(consent.replace("Z", "+00:00")) if consent else None,
            mass_application_score=float(r.get("spam") or 0.0),
        ))
    return out
