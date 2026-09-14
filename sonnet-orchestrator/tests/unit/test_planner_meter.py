from sonnet_orchestrator.models.core import PoemForm
from sonnet_orchestrator.planner.meter import best_stress, line_ok, line_syllables, stress_distance


def test_perfect_iambic_line_has_zero_distance(lexicon):
    assert stress_distance("away away away away away".split(), lexicon) == 0.0
    # real accepted line: monosyllables are wildcards, "ladder" (1,0) sits on positions 3-4 (1,0)
    assert stress_distance("I climb the ladder, kneel, and rake the hay".split(), lexicon) == 0.0


def test_trochaic_line_is_far_from_iambic(lexicon):
    d = stress_distance("ladder ladder ladder ladder ladder".split(), lexicon)
    assert d > 0
    assert d == 10.0


def test_fragment_scored_at_its_real_position(lexicon):
    # "ladder" at position 0 mismatches both slots; at position 1 (odd) it fits (1,0) on (1,0)
    assert stress_distance(["ladder"], lexicon, start_pos=0) == 2.0
    assert stress_distance(["ladder"], lexicon, start_pos=1) == 0.0


def test_overlong_line_counts_overflow(lexicon):
    assert stress_distance("away away away away away away".split(), lexicon) >= 2.0


def test_line_syllables_and_line_ok(lexicon):
    words = "My father kept the sea. He had the eye".split()
    assert line_syllables(words, lexicon) == 10
    assert line_ok(words, lexicon, PoemForm())
    assert not line_ok(words[:-1], lexicon, PoemForm())
    assert not line_ok(["notaword"], lexicon, PoemForm())


def test_best_stress_prefers_fitting_pronunciation(lexicon):
    assert best_stress("ladder", lexicon, 1) == (1, 0)
    assert len(best_stress("the", lexicon, 0)) == 1
