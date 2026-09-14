from pathlib import Path

import pytest

from sonnet_orchestrator.config import PACKAGE_ROOT
from sonnet_orchestrator.planner.validator import validate_poem_lines, validate_poem_text

FIXTURES = PACKAGE_ROOT / "data" / "fixtures"


@pytest.mark.parametrize("name", ["nohitori", "nohitori-2"])
def test_real_final_poems_pass_official_validator(lexicon, name):
    text = (FIXTURES / name / "final_poem.txt").read_text(encoding="utf-8")
    rep = validate_poem_text(text, lexicon)
    assert rep.ok, rep.errors
    assert rep.official_error is None
    assert rep.per_line_syllables == [10] * 14
    # fixtures are stored as 14 bare lines; the report's canonical form adds the 4/4/4/2 stanza breaks
    assert [l for l in rep.canonical.split("\n") if l] == [l for l in text.split("\n") if l]
    assert rep.canonical.count("\n\n") == 3
    # Rhyme is diagnostic only; both real poems happen to rhyme fully with distinct families.
    assert rep.rhyme_pairs_ok == {k: True for k in ["1-3", "2-4", "5-7", "6-8", "9-11", "10-12", "13-14"]}
    assert rep.families_distinct and rep.clashes == []
    assert rep.strict_ok


def test_wrong_syllable_count_is_reported_per_line(lexicon):
    text = (FIXTURES / "nohitori" / "final_poem.txt").read_text(encoding="utf-8")
    lines = [l for l in text.split("\n") if l]
    lines[4] = lines[4] + " again"
    rep = validate_poem_lines(lines, lexicon)
    assert not rep.ok
    assert any(e.startswith("line 5:") for e in rep.errors)
    assert rep.official_error is not None and "line 5" in rep.official_error
    assert rep.per_line_syllables[4] == 12


def test_line_count_and_unknown_word(lexicon):
    rep = validate_poem_lines(["away away away away away"] * 13, lexicon)
    assert not rep.ok and any("expected 14" in e for e in rep.errors)
    lines = ["away away away away away"] * 14
    lines[0] = "zzzqqq away away away away"
    rep = validate_poem_lines(lines, lexicon)
    assert not rep.ok and any("line 1" in e for e in rep.errors)


def test_rhyme_diagnostics_detect_non_rhyme_and_family_clash(lexicon):
    base = "away away away away the".split()      # 9 syllables + a monosyllabic end word
    lines = [" ".join(base + [w]) for w in
             ["day", "night", "stay", "light", "hand", "deep", "sand", "keep", "show", "thin", "slow", "skin", "hay", "lay"]]
    rep = validate_poem_lines(lines, lexicon)
    assert rep.ok                                   # form is fine
    assert rep.all_pairs_rhyme
    assert not rep.families_distinct and "AG" in rep.clashes   # day/hay share EY
    lines[2] = " ".join(base + ["tree"])
    rep = validate_poem_lines(lines, lexicon)
    assert rep.rhyme_pairs_ok["1-3"] is False
    assert not rep.strict_ok
