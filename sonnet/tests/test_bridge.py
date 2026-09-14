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
