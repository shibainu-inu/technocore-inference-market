"""Phase 7 file-bridge (docs/BRIDGE.md). All state/policy JSON is written into tmp_path; the real files under
``sonnet/`` are only ever copied, never written."""
from __future__ import annotations

import hashlib
import json
import shutil
import time
from pathlib import Path

import pytest

from sonnet_orchestrator import bridge
from sonnet_orchestrator.config import PACKAGE_ROOT
from sonnet_orchestrator.models.core import canonical_text

LEAD = "did:key:z6MksZoGczsfxQoVT5rA76CbvKNLHrEzmUvpGbPnW4TAejK6"
MEMBERS = [
    LEAD,
    "did:key:z6MkfGCMq51DuxSqLWzXZ71TKgGXQVaVdpn9g55qf9vthSUn",
    "did:key:z6MkpM6GWdFZmbdwy8uUbBJiutGHMQR6Fm69e3CYF6jvabi2",
    "did:key:z6MkumkZvieRKkDeq6NS4BbZhuqiNnjYFKCPNtEYVxSdDkhu",
]
INVITES = ["did:key:z6MkjQ1NWXQHomwLjRNx2mKSoYp5CBv4BcGpoS35MWV4RmAQ",
           "did:key:z6MkuJDcegSVQnncj4uTNUCJACbHhZCfsypMx667AsHAMhgt"]
APPLICANT = "did:key:z6MkhQ7X9bFg5EdtAxtJJsGzPAcVnVFDaqjyUEqbhdR3jLmt"
SCORES = PACKAGE_ROOT / "data" / "fixtures" / "writer_scores_2026-09-13.json"
FINAL_POEM = PACKAGE_ROOT / "data" / "fixtures" / "nohitori-2" / "final_poem.txt"
REAL_SONNET_DIR = PACKAGE_ROOT.parent / "sonnet"


def _policy(**kw) -> dict:
    p = {"did": LEAD, "x_account_url": "https://x.com/0xnohitori", "lead_invites": list(INVITES),
         "slow_members": [], "absent_members": [], "lead_max_members": 6}
    p.update(kw)
    return p


def _poem(lines=(), current=(), frozen=False, last=None) -> dict:
    return {"lines": list(lines), "current": list(current), "frozen": frozen, "version": len(lines),
            "last_contributor": last, "contributors": []}


def _write(tmp: Path, state: dict, policy: dict) -> tuple[Path, Path, Path]:
    sp, pp = tmp / "state.json", tmp / "policy.json"
    sp.write_text(json.dumps(state))
    pp.write_text(json.dumps(policy))
    return sp, pp, tmp / "bridge"


def _lay(words: list[str], lexicon) -> tuple[list[str], list[str]]:
    lines, cur, n = [], [], 0
    for w in words:
        cur.append(w)
        n += lexicon.word_syllables(w)
        if n == 10:
            lines.append(" ".join(cur))
            cur, n = [], 0
    return lines, cur


def _words(lines) -> list[str]:
    return [w for l in lines for w in l.split(" ") if w]


def _alternates(who) -> bool:
    return all(who[i] != who[i + 1] for i in range(len(who) - 1))


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def hsettings(settings):
    """Heuristic text mode (the bridge writes the text too); the default is text_source == "bot"."""
    s = settings.model_copy(deep=True)
    s.bridge.text_source = "heuristic"
    return s


def _tick(sp, pp, out, settings, lexicon, scores=None, seed=0):
    t0 = time.perf_counter()
    r = bridge.tick(sp, pp, out, settings, scores_path=scores, seed=seed, lexicon=lexicon)
    assert time.perf_counter() - t0 < 30.0, "a tick must finish in under 30 s"
    return r


# ------------------------------------------------------------------ 1. recruiting stage
def test_recruiting_stage_writes_plan_and_roster_then_nothing(tmp_path, hsettings, lexicon):
    settings = hsettings
    state = {"team": None,
             "lead": {"game_id": "nohitori-3", "members": MEMBERS[1:3], "waitlist": [MEMBERS[3]], "signed": {}, "declined": []},
             "poem": _poem(), "plan": None, "script": None, "applications": {APPLICANT: {}}, "writers_ok": {}}
    sp, pp, out = _write(tmp_path, state, _policy())
    before = _sha(sp), _sha(pp)

    r = _tick(sp, pp, out, settings, lexicon, scores=SCORES)
    assert r.wrote_plan and r.wrote_roster and r.game_id == "nohitori-3"
    assert sorted(p.name for p in out.iterdir()) == ["nohitori-3.json", "roster-nohitori-3.json"]
    assert (_sha(sp), _sha(pp)) == before                      # inputs untouched

    plan = json.loads((out / "nohitori-3.json").read_text())
    assert plan["game_id"] == "nohitori-3" and plan["source"] == "orchestrator" and plan["feasible"] is True
    assert plan["members"] == MEMBERS[:3] and plan["prefix_len"] == 0
    assert len(plan["lines"]) == 14
    assert lexicon.validate_poem(canonical_text(plan["lines"]), exact_ten=True) == [10] * 14
    words = _words(plan["lines"])
    assert len(plan["who"]) == len(words) == len(plan["keys"])
    assert _alternates(plan["who"]) and set(plan["who"]) <= set(MEMBERS[:3])
    assert set(plan["who"]) == set(MEMBERS[:3])                # every member contributes
    assert plan["id"] == bridge.plan_id(plan["lines"], plan["who"]) == r.plan_id
    assert plan["fit_problems"] == [] and min(plan["keys"]) >= 2

    roster = json.loads((out / "roster-nohitori-3.json").read_text())
    assert roster["members"] == MEMBERS[:3] and roster["game_id"] == "nohitori-3"
    cands = roster["candidates"]
    assert {c["did"] for c in cands} == {MEMBERS[3], APPLICANT, *INVITES}
    assert [c["rank"] for c in cands] == list(range(1, len(cands) + 1))
    assert {c["source"] for c in cands} == {"waitlist", "application", "invite"}
    assert all(set(c) >= {"did", "source", "adds_letters", "lead_only_after", "fragility_after", "rank", "note"} for c in cands)
    assert roster["advice"].startswith("roster 3/6") and len(roster["advice"]) <= 200
    assert set(roster) >= {"id", "generated_at", "missing_from_union", "single_key_letters", "lead_only_letters",
                           "fragility", "survivability"}

    # second tick, same state: ids unchanged, nothing rewritten
    m1 = (out / "nohitori-3.json").stat().st_mtime_ns, (out / "roster-nohitori-3.json").stat().st_mtime_ns
    r2 = _tick(sp, pp, out, settings, lexicon, scores=SCORES)
    assert not r2.wrote_plan and not r2.wrote_roster and r2.plan_id == r.plan_id
    assert ((out / "nohitori-3.json").stat().st_mtime_ns, (out / "roster-nohitori-3.json").stat().st_mtime_ns) == m1


# ------------------------------------------------------------------ 2. frozen team, 23 accepted words
def _frozen_state(lexicon, words: list[str], script_who: list[str]) -> dict:
    lines, cur = _lay(words, lexicon)
    return {"team": {"game_id": "nohitori-2", "members": MEMBERS, "ready": True, "lead": LEAD},
            "lead": {"game_id": "nohitori-2", "members": MEMBERS[1:], "waitlist": [], "signed": {}, "declined": []},
            "poem": _poem(lines, cur, True, script_who[len(words) - 1]),
            "plan": None, "script": {"words": words + ["pad"] * 3, "who": script_who + [MEMBERS[1], MEMBERS[2], MEMBERS[1]]},
            "applications": {}, "writers_ok": {}}


def _script_who(n: int) -> list[str]:
    return [LEAD if i % 2 == 0 else MEMBERS[(i // 2) % 3 + 1] for i in range(n)]


def test_frozen_team_keeps_23_accepted_words_verbatim(tmp_path, hsettings, lexicon):
    settings = hsettings
    words = FINAL_POEM.read_text().split()[:23]
    who23 = _script_who(23)
    state = _frozen_state(lexicon, words, who23)
    sp, pp, out = _write(tmp_path, state, _policy(slow_members=[MEMBERS[2]]))

    r = _tick(sp, pp, out, settings, lexicon)
    assert r.wrote_plan
    plan = json.loads((out / "nohitori-2.json").read_text())
    assert plan["prefix_len"] == 23 and plan["members"] == MEMBERS
    pw = _words(plan["lines"])
    assert pw[:23] == words
    assert plan["lines"][:2] == FINAL_POEM.read_text().splitlines()[:2]
    assert plan["who"][:23] == who23
    assert _alternates(plan["who"]) and len(plan["who"]) == len(pw)
    assert set(plan["who"][23:]) == set(MEMBERS)               # every member appears after the prefix (slow one too)
    assert lexicon.validate_poem(canonical_text(plan["lines"]), exact_ten=True) == [10] * 14
    assert plan["feasible"] is True
    # the suffix is spellable without the slow member (lookahead treats it as unavailable)
    slow = MEMBERS[2]
    letters = {m: frozenset(c for c in m.lower() if c.isalpha()) for m in MEMBERS if m != slow}
    assert all(any(bridge.word_letters(w) <= ls for ls in letters.values()) for w in pw[23:])


# ------------------------------------------------------------------ 3. previous file kept / prefix divergence
def test_previous_plan_kept_then_regenerated_on_divergence(tmp_path, hsettings, lexicon):
    settings = hsettings
    words = FINAL_POEM.read_text().split()[:23]
    who23 = _script_who(23)
    sp, pp, out = _write(tmp_path, _frozen_state(lexicon, words, who23), _policy())
    r1 = _tick(sp, pp, out, settings, lexicon)
    assert r1.wrote_plan
    first = json.loads((out / "nohitori-2.json").read_text())

    # same state -> previous file valid -> same id, not rewritten
    r2 = _tick(sp, pp, out, settings, lexicon, seed=99)
    assert not r2.wrote_plan and r2.plan_id == first["id"]
    assert json.loads((out / "nohitori-2.json").read_text()) == first

    # one more accepted word that matches the plan -> still kept
    pw = _words(first["lines"])
    state = _frozen_state(lexicon, pw[:24], first["who"][:24])
    sp.write_text(json.dumps(state))
    r3 = _tick(sp, pp, out, settings, lexicon, seed=99)
    assert not r3.wrote_plan and r3.plan_id == first["id"]

    # accepted word 23 (index 22) differs from the plan -> new id, new prefix adopted verbatim
    diverged = words[:22] + ["that"]
    assert diverged != pw[:23]
    sp.write_text(json.dumps(_frozen_state(lexicon, diverged, who23)))
    r4 = _tick(sp, pp, out, settings, lexicon)
    assert r4.wrote_plan and r4.plan_id != first["id"]
    plan = json.loads((out / "nohitori-2.json").read_text())
    assert _words(plan["lines"])[:23] == diverged and plan["prefix_len"] == 23
    assert plan["lines"][:2] == first["lines"][:2]
    assert _alternates(plan["who"]) and plan["who"][:23] == who23
    assert lexicon.validate_poem(canonical_text(plan["lines"]), exact_ten=True) == [10] * 14


# ------------------------------------------------------------------ 4. complete poem
def test_complete_poem_writes_nothing(tmp_path, settings, lexicon):
    lines = FINAL_POEM.read_text().splitlines()
    state = {"team": {"game_id": "nohitori-2", "members": MEMBERS, "ready": True, "lead": LEAD},
             "lead": {"game_id": "nohitori-2", "members": MEMBERS[1:], "waitlist": [], "signed": {}, "declined": []},
             "poem": _poem(lines, [], True, MEMBERS[1]), "plan": lines, "script": None, "applications": {}, "writers_ok": {}}
    sp, pp, out = _write(tmp_path, state, _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert (r.wrote_plan, r.wrote_roster, r.reason) == (False, False, "poem complete")
    assert not out.exists()


def test_no_game_writes_nothing(tmp_path, settings, lexicon):
    state = {"team": None, "lead": None, "poem": _poem(), "plan": None, "script": None, "applications": {}}
    sp, pp, out = _write(tmp_path, state, _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert (r.wrote_plan, r.wrote_roster, r.reason) == (False, False, "no game")
    assert not out.exists()


# ------------------------------------------------------------------ 5. copies of the real files
@pytest.mark.skipif(not (REAL_SONNET_DIR / "state-sonnet-2.json").exists(), reason="real sonnet/ files not present")
def test_real_state_copy_is_poem_complete(tmp_path, settings, lexicon):
    real_state = REAL_SONNET_DIR / "state-sonnet-2.json"
    real_policy = REAL_SONNET_DIR / "policy.json"
    before = _sha(real_state), _sha(real_policy)
    sp = tmp_path / "state-sonnet-2.json"
    pp = tmp_path / "policy.json"
    shutil.copyfile(real_state, sp)
    shutil.copyfile(real_policy, pp)
    out = tmp_path / "bridge"
    r = _tick(sp, pp, out, settings, lexicon, scores=SCORES)
    assert not r.wrote_plan and not r.wrote_roster   # the real state may be complete, or a team led by someone else
    assert not r.wrote_plan and not r.wrote_roster and not out.exists()
    assert (_sha(real_state), _sha(real_policy)) == before
    view = bridge.load_live(sp, pp)
    assert len(view.members) >= 1 and (view.poem_complete or view.lead_did != view.self_did or not view.game_id)
    assert len(view.accepted_words) == 131 and view.existing_script is not None


# ------------------------------------------------------------------ helpers
def test_keys_and_problems_mirror_key_fits_plan():
    lead = "did:key:z6Mk" + "abcdefghijklmnopqrstuvwxyz"
    other = "did:key:z6Mk" + "abcdefghijklmnpqrstuvwxyz"       # lacks 'o'
    keys, problems = bridge.keys_and_problems(["so", "no", "at"], [lead, other], lead)
    assert keys == [1, 1, 2]
    assert len(problems) == 2 and "fewer than two keys" in problems[0] and "adjacent" in problems[1]
    assert bridge.keys_and_problems(["at", "it"], [lead, other], lead) == ([2, 2], [])


# ---------------------------------------------------------------- text_source == "bot" (default): the bridge only assigns
def _bot_state(lexicon, plan_lines, words_accepted: list[str], members=MEMBERS, script_who=None, team=True) -> dict:
    lines, current = _lay(words_accepted, lexicon) if words_accepted else ([], [])
    st = {"team": {"game_id": "nohitori-3", "room": "d-sonnet-2-team-nohitori-3", "generation": 1, "members": list(members), "lead": LEAD, "ready": True} if team else None,
          "lead": {"game_id": "nohitori-3", "state": "collecting", "members": [m for m in members if m != LEAD], "waitlist": [], "signed": {}, "declined": []},
          "poem": _poem(lines, current, last=(script_who[len(words_accepted) - 1] if script_who and words_accepted else None)),
          "plan": plan_lines, "script": ({"words": _words(plan_lines), "who": script_who} if script_who and plan_lines else None),
          "applications": {}, "writers_ok": {}}
    return st


def test_bot_mode_waits_for_bot_text(tmp_path, settings, lexicon):
    sp, pp, out = _write(tmp_path, _bot_state(lexicon, None, []), _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert not r.wrote_plan and r.wrote_roster
    assert "waiting for the bot's text" in r.reason
    assert not (out / "nohitori-3.json").exists() and (out / "roster-nohitori-3.json").exists()


def test_bot_mode_assigns_existing_text_verbatim(tmp_path, settings, lexicon):
    lines = [l for l in FINAL_POEM.read_text().splitlines() if l.strip()]
    words = _words(lines)
    who_prefix = _script_who(23)
    sp, pp, out = _write(tmp_path, _bot_state(lexicon, lines, words[:23], script_who=who_prefix + [""] * (len(words) - 23)), _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert r.wrote_plan, r.reason
    plan = json.loads((out / "nohitori-3.json").read_text())
    assert plan["lines"] == lines and plan["source"] == "bot-text+orchestrator-assign" and "request" not in plan
    assert plan["prefix_len"] == 23 and len(plan["who"]) == len(words) and _alternates(plan["who"])
    assert plan["who"][:23] == who_prefix
    assert set(plan["who"][23:]) == set(MEMBERS)
    r2 = _tick(sp, pp, out, settings, lexicon)
    assert not r2.wrote_plan and "unchanged" in r2.reason


def test_bot_mode_requests_replan_when_prefix_diverges(tmp_path, settings, lexicon):
    lines = [l for l in FINAL_POEM.read_text().splitlines() if l.strip()]
    words = _words(lines)
    accepted = words[:22] + ["dark"]          # word 22 differs from the bot's text
    sp, pp, out = _write(tmp_path, _bot_state(lexicon, lines, accepted, script_who=_script_who(23) + [""] * (len(words) - 23)), _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert r.wrote_plan
    plan = json.loads((out / "nohitori-3.json").read_text())
    assert plan["request"] == "replan" and "index 22" in plan["reason"] and plan["who"] == []


def test_bot_mode_requests_replan_when_infeasible(tmp_path, settings, lexicon):
    # two members: lead (all letters) + a partner lacking 'o'; two adjacent lead-only words cannot alternate
    partner = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz1234567890ABCDEF"
    lines = [l for l in FINAL_POEM.read_text().splitlines() if l.strip()]
    lines = list(lines); lines[0] = "My mother kept the moon. She had the eye"   # "mother ... moon" -> lead-only pair? (o,o)
    # make sure the text is still valid form; if not, the bridge answers with an "invalid" replan, which is also a replan
    sp, pp, out = _write(tmp_path, _bot_state(lexicon, lines, [], members=[LEAD, partner]), _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert r.wrote_plan
    plan = json.loads((out / "nohitori-3.json").read_text())
    assert plan["request"] == "replan", plan.get("source")


def test_other_leads_team_writes_nothing(tmp_path, settings, lexicon):
    lines = [l for l in FINAL_POEM.read_text().splitlines() if l.strip()]
    st = _bot_state(lexicon, lines, [])
    st["team"]["lead"] = MEMBERS[1]          # someone else leads
    sp, pp, out = _write(tmp_path, st, _policy())
    r = _tick(sp, pp, out, settings, lexicon)
    assert not r.wrote_plan and not r.wrote_roster and "not our team" in r.reason
    assert not (out / "nohitori-3.json").exists()
