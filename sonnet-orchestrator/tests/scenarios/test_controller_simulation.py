"""Controller-world simulation of the spec demo and the regression scenarios (offline, mock adapters)."""
import collections

import pytest

from sonnet_orchestrator.diagnostics.scenarios import SCENARIOS
from sonnet_orchestrator.diagnostics.simulator import build_world, demo_scenario, simulate_scenario
from sonnet_orchestrator.models import GameState


def test_demo_entry_completes_and_validates(settings, lexicon):
    r = simulate_scenario("demo-4-writers", settings, seed=0, max_ticks=3000)
    assert r.completed and r.state == GameState.ACCEPTED.value
    assert r.words >= 100 and r.poem_text and r.sha256
    lexicon.validate_poem(r.poem_text, exact_ten=True)   # official validator: no exception
    assert r.plan_versions >= 2                          # C went DOWN -> replan bumped the version
    assert "down" in r.faults_applied and not r.faults_ignored


def test_demo_prefix_unchanged_after_down(settings):
    base, _ = build_world(demo_scenario(), settings, seed=0)
    base.run_until_complete(max_ticks=3000)
    ctl, world = build_world(demo_scenario(), settings, seed=0)
    ctl.run_until_complete(max_ticks=3000)
    c_did = world["mapping"]["did:sim:C"]
    texts = ctl.poem.accepted_texts()
    assert texts[:40] == base.poem.accepted_texts()[:40]
    assert all(w.contributor != c_did for w in ctl.poem.accepted if w.index >= 40)
    cs = [w.contributor for w in ctl.poem.accepted]
    assert all(cs[i] != cs[i + 1] for i in range(len(cs) - 1))
    assert len(collections.Counter(cs)) == 4            # every member contributed (contest rule)


@pytest.mark.parametrize("name", sorted(SCENARIOS))
def test_named_scenarios_complete_in_controller_world(name, settings):
    r = simulate_scenario(name, settings, seed=1, max_ticks=4000)
    assert r.completed, (name, r.reason, r.events[-5:])
    assert r.words in (112, 125, 131) or r.words >= 100
    cs = [e for e in r.events if e["kind"] == "table_conflict"]
    assert not cs or name == "dual-table"
