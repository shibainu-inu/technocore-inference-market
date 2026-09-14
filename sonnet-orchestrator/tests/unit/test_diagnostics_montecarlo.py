"""Monte Carlo runner + analytical fallback simulator: determinism, speed, injected simulator, trap semantics."""
from __future__ import annotations

import time
from collections import Counter
from dataclasses import replace
from functools import partial

from sonnet_orchestrator.diagnostics.montecarlo import (
    MonteCarloReport, SimResult, check_expectations, remove_writer, run, simple_simulate,
)
from sonnet_orchestrator.diagnostics.scenarios import Fault, Scenario, ScenarioWriter, build


def _tiny(**sim) -> Scenario:
    return Scenario(
        name="tiny", description="",
        writers=[ScenarioWriter("did:sim:L", letters="abcdefghijklmnopqrstuvwxyz", is_lead=True, latency_ms=1000),
                 ScenarioWriter("did:sim:P", letters="abcdefghijklmnpqrstuvwxyz", latency_ms=5000, x_account="x")],
        words=["I", "sit", "in", "my", "hat", "at", "sea", "near", "the", "kiss"],   # no lead-only letters
        sim=sim,
    )


def test_injected_simulator_and_report_shape():
    calls = []

    def fake(scenario, seed):
        calls.append(seed)
        return SimResult(completed=seed % 4 != 0, minutes=float(seed % 100), reason="" if seed % 4 else "boom")

    rep = run(_tiny(), 40, 1, fake, survivability=False)
    assert isinstance(rep, MonteCarloReport)
    assert rep.trials == 40 and len(calls) == 40 and len(set(calls)) == 40
    assert 0 < rep.completion_rate < 1
    assert rep.failure_reasons == Counter({"boom": sum(1 for s in calls if s % 4 == 0)})
    assert rep.median_minutes is not None and rep.p90_minutes is not None and rep.p90_minutes >= rep.median_minutes
    assert rep.single_failure_survivability is None
    d = rep.as_dict()
    assert d["scenario"] == "tiny" and d["failure_reasons"] == {"boom": rep.failure_reasons["boom"]}


def test_deterministic_given_seed():
    sc = build("case-A-writer-down-mid-poem")
    a = run(sc, 100, 42, simple_simulate)
    b = run(sc, 100, 42, simple_simulate)
    assert a.as_dict() == b.as_dict()
    c = run(sc, 100, 43, simple_simulate)
    assert c.as_dict() != a.as_dict()


def test_speed_1000_trials_under_5s():
    sc = build("nohitori-entry2-6h43m")
    t = time.time()
    rep = run(sc, 1000, 7, simple_simulate)
    assert time.time() - t < 5.0
    assert rep.trials == 1000 and rep.completion_rate > 0.9


def test_settings_injection(settings):
    sc = build("frame-churn")
    fn = partial(simple_simulate, settings=settings)
    rep = run(sc, 50, 3, fn, survivability=False)
    assert rep.completion_rate > 0.9


def test_parity_trap_dead_ends_without_replan():
    sc = build("case-E-lead-only-letter-parity-trap")
    dead = run(replace(sc, sim={**sc.sim, "replan": False}), 200, 5, simple_simulate, survivability=False)
    assert dead.completion_rate == 0.0
    assert dead.failure_reasons.most_common(1)[0][0] == "dead_end@6"
    ok = run(sc, 200, 5, simple_simulate, survivability=False)
    assert ok.completion_rate >= 0.9 and ok.mean_replans >= 1.0


def test_cover_traps_reproduced_with_lookahead_zero():
    for name, idx in (("58-59-cover-trap", 58), ("96-97-beg-trap", 96)):
        sc = build(name)
        trap = run(replace(sc, sim={**sc.sim, "lookahead": 0, "replan": False}), 200, 11, simple_simulate, survivability=False)
        safe = run(replace(sc, sim={**sc.sim, "lookahead": 1, "replan": False}), 200, 11, simple_simulate, survivability=False)
        assert trap.completion_rate < safe.completion_rate, name
        assert f"dead_end@{idx}" in trap.failure_reasons, (name, trap.failure_reasons)
        assert trap.failure_reasons[f"dead_end@{idx}"] > safe.failure_reasons.get(f"dead_end@{idx}", 0)


def test_landing_plan_matters_for_single_publisher():
    sc = build("case-F-final-word-single-publisher")
    with_plan = run(sc, 200, 9, simple_simulate, survivability=False)
    without = run(replace(sc, sim={**sc.sim, "landing_plan": False}), 200, 9, simple_simulate, survivability=False)
    assert with_plan.completion_rate == 1.0
    assert without.completion_rate < with_plan.completion_rate
    assert any("landing" in r for r in without.failure_reasons)


def test_single_failure_survivability_and_remove_writer():
    sc = build("case-A-writer-down-mid-poem")
    rep = run(sc, 100, 2, simple_simulate, survivability_trials=40)
    assert rep.single_failure_survivability == 1.0
    assert set(rep.survivability_by_writer) == {w.did for w in sc.writers if not w.is_lead}
    v = remove_writer(sc, "did:sim:B")
    assert next(w for w in v.writers if w.did == "did:sim:B").profile == "down_after"
    assert v.name.endswith("~did:sim:B"[-8:])
    # never_signs without replacement fails the roster
    ns = replace(_tiny(replace_non_signer=False), writers=[_tiny().writers[0], replace(_tiny().writers[1], profile="never_signs")])
    r = simple_simulate(ns, 1)
    assert not r.completed and r.reason == "roster: incomplete consent"


def test_faults_add_time_and_stale():
    base = run(_tiny(), 100, 1, simple_simulate, survivability=False)
    delayed = replace(_tiny(), faults=[Fault("delayed_receipt", at_index=2, params={"delay_s": 600})])
    d = run(delayed, 100, 1, simple_simulate, survivability=False)
    assert d.median_minutes >= base.median_minutes + 9.9
    storm = replace(_tiny(), faults=[Fault("stale_storm", at_index=1, params={"count": 5})])
    s = run(storm, 100, 1, simple_simulate, survivability=False)
    assert s.mean_stale >= base.mean_stale + 5
    refused = replace(_tiny(no_plan_fail_prob=1.0), faults=[Fault("long_table", at_tick=0, params={"chars": 2500, "chunked": False})])
    r = run(refused, 20, 1, simple_simulate, survivability=False)
    assert r.completion_rate == 0.0 and "table refused: post over char limit" in r.failure_reasons
    chunked = replace(refused, faults=[Fault("long_table", at_tick=0, params={"chars": 2500, "chunked": True})])
    assert run(chunked, 20, 1, simple_simulate, survivability=False).completion_rate == 1.0


def test_check_expectations():
    rep = MonteCarloReport("x", 10, 0.5, 30.0, 40.0, Counter({"dead_end@3": 5}), 0.5, {}, 1.0, 0.0, 0.0)
    assert check_expectations(rep, {}) == []
    bad = check_expectations(rep, {"completion_rate_min": 0.9, "median_minutes_max": 20, "failure_reasons_exclude": ["dead_end"],
                                   "failure_reasons_include": ["stall"], "mean_stale_min": 2, "p90_minutes_max": 39,
                                   "single_failure_survivability_min": 0.9, "controller": {"ignored": True}})
    assert len(bad) == 7
    assert check_expectations(rep, {"completion_rate_min": 0.5, "failure_reasons_include": ["dead_end"]}) == []
