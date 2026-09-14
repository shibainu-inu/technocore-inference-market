import time

import pytest

from sonnet_orchestrator.config import PACKAGE_ROOT
from sonnet_orchestrator.creative.heuristic import HeuristicCreativeEngine
from sonnet_orchestrator.lexicon.core import bare
from sonnet_orchestrator.models.core import PoemForm, WriterHealth, WriterProfile
from sonnet_orchestrator.planner.beam import PlanError, lay_prefix, partner_index, plan_poem
from sonnet_orchestrator.planner.feasible import local_check
from sonnet_orchestrator.planner.validator import validate_poem_lines

OURS = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FIXTURES = PACKAGE_ROOT / "data" / "fixtures"


def synthetic_did(missing: str) -> str:
    return "did:key:z6Mk" + "".join(c for c in ALPHABET if c not in missing)


def four_writers() -> list[WriterProfile]:
    return [
        WriterProfile(did=OURS, handle="us", is_self=True, is_lead=True, x_account="@us", reliability=0.9),
        WriterProfile(did=synthetic_did("orbj"), handle="B", reliability=0.7),
        WriterProfile(did=synthetic_did("lnosx"), handle="C", reliability=0.6),
        WriterProfile(did=synthetic_did("aglow"), handle="D", reliability=0.5),
    ]


@pytest.fixture(scope="module")
def engine(lexicon):
    return HeuristicCreativeEngine(lexicon, seed=1)


def test_synthetic_dids_lack_the_intended_letters():
    w = WriterProfile(did=synthetic_did("orbj"))
    assert w.missing_letters == "bjor"
    assert set("dikeyz") <= w.letters


def test_plan_poem_four_writers_valid_and_fast(engine, lexicon, settings):
    writers = four_writers()
    t0 = time.perf_counter()
    plan = plan_poem(engine, lexicon, writers, settings, seed=3, game_id="g1")
    elapsed = time.perf_counter() - t0
    assert elapsed < 20.0, f"plan_poem took {elapsed:.1f}s"
    assert len(plan.lines) == 14
    rep = validate_poem_lines(plan.lines, lexicon)
    assert rep.ok, rep.errors
    assert rep.all_pairs_rhyme and rep.families_distinct, (rep.rhyme_pairs_ok, rep.clashes)
    assert lexicon.validate_poem(plan.text, exact_ten=True) == [10] * 14
    # WordEntry contract
    assert [w.index for w in plan.words] == list(range(len(plan.words)))
    assert " ".join(w.text for w in plan.words) == " ".join(plan.lines)
    assert all(w.syllables == lexicon.info(w.text).syllables for w in plan.words)
    assert all(len(w.stress) == w.syllables for w in plan.words)
    assert all(w.rhyme_key for w in plan.words if w.text == plan.lines[w.line].split()[-1])
    assert all(w.letters for w in plan.words)
    assert plan.version == 1 and plan.owner == OURS and plan.accepted_prefix_len == 0
    assert plan.plan_id.endswith(plan.hash_prefix)
    # every word spellable by a non-lead writer, or at least feasible under alternation
    non_lead = writers[1:]
    for w in plan.words:
        assert any(x.can_spell(w.text) for x in non_lead) or local_check([w.text], writers).feasible
    assert local_check(plan.words, writers, lead_did=OURS).feasible
    # end words never repeat
    ends = [bare(l.split()[-1]) for l in plan.lines]
    assert len(set(ends)) == 14


def test_plan_poem_is_deterministic_for_a_seed(engine, lexicon, settings):
    writers = four_writers()
    a = plan_poem(engine, lexicon, writers, settings, seed=11)
    b = plan_poem(engine, lexicon, writers, settings, seed=11)
    c = plan_poem(engine, lexicon, writers, settings, seed=12)
    assert a.text == b.text and a.sha256 == b.sha256
    assert c.text != a.text


def test_plan_poem_keeps_accepted_prefix_verbatim(engine, lexicon, settings):
    prefix = (FIXTURES / "nohitori-2" / "final_poem.txt").read_text(encoding="utf-8").split()[:23]
    writers = four_writers()
    t0 = time.perf_counter()
    plan = plan_poem(engine, lexicon, writers, settings, accepted_prefix=prefix, seed=3)
    assert time.perf_counter() - t0 < 20.0
    assert [w.text for w in plan.words[:23]] == prefix
    assert plan.accepted_prefix_len == 23
    rep = validate_poem_lines(plan.lines, lexicon)
    assert rep.strict_ok, (rep.errors, rep.rhyme_pairs_ok, rep.clashes)
    # the prefix ends mid-line 3 ("he met the tide each" = 5 syllables): line 3 starts with it and rhymes with "eye"
    assert plan.lines[2].startswith("he met the tide each")
    assert lexicon.rhymes(bare(plan.lines[2].split()[-1]), "eye")
    assert lexicon.rhymes(bare(plan.lines[3].split()[-1]), "meet")
    assert plan.lines[0] == "My father kept the sea. He had the eye"


def test_prefix_layout_and_partner_index(lexicon):
    prefix = (FIXTURES / "nohitori-2" / "final_poem.txt").read_text(encoding="utf-8").split()[:23]
    lines, partial = lay_prefix(prefix, lexicon, PoemForm())
    assert len(lines) == 2 and partial == ["he", "met", "the", "tide", "each"]
    assert [partner_index(i, PoemForm()) for i in range(14)] == [None, None, 0, 1, None, None, 4, 5, None, None, 8, 9, None, 12]
    with pytest.raises(PlanError):
        lay_prefix(["My", "father", "kept", "the", "sea.", "He", "had", "the", "evening"], lexicon, PoemForm())


def test_plan_poem_rejects_prefix_no_available_writer_can_spell(engine, lexicon, settings):
    writers = four_writers()
    writers[0].health = WriterHealth.DOWN   # only the lead has 'o' + 'b' + 'j' etc.; drop it
    with pytest.raises(PlanError):
        plan_poem(engine, lexicon, writers, settings, accepted_prefix=["Jobs"], seed=1)


def test_plan_poem_respects_unavailable_writer_letters(engine, lexicon, settings):
    writers = four_writers()
    plan = plan_poem(engine, lexicon, writers, settings, seed=5, unavailable={OURS})
    others = writers[1:]
    union = frozenset().union(*(w.letters for w in others))
    assert all(w.letters <= union for w in plan.words)
    assert local_check(plan.words, others).feasible
