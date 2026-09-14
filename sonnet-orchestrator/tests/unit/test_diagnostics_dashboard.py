from __future__ import annotations

from rich.console import Console

from sonnet_orchestrator.diagnostics.dashboard import render, render_text
from sonnet_orchestrator.models.core import ConsentState, GameState, Role, WriterHealth

FULL = {
    "state": GameState.WRITING,
    "game_id": "nohitori-3",
    "plan": {"version": 3, "hash_prefix": "72e0b319", "next_index": 57, "owner": "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"},
    "members": [
        {"did": "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6", "role": Role.LEAD, "health": WriterHealth.HEALTHY, "keys": 26, "latency_ms": 900, "consent": ConsentState.FROZEN},
        {"did": "did:key:z6MkfGCMq51DuxSqLWzXZ71TKgGXQVaVdpn9g55qf9vthSUn", "role": "Publisher", "health": "SILENT", "keys": 22, "latency_ms": 3783.5, "consent": "FROZEN"},
    ],
    "accepted_count": 56,
    "accepted_prefix": ["My", "father", "kept", "the", "sea."],
    "next_word": {"index": 56, "text": "then", "primary": "did:key:z6MkumkZvieRKkDeq6NS4BbZhuqiNnjYFKCPNtEYVxSdDkhu", "backup": None},
    "pending_proposals": [{"request_id": "w56-abc"}],
    "landing": {"final_contributor": "did:key:z6MkfGCMq51DuxSqLWzXZ71TKgGXQVaVdpn9g55qf9vthSUn", "can_publish": True, "path": "…-f9vthSUn"},
    "approvals_pending": 2,
    "kpis": {"words_per_hour": 19.49, "minutes_elapsed": 120},
}


def _text(snapshot, width=120) -> str:
    console = Console(width=width, record=True, force_terminal=False, color_system=None, file=open("/dev/null", "w"))
    console.print(render(snapshot))
    return console.export_text()


def test_render_full_snapshot():
    out = _text(FULL)
    assert "WRITING" in out and "nohitori-3" in out
    assert "plan v3 72e0b319" in out and "next=57" in out
    assert "W4TAejK6" in out and "f9vthSUn" in out and "SILENT" in out
    assert "index 56" in out and "then" in out and "VxSdDkhu" in out
    assert "pending proposals" in out and "1" in out
    assert "approvals pending" in out and "2" in out
    assert "words_per_hour" in out and "19.49" in out
    assert "can_publish=True" in out


def test_render_tolerates_missing_keys():
    for snap in ({}, None, {"state": "DISCOVER"}, {"members": None, "plan": None, "next_word": None},
                 {"members": [{"did": None}], "pending_proposals": None, "landing": "n/a", "kpis": None}):
        out = _text(snap)
        assert "members" in out and "next word" in out and "status" in out


def test_render_text_helper():
    out = render_text(FULL, width=100)
    assert "WRITING" in out
    assert render_text({}, width=60)
