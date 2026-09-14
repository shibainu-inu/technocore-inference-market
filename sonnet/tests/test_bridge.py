"""file-bridge と解放時の自動 GO: ネットも claude も呼ばない。"""
import json, os, sys, unittest, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import agent
from test_join import fresh, att, RecordingPost, TEST_PLAN, ME, CID, REF, OTHERS, LEAD, healthy

SUBS = json.load(open(os.path.join(os.path.dirname(HERE), "policy.json")))["rooms"]["submissions"]
B, C, D = OTHERS[0], OTHERS[1], LEAD
WORDS = [w for l in TEST_PLAN for w in l.split(" ") if w]


def frozen_team(a, gid="nohitori-3", members=None):
    members = members or [ME, B, C, D]
    a.st["team"] = {"game_id": gid, "room": f"d-{CID}-team-{gid}", "generation": 1, "members": list(members), "lead": ME, "roster_signed": None, "ready": True}
    a.st["lead"] = {"game_id": gid, "request_id": "r1", "state": "collecting", "at": agent.iso(), "members": [m for m in members if m != ME],
                    "signed": {}, "declined": [], "poem_room": f"d-{CID}-team-{gid}", "generation": 1, "canonical": list(members)}
    a.st["poem"] = {"lines": [], "current": [], "version": 0, "state_hash": None, "syllables": 0, "attempts": {}, "frozen": False,
                    "desync": False, "last_contributor": None, "state_at": None}
    return a


def alternate(n, members):
    return [members[i % len(members)] for i in range(n)]


def bridge_file(dirpath, gid, lines, who, members, id_="abc123def456", prefix_len=0):
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, f"{gid}.json"), "w") as f:
        json.dump({"id": id_, "game_id": gid, "generated_at": agent.iso(), "members": members, "prefix_len": prefix_len,
                   "lines": lines, "who": who, "keys": [2] * len(who), "fit_problems": [], "source": "orchestrator", "feasible": True}, f)


class TestAutoNextEntry(unittest.TestCase):
    def receipt(self, a, rid, status="accepted", entry=None, seq=900):
        j = {"contest_id": CID, "request_id": rid, "sender_did": D, "status": status, "type": "sonnet.receipt.v1", "entry_id": entry or "x"}
        a.on_submissions({"seq": seq, "ts": agent.iso(), "from": REF, "_sig_ok": True, "_room": SUBS, "text": json.dumps(j)}, j)

    def test_release_archives_and_requests_next_game(self):
        a = fresh({"next_entry_on_release": True}); a.p["next_game_id"] = "nohitori-3"; a.post = RecordingPost()
        frozen_team(a, "nohitori-2"); a.st["poem"]["frozen"] = True
        a.st["submit_reqs"] = {"sub-1": {"game": "nohitori-2", "from": D}}
        self.receipt(a, "sub-1")
        self.assertIsNone(a.st["team"]); self.assertIsNone(a.st["lead"]); self.assertIsNone(a.st["plan"])
        self.assertEqual(a.st["lead_game_id_override"], "nohitori-3")
        self.assertEqual(a.lead_game_id(), "nohitori-3")
        self.assertEqual(len(a.st["done_games"]), 1)
        self.assertIn("withdraw", a.post.kinds())
        self.assertIn("roster released", att())
        # 次の maybe_lead は override のゲームで部屋を請求する
        a.p["auto"]["lead_team"] = True; a.st["lead_block_until"] = 0
        a.maybe_lead()
        self.assertEqual(a.st["lead"]["game_id"], "nohitori-3")
        self.assertIn("team-request", a.post.kinds())

    def test_other_games_and_rejections_do_not_trigger(self):
        a = fresh({"next_entry_on_release": True}); a.p["next_game_id"] = "nohitori-3"; a.post = RecordingPost()
        frozen_team(a, "nohitori-2")
        a.st["submit_reqs"] = {"sub-x": {"game": "someone-else", "from": D}, "sub-1": {"game": "nohitori-2", "from": D}}
        self.receipt(a, "sub-x")
        self.assertIsNotNone(a.st["team"])
        self.receipt(a, "sub-1", status="rejected")
        self.assertIsNotNone(a.st["team"])
        a.p["auto"]["next_entry_on_release"] = False
        self.receipt(a, "sub-1")
        self.assertIsNotNone(a.st["team"])

    def test_entry_id_match_is_enough(self):
        a = fresh({"next_entry_on_release": True}); a.p["next_game_id"] = "nohitori-3"; a.post = RecordingPost()
        frozen_team(a, "nohitori-2")
        self.receipt(a, "unknown-req", entry="nohitori-2")
        self.assertIsNone(a.st["team"]); self.assertEqual(a.lead_game_id(), "nohitori-3")

    def test_unusable_next_id_stays_put(self):
        a = fresh({"next_entry_on_release": True}); a.p["next_game_id"] = "nohitori-2"; a.post = RecordingPost()
        frozen_team(a, "nohitori-2"); a.st["submit_reqs"] = {"sub-1": {"game": "nohitori-2", "from": D}}
        self.receipt(a, "sub-1")
        self.assertIsNotNone(a.st["team"]); self.assertIn("staying put", att())


class TestBridge(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def make(self, ready=True):
        a = fresh(); a.post = RecordingPost(); a.p["bridge_dir"] = self.tmp; a.p.pop("plan_seed", None)
        frozen_team(a); a.st["team"]["ready"] = ready
        return a

    def test_plan_and_script_adopted_when_frozen(self):
        a = self.make()
        who = alternate(len(WORDS), [ME, B, C, D])
        bridge_file(self.tmp, "nohitori-3", TEST_PLAN, who, [ME, B, C, D])
        a.apply_bridge()
        self.assertEqual(a.st["plan"], TEST_PLAN)
        self.assertEqual(a.st["script"]["who"], who)
        self.assertEqual(a.st["bridge_done"], "abc123def456")
        self.assertIn("script", a.post.kinds())            # 手番表を部屋に投稿
        self.assertIn("plan adopted", att())
        # 同じ id は二度目に適用されない（mtime が変わっても）
        a.st["plan"] = None; os.utime(os.path.join(self.tmp, "nohitori-3.json"), None); a._bridge_mtime = None
        a.apply_bridge(); self.assertIsNone(a.st["plan"])

    def test_prefix_mismatch_rejected(self):
        a = self.make()
        a.st["poem"]["lines"] = ["Not the plan first line"]; a.st["poem"]["current"] = []
        bridge_file(self.tmp, "nohitori-3", TEST_PLAN, alternate(len(WORDS), [ME, B, C, D]), [ME, B, C, D])
        a.apply_bridge()
        self.assertIsNone(a.st["plan"]); self.assertIn("do not match its prefix", att())

    def test_members_mismatch_waits(self):
        a = self.make()
        bridge_file(self.tmp, "nohitori-3", TEST_PLAN, alternate(len(WORDS), [ME, B, C]), [ME, B, C])
        a.apply_bridge()
        self.assertIsNone(a.st["plan"]); self.assertIsNone(a.st.get("bridge_done"))

    def test_bad_who_falls_back_to_own_script(self):
        a = self.make()
        who = [ME] * len(WORDS)          # 連続同一 → 無効
        bridge_file(self.tmp, "nohitori-3", TEST_PLAN, who, [ME, B, C, D])
        a.apply_bridge()
        self.assertEqual(a.st["plan"], TEST_PLAN)
        self.assertNotEqual(a.st["script"]["who"], who)
        self.assertTrue(all(a.st["script"]["who"][i] != a.st["script"]["who"][i + 1] for i in range(len(WORDS) - 1)))

    def test_before_freeze_plan_gates_seating(self):
        a = self.make(ready=False); a.st["team"] = None
        bridge_file(self.tmp, "nohitori-3", TEST_PLAN, alternate(len(WORDS), [ME, B, C, D]), [ME, B, C, D])
        a.apply_bridge()
        self.assertEqual(a.st["plan"], TEST_PLAN); self.assertIsNone(a.st.get("script"))
        self.assertEqual(a.key_fits_plan("did:key:z6Mk" + "1" * 44), "")   # 鍵の文字は DID 全体から: 検査は走る
        self.assertNotIn("script", a.post.kinds())

    def test_roster_advice_logged_once(self):
        a = self.make()
        with open(os.path.join(self.tmp, "roster-nohitori-3.json"), "w") as f:
            json.dump({"id": "r1", "game_id": "nohitori-3", "advice": "prefer candidates with l,o"}, f)
        a.apply_bridge(); a.apply_bridge()
        self.assertEqual(att().count("bridge roster r1"), 1)

    def test_offline_check_rejects_bad_text(self):
        a = self.make()
        bad = list(TEST_PLAN); bad[3] = "this line is far too long to be ten syllables at all now"
        bridge_file(self.tmp, "nohitori-3", bad, alternate(len(WORDS), [ME, B, C, D]), [ME, B, C, D])
        a.apply_bridge()
        self.assertIsNone(a.st["plan"]); self.assertIn("rejected by the offline check", att())


if __name__ == "__main__":
    unittest.main()


class TestOpusTextBeforeFreeze(unittest.TestCase):
    """(b) 体制: 本文は bot の LLM（Opus）が書く。凍結前でも席が 2 つ埋まれば書き、席の鍵検査に使う。bridge は割当だけ"""

    def test_plan_context_before_freeze_needs_two_members(self):
        a = fresh(); a.post = RecordingPost()
        a.st["lead"] = {"game_id": "nohitori-3", "request_id": "r", "state": "collecting", "at": "t", "members": [B], "signed": {}, "declined": [], "poem_room": f"d-{CID}-team-nohitori-3", "generation": 1}
        self.assertIsNone(a.plan_context())
        a.st["lead"]["members"] = [B, C]
        ctx = a.plan_context()
        self.assertEqual(ctx["game_id"], "nohitori-3"); self.assertEqual(ctx["members"], [ME, B, C]); self.assertIsNone(ctx["room"])

    def test_periodic_calls_llm_plan_in_lead_mode(self):
        a = fresh({"plan_lines": True}); a.post = RecordingPost(); a.p.pop("plan_seed", None)
        json.dump(a.p, open(a.p["_path"], "w"))   # 60 秒ごとの再読込でも plan_seed が戻らないように写しも剥ぐ
        a.st["lead"] = {"game_id": "nohitori-3", "request_id": "r", "state": "collecting", "at": "t", "members": [B, C], "signed": {}, "declined": [], "poem_room": f"d-{CID}-team-nohitori-3", "generation": 1}
        a.opening = 0; a._plan_at = 0
        seen = {}
        a.make_plan = lambda ctx: seen.update(ctx)
        a.periodic()
        self.assertEqual(seen.get("members"), [ME, B, C]); self.assertEqual(seen.get("team_room_messages"), [])
        # 結果は凍結前でも採用され、部屋には投稿しない（403 になる）
        a.apply_plan_result(list(TEST_PLAN))
        self.assertEqual(a.st["plan"], TEST_PLAN); self.assertNotIn("plan", a.post.kinds())
        self.assertIn("plan text set for nohitori-3", att())
        self.assertIsInstance(a.key_fits_plan(B), str)   # 席の鍵検査はこの本文に対して走る（合う鍵は ""）

    def test_plan_result_must_start_with_accepted_words(self):
        a = self.frozen_with_prefix()
        a.apply_plan_result(list(TEST_PLAN))
        self.assertIsNone(a.st["plan"]); self.assertIn("do not match its prefix", att())
        # 受理済み語で始まる本文は通る
        lines = list(TEST_PLAN); lines[0] = "I climb the ladder, kneel, and rake the hay,"
        a.st["poem"]["lines"] = []; a.st["poem"]["current"] = ["I", "climb"]
        a.apply_plan_result(lines)
        self.assertEqual(a.st["plan"], lines)

    def frozen_with_prefix(self):
        a = fresh(); a.post = RecordingPost(); a.p.pop("plan_seed", None)
        frozen_team(a); a.st["poem"]["lines"] = []; a.st["poem"]["current"] = ["Not", "these"]
        return a

    def test_bridge_replan_request_clears_plan_for_llm(self):
        tmp = tempfile.mkdtemp()
        a = fresh(); a.post = RecordingPost(); a.p["bridge_dir"] = tmp; a.p.pop("plan_seed", None)
        frozen_team(a); a.st["plan"] = list(TEST_PLAN); a.st["script"] = {"words": WORDS, "who": alternate(len(WORDS), [ME, B, C, D])}
        a._plan_at = 10**12
        os.makedirs(tmp, exist_ok=True)
        with open(os.path.join(tmp, "nohitori-3.json"), "w") as f:
            json.dump({"id": "rp1", "game_id": "nohitori-3", "request": "replan", "reason": "dead ends near [40]", "members": [ME, B, C, D], "lines": TEST_PLAN, "who": []}, f)
        a.apply_bridge()
        self.assertIsNone(a.st["plan"]); self.assertIsNone(a.st["script"]); self.assertEqual(a._plan_at, 0)
        self.assertEqual(a.st["bridge_done"], "rp1"); self.assertIn("requests a rewrite", att())
        # 同じ要求は二度効かない
        a.st["plan"] = list(TEST_PLAN); a._bridge_mtime = None; a.apply_bridge()
        self.assertEqual(a.st["plan"], TEST_PLAN)

    def test_same_script_not_reposted(self):
        tmp = tempfile.mkdtemp()
        a = fresh(); a.post = RecordingPost(); a.p["bridge_dir"] = tmp; a.p.pop("plan_seed", None)
        frozen_team(a)
        who = alternate(len(WORDS), [ME, B, C, D])
        a.st["plan"] = list(TEST_PLAN); a.st["script"] = {"words": WORDS, "who": who}
        bridge_file(tmp, "nohitori-3", TEST_PLAN, who, [ME, B, C, D], id_="same1")
        a.apply_bridge()
        self.assertEqual(a.st["bridge_done"], "same1"); self.assertNotIn("script", a.post.kinds())


class TestRoomRequestFallback(unittest.TestCase):
    """審判の「team room is not claimable; request a different game_id」（problem 欄）に別名で再請求する"""

    def test_problem_field_triggers_variant_retry(self):
        a = fresh({"lead_team": True}); a.post = RecordingPost()
        a.st["lead"] = {"game_id": "nohitori-3", "request_id": "room-1", "state": "requested", "at": "t", "members": [], "signed": {}, "declined": []}
        a.st["lead_game_id_override"] = "nohitori-3"
        j = {"contest_id": CID, "game_id": "nohitori-3", "problem": "team room is not claimable by the referee; request a different game_id",
             "request_id": "room-1", "sender_did": ME, "status": "rejected", "type": "sonnet.receipt.v1"}
        a.on_lead_receipt({"seq": 5, "ts": "t", "from": REF, "_sig_ok": True}, j)
        self.assertEqual(a.st["lead"]["game_id"], "nohitori-3b"); self.assertEqual(a.st["lead_game_id_override"], "nohitori-3b")
        self.assertEqual(a.post.kinds(), ["team-request"]); self.assertIn("retrying the room request with game_id nohitori-3b", att())
        self.assertEqual(agent.Agent.next_game_variant("nohitori-3b"), "nohitori-3c")
        self.assertEqual(agent.Agent.next_game_variant("nohitori"), "nohitorib")

    def test_operator_next_game_id_change_resets_block(self):
        a = fresh({"lead_team": True}); a.post = RecordingPost()
        a.st["lead"] = None; a.st["team"] = None; a.st["lead_game_id_override"] = "nohitori-3"; a.st["lead_block_until"] = 10**12
        a.p["next_game_id"] = "nohitori-3b"
        a.maybe_lead()                      # 待ち時間中でも next_game_id の変更で即座に請求する
        self.assertEqual(a.st["lead_block_until"], 0)
        self.assertEqual(a.st["lead"]["game_id"], "nohitori-3b"); self.assertIn("team-request", a.post.kinds())


class TestConsentReleaseOnAcceptedSubmission(unittest.TestCase):
    """規則: 提出の受理レシートは全メンバーの同意を解放する。bot の live_consent もそこで消す"""

    def test_accepted_submission_clears_live_consents(self):
        a = fresh(); a.post = RecordingPost()
        a.st["live_consent"] = {B: {"game": "nohitori-2", "seq": 1}, C: {"game": "nohitori-2", "seq": 2}, D: {"game": "other", "seq": 3}}
        a.st["submit_reqs"] = {"sub-1": {"game": "nohitori-2", "from": B}}
        j = {"contest_id": CID, "request_id": "sub-1", "sender_did": B, "status": "accepted", "type": "sonnet.receipt.v1", "entry_id": "nohitori-2"}
        a.on_submissions({"seq": 900, "ts": agent.iso(), "from": REF, "_sig_ok": True, "_room": SUBS, "text": json.dumps(j)}, j)
        self.assertEqual(set(a.st["live_consent"]), {D})

    def test_resign_token_releases_and_rechecks(self):
        a = fresh(); a.post = RecordingPost()
        a.st["live_consent"] = {B: {"game": "nohitori-2", "seq": 1}}
        calls = []
        a.sign_recent_lead_roster = lambda gid, lead, hours=1: calls.append((gid, lead, hours))
        a.p["resign_token"] = {"id": "r1", "game_id": "prophet", "lead_did": B, "release": [B], "hours": 3}
        a.maybe_announce()
        self.assertEqual(calls, [("prophet", B, 3)]); self.assertEqual(a.st.get("live_consent"), {})
        self.assertEqual(a.st.get("resign_token_done"), "r1")


class TestMemberMode(unittest.TestCase):
    """他人のチームでは手番表が無くても先取りしない: 担当が member_cover_after_s 以上動かない時だけ埋める"""

    def test_member_waits_then_covers(self):
        a = fresh(); a.post = RecordingPost(); a.p["member_cover_after_s"] = 90
        a.st["team"] = {"game_id": "prophet", "room": f"d-{CID}-team-prophet", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.st["script"] = None
        a.st["poem"]["state_at"] = agent.iso()
        self.assertFalse(a.our_turn_or_cover(1, []))
        a.st["poem"]["state_at"] = "2026-09-14T00:00:00Z"
        self.assertTrue(a.our_turn_or_cover(1, []))

    def test_member_does_not_post_draft_plan(self):
        a = fresh(); a.post = RecordingPost(); a.p.pop("plan_seed", None)
        a.st["team"] = {"game_id": "prophet", "room": f"d-{CID}-team-prophet", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.apply_plan_result(list(TEST_PLAN))
        self.assertEqual(a.st["plan"], TEST_PLAN); self.assertNotIn("plan", a.post.kinds())


class TestBridgeIgnoredInOthersTeam(unittest.TestCase):
    def test_bridge_plan_ignored_when_not_lead(self):
        tmp = tempfile.mkdtemp()
        a = fresh(); a.post = RecordingPost(); a.p["bridge_dir"] = tmp; a.p.pop("plan_seed", None)
        a.st["team"] = {"game_id": "prophet", "room": f"d-{CID}-team-prophet", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.st["poem"] = {"lines": [], "current": [], "version": 0, "state_hash": None, "syllables": 0, "attempts": {}, "frozen": False, "desync": False, "last_contributor": None, "state_at": None}
        bridge_file(tmp, "prophet", TEST_PLAN, alternate(len(WORDS), [B, ME, C, D]), [B, ME, C, D], id_="x1")
        a.apply_bridge()
        self.assertIsNone(a.st.get("plan")); self.assertEqual(a.st.get("bridge_done"), "x1"); self.assertNotIn("plan adopted", att())
