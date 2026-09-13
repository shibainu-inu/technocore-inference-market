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


def roster_agent_like(tc):
    """署名条件を満たした bot（応募済み・登録済み・鍵あり・部屋 generation 1）"""
    a = fresh({"sign_roster": True}); rp = RecordingPost(); a.post = rp
    a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": agent.iso(), "manual": True}}; a.st["agreed"] = a.st["applications"]["g"]
    agent.read_json = lambda room, wait: ([], {"generation": 1})
    a.withdraw_others = lambda gid: None
    return a, rp


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

    # ---- 署名後に凍結しないロースターの損切り ----
    def stuck_agent(self, auto=None, lead=LEAD):
        a = fresh(dict({"withdraw_stuck": True}, **(auto or {}))); rp = RecordingPost(); a.post = rp
        a.st["team"] = {"game_id": "g", "room": TEAM + "g", "generation": 1, "members": [LEAD, ME] + OTHERS, "lead": lead,
                        "roster_signed": 7, "ready": False, "signed_generation": 1, "signed_at": "2026-09-13T01:00:00Z"}
        a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": "2026-09-13T00:30:00Z"}}; a.st["agreed"] = a.st["applications"]["g"]
        a.readdress_recent_offers = lambda: None
        return a, rp

    def test_stuck_roster_warns_then_withdraws(self):
        a, rp = self.stuck_agent()
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T02:00:00Z"); a.check_stuck_roster()      # 1.0h: 何もしない
        self.assertEqual(rp.calls, []); self.assertNotIn("CRITICAL", att())
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T02:40:00Z"); a.check_stuck_roster()      # 1.67h: 警告のみ
        self.assertEqual(rp.calls, []); self.assertIn("still not roster_ready", att()); self.assertIsNotNone(a.st["team"])
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T04:05:00Z"); a.check_stuck_roster()      # 3.08h: 取り下げ
        self.assertEqual(rp.kinds(), ["withdraw"]); w = json.loads(rp.calls[0][1])
        self.assertEqual((w["type"], w["contest_id"], w["game_id"]), ("sonnet.withdraw.v1", CID, "g")); self.assertIn("request_id", w)
        self.assertIsNone(a.st["team"]); self.assertEqual(a.applications(), {}); self.assertIn("g", a.st["dropped"]); self.assertEqual(a.st["intro_at"], 0)
        self.assertEqual(a.st["dropped"].count("g"), 1)
        a.check_stuck_roster(); self.assertEqual(len(rp.calls), 1)   # team が無ければ何もしない

    def test_stuck_roster_no_withdraw_when_ready_or_we_lead_or_flag_off(self):
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T05:00:00Z")
        a, rp = self.stuck_agent(); a.st["team"]["ready"] = True; a.check_stuck_roster(); self.assertEqual(rp.calls, [])
        a, rp = self.stuck_agent(lead=ME); a.check_stuck_roster(); self.assertEqual(rp.calls, []); self.assertIsNotNone(a.st["team"])
        a, rp = self.stuck_agent({"withdraw_stuck": False}); a.check_stuck_roster()
        self.assertEqual(rp.calls, []); self.assertIsNotNone(a.st["team"]); self.assertIn("withdraw_stuck=False", att())

    def test_stuck_roster_signed_at_falls_back_to_sent_log(self):
        a, rp = self.stuck_agent(); a.st["team"].pop("signed_at")
        a.st["sent"] = [{"ts": "2026-09-13T00:00:00Z", "kind": "roster", "room": DISC, "seq": 7, "text": "{}"}]
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T03:30:00Z"); a.check_stuck_roster()
        self.assertEqual(a.st["team"] and a.st["team"].get("signed_at"), None)   # 3.5h → 取り下げ済み
        self.assertEqual(rp.kinds(), ["withdraw"])

    def test_stuck_roster_withdraw_post_failure_keeps_team(self):
        a, rp = self.stuck_agent()
        def boom(room, text, kind, allow_dids=()): raise RuntimeError("post refused: test")
        a.post = boom; agent.utc_now = lambda: agent.parse_iso("2026-09-13T05:00:00Z"); a.check_stuck_roster()
        self.assertIsNotNone(a.st["team"]); self.assertIn("withdraw post failed", att())

    # ---- リーダーによるメンバー差し替えへの再同意 ----
    def signed_team(self):
        a = fresh({"sign_roster": True}); rp = RecordingPost(); a.post = rp
        a.st["team"] = {"game_id": "g", "room": TEAM + "g", "generation": 1, "members": [LEAD, OTHERS[0], OTHERS[1], ME], "lead": LEAD,
                        "roster_signed": 7, "ready": False, "signed_generation": 1, "signed_at": "2026-09-13T00:00:00Z", "stuck_warned": True}
        a.st.setdefault("writers_ok", {}).update({OTHERS[0]: 1, OTHERS[1]: 2})
        return a, rp

    def changed(self, **over):
        j = {"type": "sonnet.roster.v1", "contest_id": CID, "game_id": "g", "poem_room": TEAM + "g", "room_generation": 1,
             "members": [LEAD, LEAD2, OTHERS[1], ME]}
        j.update(over); return j

    def test_reconsent_to_leads_changed_roster(self):
        a, rp = self.signed_team()
        a.st["writers_ok"][LEAD2] = 3
        a.on_roster_for_us({"seq": 20, "from": LEAD, "ts": "t", "_sig_ok": True}, self.changed())
        self.assertEqual(rp.kinds(), ["withdraw", "roster"])
        wd, ro = json.loads(rp.calls[0][1]), json.loads(rp.calls[1][1])
        self.assertEqual((wd["type"], wd["game_id"]), ("sonnet.withdraw.v1", "g")); self.assertEqual(ro["members"], [LEAD, LEAD2, OTHERS[1], ME])
        t = a.st["team"]; self.assertEqual(t["members"], [LEAD, LEAD2, OTHERS[1], ME]); self.assertEqual(t["reconsents"], 1)
        self.assertEqual(t["source_seq"], 20); self.assertFalse(t["stuck_warned"]); self.assertNotEqual(t["signed_at"], "2026-09-13T00:00:00Z")
        self.assertIn("re-consented", att())
        # 他メンバーの写し（同内容）には何もしない
        a.on_roster_for_us({"seq": 21, "from": LEAD2, "ts": "t", "_sig_ok": True}, self.changed()); self.assertEqual(len(rp.calls), 2)

    def test_reconsent_refusals(self):
        cases = {
            "member without writer evidence": (lambda a: None, self.changed(), "without observed writer evidence"),
            "not from lead": (lambda a: a.st["writers_ok"].update({LEAD2: 3}), self.changed(), None),
            "drops us": (lambda a: a.st["writers_ok"].update({LEAD2: 3}), self.changed(members=[LEAD, LEAD2, OTHERS[0], OTHERS[1]]), "drops us"),
            "too many reconsents": (lambda a: (a.st["writers_ok"].update({LEAD2: 3}), a.st["team"].update({"reconsents": 3})), self.changed(), "reconsent_max"),
            "after ready": (lambda a: (a.st["writers_ok"].update({LEAD2: 3}), a.st["team"].update({"ready": True})), self.changed(), "after roster_ready"),
            "other generation": (lambda a: a.st["writers_ok"].update({LEAD2: 3}), self.changed(room_generation=2), "another room/generation"),
        }
        for name, (mut, j, needle) in cases.items():
            a, rp = self.signed_team(); mut(a)
            frm = OTHERS[1] if name == "not from lead" else LEAD
            a.on_roster_for_us({"seq": 20, "from": frm, "ts": "t", "_sig_ok": True}, j)
            self.assertEqual(rp.calls, [], name); self.assertEqual(a.st["team"]["members"], [LEAD, OTHERS[0], OTHERS[1], ME], name)
            if needle: self.assertIn(needle, att(), name)

    def test_pending_roster_is_reconsented_once_evidence_arrives(self):
        a, rp = self.signed_team()
        a.on_roster_for_us({"seq": 20, "from": LEAD, "ts": "t", "_sig_ok": True}, self.changed())   # LEAD2 の証拠なし → 保留
        self.assertEqual(rp.calls, []); self.assertEqual(a.st["team"]["pending_roster"]["m"]["seq"], 20)
        a.recheck_pending_roster(); self.assertEqual(rp.calls, [])                                    # まだ証拠なし
        rc_ = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "roster-l2", "sender_did": LEAD2, "roster_ready": False}
        a.handle({"seq": 25, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})   # 審判が LEAD2 の同意を受理
        a.recheck_pending_roster()
        self.assertEqual(rp.kinds(), ["withdraw", "roster"]); self.assertIsNone(a.st["team"]["pending_roster"])
        self.assertEqual(a.st["team"]["members"], [LEAD, LEAD2, OTHERS[1], ME])

    def test_roster_with_ignored_member_is_refused_and_not_kept_pending(self):
        a, rp = self.signed_team(); a.p["ignore_senders"].append(LEAD2); a.st["writers_ok"][LEAD2] = 3
        a.on_roster_for_us({"seq": 20, "from": LEAD, "ts": "t", "_sig_ok": True}, self.changed())
        self.assertEqual(rp.calls, []); self.assertIn("includes an ignored DID", att()); self.assertIsNone(a.st["team"].get("pending_roster"))
        a.recheck_pending_roster(); self.assertEqual(rp.calls, [])

    def test_referee_roster_receipt_marks_writer(self):
        a = fresh()
        rc_ = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "roster-x", "sender_did": LEAD2, "roster_ready": False, "state_hash": "h"}
        a.handle({"seq": 5, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertIn(LEAD2, a.st["writers_ok"])
        rc_["status"] = "rejected"; rc_["sender_did"] = OTHERS[0]
        a.handle({"seq": 6, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertNotIn(OTHERS[0], a.st["writers_ok"])

    def test_resync_team_roster_reconsents_from_export(self):
        a, rp = self.signed_team()
        rc_ = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "roster-l2", "sender_did": LEAD2, "roster_ready": False}
        rows = [{"seq": 30, "ts": "t", "from": REF, "text": json.dumps(rc_)},
                {"seq": 31, "ts": "t", "from": LEAD, "text": json.dumps(self.changed(members=[LEAD, LEAD2, ME, OTHERS[1]]))},   # 古い差し替え
                {"seq": 32, "ts": "t", "from": LEAD, "text": json.dumps(self.changed())}]                                      # 最新
        body = "\n".join(json.dumps(r) for r in rows) + "\n"
        old_get, old_vs = agent.fm.http_get, agent.verify_sig
        agent.fm.http_get = lambda url, timeout=30: (200, body); agent.verify_sig = lambda room, m: True
        try:
            a.resync_team_roster()
        finally:
            agent.fm.http_get, agent.verify_sig = old_get, old_vs
        self.assertEqual(rp.kinds(), ["withdraw", "roster"]); self.assertEqual(a.st["team"]["members"], [LEAD, LEAD2, OTHERS[1], ME])
        self.assertEqual(a.st["team"]["source_seq"], 32); self.assertIn(LEAD2, a.st["writers_ok"])

    # ---- リーダーに席を外された ----
    def test_lead_roster_without_us_makes_us_withdraw_and_restore_seat_drops(self):
        a, rp = self.signed_team()
        a.st["dropped"] = ["old", "h", "k"]; a.st["dropped_for_seat"] = ["h", "k"]
        a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": "t"}}; a.st["agreed"] = a.st["applications"]["g"]
        a.readdress_recent_offers = lambda: None
        # 自分の署名より古いロースター、他人のロースター、他ゲームは無視
        a.handle({"seq": 5, "ts": "t", "from": LEAD, "_sig_ok": True, "_room": DISC, "text": json.dumps(self.changed(members=[LEAD, LEAD2] + OTHERS))})
        a.handle({"seq": 30, "ts": "t", "from": OTHERS[0], "_sig_ok": True, "_room": DISC, "text": json.dumps(self.changed(members=[LEAD, LEAD2] + OTHERS))})
        a.handle({"seq": 31, "ts": "t", "from": LEAD, "_sig_ok": True, "_room": DISC, "text": json.dumps(self.changed(game_id="z", poem_room=TEAM + "z", members=[LEAD, LEAD2] + OTHERS))})
        self.assertEqual(rp.calls, []); self.assertIsNotNone(a.st["team"])
        # リーダーの新しいロースターに自分がいない → withdraw して離脱、席のために落とした h, k を復活
        a.handle({"seq": 40, "ts": "t", "from": LEAD, "_sig_ok": True, "_room": DISC, "text": json.dumps(self.changed(members=[LEAD, LEAD2] + OTHERS))})
        self.assertEqual(rp.kinds(), ["withdraw"]); self.assertEqual(json.loads(rp.calls[0][1])["game_id"], "g")
        self.assertIsNone(a.st["team"]); self.assertEqual(a.applications(), {}); self.assertEqual(a.st["dropped"], ["old", "g"])
        self.assertNotIn("dropped_for_seat", a.st); self.assertIn("no longer lists us", att())

    def test_resync_detects_lead_roster_without_us(self):
        a, rp = self.signed_team(); a.readdress_recent_offers = lambda: None
        rows = [{"seq": 40, "ts": "t", "from": LEAD, "text": json.dumps(self.changed(members=[LEAD, LEAD2] + OTHERS))}]
        body = "\n".join(json.dumps(r) for r in rows) + "\n"
        old_get, old_vs = agent.fm.http_get, agent.verify_sig
        agent.fm.http_get = lambda url, timeout=30: (200, body); agent.verify_sig = lambda room, m: True
        try:
            a.resync_team_roster()
        finally:
            agent.fm.http_get, agent.verify_sig = old_get, old_vs
        self.assertEqual(rp.kinds(), ["withdraw"]); self.assertIsNone(a.st["team"])

    def test_readdress_requeues_recent_notes_to_us(self):
        a = fresh(); a.p["ignore_senders"].append(LEAD2)
        now = agent.utc_now()
        def ts(sec_ago): return agent.iso() if False else __import__("datetime").datetime.utcfromtimestamp(now - sec_ago).strftime("%Y-%m-%dT%H:%M:%SZ")
        note = lambda frm, target, text: {"type": "sonnet.note.v1", "contest_id": CID, "game_id": "h", "target_did": target, "request_id": "n", "text": text}
        rows = [{"seq": 1, "ts": ts(600), "from": LEAD, "text": json.dumps(note(LEAD, ME, "seat for you"))},          # 採用
                {"seq": 2, "ts": ts(600), "from": LEAD2, "text": json.dumps(note(LEAD2, ME, "ignored sender"))},     # 無視対象
                {"seq": 3, "ts": ts(5 * 3600), "from": LEAD, "text": json.dumps(note(LEAD, ME, "too old"))},          # 古い
                {"seq": 4, "ts": ts(600), "from": LEAD, "text": json.dumps(note(LEAD, OTHERS[0], "not us"))},        # 他人宛
                {"seq": 5, "ts": ts(600), "from": REF, "text": json.dumps(note(REF, ME, "referee"))},                # 審判
                {"seq": 6, "ts": ts(600), "from": OTHERS[1], "text": json.dumps(note(OTHERS[1], None, "@" + ME[-8:] + " hello"))}]  # @suffix
        body = "\n".join(json.dumps(r) for r in rows) + "\n"
        old_get, old_vs = agent.fm.http_get, agent.verify_sig
        agent.fm.http_get = lambda url, timeout=30: (200, body); agent.verify_sig = lambda room, m: m["seq"] != 6 or True
        try:
            a.readdress_recent_offers()
        finally:
            agent.fm.http_get, agent.verify_sig = old_get, old_vs
        self.assertEqual(sorted(m["seq"] for m in a.addressed), [1, 6]); self.assertTrue(all(m.get("_sig_ok") and "_at" in m for m in a.addressed))

    def test_operator_switches_undrop_and_readdress(self):
        a = fresh(); a.st["dropped"] = ["a", "b", "c"]; calls = []
        a.readdress_recent_offers = lambda: calls.append(1)
        p = json.loads(json.dumps(a.p)); p["undrop"] = ["b", "zzz"]; p["readdress_token"] = "t1"
        a.apply_operator_switches(p); a.apply_operator_switches(p)
        self.assertEqual(a.st["dropped"], ["a", "c"]); self.assertEqual(calls, [1])       # 同じ token では 1 回だけ
        p["readdress_token"] = "t2"; a.apply_operator_switches(p); self.assertEqual(calls, [1, 1])

    def test_withdraw_is_resent_until_receipted(self):
        a, rp = self.signed_team(); a.readdress_recent_offers = lambda: None
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T07:28:00Z")
        a.lose_team("test", withdraw=True)
        pw = a.st["pending_withdraw"]; self.assertEqual((pw["game_id"], pw["n"]), ("g", 1)); rid1 = pw["request_id"]
        pw["at"] = "2026-09-13T07:28:00Z"   # iso() は実時刻なので試験時刻に合わせる
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T07:33:00Z"); a.check_pending_withdraw(); self.assertEqual(len(rp.calls), 1)   # 5 分: まだ
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T07:39:00Z"); a.check_pending_withdraw()
        self.assertEqual(rp.kinds(), ["withdraw", "withdraw"]); self.assertNotEqual(a.st["pending_withdraw"]["request_id"], rid1); self.assertEqual(a.st["pending_withdraw"]["n"], 2)
        # 審判の受領（一括 receipts 形式でも可）で消える
        rc_ = {"type": "sonnet.receipts.v1", "receipts": [{"request_id": a.st["pending_withdraw"]["request_id"], "status": "accepted"}]}
        a.handle({"seq": 9, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertIsNone(a.st["pending_withdraw"])
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T08:30:00Z"); a.check_pending_withdraw(); self.assertEqual(len(rp.calls), 2)

    def test_withdraw_resend_gives_up_after_max(self):
        a, rp = self.signed_team(); a.readdress_recent_offers = lambda: None
        a.st["pending_withdraw"] = {"game_id": "g", "request_id": "w1", "at": "2026-09-13T06:00:00Z", "n": 3}
        agent.utc_now = lambda: agent.parse_iso("2026-09-13T07:00:00Z"); a.check_pending_withdraw()
        self.assertEqual(rp.calls, []); self.assertTrue(a.st["pending_withdraw"]["gave_up"]); self.assertIn("may still count as live", att())

    # ---- halftongue 本命: 合流を取りこぼさない ----
    def test_consent_rejection_of_our_roster_resends_withdraw_and_resigns(self):
        a, rp = self.signed_team(); a.st["team"]["roster_request_id"] = "roster-1"
        a.st["sent"] = [{"ts": agent.iso(), "kind": "withdraw", "room": DISC, "seq": 1, "text": json.dumps({"type": "sonnet.withdraw.v1", "game_id": "oldgame"})}]
        rc_ = {"type": "sonnet.receipt.v1", "status": "rejected", "reason": "consent: withdraw before changing", "request_id": "roster-1", "sender_did": ME}
        a.handle({"seq": 50, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertEqual(rp.kinds(), ["withdraw", "roster"]); self.assertEqual(json.loads(rp.calls[0][1])["game_id"], "oldgame")
        self.assertEqual(json.loads(rp.calls[1][1])["members"], [LEAD, OTHERS[0], OTHERS[1], ME])
        self.assertIsNotNone(a.st["team"]); self.assertEqual(a.st["team"]["consent_retries"], 1); self.assertNotEqual(a.st["team"]["roster_request_id"], "roster-1")
        self.assertNotIn("g", a.st.get("dropped", []))
        # 2 回目も consent なら再試行、3 回目は席を手放す
        rc_["request_id"] = a.st["team"]["roster_request_id"]
        a.handle({"seq": 51, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)}); self.assertEqual(len(rp.calls), 4)
        rc_["request_id"] = a.st["team"]["roster_request_id"]
        a.handle({"seq": 52, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertIsNone(a.st["team"]); self.assertIn("g", a.st["dropped"]); self.assertEqual(len(rp.calls), 4)

    def test_non_consent_rejection_still_releases_seat(self):
        a, rp = self.signed_team(); a.st["team"]["roster_request_id"] = "roster-1"
        rc_ = {"type": "sonnet.receipt.v1", "status": "rejected", "reason": "roster: writer required", "request_id": "roster-1", "sender_did": ME}
        a.handle({"seq": 50, "ts": "t", "from": REF, "_sig_ok": True, "_room": DISC, "text": json.dumps(rc_)})
        self.assertEqual(rp.calls, []); self.assertIsNone(a.st["team"]); self.assertIn("g", a.st["dropped"])

    def test_initial_signing_resends_unreceipted_withdraw_first(self):
        a, rp = roster_agent_like(self)
        a.st["pending_withdraw"] = {"game_id": "zzz", "request_id": "w1", "at": agent.iso(), "n": 1}
        a.st["sent"] = [{"ts": agent.iso(), "kind": "withdraw", "room": DISC, "seq": 1, "text": json.dumps({"type": "sonnet.withdraw.v1", "game_id": "zzz"})}]
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True},
                           {"type": "sonnet.roster.v1", "contest_id": CID, "game_id": "g", "poem_room": TEAM + "g", "room_generation": 1, "members": [LEAD, ME] + OTHERS})
        self.assertEqual(rp.kinds(), ["withdraw", "roster"]); self.assertEqual(json.loads(rp.calls[0][1])["game_id"], "zzz")
        # 未受領の withdraw が無ければ余計な投稿はしない
        a2, rp2 = roster_agent_like(self)
        a2.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True},
                            {"type": "sonnet.roster.v1", "contest_id": CID, "game_id": "g", "poem_room": TEAM + "g", "room_generation": 1, "members": [LEAD, ME] + OTHERS})
        self.assertEqual(rp2.kinds(), ["roster"])

    def test_trusted_sender_is_never_ignored_or_auto_ignored(self):
        a = fresh(); a.p["trusted_senders"] = [LEAD]; a.p["ignore_senders"].append(LEAD); a.st["auto_ignored"] = [LEAD]
        self.assertNotIn(LEAD, a.ignored())
        for i in range(25):
            a.note_broadcaster({"from": LEAD, "text": "same text every time"})
        self.assertEqual(a.st.get("auto_ignored"), [LEAD]); self.assertNotIn(LEAD, a.ignored())   # 増えない・無視されない

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
