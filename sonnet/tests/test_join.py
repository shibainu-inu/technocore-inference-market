"""チーム合流・編成の経路: results の setup.v1 で lead を room_ready にする、募集への自発応募、results 経由の部屋再設定。
ネットも claude も呼ばない。"""
import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import agent

POLICY = json.load(open(os.path.join(os.path.dirname(HERE), "policy.json")))
ME = POLICY["did"]; CID = POLICY["contest_id"]; TEAM = f"d-{CID}-team-"; REF = POLICY["referee_did"]
DISC = POLICY["rooms"]["discovery"]; RESULTS = POLICY["rooms"]["results"]
LEAD = "did:key:z6MkjED8WPaYvu2pmr8qRvszf95ankNCBLmoyexoepTmGhcj"
LEAD2 = "did:key:z6MkwfnckxULjn9dPvoPnJSPbc7aWNegeXrirWzBLpfVgqSM"
OTHERS = ["did:key:z6MkvBBoP3VST9xF833FLRLdZRG8d92uXahXgAW3BR9W9Uxu", "did:key:z6MktrGB8UZGApSNcRuhxTbyHdf8aGVS5ruLMJZhWMTg9Njo"]
BEFORE = "2026-09-11T09:00:00Z"   # 開始 12:00Z より前


class RecordingPost:
    def __init__(self): self.calls = []
    def __call__(self, room, text, kind, allow_dids=()):
        self.calls.append((room, text, kind)); return 1
    def kinds(self): return [c[2] for c in self.calls]


def fresh(auto=None):
    p = json.loads(json.dumps(POLICY))
    p["auto"] = {k: False for k in p["auto"]}
    if auto: p["auto"].update(auto)
    agent.STATE_PATH = os.path.join(HERE, "_state_join.json")
    agent.ATTENTION_PATH = os.path.join(HERE, "_attention_join.md")
    agent.LOG_PATH = os.path.join(HERE, "_agent_join.log")
    agent.INBOX_DIR = os.path.join(HERE, "_inbox_join")
    for f in (agent.STATE_PATH, agent.ATTENTION_PATH):
        if os.path.exists(f): os.remove(f)
    agent._ATT_COUNT.clear()
    open(agent.ATTENTION_PATH, "w").close()
    a = agent.Agent(p); a.save = lambda: None; a.sync_llm = True
    a.st["referee"] = REF; a.st["registered"] = {"seq": 43231}; a.key = object()
    a.start_reader = lambda room: None; a.replay_room = lambda room: None
    return a


def att(): return open(agent.ATTENTION_PATH).read()


def setup_msg(seq, gid, gen=1, room=None):
    j = {"contest_id": CID, "game_id": gid, "poem_room": room or TEAM + gid, "request_id": f"setup-{gid}", "room_generation": gen, "type": "sonnet.setup.v1"}
    return {"seq": seq, "ts": "2026-09-12T23:05:27Z", "from": REF, "_sig_ok": True, "_room": RESULTS, "text": json.dumps(j)}


def recruit_msg(seq, gid, frm, ts="2026-09-13T00:21:39Z", sig=True):
    j = {"type": "sonnet.recruit.v1", "contest_id": CID, "game_id": gid, "request_id": f"recruit-{gid}-{seq}", "text": f"OPEN SEATS on {gid}"}
    return {"seq": seq, "ts": ts, "from": frm, "_sig_ok": sig, "_room": DISC, "text": json.dumps(j)}


class Join(unittest.TestCase):
    def setUp(self):
        self._now = agent.utc_now
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T01:00:00Z")   # 募集から 40 分後
    def tearDown(self):
        agent.utc_now = self._now

    # ---- lead: results の setup.v1 で room_ready になり募集文が出る ----
    def test_results_setup_moves_lead_to_room_ready_and_intro_posts(self):
        a = fresh({"lead_team": True}); rp = RecordingPost(); a.post = rp
        a.st["lead"] = {"game_id": "g", "request_id": "room-1", "state": "allocated", "at": "t", "members": [], "signed": {}, "declined": [], "poem_room": TEAM + "g"}
        a.handle(setup_msg(361, "g"))
        self.assertEqual(a.st["lead"]["state"], "room_ready"); self.assertEqual(a.st["lead"]["generation"], 1)
        self.assertEqual(a.st["setups"]["g"]["generation"], 1)
        a.maybe_lead()
        self.assertEqual(rp.kinds(), ["lead-intro"]); self.assertIn("yes-g", rp.calls[0][1]); self.assertIn(ME, rp.calls[0][1])
        a.maybe_lead(); self.assertEqual(len(rp.calls), 1)   # intro_repeat_hours 以内は繰り返さない

    def test_setup_for_other_games_or_bad_room_does_not_touch_lead(self):
        a = fresh({"lead_team": True})
        a.st["lead"] = {"game_id": "g", "request_id": "room-1", "state": "allocated", "at": "t", "members": [], "signed": {}, "declined": [], "poem_room": TEAM + "g"}
        a.handle(setup_msg(1, "h"))
        a.handle(setup_msg(2, "g", room=TEAM + "other"))        # poem_room が game_id と合わない
        m = setup_msg(3, "g"); m["from"] = LEAD; a.handle(m)     # 審判でない
        m = setup_msg(4, "g"); m["_sig_ok"] = False; a.handle(m)  # 署名不成立
        self.assertEqual(a.st["lead"]["state"], "allocated"); self.assertNotIn("g", a.st.get("setups", {}))
        self.assertEqual(a.st["setups"]["h"]["room"], TEAM + "h")

    # ---- 募集への自発応募 ----
    def ready(self, auto=None):
        a = fresh(dict({"apply_recruits": True}, **(auto or {}))); rp = RecordingPost(); a.post = rp
        a.st.setdefault("writers_ok", {})[LEAD] = 100; a.st["first_seen"][LEAD] = BEFORE
        a.handle(setup_msg(15, "g")); a.handle(recruit_msg(24729, "g", LEAD))
        return a, rp

    def test_applies_to_a_fresh_recruit_from_a_receipted_lead(self):
        a, rp = self.ready()
        a.maybe_apply_recruits()
        self.assertEqual(rp.kinds(), ["apply", "apply-json"])
        prose, frame = rp.calls[0][1], json.loads(rp.calls[1][1])
        self.assertTrue(prose.startswith("yes-g")); self.assertIn(ME, prose); self.assertIn("43231", prose)
        self.assertEqual(frame["type"], "sonnet.application.v1"); self.assertEqual(frame["game_id"], "g")
        self.assertEqual(frame["room_generation"], 1); self.assertEqual(frame["poem_room"], TEAM + "g"); self.assertEqual(frame["did"], ME)
        ap = a.application_for("g"); self.assertEqual(ap["lead_did"], LEAD); self.assertEqual(ap["source"], "recruit")
        a._apply_at = 0; a.maybe_apply_recruits(); self.assertEqual(len(rp.calls), 2)   # 二重応募しない
        # 応募後にリーダーが自分を載せたロースターを出したら署名する（既存経路）
        agent.read_json = lambda room, wait: ([], {"generation": 1})
        a.p["auto"]["sign_roster"] = True
        roster = {"type": "sonnet.roster.v1", "contest_id": CID, "game_id": "g", "poem_room": TEAM + "g", "room_generation": 1, "members": [LEAD, ME] + OTHERS}
        a.handle({"seq": 30, "ts": "t", "from": LEAD, "_sig_ok": True, "_room": DISC, "text": json.dumps(roster)})
        self.assertEqual(rp.kinds(), ["apply", "apply-json", "roster"]); self.assertEqual(a.st["team"]["game_id"], "g")

    def test_does_not_apply_when_conditions_fail(self):
        cases = {
            "auto off": lambda a: a.p["auto"].update({"apply_recruits": False}),
            "no key": lambda a: setattr(a, "key", None),
            "not registered": lambda a: a.st.update({"registered": None}),
            "have team": lambda a: a.st.update({"team": {"game_id": "z", "room": TEAM + "z", "generation": 1, "members": [], "ready": False}}),
            "lead not receipted writer": lambda a: a.st["writers_ok"].pop(LEAD),
            "lead ignored": lambda a: a.p["ignore_senders"].append(LEAD),
            "game dropped": lambda a: a.st.setdefault("dropped", []).append("g"),
            "our own lead game": lambda a: a.st.update({"lead": {"game_id": "g", "state": "room_ready", "members": [], "poem_room": TEAM + "g"}}),
            "no referee setup": lambda a: a.st["setups"].pop("g"),
            "recruit stale": lambda a: a.st["teams"]["g"].update({"recruit_ts": "2026-09-12T20:00:00Z"}),
            "recruit unsigned": lambda a: (a.st["teams"]["g"].pop("recruit_seq"), a.handle(recruit_msg(24730, "g", LEAD, sig=False))),
            "cap reached": lambda a: a.st.update({"applications": {k: {"game_id": k, "lead_did": LEAD2, "at": "t"} for k in ("p", "q", "r")}}),
            "lead too new": lambda a: a.st["first_seen"].update({LEAD: "2026-09-13T00:59:00Z"}),
        }
        for name, mut in cases.items():
            a, rp = self.ready(); mut(a); a.maybe_apply_recruits()
            self.assertEqual(rp.calls, [], name)

    def test_lead_seen_only_after_opening_is_allowed_by_policy_age(self):
        a, rp = self.ready(); a.st["first_seen"][LEAD] = "2026-09-12T00:21:04Z"   # 開始後だが 600 秒以上前
        self.assertFalse(a.p["accept"]["require_lead_seen_before_opening"])
        a.maybe_apply_recruits(); self.assertEqual(rp.kinds(), ["apply", "apply-json"])

    def test_prefers_pre_start_lead_then_newest_recruit_one_per_call(self):
        a, rp = self.ready()
        a.st["writers_ok"][LEAD2] = 101; a.st["first_seen"][LEAD2] = "2026-09-12T00:00:00Z"   # 開始後に初観測
        a.handle(setup_msg(16, "h")); a.handle(recruit_msg(29000, "h", LEAD2))               # より新しい募集
        a.maybe_apply_recruits()
        self.assertEqual([json.loads(c[1])["game_id"] for c in rp.calls if c[2] == "apply-json"], ["g"])   # 開始前リーダー優先
        a._apply_at = 0; a.maybe_apply_recruits()
        self.assertEqual([json.loads(c[1])["game_id"] for c in rp.calls if c[2] == "apply-json"], ["g", "h"])
        self.assertEqual(sorted(a.applications()), ["g", "h"])

    def test_apply_post_failure_records_nothing(self):
        a, rp = self.ready()
        def boom(room, text, kind, allow_dids=()): raise RuntimeError("post refused: test")
        a.post = boom; a.maybe_apply_recruits()
        self.assertIsNone(a.application_for("g")); self.assertIn("application to g failed", att())

    # ---- results 経由の部屋再設定 ----
    def test_results_resetup_of_our_signed_team_resigns(self):
        a = fresh({"sign_roster": True}); rp = RecordingPost(); a.post = rp
        a.st["team"] = {"game_id": "g", "room": TEAM + "g", "generation": 1, "members": [LEAD, ME] + OTHERS, "lead": LEAD,
                        "roster_signed": 7, "ready": False, "signed_generation": 1}
        a.handle(setup_msg(400, "g", gen=2))
        self.assertEqual(rp.kinds(), ["roster"]); self.assertEqual(json.loads(rp.calls[0][1])["room_generation"], 2)
        self.assertEqual(a.st["team"]["generation"], 2); self.assertEqual(a.st["team"]["signed_generation"], 2); self.assertFalse(a.st["team"]["ready"])
        self.assertIn("re-bound from generation 1 to 2", att())
        a.handle(setup_msg(401, "g", gen=2)); self.assertEqual(len(rp.calls), 1)   # 同じ generation の再掲では何もしない

    def test_results_resetup_when_we_lead_is_manual(self):
        a = fresh({"lead_team": True}); rp = RecordingPost(); a.post = rp
        a.st["team"] = {"game_id": "g", "room": TEAM + "g", "generation": 1, "members": [ME, LEAD] + OTHERS, "lead": ME, "roster_signed": None, "ready": False}
        a.handle(setup_msg(400, "g", gen=2))
        self.assertEqual(rp.calls, []); self.assertEqual(a.st["team"]["generation"], 2); self.assertIn("manual", att())

    # ---- 起動時の setup 同期 ----
    def test_sync_setups_reads_export_and_advances_lead(self):
        a = fresh({"lead_team": True})
        a.st["lead"] = {"game_id": "g", "request_id": "room-1", "state": "allocated", "at": "t", "members": [], "signed": {}, "declined": [], "poem_room": TEAM + "g"}
        good = setup_msg(361, "g"); good.pop("_sig_ok"); good.pop("_room")
        fake = dict(good, seq=362, **{"from": LEAD})
        body = "garbage\n" + json.dumps(good) + "\n" + json.dumps(fake) + "\n"
        old_get, old_vs = agent.fm.http_get, agent.verify_sig
        agent.fm.http_get = lambda url, timeout=30: (200, body)
        agent.verify_sig = lambda room, m: m["seq"] == 361
        try:
            a.sync_setups()
        finally:
            agent.fm.http_get, agent.verify_sig = old_get, old_vs
        self.assertEqual(a.st["lead"]["state"], "room_ready"); self.assertEqual(a.st["setups"]["g"]["seq"], 361)


if __name__ == "__main__":
    unittest.main()
