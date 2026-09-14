"""Replay of the two real team-room exports must reproduce the final poems and their canonical hashes."""
from __future__ import annotations

import hashlib

import pytest

from sonnet_orchestrator.config import PACKAGE_ROOT
from sonnet_orchestrator.diagnostics.replay import (
    REFEREE_DID, ReplayLog, accepted_from_export, canonical_from_export, lines_from_words, load_final_poem, parse_export,
    word_spellers,
)
from sonnet_orchestrator.models.core import canonical_text

FIX = PACKAGE_ROOT / "data" / "fixtures"
EXPECTED = {
    "nohitori": ("4a555d51fec11f2fc83d88e0a30b45e2c71a711233c44b1f4c0f559e38ef07cd", 125, 4),
    "nohitori-2": ("72e0b31939b10195cdbaa5e348124e20c23f2fbccc8b520f22c6eb345b5e0aca", 131, 4),
}


@pytest.fixture(scope="module", params=sorted(EXPECTED))
def game(request):
    return request.param


@pytest.fixture(scope="module")
def log(game) -> ReplayLog:
    return parse_export(FIX / game / "team_room_export.ndjson")


def test_accepted_stream_reproduces_final_poem(game, log, lexicon):
    sha, n_words, _ = EXPECTED[game]
    accepted = accepted_from_export(log.path)
    assert len(accepted) == n_words
    assert [w.index for w in accepted] == list(range(n_words))
    lines = lines_from_words([w.text for w in accepted], lexicon)
    assert len(lines) == 14
    # final_poem.txt is stored as 14 LF-joined lines without stanza blank lines; compare line by line
    file_lines = load_final_poem(FIX / game / "final_poem.txt").split("\n")
    assert lines == file_lines
    text, h = canonical_from_export(log.path, lexicon)
    assert text == canonical_text(lines)
    assert h == sha
    assert hashlib.sha256(text.encode()).hexdigest() == sha
    assert lexicon.validate_poem(text, exact_ten=True) == [10] * 14


def test_members_and_contributions(game, log):
    _, n_words, n_members = EXPECTED[game]
    assert len(log.members) == n_members
    assert REFEREE_DID not in log.members
    contrib = {m[-8:]: n for m, n in log.contributions().items()}
    assert sum(contrib.values()) == n_words
    if game == "nohitori-2":
        assert contrib == {"VxSdDkhu": 43, "W4TAejK6": 41, "f9vthSUn": 28, "F6jvabi2": 19}
        assert log.final_contributor.endswith("f9vthSUn")
        assert log.final_version == 131
    else:
        assert contrib == {"MWV4RmAQ": 61, "W4TAejK6": 58, "kc46mJuz": 4, "3sLzg7ws": 2}
        assert log.final_contributor.endswith("MWV4RmAQ")
        assert log.final_version == 125
    assert log.complete
    assert log.lead.endswith("W4TAejK6")


def test_versions_are_contiguous_and_no_consecutive_contributor(log):
    versions = [w.version for w in log.accepted]
    assert versions == list(range(len(versions)))
    for a, b in zip(log.accepted, log.accepted[1:]):
        assert a.contributor != b.contributor
        assert a.receipt_seq < b.receipt_seq
        assert a.accepted_at <= b.accepted_at


def test_timeline_and_receipts(game, log):
    assert all(p.kind == "note" for p in log.timeline)
    kinds = {p.kind for p in log.posts}
    assert {"word", "receipt", "note", "room"} <= kinds
    assert log.room_created_at is not None
    assert log.roster_ready_at is not None
    assert log.completed_at is not None and log.completed_at > log.roster_ready_at
    stale = [r for r in log.rejections if r.reason.startswith("version: stale")]
    if game == "nohitori-2":
        assert "receipts" in kinds
        assert len(log.rejections) == 44 and len(stale) == 41
        assert sum(r.batch for r in log.rejections) == 21
        assert sum(1 for r in log.rejections if r.reason == "roster: incomplete consent") == 1
        assert len(log.roster_receipts) == 6
        assert log.roster_ready_at.isoformat().startswith("2026-09-14T03:49:57")
    else:
        assert len(log.rejections) == 4 and len(stale) == 4
        assert log.roster_ready_at.isoformat().startswith("2026-09-13T17:22:01")


def test_tables_parsed(game, log):
    tables = [t for t in log.tables if t.kind == "table"]
    assert tables
    if game == "nohitori-2":
        v3 = next(t for t in tables if t.version_label == "v3")
        assert v3.words[97] == "beg" and v3.rows[97] == "F6jvabi2"
        assert v3.words[98] == "this:" and v3.rows[98] == "W4TAejK6"
        assert log.resolve_label("F6jvabi2").endswith("F6jvabi2")
    else:
        t = next(t for t in tables if t.version_label == "2/5")
        assert t.words[59] == "The" and t.rows[59] == "W4TAejK6"
        assert log.resolve_label("leidream").endswith("MWV4RmAQ")
        assert log.resolve_label("sifat").endswith("3sLzg7ws")
    assert log.resolve_label("nobody-here") is None


def test_trap_words_and_spellers():
    log2 = parse_export(FIX / "nohitori-2" / "team_room_export.ndjson")
    words = log2.accepted_texts()
    # 96->97 (1-based): lead posted 'dead', planned 'beg' was spellable only by F6jvabi2 or the lead
    assert words[95] == "dead" and log2.accepted[95].contributor.endswith("W4TAejK6")
    assert words[96] == "ask" and log2.accepted[96].contributor.endswith("f9vthSUn")
    assert sorted(m[-8:] for m in word_spellers("beg", log2.members)) == ["F6jvabi2", "W4TAejK6"]
    assert sorted(m[-8:] for m in word_spellers("ask", log2.members)) == ["W4TAejK6", "f9vthSUn"]
    # 58->59 in nohitori-2 was not a trap ('if' -> 'my', 4 spellers each)
    assert (words[57], words[58]) == ("if", "my")
    assert len(word_spellers("my", log2.members)) == 4
    # the entry-1 58->59 trap: 'more.' by the lead, then 'The' (only lead or absent 3sLzg7ws) edited to 'Some'
    log1 = parse_export(FIX / "nohitori" / "team_room_export.ndjson")
    w1 = log1.accepted_texts()
    assert (w1[57], w1[58]) == ("more.", "Some") and log1.accepted[57].contributor.endswith("W4TAejK6")
    assert sorted(m[-8:] for m in word_spellers("The", log1.members)) == ["3sLzg7ws", "W4TAejK6"]


def test_lines_from_words_rejects_boundary_crossing(lexicon):
    with pytest.raises(ValueError):
        lines_from_words(["I"] * 9 + ["ladder,"], lexicon)   # 9 + 2 crosses 10
    assert lines_from_words(["I"] * 10, lexicon) == ["I I I I I I I I I I"]
