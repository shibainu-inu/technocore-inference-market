"""実データの再生テスト: sonnet-2 の完成チーム部屋と募集部屋の断片を bot に流し、実物の受領形式で状態が正しく復元されることを確かめる"""
import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import agent, prosody

POLICY = json.load(open(os.path.join(os.path.dirname(HERE), "policy.json")))
REF = "did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte"
FIX = os.path.join(HERE, "fixtures")


def fresh():
    p = json.loads(json.dumps(POLICY)); p["auto"] = {k: False for k in p["auto"]}
    agent.STATE_PATH = os.path.join(HERE, "_state_replay.json"); agent.ATTENTION_PATH = os.path.join(HERE, "_attention_replay.md")
    agent.LOG_PATH = os.path.join(HERE, "_agent_replay.log"); agent.INBOX_DIR = os.path.join(HERE, "_inbox_replay")
    if os.path.exists(agent.STATE_PATH): os.remove(agent.STATE_PATH)
    a = agent.Agent(p); a.save = lambda: None; a.sync_llm = True
    return a


class Replay(unittest.TestCase):
    def setUp(self):
        self._ask, self._get = agent.llm.ask, agent.fm.http_get

    def tearDown(self):
        agent.llm.ask, agent.fm.http_get = self._ask, self._get

    def test_finished_team_room_reconstructs_the_poem(self):
        """gucci-2: 審判受領 119 件 → 14 行 140 音節。行の文面は、受理された提案（request_id で対応）を独立に並べた結果と一致する。
        注: チームが投稿した「凍結テキスト」は審判の台帳と 2 行で食い違っており（提出は eligibility pending）、台帳の側を正とする"""
        a = fresh(); a.st["referee"] = REF
        room = f"d-{POLICY['contest_id']}-team-gucci-2"
        a.st["team"] = {"game_id": "gucci-2", "room": room, "generation": 1, "members": [], "ready": False}
        body = open(os.path.join(FIX, "team-gucci-2.jsonl"), encoding="utf-8").read()
        agent.fm.http_get = lambda url, timeout=30: (200, body)
        a.replay_room(room)
        poem = a.st["poem"]
        self.assertEqual(poem["version"], 119); self.assertEqual(poem["syllables"], 140); self.assertTrue(poem["frozen"])
        self.assertEqual(len(poem["lines"]), 14); self.assertEqual(poem["current"], []); self.assertFalse(poem["desync"])
        self.assertTrue(a.st["team"]["ready"])
        # 独立再構成: 受理受領の順に、(sender, request_id) の最初の提案語を並べる
        props, words = {}, []
        for l in body.splitlines():
            m = json.loads(l)
            try:
                j = json.loads(m["text"])
            except ValueError:
                continue  # noqa: S112 - 平文行は対象外
            if m["from"] != REF and j.get("type") == "sonnet.word.v1":
                props.setdefault((m["from"], j["request_id"]), j["word"])
            elif m["from"] == REF and j.get("status") == "accepted" and "version" in j:
                words.append(props[(j["sender_did"], j["request_id"])])
        self.assertEqual(" ".join(w for line in poem["lines"] for w in line.split(" ")), " ".join(words))
        self.assertEqual(len(words), 119)
        self.assertEqual(agent.check_poem(poem["lines"], prosody.lexicon())[:0], [])   # 14 行 exact-ten は満たす（韻律は問わない）
        self.assertEqual([prosody.line_syllables(l.split(" ")) for l in poem["lines"]], [10] * 14)

    def test_discovery_slice_runs_clean_and_flags_the_broadcaster(self):
        """募集部屋 seq 11400-12300（luxion-1 の放送 bot を含む）: 例外なく処理し、放送 bot を自動除外する"""
        a = fresh(); a.st["referee"] = REF; a.key = object(); a.p["ignore_senders"] = []
        posted = []; a.post = lambda room, text, kind, allow_dids=(): posted.append(kind) or 1
        disc = POLICY["rooms"]["discovery"]
        n = 0
        for l in open(os.path.join(FIX, "discovery-2-slice.jsonl"), encoding="utf-8"):
            m = json.loads(l); m["_room"] = disc; m["_sig_ok"] = True
            a.handle(m); n += 1
        self.assertGreater(n, 700)
        self.assertTrue(any(d.endswith("cjaxKi") for d in a.st.get("auto_ignored", [])))   # luxion-1 の放送 bot
        self.assertEqual(posted, [])                                                       # 観測だけなら投稿しない
        self.assertGreater(len(a.st["teams"]), 5)


if __name__ == "__main__":
    unittest.main()
