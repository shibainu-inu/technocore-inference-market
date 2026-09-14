import pytest

from sonnet_orchestrator.creative.heuristic import HeuristicCreativeEngine
from sonnet_orchestrator.models.core import AcceptedWord, PoemState, WriterProfile
from sonnet_orchestrator.planner.beam import plan_poem
from sonnet_orchestrator.planner.landing import landing_routes
from tests.unit.test_planner_beam import OURS, four_writers


@pytest.fixture(scope="module")
def plan(lexicon, settings):
    engine = HeuristicCreativeEngine(lexicon, seed=1)
    return plan_poem(engine, lexicon, four_writers(), settings, seed=3, game_id="g")


def _poem(plan, n):
    writers = four_writers()
    acc = [AcceptedWord(index=i, text=plan.words[i].text, contributor=writers[i % 2].did, version=i + 1) for i in range(n)]
    return PoemState(game_id="g", accepted=acc, version=n)


def _valid(route, plan, poem, writers):
    by = {w.did: w for w in writers}
    idxs = [i for i, _ in route.path]
    assert idxs == list(range(poem.next_index, len(plan.words)))
    prev = poem.last_contributor
    for i, d in route.path:
        assert d != prev
        assert by[d].can_spell(plan.words[i].text)
        prev = d
    assert route.path[-1][1] == route.final_contributor


def test_routes_are_valid_and_publisher_first(plan, settings):
    writers = four_writers()
    poem = _poem(plan, 100)
    routes = landing_routes(plan, poem, writers, settings)
    assert len(routes) >= settings.planner.landing_routes
    for r in routes:
        _valid(r, plan, poem, writers)
    assert routes[0].can_publish and routes[0].final_contributor == OURS
    assert len({tuple(r.path) for r in routes}) == len(routes)


def test_alternation_blocks_last_contributor_from_a_single_final_word(plan, settings):
    writers = four_writers()
    poem = _poem(plan, len(plan.words) - 1)          # one word left
    routes = landing_routes(plan, poem, writers, settings)
    assert routes
    assert all(r.final_contributor != poem.last_contributor for r in routes)
    assert all(len(r.path) == 1 for r in routes)


def test_no_routes_when_nothing_remains_or_nobody_available(plan, settings):
    writers = four_writers()
    assert landing_routes(plan, _poem(plan, len(plan.words)), writers, settings) == []
    assert landing_routes(plan, _poem(plan, 50), writers, settings, unavailable={w.did for w in writers}) == []


def test_publisher_preference_uses_x_account(plan, settings):
    writers = four_writers()
    writers[0].x_account = None
    b = WriterProfile(did=writers[1].did, handle="B", x_account="@b", reliability=0.7)
    writers[1] = b
    poem = _poem(plan, 100)
    routes = landing_routes(plan, poem, writers, settings)
    assert routes
    pubs = [r for r in routes if r.can_publish]
    if pubs:
        assert routes[0].can_publish and routes[0].final_contributor == b.did
