"""Per-writer metrics and game KPIs from the real exports; benchmarks 94 min and 403 min."""
from __future__ import annotations

import pytest

from sonnet_orchestrator.config import PACKAGE_ROOT
from sonnet_orchestrator.diagnostics.metrics import (
    accepted_gaps, cover_events, game_kpis, load_writer_scores, sign_latencies, word_latencies, writer_metrics,
)
from sonnet_orchestrator.diagnostics.replay import parse_export
from sonnet_orchestrator.models.core import WriterProfile

FIX = PACKAGE_ROOT / "data" / "fixtures"


@pytest.fixture(scope="module")
def log1():
    return parse_export(FIX / "nohitori" / "team_room_export.ndjson")


@pytest.fixture(scope="module")
def log2():
    return parse_export(FIX / "nohitori-2" / "team_room_export.ndjson")


def test_entry1_benchmark(log1, settings):
    k = game_kpis(log1)
    assert k.words == 125
    assert round(k.minutes_to_complete) == 94
    assert 75 < k.words_per_hour < 85
    assert k.stale_count == 4 and k.stale_batch_count == 0
    assert k.incomplete_consent_count == 0
    assert k.longest_gap_index == 14              # word 15 'the'/'a' stall (case 8, item 2)
    assert 1100 < k.longest_gap_s < 1200
    assert k.stalls_over_s[300] == 3
    assert k.table_posts >= 5 and k.turn_script_posts == 4
    assert k.final_contributor.endswith("MWV4RmAQ")


def test_entry2_benchmark(log2):
    k = game_kpis(log2)
    assert k.words == 131
    assert round(k.minutes_to_complete) == 403
    assert k.roster_ready_at.isoformat().startswith("2026-09-14T03:49:57")
    assert k.completed_at.isoformat().startswith("2026-09-14T10:33:08")
    assert 19 < k.words_per_hour < 20
    assert k.stale_count == 41 and k.stale_batch_count == 21
    assert k.incomplete_consent_count == 1
    assert k.letters_absent_count == 2           # F6jvabi2 posted 'and' twice (no 'n')
    assert k.longest_gap_index == 50             # word 51: 'and' -> 'but' rewrite, 2 h stall
    assert 7200 < k.longest_gap_s < 7400
    assert k.stalls_over_s[1800] == 3
    assert k.table_posts == 4                    # v2, v3, v4, v5
    assert k.contributions[next(m for m in k.members if m.endswith("VxSdDkhu"))] == 43


def test_writer_metrics_entry2(log2):
    prof = writer_metrics(log2)
    assert set(prof) == set(log2.members)
    by = {m[-8:]: p for m, p in prof.items()}
    assert all(isinstance(p, WriterProfile) for p in prof.values())
    assert by["W4TAejK6"].is_lead and by["W4TAejK6"].is_self
    assert by["VxSdDkhu"].words_accepted == 43 and by["VxSdDkhu"].words_rejected == 13
    assert by["F6jvabi2"].words_accepted == 19 and by["F6jvabi2"].words_rejected == 16
    assert by["f9vthSUn"].published_entry_count == 1 and by["W4TAejK6"].published_entry_count == 0
    # word latency medians (seconds): lead/Jingdu/weather-prophet a few seconds, KIMI over a minute
    assert by["W4TAejK6"].word_latency_median_ms < 5000
    assert by["VxSdDkhu"].word_latency_median_ms < 5000
    assert by["F6jvabi2"].word_latency_median_ms > 60000
    # sign latency: measured from the lead's roster receipt (03:54:10Z)
    assert by["VxSdDkhu"].sign_latency_median_ms < 2000
    assert 90000 < by["f9vthSUn"].sign_latency_median_ms < 100000
    assert by["F6jvabi2"].sign_latency_median_ms is None
    assert all(p.letters for p in prof.values())
    assert by["W4TAejK6"].missing_letters == ""
    assert by["VxSdDkhu"].missing_letters == "aglow"


def test_word_latency_definition_matches_writer_scores(log1):
    lat = word_latencies(log1)
    # 125 accepted words, the first has no predecessor -> 124 latencies in total
    assert sum(len(v) for v in lat.values()) == 124
    gaps = accepted_gaps(log1)
    assert len(gaps) == 125          # roster_ready -> word 0 included
    assert all(g >= 0 for g in gaps)
    assert sign_latencies(log1) == {}   # entry 1 export has no lead roster receipt


def test_cover_events(log1, log2):
    ev2 = cover_events(log2)
    assert len(ev2) == 27
    lead_covers = [e for e in ev2 if e.by_lead]
    assert any(e.index == 95 and e.word == "dead" for e in lead_covers)   # lead took 96 (1-based) -> 'beg' trap
    ev1 = cover_events(log1)
    assert any(e.index == 57 and e.word == "more." and e.by_lead for e in ev1)   # lead took 58 -> 59 'The' trap
    assert all(e.planned_did is not None for e in ev1 + ev2)


def test_load_writer_scores():
    rows = load_writer_scores(FIX / "writer_scores_2026-09-13.json")
    assert len(rows) == 196
    by = {p.did[-8:]: p for p in rows}
    p = by["MWV4RmAQ"]
    assert p.words_accepted == 118 and p.words_rejected == 3 and p.published_entry_count == 2
    assert p.word_latency_median_ms == 16000.0 and p.sign_latency_median_ms == 131000.0
    assert p.mass_application_score == 0.22 and not p.is_lead
    assert by["W4TAejK6"].is_lead
    assert by["3sLzg7ws"].mass_application_score == 0.91
    assert by["3sLzg7ws"].words_accepted == 2
    spam = sorted(rows, key=lambda r: -r.mass_application_score)[0]
    assert spam.mass_application_score >= 0.9
