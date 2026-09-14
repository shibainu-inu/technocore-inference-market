"""Controller-based simulator: a Scenario → mock world (FakeClock, MockReferee, ScriptedWriters) → Controller ticks.

This is the "real" offline loop behind `sonnet-orchestrator simulate entry` and the Controller-level Monte Carlo.
`montecarlo.simple_simulate` is the fast analytical model; this one exercises every orchestration module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..adapters.mock import (FakeClock, MockDiscovery, MockPublication, MockReferee, MockTeamRoom, ScriptedWriters,
                             WriterScript, synthetic_did)
from ..db import Store
from ..models import GameState, WriterProfile, canonical_text, poem_sha256, did_letters
from ..orchestration import Controller
from .scenarios import SCENARIOS, Scenario, ScenarioWriter, build

SELF_DID = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
ALL = "abcdefghijklmnopqrstuvwxyz"
DEMO = "demo-4-writers"

# Faults the Controller world can inject directly; the rest are consent/recruitment-layer faults that the
# analytical model covers (montecarlo.simple_simulate) and unit tests exercise module by module.
CONTROLLER_FAULTS = {"down", "race", "delayed_receipt", "stale_storm", "cover_trap", "pre_roster_403", "long_table",
                     "landing", "parity_trap", "hybrid_plan"}


@dataclass
class ControllerSimResult:
    scenario: str
    completed: bool
    minutes: float
    words: int
    reason: str
    state: str
    snapshot: dict
    poem_text: str = ""
    sha256: str = ""
    plan_versions: int = 0
    covers: int = 0
    stale: int = 0
    replans: int = 0
    faults_applied: list[str] = field(default_factory=list)
    faults_ignored: list[str] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)


def demo_scenario() -> Scenario:
    """Spec demo fixture: 4 writers A–D, C goes DOWN mid-poem; accepted prefix must stay unchanged."""
    return Scenario(
        name=DEMO,
        description="4 writers A-D with the heuristic planner; C goes DOWN at word 40; prefix unchanged, poem completes",
        writers=[
            ScenarioWriter(did=SELF_DID, profile="healthy", is_lead=True, latency_ms=2000, x_account="https://x.com/0xnohitori", handle="A"),
            ScenarioWriter(did="did:sim:B", letters="abcdefghilmnoprstuvwy", profile="healthy", latency_ms=15000, handle="B"),
            ScenarioWriter(did="did:sim:C", letters="abcdefghiklmnoprstuwy", profile="healthy", latency_ms=20000, handle="C"),
            ScenarioWriter(did="did:sim:D", letters="abdefghilmnoprstuvwy", profile="healthy", latency_ms=25000,
                           x_account="https://x.com/d", handle="D"),
        ],
        faults=[{"kind": "down", "at_index": 40, "params": {"did": "did:sim:C"}}],  # type: ignore[list-item]
        expectations={"completion_rate_min": 1.0, "controller": {"prefix_unchanged": True, "plan_version_bumped": True}},
        tags=["demo"],
    )


def _fault(f):
    if isinstance(f, dict):
        return f.get("kind"), f.get("at_index"), f.get("at_tick"), f.get("params") or {}
    return f.kind, f.at_index, f.at_tick, f.params or {}


def resolve_scenario(name_or_scenario) -> Scenario:
    if isinstance(name_or_scenario, Scenario):
        return name_or_scenario
    if name_or_scenario == DEMO:
        return demo_scenario()
    if name_or_scenario in SCENARIOS:
        return build(name_or_scenario)
    raise KeyError(f"unknown scenario {name_or_scenario!r}; try `simulate list`")


def _real_did(w: ScenarioWriter, mapping: dict[str, str]) -> str:
    if w.did in mapping:
        return mapping[w.did]
    if w.did.startswith("did:key:"):
        mapping[w.did] = w.did
    else:
        letters = w.letters or ALL
        mapping[w.did] = synthetic_did(letters, salt=w.did)
    return mapping[w.did]


def build_world(scenario: Scenario, settings, *, seed: int = 0, tick_seconds: Optional[int] = None):
    """Construct the mock world for a scenario. Returns (controller, world dict)."""
    from ..creative.heuristic import HeuristicCreativeEngine
    from ..lexicon import load_lexicon

    settings = settings.model_copy(deep=True)
    if tick_seconds:
        settings.scheduler.tick_seconds = tick_seconds
    lexicon = load_lexicon(str(settings.cmudict_path))
    mapping: dict[str, str] = {}
    writers = list(scenario.writers)
    lead = next((w for w in writers if w.is_lead), None)
    if lead is None:
        lead = ScenarioWriter(did=SELF_DID, profile="healthy", is_lead=True, latency_ms=2000, x_account="https://x.com/0xnohitori")
        writers.insert(0, lead)
    self_did = _real_did(lead, mapping)
    members = [_real_did(w, mapping) for w in writers if w is not lead and w.profile != "mass_applicant"]

    clock = FakeClock(step_seconds=5.0)
    referee_kwargs: dict = {"seed": seed}
    delayed: dict[str, float] = {}
    applied, ignored = [], []
    scripts: dict[str, WriterScript] = {}
    for w in writers:
        if w is lead:
            continue
        if w.profile == "mass_applicant" or w.did not in mapping:
            continue          # never seated: recruitment-layer scenario (consent filters are unit-tested)
        did = mapping[w.did]
        latency_s = max(1.0, (w.latency_ms or 15000.0) / 1000.0)
        profile = w.profile
        kw: dict = {}
        if profile == "slow":
            profile = "healthy"; latency_s = max(latency_s, settings.health.minimum_timeout_ms / 1000.0 * settings.health.slow_multiplier + 1)
        elif profile == "down_after":
            profile = "down_after_index"; kw["down_after_index"] = w.down_after if w.down_after is not None else 40
        elif profile == "mass_applicant":
            continue
        elif profile not in ("healthy", "silent", "never_signs", "down_after_index"):
            profile = "healthy"
        scripts[did] = WriterScript(did=did, profile=profile, latency_s=latency_s, **kw)
    for f in scenario.faults:
        kind, at_index, at_tick, params = _fault(f)
        if kind == "down" and params.get("did") in mapping:
            did = mapping[params["did"]]
            if did in scripts:
                scripts[did].profile = "down_after_index"; scripts[did].down_after_index = at_index or 0
            applied.append(kind)
        elif kind == "race" and at_index is not None and scripts:
            did = sorted(scripts)[(at_index or 0) % len(scripts)]
            scripts[did].race_index = at_index; applied.append(kind)
        elif kind == "delayed_receipt":
            for did in scripts:
                delayed[did] = float(params.get("delay_s", 600))
            applied.append(kind)
        elif kind in ("stale_storm",) and scripts:
            for did in scripts:
                scripts[did].race_index = at_index
            applied.append(kind)
        elif kind in CONTROLLER_FAULTS:
            applied.append(kind)      # exercised by the world itself (403, chunking, landing, planner)
        else:
            ignored.append(kind)
    if delayed:
        referee_kwargs["delayed_receipt"] = delayed
    referee = MockReferee(lexicon, clock, **referee_kwargs)
    discovery = MockDiscovery(clock, self_did)
    room = MockTeamRoom(clock, self_did, referee=referee, char_limit=settings.room.post_char_limit)
    publishers = {self_did} | {mapping[w.did] for w in writers if w.x_account and w.did in mapping}
    publication = MockPublication(clock, publishers=publishers)
    store = Store(":memory:")
    for w in writers:
        if w.did not in mapping:
            continue
        store.upsert_writer(WriterProfile(did=mapping[w.did], handle=w.handle or w.did[-8:], x_account=w.x_account,
                                          is_self=(w is lead), is_lead=(w is lead),
                                          word_latency_median_ms=w.latency_ms))
    engine = HeuristicCreativeEngine(lexicon, seed=seed)
    planner_fn = None
    fixed = None
    if scenario.words:
        from ..orchestration.table import lines_from_words
        try:
            fixed = lines_from_words(list(scenario.words), lexicon)
            if len(fixed) != 14:
                raise ValueError("not a full poem")
        except ValueError:
            fixed = None
            ignored.append("fixed_words(not a 14-line poem; heuristic planner used)")
    if fixed:

        def planner_fn(prefix, ws, s, _fixed=fixed):
            """Historical text while it stays feasible for the available writers; otherwise regenerate the suffix
            (accepted prefix verbatim) with the heuristic engine — roster freeze is not text freeze."""
            from ..planner.beam import plan_poem
            from ..planner.validator import words_of_poem
            from ..solver.feasibility import check
            words = [t for l in _fixed for t in l.split()]
            if list(prefix) == words[:len(prefix)]:
                entries = words_of_poem(_fixed, lexicon)
                lead = next((w.did for w in ws if w.is_self or w.is_lead), ws[0].did if ws else None)
                last = None
                if check(entries, ws, lead_did=lead, start_index=len(prefix), last_contributor=last).feasible:
                    return list(_fixed)
            plan = plan_poem(engine, lexicon, ws, s, accepted_prefix=list(prefix), seed=seed)
            return list(plan.lines)
    ctl = Controller(settings, store, lexicon, referee, discovery, room, publication, engine=engine, clock=clock,
                     self_did=self_did, game_id=scenario.name, planner_fn=planner_fn,
                     members=members, poem_room=f"d-sim-team-{scenario.name}", seed=seed)
    sw = ScriptedWriters(referee, room, publication, clock, lexicon, settings, scenario.name, self_did,
                         list(scripts.values())).attach()
    world = dict(settings=settings, lexicon=lexicon, clock=clock, referee=referee, discovery=discovery, room=room,
                 publication=publication, store=store, writers=sw, mapping=mapping, faults_applied=applied,
                 faults_ignored=ignored, members=members, self_did=self_did)
    return ctl, world


def dashboard_snapshot(ctl: Controller) -> dict:
    """Adapt Controller.snapshot() to the dashboard's expected keys."""
    s = ctl.snapshot()
    plan = s.get("plan") or {}
    return {
        "game_id": s.get("game_id"), "state": s.get("state"), "tick": s.get("tick"), "now": s.get("now"),
        "plan": {"version": plan.get("version"), "hash_prefix": plan.get("hash"), "next_index": s.get("next_index"),
                 "owner": s.get("self_did"), "source": plan.get("source")} if plan else None,
        "members": [{"did": m.get("did"), "role": "Lead" if m.get("did") == s.get("self_did") else "Author",
                     "health": m.get("health"), "keys": m.get("keys"), "latency_ms": m.get("latency_ms"),
                     "consent": m.get("consent"), "words": m.get("words")} for m in s.get("members", [])],
        "accepted_count": len(s.get("accepted", [])),
        "next_word": {"index": s.get("next_index"), "text": s.get("next_word"), "primary": s.get("primary"), "backup": s.get("backup")},
        "pending_proposals": s.get("pending_proposals", []),
        "landing": s.get("landing_route"),
        "approvals_pending": s.get("operator_pending", []),
        "final_sha256": s.get("final_sha256"),
        "kpis": s.get("kpis", {}),
    }


def simulate_scenario(name_or_scenario, settings, *, seed: int = 0, max_ticks: int = 5000,
                      tick_seconds: Optional[int] = None) -> ControllerSimResult:
    scenario = resolve_scenario(name_or_scenario)
    ctl, world = build_world(scenario, settings, seed=seed, tick_seconds=tick_seconds)
    clock = world["clock"]
    t0 = clock.now()
    final = ctl.run_until_complete(max_ticks=max_ticks)
    minutes = (clock.now() - t0).total_seconds() / 60.0
    completed = final in (GameState.SUBMITTED, GameState.ACCEPTED) or bool(ctl.final_lines)
    kinds = [e["kind"] for e in ctl.events]
    reason = "ok" if completed else (f"stopped in {final.value}: " + (ctl.events[-1]["detail"] if ctl.events else ""))
    text = canonical_text(ctl.final_lines) if ctl.final_lines else ""
    return ControllerSimResult(
        scenario=scenario.name, completed=completed, minutes=minutes, words=len(ctl.poem.accepted), reason=reason,
        state=final.value, snapshot=dashboard_snapshot(ctl), poem_text=text,
        sha256=poem_sha256(ctl.final_lines) if ctl.final_lines else "",
        plan_versions=ctl.plan.version if ctl.plan else 0,
        covers=sum(1 for k in kinds if k == "cover"), stale=sum(1 for k in kinds if "stale" in k),
        replans=sum(1 for k in kinds if k == "replan"),
        faults_applied=world["faults_applied"], faults_ignored=world["faults_ignored"], events=ctl.events)


def controller_simulate_fn(settings, *, max_ticks: int = 5000):
    """Adapter for montecarlo.run: simulate_fn(scenario, seed) -> SimResult."""
    from .montecarlo import SimResult

    def fn(scenario, seed):
        r = simulate_scenario(scenario, settings, seed=seed, max_ticks=max_ticks)
        return SimResult(completed=r.completed, minutes=r.minutes, reason=r.reason, stale=r.stale, covers=r.covers,
                         replans=r.replans, reposts=r.plan_versions)
    return fn
