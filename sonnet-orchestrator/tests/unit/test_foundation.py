"""Foundation tests: config, models, store, lexicon, DID analyzer."""
from datetime import datetime, timezone

import pytest

from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.db import Store
from sonnet_orchestrator.did import coverage, keys_for_word
from sonnet_orchestrator.models import (AcceptedWord, Assignment, Plan, PoemState, Proposal, ProposalStatus, WordEntry,
                                        WriterProfile, canonical_text, poem_sha256, did_letters)

OUR = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"


def test_settings_load_no_magic_numbers():
    s = load_settings()
    assert s.solver.lookahead_words >= s.solver.minimum_lookahead >= 2
    assert s.room.post_char_limit == 2000
    assert s.scheduler.tick_seconds == 60
    assert s.contest["id"] == "sonnet-2"
    assert "start_next_entry" in s.operator.approval_required


def test_did_letters_and_profile():
    w = WriterProfile(did=OUR, is_self=True)
    assert len(w.letters) == 26 and w.missing_letters == ""
    w2 = WriterProfile(did="did:key:z6Mkabc")
    assert did_letters("did:key:z6Mkabc") == frozenset("dikeyzmabc")
    assert w2.can_spell("bad") and not w2.can_spell("post")


def test_canonical_text_and_sha(tmp_path):
    lines = [f"l{i}" for i in range(14)]
    t = canonical_text(lines)
    assert t.count("\n\n") == 3 and not t.endswith("\n")
    assert poem_sha256(lines) == __import__("hashlib").sha256(t.encode()).hexdigest()


def test_store_prefix_immutable_and_contiguous():
    st = Store()
    st.upsert_game("g")
    st.append_accepted("g", AcceptedWord(index=0, text="My", contributor="a", version=1))
    with pytest.raises(ValueError):
        st.append_accepted("g", AcceptedWord(index=0, text="Your", contributor="a", version=1))
    with pytest.raises(ValueError):
        st.append_accepted("g", AcceptedWord(index=2, text="sea", contributor="b", version=3))
    st.append_accepted("g", AcceptedWord(index=0, text="My", contributor="a", version=1))  # idempotent
    assert [w.text for w in st.accepted("g")] == ["My"]


def test_store_single_active_plan():
    st = Store()
    st.upsert_game("g")
    for v in (1, 2, 3):
        st.save_plan(Plan(plan_id=f"p{v}", game_id="g", version=v, owner=OUR,
                          words=[WordEntry(index=0, text="My", line=0, syllables=1)], lines=["My"] * 14,
                          assignments=[Assignment(index=0, primary=OUR, keys=1)]))
    assert st.active_plan("g").plan_id == "p3"
    assert sum(p.is_active for p in st.plans("g")) == 1


def test_store_proposals_and_writers():
    st = Store()
    st.upsert_game("g")
    p = Proposal(request_id="w0-abc-xyz-1", index=0, text="My", contributor=OUR, base_version=0)
    st.add_proposal("g", p)
    st.resolve_proposal(p.request_id, ProposalStatus.STALE, "version: stale", datetime.now(timezone.utc))
    assert st.proposals("g", ProposalStatus.STALE)[0].reason == "version: stale"
    w = WriterProfile(did=OUR, seat_no_sign_count=2, sign_latency_median_ms=131000.0)
    st.upsert_writer(w)
    got = st.get_writer(OUR)
    assert got.seat_no_sign_count == 2 and got.sign_latency_median_ms == 131000.0 and got.letters == w.letters


def test_lexicon_real_dictionary(lexicon):
    assert len(lexicon) > 100_000
    assert lexicon.word_syllables("father,") == 2
    assert lexicon.rhymes("sea", "me") and not lexicon.rhymes("sea", "sea")
    assert lexicon.line_syllables("My father kept the sea. He had the eye".split()) == 10
    with pytest.raises(ValueError):
        lexicon.validate_word("post", "did:key:z6Mkabc")
    cands = lexicon.candidates("abdeghiklmnopqrstuvwxyz", 2, rhyme_with="sea")
    assert cands and all(lexicon.rhymes(c, "sea") for c in cands[:20])


def test_coverage_report():
    members = [OUR, "did:key:z6Mkabcefghlnprstuvw", "did:key:z6Mkabcefghlnprstuvo"]
    rep = coverage(members, lead=OUR)
    assert rep.missing_from_union == ""
    assert "j" in rep.lead_only_letters and "q" in rep.lead_only_letters
    assert 0 < rep.fragility < 1
    assert keys_for_word("son", rep.letters_per_member) == [OUR, members[2]]


def test_poem_state():
    ps = PoemState(game_id="g", accepted=[AcceptedWord(index=0, text="My", contributor="a", version=1)], version=1)
    assert ps.next_index == 1 and ps.last_contributor == "a"
