"""Rich dashboard for a Controller ``snapshot()`` dict. Tolerant of missing keys.

Snapshot keys (all optional): state, game_id, plan {version, hash_prefix, next_index, owner},
members [{did, role, health, keys, latency_ms, consent}], accepted_count, accepted_prefix (str or list),
next_word {index, text, primary, backup}, pending_proposals (int or list), landing (dict or str),
approvals_pending (int or list), kpis (dict).
"""
from __future__ import annotations

from typing import Any, Optional

from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

HEALTH_STYLE = {"HEALTHY": "green", "SLOW": "yellow", "SUSPECT": "dark_orange", "DOWN": "red", "SILENT": "magenta"}


def _short(did: Any, n: int = 8) -> str:
    s = str(did or "-")
    return s[-n:] if s.startswith("did:") else s


def _get(d: Any, key: str, default: Any = None) -> Any:
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default) if d is not None else default


def _fmt_ms(ms: Any) -> str:
    try:
        v = float(ms)
    except (TypeError, ValueError):
        return "-"
    return f"{v / 1000:.1f}s" if v >= 1000 else f"{v:.0f}ms"


def _count(x: Any) -> str:
    if x is None:
        return "0"
    if isinstance(x, (list, tuple, set, dict)):
        return str(len(x))
    return str(x)


def header(snapshot: dict) -> Text:
    state = _get(snapshot, "state", "?")
    state = getattr(state, "value", state)
    plan = _get(snapshot, "plan") or {}
    txt = Text()
    txt.append(f" {state} ", style="bold reverse")
    txt.append(f"  game={_get(snapshot, 'game_id', '-')}")
    txt.append(f"  plan v{_get(plan, 'version', '-')} {_get(plan, 'hash_prefix', '-')}")
    txt.append(f"  next={_get(plan, 'next_index', _get(snapshot, 'accepted_count', '-'))}")
    txt.append(f"  owner={_short(_get(plan, 'owner'))}")
    txt.append(f"  accepted={_get(snapshot, 'accepted_count', '-')}")
    return txt


def members_table(members: Optional[list]) -> Table:
    t = Table(title="members", expand=True, show_edge=False, pad_edge=False)
    for col in ("did", "role", "health", "keys", "latency", "consent"):
        t.add_column(col)
    for m in members or []:
        health = _get(m, "health", "-")
        health = getattr(health, "value", health)
        consent = _get(m, "consent", "-")
        consent = getattr(consent, "value", consent)
        role = _get(m, "role", "-")
        role = getattr(role, "value", role)
        t.add_row(_short(_get(m, "did")), str(role), Text(str(health), style=HEALTH_STYLE.get(str(health), "")),
                  str(_get(m, "keys", "-")), _fmt_ms(_get(m, "latency_ms")), str(consent))
    if not members:
        t.add_row("-", "-", "-", "-", "-", "-")
    return t


def next_word_panel(snapshot: dict) -> Panel:
    nw = _get(snapshot, "next_word") or {}
    prefix = _get(snapshot, "accepted_prefix")
    if isinstance(prefix, (list, tuple)):
        prefix = " ".join(str(w) for w in prefix)
    body = Text()
    body.append(f"index {_get(nw, 'index', '-')}: ", style="bold")
    body.append(f"{_get(nw, 'text', '-')}  ")
    body.append(f"primary={_short(_get(nw, 'primary'))} backup={_short(_get(nw, 'backup'))}\n")
    if prefix:
        tail = str(prefix)
        if len(tail) > 160:
            tail = "…" + tail[-159:]
        body.append(f"prefix: {tail}", style="dim")
    return Panel(body, title="next word", expand=True)


def status_table(snapshot: dict) -> Table:
    t = Table(show_header=False, show_edge=False, pad_edge=False, expand=True)
    t.add_column("k", style="bold")
    t.add_column("v")
    t.add_row("pending proposals", _count(_get(snapshot, "pending_proposals")))
    landing = _get(snapshot, "landing")
    if isinstance(landing, dict):
        landing = f"final={_short(landing.get('final_contributor'))} can_publish={landing.get('can_publish', '-')} path={landing.get('path', '-')}"
    t.add_row("landing", str(landing if landing is not None else "-"))
    t.add_row("approvals pending", _count(_get(snapshot, "approvals_pending")))
    kpis = _get(snapshot, "kpis") or {}
    if isinstance(kpis, dict):
        for k, v in kpis.items():
            t.add_row(f"kpi {k}", f"{v:.2f}" if isinstance(v, float) else str(v))
    return t


def render(snapshot: dict) -> RenderableType:
    """Full dashboard renderable (Group of header, members, next word, status)."""
    snapshot = snapshot or {}
    return Group(
        header(snapshot),
        members_table(_get(snapshot, "members")),
        next_word_panel(snapshot),
        Panel(status_table(snapshot), title="status", expand=True),
    )


def render_text(snapshot: dict, width: int = 100) -> str:
    """Plain-text rendering (for logs and tests)."""
    import io
    from rich.console import Console
    buf = io.StringIO()
    console = Console(width=width, file=buf, force_terminal=False, color_system=None)
    console.print(render(snapshot))
    return buf.getvalue()


def demo_snapshot() -> dict:
    """A static snapshot for `sonnet-orchestrator dashboard` without a database."""
    return {
        "game_id": "demo", "state": "WRITING", "tick": 42,
        "plan": {"version": 3, "hash_prefix": "72e0b319", "next_index": 57, "owner": "did:key:z6Mk...W4TAejK6", "source": "solver"},
        "members": [
            {"did": "did:key:z6Mk...W4TAejK6", "role": "Lead", "health": "HEALTHY", "keys": 131, "latency_ms": 2000, "consent": "FROZEN", "words": 20},
            {"did": "did:key:z6Mk...f9vthSUn", "role": "Author", "health": "SLOW", "keys": 90, "latency_ms": 96000, "consent": "FROZEN", "words": 14},
            {"did": "did:key:z6Mk...F6jvabi2", "role": "Author", "health": "SILENT", "keys": 40, "latency_ms": None, "consent": "FROZEN", "words": 9},
            {"did": "did:key:z6Mk...VxSdDkhu", "role": "Publisher", "health": "HEALTHY", "keys": 88, "latency_ms": 500, "consent": "FROZEN", "words": 14},
        ],
        "accepted_count": 57, "next_word": {"index": 57, "text": "then", "primary": "did:key:z6Mk...f9vthSUn", "backup": "did:key:z6Mk...VxSdDkhu"},
        "pending_proposals": [], "landing": {"final_contributor": "did:key:z6Mk...f9vthSUn"}, "approvals_pending": [],
        "kpis": {"words_per_hour": 19.5, "single_failure_survivability": 0.75},
    }
