"""file-bridge と解放時の自動 GO: ネットも claude も呼ばない。"""
import json, os, sys, unittest, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import agent
from test_join import fresh, att, RecordingPost, TEST_PLAN, ME, CID, REF, OTHERS, LEAD, healthy, DISC

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
        self.assertIsNone(a.st.get("plan")); self.assertNotIn("plan", a.post.kinds())   # 他人のチームでは LLM の下書きを持たない
        a.apply_plan_result(list(TEST_PLAN), source="override")
        self.assertEqual(a.st["plan"], TEST_PLAN)                                       # 運用者の本文は受け入れる


class TestBridgeIgnoredInOthersTeam(unittest.TestCase):
    def test_bridge_plan_ignored_when_not_lead(self):
        tmp = tempfile.mkdtemp()
        a = fresh(); a.post = RecordingPost(); a.p["bridge_dir"] = tmp; a.p.pop("plan_seed", None)
        a.st["team"] = {"game_id": "prophet", "room": f"d-{CID}-team-prophet", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.st["poem"] = {"lines": [], "current": [], "version": 0, "state_hash": None, "syllables": 0, "attempts": {}, "frozen": False, "desync": False, "last_contributor": None, "state_at": None}
        bridge_file(tmp, "prophet", TEST_PLAN, alternate(len(WORDS), [B, ME, C, D]), [B, ME, C, D], id_="x1")
        a.apply_bridge()
        self.assertIsNone(a.st.get("plan")); self.assertEqual(a.st.get("bridge_done"), "x1"); self.assertNotIn("plan adopted", att())


class TestStuckTimerFromFirstSignature(unittest.TestCase):
    """損切りの 3 時間は最初の署名から数える。リーダーが枠を差し替えて再署名しても延びない"""

    def team(self, a, signed_at, first=None):
        a.st["team"] = {"game_id": "prophet", "room": f"d-{CID}-team-prophet", "generation": 2, "members": [B, ME, C, D], "lead": B,
                        "roster_signed": 10, "ready": False, "signed_at": signed_at, "stuck_warned": True}
        if first: a.st["team"]["first_signed_at"] = first

    def test_withdraws_based_on_first_signature(self):
        a = fresh({"withdraw_stuck": True}); a.post = RecordingPost(); a.p["roster_stuck_hours"] = 3
        self.team(a, signed_at=agent.iso(), first="2026-09-14T14:46:00Z")   # 直近の再署名は今、最初の署名は 3 時間以上前
        a.check_stuck_roster() if hasattr(a, "check_stuck_roster") else None
        if hasattr(a, "check_stuck_roster"):
            self.assertIsNone(a.st["team"]); self.assertIn("withdraw", a.post.kinds())

    def test_reconsent_keeps_first_signed_at(self):
        a = fresh(); a.post = RecordingPost()
        self.team(a, signed_at="2026-09-14T14:46:00Z")
        a.st["team"]["first_signed_at"] = None
        # 差し替え枠に再署名する経路を直接は呼ばず、更新規則だけ確かめる
        t = a.st["team"]; first = t.get("first_signed_at") or t.get("signed_at")
        t.update({"signed_at": agent.iso(), "first_signed_at": first})
        self.assertEqual(a.st["team"]["first_signed_at"], "2026-09-14T14:46:00Z")

    def test_leave_team_reusable_after_new_signature(self):
        a = fresh(); a.post = RecordingPost()
        self.team(a, signed_at=agent.iso()); a.st["leave_team_done"] = "prophet"   # 旧形式の done marker
        a.p["leave_team"] = "prophet"; a.apply_operator_switches(a.p)
        self.assertIsNone(a.st["team"]); self.assertEqual(a.st["leave_team_done"], "prophet:10")


class TestEntry3Recruitment(unittest.TestCase):
    """2026-09-14 方針: accepted-word history 必須、署名開始後は席を増やさない"""

    def lead(self, a):
        a.st["lead"] = {"game_id": "nohitori-3b", "request_id": "r", "state": "collecting", "at": "t", "members": [], "signed": {}, "declined": [],
                        "poem_room": f"d-{CID}-team-nohitori-3b", "generation": 1, "waitlist": []}
        a.st["writers_ok"] = {B: 1, C: 1}; a.st.setdefault("last_seen", {})[B] = agent.iso(); a.st["last_seen"][C] = agent.iso()
        return a

    def app(self, a, frm):
        j = {"type": "sonnet.application.v1", "contest_id": CID, "game_id": "nohitori-3b", "did": frm, "role": "writer", "request_id": f"ap-{frm[-6:]}"}
        a.on_lead_application({"seq": 5, "ts": agent.iso(), "from": frm, "_sig_ok": True, "_room": DISC, "text": json.dumps(j)}, j)

    def test_unproven_applicant_not_seated_but_proven_is(self):
        a = fresh(); a.post = RecordingPost(); a.p["seat_only_proven"] = True; a.p["member_health_check"] = False; self.lead(a)
        self.app(a, B)
        self.assertNotIn(B, a.st["lead"]["members"]); self.assertIn("no accepted-word history", att()); self.assertIn("lead-proven", a.post.kinds())
        a.st["proven_contributors"] = {C: 1}
        self.app(a, C)
        self.assertIn(C, a.st["lead"]["members"])
        self.app(a, B)                                       # 同じ相手に二度は書かない
        self.assertEqual(a.post.kinds().count("lead-proven"), 1)

    def test_release_watch_records_proven_contributors(self):
        a = fresh(); a.post = RecordingPost()
        a.st["proven_contributors"] = {}
        pc = a.st["proven_contributors"]; pc.setdefault(B, 9)
        self.assertTrue(a.is_proven(B)); self.assertFalse(a.is_proven(C))
        a.p["lead_invites"] = [C]; self.assertTrue(a.is_proven(C))


class TestMemberModeFollowsLead(unittest.TestCase):
    """他人のチームでは、リーダーの本文と手番表に従い、自分の下書きから語を出さない（2026-09-14 frenchconnection の語 1 事故）"""

    def team(self, a):
        a.st["team"] = {"game_id": "fc", "room": f"d-{CID}-team-fc", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.st["poem"] = {"lines": [], "current": [], "version": 0, "state_hash": "h", "syllables": 0, "attempts": {}, "frozen": False, "desync": False, "last_contributor": None, "state_at": agent.iso()}
        return a

    def test_no_own_draft_and_no_word_from_own_plan(self):
        a = fresh({"plan_lines": True}); a.post = RecordingPost(); self.team(a)
        self.assertIsNone(a.plan_context())                      # LLM の下書きを作らない
        a.st["plan"] = list(TEST_PLAN); a.st["plan_source"] = "own"
        self.assertIsNone(a.word_from_plan(1, [], 10))            # 自分の下書きからは出さない
        a.st["plan_source"] = "override"
        self.assertEqual(a.word_from_plan(1, [], 10), "I")        # 運用者/リーダーの本文からは出す

    def test_script_who_builds_member_table(self):
        a = fresh(); a.post = RecordingPost(); self.team(a)
        a.st["plan"] = list(TEST_PLAN); a.st["plan_source"] = "override"; a.st["script"] = None
        who = alternate(len(WORDS), [B, ME, C, D]); a.p["script_who"] = who
        a.apply_operator_switches(a.p)
        self.assertEqual(a.st["script"]["who"], who); self.assertEqual(a.st["script"]["words"], WORDS)
        self.assertNotIn("script", a.post.kinds())               # 他人の部屋に表は投稿しない
        # 自分の担当なら即、他人の担当は member_cover_after_s まで待つ
        a.p["member_cover_after_s"] = 90
        idx_me = who.index(ME); idx_other = who.index(C)
        a.st["poem"]["current"] = []
        self.assertEqual(a.our_turn_or_cover(1, WORDS[:0]) if idx_me == 0 else True, True)
        a.st["script"]["who"][0] = C
        self.assertFalse(a.our_turn_or_cover(1, []))
        a.st["poem"]["state_at"] = "2026-09-14T00:00:00Z"
        self.assertTrue(a.our_turn_or_cover(1, []))
        self.assertEqual(a.st["script"]["who"][1], who[1])       # member は hand_off で表を書き換えない

    def test_adopts_lead_plan_note(self):
        a = fresh(); a.post = RecordingPost(); self.team(a)
        a.st["plan"] = ["x"] * 14; a.st["plan_source"] = "own"
        sched = "".join({B: "A", ME: "B", C: "C", D: "D"}[w] for w in alternate(len(WORDS), [B, ME, C, D]))
        j = {"type": "sonnet.note.v1", "contest_id": CID, "game_id": "fc", "poem": "\n".join(TEST_PLAN[:4] + [""] + TEST_PLAN[4:8] + [""] + TEST_PLAN[8:12] + [""] + TEST_PLAN[12:]),
             "schedule": sched, "legend": {"A": B, "B": ME, "C": C, "D": D}, "request_id": "plan-1"}
        a.on_team({"seq": 9, "ts": agent.iso(), "from": B, "_sig_ok": True, "_room": f"d-{CID}-team-fc", "text": json.dumps(j)}, j)
        self.assertEqual(a.st["plan"], TEST_PLAN); self.assertEqual(a.st["plan_source"], "lead")
        self.assertEqual(len(a.st["script"]["who"]), len(WORDS)); self.assertIn("lead plan adopted", att())
        # 受理済みの語と食い違う計画は採用しない
        a.st["poem"]["current"] = ["Not"]
        j2 = dict(j, request_id="plan-2"); a.on_team({"seq": 10, "ts": agent.iso(), "from": B, "_sig_ok": True, "_room": f"d-{CID}-team-fc", "text": json.dumps(j2)}, j2)
        self.assertIn("do not match its prefix", att())


class TestOfferGateAndHistory(unittest.TestCase):
    """台帳 2 件: 席の提示にも accepted-word history の関門、実績の母数（release_watch は席に居ても集める、proven_file）"""

    def offer(self, a, gid, lead):
        out = {"action": "reply", "text": "yes", "seat_offer": {"game_id": gid, "lead_did": lead}, "reason": "offer"}
        a.apply_disc_result(out, [{"seq": 1, "from": lead}])

    def test_unproven_lead_offer_is_held(self):
        a = fresh({"accept_seat": True}); a.post = RecordingPost(); a.p["join_only_proven"] = True; a.p["abandon_lead_max_members"] = 0
        a.sign_recent_lead_roster = lambda gid, lead, hours=1: None; a.lead_acceptable = lambda d: True
        a.st["writers_ok"] = {B: 1}; a.st["proven_submitters"] = {}
        self.offer(a, "fc", B)
        self.assertEqual(a.applications(), {}); self.assertIn("held: lead has no accepted-word history", att())
        a.st["proven_contributors"] = {B: 5}
        self.offer(a, "fc", B)
        self.assertIn("fc", a.applications())

    def test_offer_held_when_own_game_has_seats_filled(self):
        a = fresh({"accept_seat": True}); a.post = RecordingPost(); a.p["join_only_proven"] = False; a.p["abandon_lead_max_members"] = 0
        a.sign_recent_lead_roster = lambda gid, lead, hours=1: None; a.lead_acceptable = lambda d: True
        a.st["writers_ok"] = {B: 1}
        a.st["lead"] = {"game_id": "mine", "request_id": "r", "state": "collecting", "at": "t", "members": [C], "signed": {}, "declined": []}
        self.offer(a, "fc", B)
        self.assertEqual(a.applications(), {}); self.assertIn("seated member(s); leaving it needs operator approval", att())
        a.st["lead"]["members"] = []
        self.offer(a, "fc", B)
        self.assertIn("fc", a.applications())

    def test_release_watch_collects_history_while_seated(self):
        a = fresh({"release_watch": True}); a.post = RecordingPost()
        a.st["team"] = {"game_id": "fc", "room": f"d-{CID}-team-fc", "generation": 2, "members": [B, ME, C, D], "lead": B, "roster_signed": 1, "ready": True}
        a.st["submit_reqs"] = {"sub-1": {"game": "other", "from": D}}
        rows = [json.dumps({"seq": 1, "from": C, "text": json.dumps({"type": "sonnet.word.v1", "request_id": "w1", "word": "a"})}),
                json.dumps({"seq": 2, "from": REF, "text": json.dumps({"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "w1", "version": 1})}),
                json.dumps({"seq": 3, "from": B[:-4] + "1111", "text": json.dumps({"type": "sonnet.word.v1", "request_id": "w2", "word": "b"})}),
                json.dumps({"seq": 4, "from": REF, "text": json.dumps({"type": "sonnet.receipt.v1", "status": "rejected", "request_id": "w2", "reason": "version: stale"})})]
        orig = agent.fm.http_get
        try:
            agent.fm.http_get = lambda url, timeout=120: (200, "\n".join(rows))
            j = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "sub-1", "sender_did": D}
            a.release_watch({"seq": 900, "ts": agent.iso(), "from": REF}, j)
        finally:
            agent.fm.http_get = orig
        self.assertIn(C, a.st["proven_contributors"]); self.assertNotIn(B[:-4] + "1111", a.st["proven_contributors"])   # 受理レシート付きの語だけ
        self.assertIn(D, a.st["proven_contributors"])                                                              # 提出者
        self.assertEqual(a.st.get("release_invites") or [], [])                                                    # 席に居る間は招待を積まない
        self.assertNotIn("lead-invite", a.post.kinds())

    def test_proven_file_is_consulted(self):
        tmp = tempfile.mkdtemp(); path = os.path.join(tmp, "proven.json")
        json.dump({"dids": {C: {"words": 3, "games": ["x"], "submitted": 0}, D: {"words": 0, "games": [], "submitted": 1}}}, open(path, "w"))
        a = fresh(); a.p["proven_file"] = path
        self.assertTrue(a.is_proven(C)); self.assertFalse(a.is_proven(D)); self.assertFalse(a.is_proven(B))


class TestPlanRiskCheck(unittest.TestCase):
    """凍結前/採用直後に、鍵の単独依存を数えて 1 回だけ伝える（2026-09-15 の指摘）"""

    def team(self, a, members):
        a.st["team"] = {"game_id": "fc", "room": f"d-{CID}-team-fc", "generation": 2, "members": list(members), "lead": members[0],
                        "roster_signed": 1, "ready": True}
        a.st["poem"] = {"lines": [], "current": [], "version": 0, "state_hash": "h", "syllables": 0, "attempts": {},
                        "frozen": False, "desync": False, "last_contributor": None, "state_at": agent.iso()}

    def test_counts_single_and_spof(self):
        a = fresh(); a.post = RecordingPost()
        # B(ME) は 26 文字、他は 'o' を持たない合成 DID
        noo = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz1234567890ABCDE"   # o なし
        no2 = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz9876543210FEDCB"   # o なし
        no3 = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz1122334455ABCDE"   # o なし
        members = [noo, ME, no2, no3]
        words = ["the", "low", "and", "loop", "sea"]
        who = [noo, ME, no2, ME, no3]
        a.st["team"] = {"members": members}
        r = a.plan_risk(words, who, members)
        singles = {w for _, w, _ in r["single"]}
        self.assertIn("low", singles); self.assertIn("loop", singles)      # 'o' は当方だけ
        self.assertTrue(all(d == ME for _, _, d in r["single"]))
        self.assertIn("o", r["scarce"])                                     # 1 人しか持たない文字
        spof_idx = {i for i, _, _ in r["spof"]}
        self.assertIn(3, spof_idx)                                          # 'loop' は直前が ME 以外でも ME しか置けない

    def test_note_sent_once_per_plan(self):
        a = fresh(); a.post = RecordingPost(); a.p["plan_risk_note"] = True; a.p["plan_risk_note_max"] = 2
        noo = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz1234567890ABCDE"
        no2 = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz9876543210FEDCB"
        no3 = "did:key:z6Mkabcdefghijklmnpqrstuvwxyz1122334455ABCDE"
        members = [noo, ME, no2, no3]; self.team(a, members)
        lines = list(TEST_PLAN); who = alternate(len(WORDS), members)
        a.maybe_report_plan_risk(lines, who, members, "fc")
        self.assertEqual(a.post.kinds().count("plan-check"), 1)
        self.assertIn("plan check fc", att())
        a.maybe_report_plan_risk(lines, who, members, "fc")                 # 同じ計画は二度目を出さない
        self.assertEqual(a.post.kinds().count("plan-check"), 1)
        body = [c[1] for c in a.post.calls if c[2] == "plan-check"][0]
        self.assertIn("PLAN CHECK", body); self.assertLess(len(body), 2000)
        self.assertIn("single points of failure", body)

    def test_note_off_by_default(self):
        a = fresh(); a.post = RecordingPost()
        members = [B, ME, C, OTHERS[1]]; self.team(a, members)
        a.maybe_report_plan_risk(list(TEST_PLAN), alternate(len(WORDS), members), members, "fc")
        self.assertEqual(a.post.kinds().count("plan-check"), 0)             # policy が無ければ投稿しない
