import pytest

from sonnet_orchestrator.creative import CreativeEngine, HeuristicCreativeEngine, LineContext
from sonnet_orchestrator.lexicon.core import bare
from sonnet_orchestrator.models.core import did_letters
from tests.unit.test_planner_beam import OURS, synthetic_did

DIDS = [OURS, synthetic_did("orbj"), synthetic_did("lnosx"), synthetic_did("aglow")]


@pytest.fixture(scope="module")
def engine(lexicon):
    return HeuristicCreativeEngine(lexicon, seed=1)


def _ctx(**kw):
    per = {d: did_letters(d) for d in DIDS}
    base = dict(line_index=0, previous_lines=[], rhyme_key=None, allowed_letters=frozenset().union(*per.values()),
                per_writer_letters=per, max_candidates=24)
    base.update(kw)
    return LineContext(**base)


def test_engine_satisfies_protocol_and_vocabulary_is_in_dictionary(engine, lexicon):
    assert isinstance(engine, CreativeEngine)
    assert all(w in lexicon for w in engine.vocab)
    assert len(engine.vocab) > 500


def test_free_lines_have_exactly_ten_syllables_and_allowed_letters(engine, lexicon):
    ctx = _ctx()
    cands = engine.propose_lines(ctx)
    assert 1 <= len(cands) <= 24
    for c in cands:
        assert lexicon.line_syllables(c.words) == 10
        assert all(lexicon.info(w).letters <= ctx.allowed_letters for w in c.words)
    assert cands == sorted(cands, key=lambda c: (-c.score, c.words))


def test_rhyme_constrained_end_words(engine, lexicon):
    ctx = _ctx(line_index=2, rhyme_key="day", forbidden_end_words={"day", "night"})
    cands = engine.propose_lines(ctx)
    assert cands
    for c in cands:
        assert lexicon.line_syllables(c.words) == 10
        end = bare(c.words[-1])
        assert lexicon.rhymes(end, "day") and end not in {"day", "night"}
        assert end in engine._vocab_set             # curated words preferred over dictionary junk


def test_family_opening_line_avoids_existing_family_keys(engine, lexicon):
    ctx = _ctx(line_index=4, forbidden_end_words={"day", "night", "away", "light"})
    for c in engine.propose_lines(ctx):
        end = bare(c.words[-1])
        assert not (lexicon.rhyme_keys(end) & (lexicon.rhyme_keys("day") | lexicon.rhyme_keys("night")))


def test_fragment_completion_budget(engine, lexicon):
    ctx = _ctx(line_index=2, rhyme_key="eye", syllables=5, forbidden_end_words={"eye", "meet"})
    cands = engine.propose_lines(ctx)
    assert cands
    for c in cands:
        assert lexicon.line_syllables(c.words) == 5
        assert lexicon.rhymes(bare(c.words[-1]), "eye")
    one = engine.propose_lines(_ctx(line_index=3, rhyme_key="meet", syllables=1, forbidden_end_words={"meet"}))
    assert one and all(len(c.words) == 1 and lexicon.rhymes(c.words[0], "meet") for c in one)


def test_impossible_rhyme_returns_empty(engine):
    assert engine.propose_lines(_ctx(line_index=2, rhyme_key="orange")) == []
    assert engine.propose_lines(_ctx(syllables=0)) == []


def test_letter_restriction_is_hard(engine, lexicon):
    per = {synthetic_did("aglow"): did_letters(synthetic_did("aglow"))}
    allowed = frozenset().union(*per.values())
    cands = engine.propose_lines(_ctx(allowed_letters=allowed, per_writer_letters=per))
    assert cands
    for c in cands:
        assert all(lexicon.info(w).letters <= allowed for w in c.words)
        assert not any(set("aglow") & lexicon.info(w).letters for w in c.words)


def test_two_key_rule_prefers_redundant_words(engine, lexicon):
    per = {d: did_letters(d) for d in DIDS}
    cands = engine.propose_lines(_ctx())
    total = sum(len(c.words) for c in cands)
    two_key = sum(1 for c in cands for w in c.words if sum(1 for ls in per.values() if lexicon.info(w).letters <= ls) >= 2)
    assert two_key / total > 0.9


def test_deterministic_with_seed(lexicon):
    a = HeuristicCreativeEngine(lexicon, seed=7).propose_lines(_ctx())
    b = HeuristicCreativeEngine(lexicon, seed=7).propose_lines(_ctx())
    c = HeuristicCreativeEngine(lexicon, seed=8).propose_lines(_ctx())
    assert [x.words for x in a] == [x.words for x in b]
    assert [x.words for x in a] != [x.words for x in c]
    e = HeuristicCreativeEngine(lexicon, seed=7)
    first = e.propose_lines(_ctx())
    e.reseed(7)
    assert [x.words for x in e.propose_lines(_ctx())] == [x.words for x in first]


def test_word_alternatives_same_syllables_and_letters(engine, lexicon):
    ctx = _ctx()
    alts = engine.propose_word_alternatives("ladder,", ctx, 2)
    assert alts and len(alts) <= ctx.max_candidates
    assert "ladder" not in alts
    assert all(lexicon.info(w).syllables == 2 and lexicon.info(w).letters <= ctx.allowed_letters for w in alts)
    assert all(engine.category_of.get(w) == "NOUN" for w in alts)
    # unknown category falls back to the curated vocabulary, then to the dictionary
    assert engine.propose_word_alternatives("xylophone", ctx, 3)
