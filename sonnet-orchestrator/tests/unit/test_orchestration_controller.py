"""Controller phases that the end-to-end games do not reach: frame timeout → drop → waitlist → re-issue, and
the snapshot before writing starts. World = mocks; planner/solver stubbed like tests/integration/test_mock_game.py."""
import json
from pathlib import Path

import pytest

from sonnet_orchestrator.adapters.mock import (FakeClock, MockDiscovery, MockPublication, MockReferee, MockTeamRoom,
                                               ScriptedWriters, WriterScript, synthetic_did)
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.db import Store
from sonnet_orchestrator.lexicon.core import load_lexicon
from sonnet_orchestrator.models import Assignment, ConsentState, FrameState, GameState, WriterProfile, word_letters
from sonnet_orchestrator.orchestration import Controller

ROOT = Path(__file__).resolve().parents[2]
SELF = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
B = synthetic_did("abcfghlnoprstuvw")
C = synthetic_did("abcfghlnorstuv")
D = synthetic_did("abfghlnoprstuw")
E = synthetic_did("abcfghlnoprstuvw", salt="e")
GAME = "mock-2"


@pytest.fixture(scope="module")
def lexicon():
    return load_lexicon(str(ROOT / "data" / "cmudict" / "cmudict.dict"))


@pytest.fixture(scope="module")
def poem_lines():
    p = ROOT / "data" / "fixtures" / "nohitori-2" / "final_poem.txt"
    return [l for l in p.read_text(encoding="utf-8").split("\n") if l.strip()]


class Res:
    def __init__(self, assignments, dead):
        self.assignments, self.feasible, self.dead_ends = assignments, not dead, dead


def rr_assign(words, writers, *, settings, lead_did, start_index=0, last_contributor=None, unavailable=set()):
    order = [w.did for w in writers if w.did not in unavailable]
    letters = {w.did: w.letters for w in writers}
    out, dead, last, pos = [], [], last_contributor, 0
    for w in words:
        if w.index < start_index:
            continue
        cands = [order[(pos + k) % len(order)] for k in range(len(order))]
        cands = [d for d in cands if d != last and word_letters(w.text) <= letters[d]]
        if not cands:
            dead.append(w.index); out.append(Assignment(index=w.index, primary=lead_did)); continue
        out.append(Assignment(index=w.index, primary=cands[0]))
        last, pos = cands[0], order.index(cands[0]) + 1
    return Res(out, dead)


def world(lexicon, poem_lines, scripts):
    settings = load_settings()
    settings.scheduler.tick_seconds = 60
    clock = FakeClock(step_seconds=15)
    referee = MockReferee(lexicon, clock)
    discovery = MockDiscovery(clock, SELF)
    room = MockTeamRoom(clock, SELF, referee=referee)
    publication = MockPublication(clock, publishers={SELF})
    store = Store(":memory:")
    for did in (SELF, B, C, D, E):
        store.upsert_writer(WriterProfile(did=did))
    writers = ScriptedWriters(referee, room, publication, clock, lexicon, settings, GAME, SELF, scripts).attach()
    ctl = Controller(settings, store, lexicon, referee, discovery, room, publication, None, clock, SELF, GAME,
                     planner_fn=lambda prefix, ws, s: list(poem_lines), assign_fn=rr_assign, members=[B, C, D])
    return ctl, referee, discovery, clock, settings


def test_never_signer_is_dropped_and_replaced_from_waitlist(lexicon, poem_lines):
    scripts = [WriterScript(did=B), WriterScript(did=C), WriterScript(did=D, profile="never_signs"), WriterScript(did=E)]
    ctl, referee, discovery, clock, settings = world(lexicon, poem_lines, scripts)
    assert ctl.tick() == GameState.ROSTER_PENDING
    f1 = ctl.frames.frame
    assert f1.members == [SELF, B, C, D] and f1.state == FrameState.SIGNING
    snap = ctl.snapshot(); json.dumps(snap)
    assert snap["state"] == "ROSTER_PENDING" and snap["frame"]["signature"] == f1.signature
    # E applies while the frame is out for signature: waitlisted, never seated into a signing frame
    assert ctl.frames.seat(E).kind == "waitlist"
    clock.sleep(settings.scheduler.tick_seconds)
    assert ctl.tick() == GameState.ROSTER_PENDING
    assert {B, C} <= f1.signed_by and D not in f1.signed_by and f1.members == [SELF, B, C, D]
    # the signature window passes: D (never signed anything) is dropped, E is seated, the frame is re-issued
    clock.sleep(settings.consent.signature_timeout_s)
    st = ctl.tick()
    kinds = [e["kind"] for e in ctl.events]
    assert "consent_drop" in kinds and "consent_reissue" in kinds
    assert st == GameState.ROSTER_PENDING and ctl.frames.frame is not f1
    f2 = ctl.frames.frame
    assert f2.members == [SELF, B, C, E] and f1.state == FrameState.SUPERSEDED
    assert ctl.frames.consent(D).state == ConsentState.NONE and D in ctl.frames.declined
    assert any(e["kind"] == "withdraw" and "ok" in e["detail"] for e in ctl.events)   # withdraw before re-issue
    assert referee.roster_status(GAME)["members"] == [SELF, B, C, E]
    # B and C re-sign (withdraw first, then sign the new frame), E signs: roster ready -> writing starts
    for _ in range(4):
        clock.sleep(settings.scheduler.tick_seconds)
        st = ctl.tick()
        if st == GameState.WRITING:
            break
    assert st == GameState.WRITING and referee.roster_status(GAME)["frozen"]
    assert ctl.frames.frame.state == FrameState.FROZEN
    assert all(ctl.frames.consent(d).state == ConsentState.FROZEN for d in (SELF, B, C, E))
    assert ctl.members() == [SELF, B, C, E]
    final = ctl.run_until_complete(max_ticks=300)
    assert final in (GameState.SUBMITTED, GameState.ACCEPTED)
    assert D not in {w.contributor for w in ctl.poem.accepted}


def test_previous_frame_signers_get_reminders_not_the_door(lexicon, poem_lines):
    # C signs the first frame, then never re-signs the changed one: C is reminded, never dropped
    scripts = [WriterScript(did=B), WriterScript(did=C), WriterScript(did=D, profile="never_signs"), WriterScript(did=E)]
    ctl, referee, discovery, clock, settings = world(lexicon, poem_lines, scripts)
    ctl.tick()
    ctl.frames.seat(E)
    clock.sleep(settings.scheduler.tick_seconds)
    ctl.tick()
    assert C in ctl.frames.frame.signed_by
    scripts[1].profile = "never_signs"                 # C stops responding after its first signature
    clock.sleep(settings.consent.signature_timeout_s)
    ctl.tick()                                        # D dropped, E seated, frame 2 issued
    clock.sleep(settings.consent.signature_timeout_s)
    ctl.tick()
    reminders = [e for e in ctl.events if e["kind"] == "consent_remind"]
    drops = [e for e in ctl.events if e["kind"] == "consent_drop"]
    assert reminders and all(C[-8:] in e["detail"] for e in reminders)
    assert [e["detail"].split()[0] for e in drops] == [D[-8:]]
    assert C in ctl.frames.members
    assert any(p.meta.get("to_did") == C for p in discovery.posts)
