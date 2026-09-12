import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import agent

POLICY = json.load(open(os.path.join(os.path.dirname(HERE), "policy.json")))
ME = POLICY["did"]
LEAD = "did:key:z6MkjED8WPaYvu2pmr8qRvszf95ankNCBLmoyexoepTmGhcj"
OTHERS = ["did:key:z6MkvBBoP3VST9xF833FLRLdZRG8d92uXahXgAW3BR9W9Uxu", "did:key:z6MktrGB8UZGApSNcRuhxTbyHdf8aGVS5ruLMJZhWMTg9Njo"]


def fresh(auto=None):
    p = json.loads(json.dumps(POLICY))
    if auto:
        p["auto"].update(auto)
    agent.STATE_PATH = os.path.join(HERE, "_state_test.json")
    agent.ATTENTION_PATH = os.path.join(HERE, "_attention_test.md")
    agent.LOG_PATH = os.path.join(HERE, "_agent_test.log")
    agent.INBOX_DIR = os.path.join(HERE, "_inbox_test")
    if os.path.exists(agent.STATE_PATH):
        os.remove(agent.STATE_PATH)
    a = agent.Agent(p)
    a.save = lambda: None
    a.sync_llm = True
    return a


class T(unittest.TestCase):
    def setUp(self):
        self._ask = agent.llm.ask
        agent.llm.ask = lambda *x, **k: (_ for _ in ()).throw(AssertionError("real LLM call in test"))

    def tearDown(self):
        agent.llm.ask = self._ask

    def test_mentions(self):
        a = fresh()
        self.assertTrue(a.mentions_us("@TAejK6 seat"))
        self.assertTrue(a.mentions_us(ME))
        self.assertTrue(a.mentions_us("@nohitori hi"))
        self.assertFalse(a.mentions_us("nothing here"))

    def test_parse_receipt(self):
        a = fresh()
        r = a.parse_receipt({"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "w0-x", "sender_did": LEAD, "version": 3, "state_hash": "ab", "syllables": 4, "complete": False}, "")
        self.assertEqual((r["status"], r["version"], r["state_hash"], r["syllables"], r["complete"]), ("accepted", 3, "ab", 4, False))
        self.assertTrue(a.parse_receipt({"type": "note", "text": "hi"}, "")["unknown"])
        self.assertTrue(a.parse_receipt(None, "plain")["unknown"])
        self.assertTrue(a.parse_receipt({"type": "sonnet.room.v1", "game_id": "g"}, "")["room"])
        self.assertTrue(a.parse_receipt({"type": "sonnet.notice.v1", "subject": "x"}, "")["notice"])

    def test_apply_receipt_builds_lines(self):
        """sonnet-2 実物: 提案(request_id→語) と受領(version/state_hash/syllables) から行を組み立てる"""
        a = fresh()
        a.st["team"] = {"game_id": "g", "room": "d-sonnet-2-team-g", "generation": 1, "members": [ME, LEAD]}
        a.st["referee"] = "did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte"
        REF = a.st["referee"]
        setup = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "room-1", "sender_did": REF, "game_id": "g",
                 "poem_room": "d-sonnet-2-team-g", "room_generation": 1, "state_hash": "h0", "reason": ""}
        a.on_team({"seq": 1, "from": REF, "_sig_ok": True, "text": json.dumps(setup)}, setup)
        self.assertEqual((a.st["poem"]["version"], a.st["poem"]["state_hash"], a.st["poem"]["syllables"]), (0, "h0", 0))
        words = "Shall I compare thee to a summer's day".split()
        total = 0
        for i, w in enumerate(words):
            prop = {"type": "sonnet.word.v1", "contest_id": "sonnet-2", "game_id": "g", "room_generation": 1, "version": i,
                    "previous_state_hash": f"h{i}", "word": w, "request_id": f"w{i}-x-{LEAD[-6:]}"}
            a.on_team({"seq": 10 + 2 * i, "from": LEAD, "_sig_ok": True, "text": json.dumps(prop)}, prop)
            total += agent.prosody.line_syllables([w])
            rc = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": prop["request_id"], "sender_did": LEAD,
                  "version": i + 1, "state_hash": f"h{i + 1}", "syllables": total, "complete": False, "reason": ""}
            a.on_team({"seq": 11 + 2 * i, "from": REF, "_sig_ok": True, "text": json.dumps(rc)}, rc)
        self.assertEqual(a.st["poem"]["lines"], ["Shall I compare thee to a summer's day"])
        self.assertEqual(a.st["poem"]["current"], [])
        self.assertEqual((a.st["poem"]["version"], a.st["poem"]["syllables"], a.st["poem"]["last_contributor"]), (8, 10, LEAD))
        # 拒否は状態を変えない
        rej = {"type": "sonnet.receipt.v1", "status": "rejected", "request_id": "w8-x-zzz", "sender_did": LEAD, "reason": "version: stale"}
        a.on_team({"seq": 40, "from": REF, "_sig_ok": True, "text": json.dumps(rej)}, rej)
        self.assertEqual(a.st["poem"]["version"], 8)
        # complete
        fin = {"type": "sonnet.receipt.v1", "status": "accepted", "request_id": "w8-x-fin", "sender_did": LEAD, "version": 9,
               "state_hash": "h9", "syllables": 140, "complete": True, "reason": ""}
        a.on_team({"seq": 41, "from": REF, "_sig_ok": True, "text": json.dumps(fin)}, fin)
        self.assertTrue(a.st["poem"]["frozen"]); self.assertTrue(a.st["poem"]["desync"])   # 提案未観測の語 → desync 印

    def test_valid_word_rules(self):
        a = fresh()
        self.assertTrue(a.valid_word("The", 1, 10))
        self.assertFalse(a.valid_word("xyzzy", 1, 10))          # 辞書外
        self.assertFalse(a.valid_word("extraordinary", 1, 3))   # 音節超過
        self.assertFalse(a.valid_word("day", 14, 1))            # 14 行目を閉じない方針
        self.assertTrue(a.valid_word("day", 13, 1))

    def test_word_from_plan(self):
        a = fresh()
        a.st["plan"] = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        self.assertEqual(a.word_from_plan(1, ["Shall", "I"], 8), "compare")
        self.assertIsNone(a.word_from_plan(1, ["Shall", "we"], 8))

    def test_post_refusals(self):
        a = fresh()
        with self.assertRaises(RuntimeError):
            a.post("inference-agents", "hi", "x")          # 部屋外
        a.key = object()
        with self.assertRaises(RuntimeError):
            a.post(a.p["rooms"]["discovery"], '{"type":"evil.v1"}', "x")   # 型外
        with self.assertRaises(RuntimeError):
            a.post(a.p["rooms"]["discovery"], "my passphrase is 123", "x")  # 秘密
        with self.assertRaises(RuntimeError):
            a.post(a.p["rooms"]["discovery"], f"join {LEAD}", "x")          # 未知 DID の言及
        self.assertEqual(a.parse_iso if False else agent.parse_iso("2026-09-11T12:00:00Z"), 1789128000)

    def test_roster_not_signed_without_conditions(self):
        a = fresh({"sign_roster": True})
        posted = []
        a.post = lambda room, text, kind: posted.append((room, text)) or 1
        members = [LEAD, ME] + OTHERS
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "2026-09-11T08:00:00Z", "_sig_ok": True},
                           {"type": "sonnet.roster.v1", "game_id": "g", "poem_room": "d-sonnet-1-team-g", "room_generation": 1, "members": members})
        self.assertEqual(posted, [])   # agreed でも registered でもない

    def test_roster_from_text_needs_setup_receipt(self):
        a = fresh({"sign_roster": True})
        a.st["registered"] = {"seq": 1}
        a.st["agreed"] = {"game_id": "g", "lead_did": LEAD}
        a.st["first_seen"][LEAD] = "2026-09-11T08:00:00Z"
        posted = []
        a.post = lambda room, text, kind: posted.append((room, text)) or 1
        text = "canonical roster for g, mirror byte for byte: " + " ".join([LEAD, ME] + OTHERS)
        a.on_discovery({"seq": 9, "from": LEAD, "ts": "2026-09-11T12:30:00Z", "text": text, "_sig_ok": True}, None)
        self.assertEqual(posted, [])   # 平文の一覧では署名しない（署名済み JSON のみ）

    def test_check_poem(self):
        lines = [l for l in open(os.path.join(HERE, "format-poem.txt")).read().split("\n") if l.strip()]
        self.assertEqual(agent.check_poem(lines, agent.prosody.lexicon()), [])
        bad = lines[:13] + ["a"]
        self.assertTrue(any("syllables" in p for p in agent.check_poem(bad, agent.prosody.lexicon())))


if __name__ == "__main__":
    unittest.main()
