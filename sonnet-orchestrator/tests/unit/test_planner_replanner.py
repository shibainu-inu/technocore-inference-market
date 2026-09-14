import pytest

from sonnet_orchestrator.creative.heuristic import HeuristicCreativeEngine
from sonnet_orchestrator.models.core import AcceptedWord, PoemState
from sonnet_orchestrator.planner.beam import plan_poem
from sonnet_orchestrator.planner.replanner import first_infeasible_index, reconcile, replan
from sonnet_orchestrator.planner.validator import validate_poem_lines
from tests.unit.test_planner_beam import OURS, four_writers


@pytest.fixture(scope="module")
def engine(lexicon):
    return HeuristicCreativeEngine(lexicon, seed=1)


@pytest.fixture(scope="module")
def base_plan(engine, lexicon, settings):
    return plan_poem(engine, lexicon, four_writers(), settings, seed=3, game_id="g")


def _poem(plan, n, replace: dict[int, str] | None = None) -> PoemState:
    replace = replace or {}
    writers = four_writers()
    acc = [AcceptedWord(index=i, text=replace.get(i, plan.words[i].text), contributor=writers[i % 2].did, version=i + 1)
           for i in range(n)]
    return PoemState(game_id=plan.game_id, accepted=acc, version=n)


def test_reconcile_matching_prefix(base_plan):
    rec = reconcile(base_plan, _poem(base_plan, 12))
    assert rec.prefix_matches and rec.divergence_index is None and not rec.hybrid
    assert rec.accepted_len == 12 and rec.plan_len == len(base_plan.words)


def test_reconcile_detects_divergence_at_word_9(base_plan):
    poem = _poem(base_plan, 10, {9: "sun,"})
    assert poem.accepted[9].text != base_plan.words[9].text
    rec = reconcile(base_plan, poem)
    assert not rec.prefix_matches and rec.divergence_index == 9 and rec.hybrid


def test_replan_keeps_accepted_words_and_bumps_version(engine, lexicon, settings, base_plan):
    poem = _poem(base_plan, 10, {9: "sun,"})
    new = replan(base_plan, poem, four_writers(), engine=engine, lexicon=lexicon, settings=settings)
    assert new.version == base_plan.version + 1
    assert new.source == "solver" and new.game_id == base_plan.game_id and new.owner == OURS
    assert [w.text for w in new.words[:10]] == poem.accepted_texts()
    assert [w.text for w in new.words[:9]] == [w.text for w in base_plan.words[:9]]
    assert new.words[9].text == "sun,"
    assert new.accepted_prefix_len == 10
    rep = validate_poem_lines(new.lines, lexicon)
    assert rep.strict_ok, (rep.errors, rep.rhyme_pairs_ok, rep.clashes)
    assert reconcile(new, poem).prefix_matches
    assert new.text != base_plan.text


def test_replan_with_matching_prefix_keeps_the_plan_text(engine, lexicon, settings, base_plan):
    poem = _poem(base_plan, 12)
    new = replan(base_plan, poem, four_writers(), engine=engine, lexicon=lexicon, settings=settings)
    assert new.version == base_plan.version + 1
    assert new.text == base_plan.text                      # nothing became infeasible: minimal change
    assert first_infeasible_index(base_plan, poem, four_writers(), lead_did=OURS) is None


def test_replan_is_deterministic(engine, lexicon, settings, base_plan):
    poem = _poem(base_plan, 10, {9: "sun,"})
    a = replan(base_plan, poem, four_writers(), engine=engine, lexicon=lexicon, settings=settings)
    b = replan(base_plan, poem, four_writers(), engine=engine, lexicon=lexicon, settings=settings)
    assert a.text == b.text
