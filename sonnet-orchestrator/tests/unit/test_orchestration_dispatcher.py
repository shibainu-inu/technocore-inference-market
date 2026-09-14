from pathlib import Path

import pytest

from sonnet_orchestrator.adapters.mock import FakeClock, MockReferee, synthetic_did
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.db import Store
from sonnet_orchestrator.lexicon.core import load_lexicon
from sonnet_orchestrator.models import AcceptedWord, Frame, ProposalStatus as P, Receipt
from sonnet_orchestrator.orchestration.dispatcher import Dispatcher

ROOT = Path(__file__).resolve().parents[2]
SELF = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
B = synthetic_did("abcfghlnoprstuvw")
C = synthetic_did("abcfghlnorstuv")
GAME = "g1"


@pytest.fixture(scope="module")
def lexicon():
    return load_lexicon(str(ROOT / "data" / "cmudict" / "cmudict.dict"))


def ready_referee(lexicon, clock, **kw):
    ref = MockReferee(lexicon, clock, **kw)
    frame = Frame(frame_id="f1", game_id=GAME, members=[SELF, B, C], poem_room="r", room_generation=1)
    assert ref.issue_frame(frame).ok
    for d in (B, C):
        assert ref.sign_frame(frame, d).ok
    assert ref.roster_status(GAME)["ready"]
    return ref


def mk(lexicon, **kw):
    settings = load_settings()
    clock = FakeClock()
    ref = ready_referee(lexicon, clock, **kw)
    store = Store(":memory:")
    d = Dispatcher(ref, store, clock, GAME, timeout_ms=settings.health.minimum_timeout_ms)
    return settings, clock, ref, store, d


def test_request_id_format_and_uniqueness(lexicon):
    settings, clock, ref, store, d = mk(lexicon)
    p1 = d.propose(0, "My", SELF, 0)
    parts = p1.request_id.split("-")
    assert parts[0] == "w0" and len(parts[1]) == 8 and parts[2] == SELF[-6:] and parts[3].isdigit()
    p2 = d.propose(0, "My", SELF, 0)                 # same instant, same word: still unique
    assert p1.request_id != p2.request_id
    assert store.proposals(GAME)[0].request_id == p1.request_id


def test_accept_stale_reject_and_duplicates_are_idempotent(lexicon):
    settings, clock, ref, store, d = mk(lexicon, duplicate_receipts=True)
    p = d.propose(0, "My", SELF, 0)
    out = d.process_receipts()
    assert [o.kind for o in out] == ["applied"] and p.status == P.ACCEPTED
    assert [w.text for w in store.accepted(GAME)] == ["My"]
    out = d.process_receipts()                        # the referee re-delivers the same receipt
    assert [o.kind for o in out] == ["duplicate"] and [w.text for w in store.accepted(GAME)] == ["My"]
    # somebody else takes index 1; our proposal for index 1 with the old version is STALE
    ref.propose_word(GAME, "b-1", 1, "father", B, 1)
    q = d.propose(1, "father", SELF, 0)
    kinds = [o.kind for o in d.process_receipts()]
    assert "applied" in kinds and "stale" in kinds and q.status == P.STALE and d.needs_resync
    assert [w.contributor for w in store.accepted(GAME)] == [SELF, B]
    # a rejected word (letters not in our DID? we have all; use consecutive-contributor instead)
    r = d.propose(2, "kept", B, 2)                     # B posted the previous word
    d.process_receipts()
    assert r.status == P.REJECTED and "consecutive" in r.reason


def test_unknown_request_ids_logged_not_applied_and_foreign_accepted_stream(lexicon):
    settings, clock, ref, store, d = mk(lexicon)
    # foreign accepted receipts (other members' words) form the accepted stream, in order, with buffering
    r1 = Receipt(request_id="x-1", status=P.ACCEPTED, index=1, text="father", contributor=B, version=2, seq=2, at=clock.now())
    r0 = Receipt(request_id="x-0", status=P.ACCEPTED, index=0, text="My", contributor=C, version=1, seq=1, at=clock.now())
    junk = Receipt(request_id="???", status=P.REJECTED, reason="word: bad", seq=3, at=clock.now())
    out = d.process_receipts([r1, junk, r0])
    assert [o.kind for o in out] == ["buffered", "unknown", "applied", "applied"]
    assert [w.text for w in store.accepted(GAME)] == ["My", "father"]
    assert any("unknown request_id" in line for line in d.log)
    # a repeat of a recorded word is a no-op; a different word at a recorded index is a conflict, never applied
    again = d.process_receipts([r0])
    assert [o.kind for o in again] == ["duplicate"]
    bad = Receipt(request_id="x-0b", status=P.ACCEPTED, index=0, text="Our", contributor=B, version=9, seq=9, at=clock.now())
    assert [o.kind for o in d.process_receipts([bad])] == ["conflict"]
    assert [w.text for w in store.accepted(GAME)] == ["My", "father"]


def test_timeout_then_late_receipt_still_resolves(lexicon):
    timeout_ms = load_settings().health.minimum_timeout_ms
    settings, clock, ref, store, d = mk(lexicon, delayed_receipt={SELF: timeout_ms * 2})
    p = d.propose(0, "My", SELF, 0)
    assert d.process_receipts() == []
    clock.advance(settings.health.minimum_timeout_ms / 1000.0)
    assert d.expire() == [p] and p.status == P.TIMED_OUT
    assert d.process_receipts() == []                 # still delayed
    clock.advance(settings.health.minimum_timeout_ms / 1000.0)
    out = d.process_receipts()
    assert [o.kind for o in out] == ["timed_out_late"] and p.status == P.ACCEPTED
    assert [w.text for w in store.accepted(GAME)] == ["My"]
    assert d.process_receipts() == [] and d.expire() == []


def test_resync_adopts_referee_state(lexicon):
    settings, clock, ref, store, d = mk(lexicon)
    ref.propose_word(GAME, "b-0", 0, "My", B, 0)
    ref.propose_word(GAME, "c-1", 1, "father", C, 1)
    ref.poll_receipts(GAME)                           # receipts consumed elsewhere (we never saw them)
    q = d.propose(0, "My", SELF, 0)
    d.process_receipts()
    assert q.status == P.STALE and d.needs_resync
    assert d.resync(ref.accepted_words(GAME)) == 2 and not d.needs_resync
    assert [w.contributor for w in store.accepted(GAME)] == [B, C]
    assert d.resync(ref.accepted_words(GAME)) == 0    # idempotent


def test_referee_rules(lexicon):
    settings, clock, ref, store, d = mk(lexicon)
    g = ref.truth(GAME)
    # not a member
    ref.propose_word(GAME, "z", 0, "My", synthetic_did("xyz"), 0)
    assert g.receipts[-1].reason == "roster: not a member"
    # letters not in the DID (C lacks 'w')
    ref.propose_word(GAME, "c-w", 0, "wave", C, 0)
    assert "letters absent" in g.receipts[-1].reason
    # not in the dictionary
    ref.propose_word(GAME, "s-x", 0, "Qzxv", SELF, 0)
    assert "not in the frozen dictionary" in g.receipts[-1].reason
    # roster not ready: rejected with the referee's reason
    ref2 = MockReferee(lexicon, clock)
    ref2.propose_word("g2", "s-0", 0, "My", SELF, 0)
    assert ref2.truth("g2").receipts[-1].reason == "roster: incomplete consent"


def test_consent_rules(lexicon):
    clock = FakeClock()
    ref = MockReferee(lexicon, clock)
    f1 = Frame(frame_id="f1", game_id="g1", members=[SELF, B], poem_room="r", room_generation=1)
    f2 = Frame(frame_id="f2", game_id="g2", members=[C, B], poem_room="r2", room_generation=1)
    assert ref.issue_frame(f1).ok and ref.sign_frame(f1, B).ok
    assert ref.roster_status("g1")["frozen"]
    assert ref.issue_frame(f2).ok
    res = ref.sign_frame(f2, B)                       # B is frozen on g1
    assert not res.ok and res.error == "roster: member already frozen"
    f3 = Frame(frame_id="f3", game_id="g3", members=[C, "did:key:z6Mk" + "x" * 44], poem_room="r3", room_generation=1)
    res = ref.issue_frame(f3)                          # C's live consent is on g2 -> withdraw first
    assert not res.ok and res.error == "consent: withdraw before changing"
    assert ref.withdraw("g2", C).ok and ref.issue_frame(f3).ok
    assert not ref.withdraw("g1", B).ok                # frozen roster: withdraw refused
