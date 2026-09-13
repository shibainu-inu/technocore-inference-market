"""敵対的・境界条件テスト（独立テスターによる）。

失敗するテストには `# BUG:` を付けてある。それ以外は「攻めてみたが持ちこたえた」記録。
ネットも `claude` も呼ばない: llm.ask / fm.http_get / read_json / post は全て差し替える。
"""
import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import agent, prosody

POLICY = json.load(open(os.path.join(os.path.dirname(HERE), "policy.json")))
ME = POLICY["did"]
CID = POLICY["contest_id"]
TEAM = f"d-{CID}-team-"
REF = POLICY["referee_did"]
LEAD = "did:key:z6MkjED8WPaYvu2pmr8qRvszf95ankNCBLmoyexoepTmGhcj"
OTHERS = ["did:key:z6MkvBBoP3VST9xF833FLRLdZRG8d92uXahXgAW3BR9W9Uxu", "did:key:z6MktrGB8UZGApSNcRuhxTbyHdf8aGVS5ruLMJZhWMTg9Njo"]
L2 = "did:key:z6MkwfnckxULjn9dPvoPnJSPbc7aWNegeXrirWzBLpfVgqSM"
FIX = os.path.join(HERE, "fixtures")
DISC = POLICY["rooms"]["discovery"]


def fresh(auto=None):
    p = json.loads(json.dumps(POLICY))
    p["auto"] = {k: False for k in p["auto"]}
    if auto:
        p["auto"].update(auto)
    agent.STATE_PATH = os.path.join(HERE, "_state_adv.json")
    agent.ATTENTION_PATH = os.path.join(HERE, "_attention_adv.md")
    agent.LOG_PATH = os.path.join(HERE, "_agent_adv.log")
    agent.INBOX_DIR = os.path.join(HERE, "_inbox_adv")
    for f in (agent.STATE_PATH, agent.ATTENTION_PATH):
        if os.path.exists(f):
            os.remove(f)
    a = agent.Agent(p)
    a.save = lambda: None
    a.sync_llm = True
    return a


def attention_text():
    return open(agent.ATTENTION_PATH).read() if os.path.exists(agent.ATTENTION_PATH) else ""


def rc(**k):
    d = {"type": "sonnet.receipt.v1", "status": "accepted", "reason": ""}
    d.update(k)
    return d


def ref_msg(seq, j):
    return {"seq": seq, "from": REF, "_sig_ok": True, "ts": "2026-09-11T13:00:00Z", "text": json.dumps(j)}


def recv(a, seq, j):
    """審判の受領を on_team に流す（parse 済み JSON も渡す）"""
    a.on_team(ref_msg(seq, j), j)


def member_msg(seq, frm, j):
    return {"seq": seq, "from": frm, "_sig_ok": True, "ts": "2026-09-11T13:00:00Z", "text": json.dumps(j)}


def with_team(a, ready=True, gen=1):
    a.st["referee"] = REF
    a.st["team"] = {"game_id": "g", "room": TEAM + "g", "generation": gen, "members": [ME, LEAD] + OTHERS, "ready": ready,
                    "lead": LEAD, "roster_request_id": "roster-1"}
    a.st["poem"].update({"state_hash": "h0", "version": 0, "syllables": 0, "last_contributor": LEAD})
    return a


class RecordingPost:
    def __init__(self):
        self.calls = []

    def __call__(self, room, text, kind, allow_dids=()):
        self.calls.append((room, text, kind)); return 1

    def kinds(self):
        return [c[2] for c in self.calls]


def roster_agent(view_gen=1):
    """署名条件をすべて満たした状態の bot（応募済み・登録済み・鍵あり・部屋 generation は view_gen）"""
    a = fresh({"sign_roster": True}); a.key = object(); a.st["registered"] = {"seq": 1}
    a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": agent.iso(), "manual": True}}
    a.st["agreed"] = a.st["applications"]["g"]
    rp = RecordingPost(); a.post = rp
    agent.read_json = lambda room, wait: ([], {"generation": view_gen})
    a.replay_room = lambda room: None; a.start_reader = lambda room: None
    return a, rp


def roster_json(**over):
    j = {"type": "sonnet.roster.v1", "contest_id": CID, "game_id": "g", "poem_room": TEAM + "g", "room_generation": 1,
         "members": [LEAD, ME] + OTHERS}
    j.update(over)
    return j


class Adversarial(unittest.TestCase):
    def setUp(self):
        self._ask, self._get, self._read, self._flag = agent.llm.ask, agent.fm.http_get, agent.read_json, agent.RESTART_FLAG
        self.llm_calls = []
        self.llm_out = None
        def ask(system, user, schema, **k):
            self.llm_calls.append((k.get("task"), user)); return self.llm_out
        agent.llm.ask = ask
        agent.fm.http_get = lambda url, timeout=30: (_ for _ in ()).throw(AssertionError(f"network in test: {url}"))
        agent._ATT_COUNT.clear()   # attention() の key ごと毎時上限はプロセス全体で共有。他モジュールのテストに漏らさない

    def tearDown(self):
        agent.llm.ask, agent.fm.http_get, agent.read_json, agent.RESTART_FLAG = self._ask, self._get, self._read, self._flag
        agent._ATT_COUNT.clear()

    # ---------------- 1. 状態機械 ----------------
    def test_duplicate_accepted_receipt_appends_word_twice(self):
        """規則: 同じ request_id の再送に審判は「元の受領をそのまま返す」(sonnet-game.md 'An identical retry ... returns its original receipt').
        同じ受領が 2 回流れても語は 1 回だけ足されるべき"""
        a = with_team(fresh())
        prop = {"type": "sonnet.word.v1", "word": "day", "request_id": "r1"}
        a.on_team(member_msg(1, LEAD, prop), prop)
        r = rc(request_id="r1", sender_did=LEAD, version=1, state_hash="h1", syllables=1, complete=False)
        a.on_team(ref_msg(2, r), r)
        a.on_team(ref_msg(3, r), r)   # 審判がリトライに対して元の受領を再掲
        self.assertEqual(a.st["poem"]["version"], 1)
        # BUG: agent.py:873-884 apply_receipt は version の単調性を見ないので同じ受領を 2 回適用し current=['day','day'] になる
        self.assertEqual(a.st["poem"]["current"], ["day"])

    def test_version_gap_is_not_silently_absorbed(self):
        """行を閉じた受領を 1 件取りこぼす（リングから消えた等）と、行境界を跨いだまま語が同じ行に足され続ける"""
        a = with_team(fresh())
        words = ["Shall", "I", "compare", "thee", "to", "a", "summer's", "day"]
        for i, w in enumerate(words):
            prop = {"type": "sonnet.word.v1", "word": w, "request_id": f"r{i}"}
            a.on_team(member_msg(10 + i, LEAD, prop), prop)
        tot = 0
        for i, w in enumerate(words):
            tot += prosody.line_syllables([w])
            if i == 7:
                continue   # version 8（行 1 を閉じる受領）を取りこぼす
            recv(a, 30 + i, rc(request_id=f"r{i}", sender_did=LEAD, version=i + 1, state_hash=f"h{i + 1}", syllables=tot, complete=False))
        prop = {"type": "sonnet.word.v1", "word": "Thou", "request_id": "r8"}
        a.on_team(member_msg(50, LEAD, prop), prop)
        recv(a, 51, rc(request_id="r8", sender_did=LEAD, version=9, state_hash="h9", syllables=11, complete=False))
        poem = a.st["poem"]
        self.assertEqual(poem["version"], 9); self.assertEqual(poem["syllables"], 11)
        # BUG: agent.py:895-902 append_word は total%10==0 の瞬間だけ行を閉じ、agent.py:873 は version の飛び (7→9) を検知しない。
        #      行 1 が閉じないまま 'Thou' が行 1 に足され desync も立たない（README: 行の境界は累積音節で決める）
        self.assertTrue(poem["desync"] or (len(poem["lines"]) == 1 and poem["current"] == ["Thou"]),
                        f"lines={poem['lines']} current={poem['current']} desync={poem['desync']}")

    def test_receipt_with_our_request_id_but_other_sender_is_not_ours(self):
        """request_id は w<version>-<hash8>-<suffix> で予測可能。チームメイトが同じ request_id で投稿すると、
        審判はその人の (signer, request_id) に受領を出す。sender_did が自分でない受領で pending を消してはいけない"""
        a = with_team(fresh())
        a.st["pending_word"] = {"request_id": "w0-h0-TAejK6", "word": "Shall", "at": agent.iso()}
        recv(a, 5, rc(status="rejected", request_id="w0-h0-TAejK6", sender_did=LEAD, reason="word: letters absent from contributor DID"))
        # BUG: agent.py:844 `mine = bool(pend and rid == pend["request_id"])` は sender_did を見ない。
        #      他人宛ての拒否で自分の pending が消え、自分の語が rejected に記録される（再提案→同 ID 別内容→審判が拒否）
        self.assertIsNotNone(a.st["pending_word"])
        self.assertEqual(a.st["poem"].get("rejected"), None)

    def test_accepted_receipt_with_our_request_id_but_other_sender_appends_their_word(self):
        a = with_team(fresh())
        a.st["pending_word"] = {"request_id": "w0-h0-TAejK6", "word": "Shall", "at": agent.iso()}
        prop = {"type": "sonnet.word.v1", "word": "Thou", "request_id": "w0-h0-TAejK6"}
        a.on_team(member_msg(4, LEAD, prop), prop)   # 同じ ID を使った他人の提案
        recv(a, 5, rc(request_id="w0-h0-TAejK6", sender_did=LEAD, version=1, state_hash="h1", syllables=1, complete=False))
        # BUG: agent.py:882 mine=True なので受理された語は他人の 'Thou' なのに自分の pending 'Shall' を行に足す
        self.assertEqual(a.st["poem"]["current"], ["Thou"])
        self.assertIsNotNone(a.st["pending_word"])

    def test_own_proposal_is_tracked_when_receipt_arrives_after_pending_ttl(self):
        """実物 (fixtures/team-gucci-2.jsonl) では提案→受領が最大 129 秒。pending_word_ttl_s=120 を超えると
        maybe_propose が pending を消す。その後に来た自分宛ての受理で語が失われてはいけない"""
        a = with_team(fresh({"propose_words": True})); a.key = object(); a.opening = 0
        a.st["plan"] = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        rp = RecordingPost(); a.post = rp
        a.maybe_propose()
        self.assertEqual(rp.kinds(), ["word"])
        posted = json.loads(rp.calls[0][1]); rid = posted["request_id"]
        # 自分の投稿が部屋に現れ、reader が handle() に流す
        a.handle({"_room": TEAM + "g", "from": ME, "seq": 20, "_sig_ok": True, "ts": "t", "text": rp.calls[0][1]})
        # TTL 切れ: pending は消え、LLM ジョブが飛行中（plan が外れた場合の経路）
        a.st["pending_word"] = None; a._word_job = (0, 1)
        recv(a, 21, rc(request_id=rid, sender_did=ME, version=1, state_hash="h1", syllables=1, complete=False))
        # BUG: agent.py:476 handle() は自分の投稿を on_team に渡さず、agent.py:964 propose() も proposals に記録しないので、
        #      pending が消えた後の受理は agent.py:882 で語を引けず desync になり 'Shall' が行から落ちる
        self.assertEqual(a.st["poem"]["current"], ["Shall"])
        self.assertFalse(a.st["poem"]["desync"])

    def test_reproposal_after_ttl_uses_a_fresh_request_id(self):
        """規則: 'Reusing that ID with different content is rejected. After correcting a rejected request, use a new request ID.'
        pending が期限切れになった後の別の語の提案は新しい request_id でなければならない"""
        a = with_team(fresh({"propose_words": True})); a.key = object(); a.opening = 0
        rp = RecordingPost(); a.post = rp
        a.propose("Shall")
        first = json.loads(rp.calls[0][1])["request_id"]
        a.st["pending_word"]["at"] = "2026-09-11T00:00:00Z"   # 期限切れ
        self.llm_out = {"word": "Thou", "alternatives": [], "reason": ""}
        a.maybe_propose()
        if not a.q.empty():
            a.handle(a.q.get_nowait())
        self.assertEqual(len(rp.calls), 2, rp.calls)
        second = json.loads(rp.calls[1][1])
        self.assertEqual(second["word"], "Thou")
        # BUG: agent.py:969 request_id は (version, state_hash, suffix) から決定的に作られるため、同じ状態への別の語は同じ ID を再利用し、
        #      審判に「同 ID 別内容」として拒否される。旧提案が受理されると agent.py:882 で pending の新語が行に足される
        self.assertNotEqual(second["request_id"], first)

    def test_rejected_receipt_for_unknown_request_changes_nothing(self):
        a = with_team(fresh())
        recv(a, 5, rc(status="rejected", request_id="w0-zzz-abcdef", sender_did=LEAD, reason="version: stale"))
        self.assertEqual((a.st["poem"]["version"], a.st["poem"]["current"], a.st["pending_word"]), (0, [], None))

    def test_receipt_for_our_request_with_unexpected_version_and_string_version(self):
        a = with_team(fresh())
        a.st["pending_word"] = {"request_id": "w0-h0-TAejK6", "word": "Shall", "at": agent.iso()}
        recv(a, 5, rc(request_id="w0-h0-TAejK6", sender_did=ME, version="7", state_hash="h7", syllables=1, complete=False))
        self.assertEqual(a.st["poem"]["version"], 7); self.assertEqual(a.st["poem"]["current"], ["Shall"])
        self.assertIsNone(a.st["pending_word"])
        recv(a, 6, rc(request_id="x", sender_did=LEAD, version="abc", state_hash="h8", syllables=1))
        self.assertEqual(a.st["poem"]["version"], 7)   # 壊れた version は無視して続行

    def test_roster_ready_then_setup_in_odd_order_and_replay_is_idempotent(self):
        """replay_room を 2 回呼んでも（再起動 2 回）状態は同じ。実物の完成部屋で確かめる"""
        a = fresh(); a.st["referee"] = REF
        room = TEAM + "gucci-2"
        a.st["team"] = {"game_id": "gucci-2", "room": room, "generation": 1, "members": [], "ready": False}
        body = open(os.path.join(FIX, "team-gucci-2.jsonl"), encoding="utf-8").read()
        agent.fm.http_get = lambda url, timeout=30: (200, body)
        a.replay_room(room); first = json.loads(json.dumps(a.st["poem"]))
        a.replay_room(room); second = a.st["poem"]
        self.assertEqual(first, second)
        self.assertEqual(second["version"], 119); self.assertEqual(len(second["lines"]), 14); self.assertTrue(second["frozen"])
        self.assertEqual(a.st["seen"][room], 332)
        # 完成後に maybe_propose を呼んでも何も出さない
        a.p["auto"]["propose_words"] = True; a.key = object(); a.opening = 0
        rp = RecordingPost(); a.post = rp
        a.maybe_propose(); self.assertEqual(rp.calls, []); self.assertEqual(self.llm_calls, [])

    def test_replay_with_garbage_lines_and_bad_signatures(self):
        a = fresh(); a.st["referee"] = REF
        room = TEAM + "g"; a.st["team"] = {"game_id": "g", "room": room, "generation": 1, "members": [], "ready": False}
        fake = {"seq": 1, "from": REF, "ts": "t", "text": json.dumps(rc(request_id="r", sender_did=LEAD, version=5, state_hash="h5", syllables=3)),
                "nonce": 1, "sig": "AAAA"}   # 審判 DID を名乗るが署名が合わない
        body = "not json\n" + json.dumps(fake) + "\n"
        agent.fm.http_get = lambda url, timeout=30: (200, body)
        a.replay_room(room)
        self.assertEqual(a.st["poem"]["version"], 0)   # 署名不成立の「受領」は無視

    def test_room_resetup_with_new_generation_after_signing_is_flagged(self):
        """規則: ロースターは actual room generation を束縛する。署名後に審判が部屋を作り直して generation が変わったら、
        旧署名は無効で全員の再同意が要る。bot は黙って新 generation を採用してはいけない"""
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        self.assertEqual(rp.kinds(), ["roster"]); self.assertEqual(a.st["team"]["generation"], 1)
        a.st["referee"] = REF
        n_before = len(rp.calls); att_before = attention_text()
        recv(a, 9, rc(request_id="resetup-g-2", sender_did=REF, game_id="g", poem_room=TEAM + "g", room_generation=2, state_hash="hh"))
        a.on_roster_for_us({"seq": 12, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=2))   # 再同意の依頼
        new_posts = rp.calls[n_before:]
        # 直った: 受領時点で同じロースターを gen 2 に署名し直し、ATTENTION に CRITICAL を出す。再同意依頼（seq 12）は同内容なので二重には出さない
        self.assertTrue(any(k == "roster" for _, _, k in new_posts) or "generation" in attention_text()[len(att_before):],
                        "re-setup to a new generation neither re-signed nor reported")
        self.assertEqual([k for _, _, k in new_posts], ["roster"])
        self.assertEqual(a.st["team"]["generation"], 2); self.assertEqual(a.st["team"]["signed_generation"], 2)
        self.assertIn('"room_generation": 2', new_posts[0][1].replace('":2', '": 2'))

    def test_room_resetup_seen_while_replaying_is_resigned_on_the_lead_request(self):
        """起動時の再生中に再設定受領を見た場合は投稿しない。その後リーダーの再同意依頼（同メンバー・新 generation）が来たら
        その時点で 1 回だけ署名し直す。メンバーや部屋が違う依頼、同じ generation の再送には署名しない"""
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        a.st["referee"] = REF; a._replaying = True
        recv(a, 9, rc(request_id="resetup-g-2", sender_did=REF, game_id="g", poem_room=TEAM + "g", room_generation=2, state_hash="hh"))
        a._replaying = False
        self.assertEqual(rp.kinds(), ["roster"]); self.assertEqual(a.st["team"]["generation"], 2); self.assertEqual(a.st["team"]["signed_generation"], 1)
        # 違うメンバー / 違う部屋 / 古い generation には署名しない
        a.on_roster_for_us({"seq": 11, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=2, members=[LEAD, ME, OTHERS[0], L2]))
        a.on_roster_for_us({"seq": 11, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=2, poem_room=TEAM + "h"))
        a.on_roster_for_us({"seq": 11, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=1))
        self.assertEqual(rp.kinds(), ["roster"])
        # 正しい再同意依頼には 1 回だけ署名し直す（他メンバーの写しが続いても二重に出さない）
        a.on_roster_for_us({"seq": 12, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=2))
        a.on_roster_for_us({"seq": 13, "from": OTHERS[0], "ts": "t", "_sig_ok": True}, roster_json(room_generation=2))
        self.assertEqual(rp.kinds(), ["roster", "roster"]); self.assertEqual(a.st["team"]["signed_generation"], 2)
        self.assertIn("re-signed the same roster", attention_text())

    # ---------------- 2. ロースター署名 ----------------
    def test_roster_variants_that_must_not_be_signed(self):
        cases = {
            "3 members": roster_json(members=[LEAD, ME, OTHERS[0]]),
            "9 members": roster_json(members=[LEAD, ME] + OTHERS + [L2] + [f"did:key:z6Mk{c * 44}" for c in "ABCD"]),
            "dup DID": roster_json(members=[LEAD, ME, ME, OTHERS[0]]),
            "string generation": roster_json(room_generation="1"),
            "poem_room case": roster_json(poem_room=("D-" + CID + "-team-g")),
            "poem_room other game": roster_json(poem_room=TEAM + "h"),
            "game_id mismatch": roster_json(game_id="h", poem_room=TEAM + "h"),
            "bad DID in list": roster_json(members=[LEAD, ME, OTHERS[0], "did:key:z6Mkshort"]),
        }
        for name, j in cases.items():
            a, rp = roster_agent()
            a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, j)
            self.assertEqual(rp.calls, [], name); self.assertIsNone(a.st["team"], name)

    def test_roster_generation_true_is_not_an_integer(self):
        a, rp = roster_agent(view_gen=1)
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=True))
        # BUG: agent.py:618 isinstance(True, int) が真で、agent.py:627 True == 1 も真なので "room_generation":true のロースターに署名する
        self.assertEqual(rp.calls, [])

    def test_roster_with_foreign_contest_id_is_not_mirrored(self):
        """intro_text の約束は「リーダーの正式ロースターをバイト単位で写す」。contest_id が違うロースターを
        自分の contest_id に書き換えて署名すると、誰も同意していない別内容のロースターに同意することになる"""
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(contest_id="sonnet-1"))
        # BUG: agent.py:615 は j["contest_id"] を検証せず自分の contest_id で上書きして署名する
        self.assertEqual(rp.calls, [])

    def test_roster_signed_from_member_and_our_position_in_list_is_preserved(self):
        for members in ([ME, LEAD] + OTHERS, OTHERS + [LEAD, ME]):
            a, rp = roster_agent()
            a.on_roster_for_us({"seq": 5, "from": OTHERS[1], "ts": "t", "_sig_ok": True}, roster_json(members=members))
            self.assertEqual(rp.kinds(), ["roster"])
            self.assertEqual(json.loads(rp.calls[0][1])["members"], members)   # 順序を変えない

    def test_roster_from_stranger_or_unsigned_or_ignored_is_not_signed(self):
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": L2, "ts": "t", "_sig_ok": True}, roster_json())         # 一覧にいない他人
        a.on_roster_for_us({"seq": 6, "from": LEAD, "ts": "t", "_sig_ok": False}, roster_json())      # 署名不成立
        a.on_roster_for_us({"seq": 7, "from": LEAD, "ts": "t", "_sig_ok": None}, roster_json())       # sig 無し
        a.p["ignore_senders"].append(LEAD)
        a.on_roster_for_us({"seq": 8, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())       # 無視リスト
        self.assertEqual(rp.calls, [])

    def test_second_roster_after_signing_is_not_signed_again(self):
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        a.on_roster_for_us({"seq": 6, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(members=[LEAD, ME] + OTHERS + [L2]))
        a.on_roster_for_us({"seq": 7, "from": L2, "ts": "t", "_sig_ok": True}, roster_json(game_id="h", poem_room=TEAM + "h", members=[L2, ME] + OTHERS))
        self.assertEqual(rp.kinds(), ["roster"])

    def test_roster_for_dropped_game_is_not_signed(self):
        a, rp = roster_agent()
        a.drop_application("g", "test", note=False)
        self.assertEqual(a.applications(), {})
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        self.assertEqual(rp.calls, []); self.assertIsNone(a.st["team"])

    def test_roster_generation_mismatch_with_room_is_not_signed(self):
        a, rp = roster_agent(view_gen=2)
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json(room_generation=1))
        self.assertEqual(rp.calls, [])
        a, rp = roster_agent()
        agent.read_json = lambda room, wait: (_ for _ in ()).throw(RuntimeError("503"))
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        self.assertEqual(rp.calls, [])   # 部屋が読めなければ署名しない

    def test_roster_members_not_strings_does_not_crash_handle(self):
        a, rp = roster_agent()
        j = roster_json(members=[LEAD, ME, 123, {"x": 1}])
        try:
            a.handle({"_room": DISC, "from": LEAD, "seq": 5, "ts": "t", "_sig_ok": True, "text": json.dumps(j)})
        except TypeError:
            pass   # agent.py:603 は非文字列メンバーで TypeError を投げる。run() のループが握りつぶすので投稿はされない（観察のみ、バグ扱いにしない）
        self.assertEqual(rp.calls, []); self.assertIsNone(a.st["team"])

    # ---------------- 3. 応募 ----------------
    def offer(self, a, seq, gid, lead, text=None):
        a.addressed.append({"seq": seq, "from": lead, "text": text or f"@TAejK6 seat on {gid}", "ts": "2026-09-11T08:00:00Z", "_at": 0})
        a._disc_at = 0
        self.llm_out = {"action": "reply", "text": f"yes-{gid}. accepting the seat.", "reason": "",
                        "seat_offer": {"game_id": gid, "lead_did": lead, "member_list_seq": None}}
        a.maybe_reply_discovery()
        if not a.q.empty():
            a.handle(a.q.get_nowait())

    def disc_agent(self):
        a = fresh({"reply_discovery": True, "accept_seat": True}); a.key = object(); a.st["registered"] = {"seq": 1}
        a.p["accept"]["require_lead_seen_before_opening"] = False
        for d in (LEAD, OTHERS[0], OTHERS[1], L2):
            a.st["first_seen"][d] = agent.iso(agent.utc_now() - 3600)
        rp = RecordingPost(); a.post = rp
        return a, rp

    def test_offers_at_cap_are_declined_and_reply_suppressed(self):
        a, rp = self.disc_agent(); a.p["max_applications"] = 2
        self.offer(a, 1, "g1", LEAD); self.offer(a, 2, "g2", OTHERS[0]); self.offer(a, 3, "g3", OTHERS[1])
        self.assertEqual(sorted(a.applications()), ["g1", "g2"])
        self.assertEqual(sum(1 for k in rp.kinds() if k == "disc-reply"), 2)   # 3 件目の受諾文は出さない
        self.assertIn("NOT accepted", attention_text())

    def test_same_lead_two_games_and_drop_then_reoffer(self):
        a, rp = self.disc_agent()
        self.offer(a, 1, "g1", LEAD); self.offer(a, 2, "g2", LEAD)
        self.assertEqual(sorted(a.applications()), ["g1", "g2"])
        a.drop_application("g1", "test", note=True)
        self.assertEqual(rp.kinds()[-1], "release-note"); self.assertIn(LEAD[-8:], rp.calls[-1][1])
        self.offer(a, 3, "g1", LEAD)
        self.assertNotIn("g1", a.applications())   # 解除済みは再受諾しない
        self.assertEqual(a.st["agreed"]["game_id"], "g2")

    def test_manual_agreed_for_dropped_game_is_ignored_and_cap_respected(self):
        a = fresh(); a.st["dropped"] = ["g1"]
        a.p["manual_agreed"] = {"game_id": "g1", "lead_did": LEAD}; a.maybe_announce()
        self.assertEqual(a.applications(), {})
        a.p["max_applications"] = 1; a.st["applications"] = {"x": {"game_id": "x", "lead_did": L2, "at": agent.iso()}}
        a.p["manual_agreed"] = {"game_id": "g2", "lead_did": LEAD}; a.maybe_announce()
        self.assertNotIn("g2", a.applications())
        a.p["manual_agreed"] = {"game_id": "BAD ID", "lead_did": LEAD}; a.maybe_announce()
        self.assertEqual(sorted(a.applications()), ["x"])

    def test_expiry_math_uses_later_of_application_and_referee(self):
        a = fresh(); a.p["agreed_ttl_hours"] = 6; a.p["lead_silence_hours"] = 48
        now = agent.utc_now()
        a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": agent.iso(now - 7 * 3600), "lead_last_seen": agent.iso(now)}}
        a.st["agreed"] = a.st["applications"]["g"]
        a.st["referee_at"] = agent.iso(now - 3600)
        a.expire_agreed(); self.assertIn("g", a.applications())          # 審判確定から 1 時間: まだ
        a.st["applications"]["g"]["at"] = agent.iso(now - 3600); a.st["referee_at"] = agent.iso(now - 7 * 3600)
        a.expire_agreed(); self.assertIn("g", a.applications())          # 応募から 1 時間: まだ
        a.st["applications"]["g"]["at"] = agent.iso(now - 7 * 3600)
        a.expire_agreed(); self.assertEqual(a.applications(), {}); self.assertIsNone(a.st["agreed"])
        # 沈黙: lead_last_seen 無し・応募が silence より新しい → 落とさない
        a = fresh(); a.p["lead_silence_hours"] = 1
        a.st["applications"] = {"g": {"game_id": "g", "lead_did": LEAD, "at": agent.iso(agent.utc_now() - 1800)}}
        a.expire_agreed(); self.assertIn("g", a.applications())
        a.st["applications"]["g"]["at"] = agent.iso(agent.utc_now() - 7200)
        a.expire_agreed(); self.assertEqual(a.applications(), {})

    def test_withdraw_others_posts_one_note_per_other_application(self):
        a, rp = roster_agent()
        a.st["applications"].update({"h": {"game_id": "h", "lead_did": OTHERS[0], "at": agent.iso()},
                                     "k": {"game_id": "k", "lead_did": L2, "at": agent.iso()}})
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        notes = [t for _, t, k in rp.calls if k == "release-note"]
        self.assertEqual(len(notes), 2)
        self.assertTrue(any("h:" in t and OTHERS[0][-8:] in t for t in notes))
        self.assertTrue(any("k:" in t and L2[-8:] in t for t in notes))
        self.assertEqual(sorted(a.st["dropped"]), ["h", "k"]); self.assertEqual(list(a.applications()), ["g"])
        self.assertEqual(a.st["agreed"]["game_id"], "g")

    # ---------------- 4. 語の提案 ----------------
    def proposer(self, syllables, current, plan=None):
        a = with_team(fresh({"propose_words": True})); a.key = object(); a.opening = 0
        a.st["poem"].update({"syllables": syllables, "current": current, "version": 5, "state_hash": "h5"})
        a.st["plan"] = plan
        rp = RecordingPost(); a.post = rp
        return a, rp

    def test_line_14_at_139_never_proposes(self):
        plan = ["x"] * 13 + ["And every fair from fair sometime declines"]
        a, rp = self.proposer(139, "And every fair from fair sometime".split(), plan)
        self.llm_out = {"word": "day", "alternatives": ["I", "a", "the"], "reason": ""}
        a.maybe_propose()
        while not a.q.empty():
            a.handle(a.q.get_nowait())
        self.assertEqual(rp.calls, [])
        # LLM 候補も全て弾く
        for w in ("a", "I", "day", "declines"):
            self.assertFalse(a.valid_word(w, 14, 1))

    def test_nine_syllables_and_two_syllable_plan_word_falls_back_to_llm(self):
        plan = ["Shall I compare thee to a summer"] + ["x"] * 13
        a, rp = self.proposer(9, "Shall I compare thee to a".split(), plan)   # 9 音節、plan の次は summer (2)
        self.llm_out = None
        a.maybe_propose()
        self.assertEqual(rp.calls, []); self.assertEqual([t for t, _ in self.llm_calls], ["word"])
        self.assertEqual(json.loads(self.llm_calls[0][1])["syllables_remaining"], 1)

    def test_plan_divergence_and_desync_do_not_post_plan_word(self):
        plan = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        a, rp = self.proposer(3, ["Shall", "we"], plan)
        a.maybe_propose()
        self.assertEqual(rp.calls, []); self.assertEqual(len(self.llm_calls), 1)
        a, rp = self.proposer(2, ["Shall", "I"], plan); a.st["poem"]["desync"] = True
        a.maybe_propose()
        self.assertEqual(rp.kinds(), ["word"]); self.assertIn('"word":"compare"', rp.calls[0][1])

    def test_pending_expired_reproposes_only_once_and_not_while_pending(self):
        plan = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        a, rp = self.proposer(0, [], plan)
        a.st["pending_word"] = {"request_id": "w5-h5-TAejK6", "word": "Shall", "at": agent.iso()}
        a.maybe_propose(); self.assertEqual(rp.calls, [])
        a.st["pending_word"]["at"] = "2026-09-11T00:00:00Z"
        a.maybe_propose(); self.assertEqual(len(rp.calls), 1)
        a.maybe_propose(); self.assertEqual(len(rp.calls), 1)

    def test_rejection_cap_and_retry_backoff(self):
        plan = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        a, rp = self.proposer(0, [], plan)
        a.st["poem"]["rejected"] = {"5": [{"word": "w", "reason": "", "at": "2026-09-11T00:00:00Z"}] * 3}
        a.maybe_propose(); self.assertEqual(rp.calls, [])                        # 上限
        a.st["poem"]["rejected"] = {"5": [{"word": "w", "reason": "", "at": agent.iso()}]}
        a.maybe_propose(); self.assertEqual(rp.calls, [])                        # 直後は待つ
        a.st["poem"]["rejected"] = {"5": [{"word": "Shall", "reason": "", "at": "2026-09-11T00:00:00Z"}]}
        a.maybe_propose(); self.assertEqual(rp.calls, [])                        # 拒否済みの plan 語は出さず LLM へ
        self.assertEqual(len(self.llm_calls), 1)
        a.st["poem"]["rejected"] = {"4": [{"word": "Shall", "reason": "", "at": agent.iso()}] * 3}
        a.maybe_propose(); self.assertEqual(rp.kinds(), ["word"])                # 別の版の拒否は関係ない

    def test_no_proposal_before_ready_or_when_last_contributor(self):
        plan = ["Shall I compare thee to a summer's day"] + ["x"] * 13
        a, rp = self.proposer(0, [], plan); a.st["team"]["ready"] = False
        a.maybe_propose(); self.assertEqual(rp.calls, [])
        a, rp = self.proposer(0, [], plan); a.st["poem"]["last_contributor"] = ME
        a.maybe_propose(); self.assertEqual(rp.calls, [])
        a, rp = self.proposer(0, [], plan); a.st["poem"]["state_hash"] = None
        a.maybe_propose(); self.assertEqual(rp.calls, [])

    # ---------------- 5. 韻律 ----------------
    def test_canonical_text_keeps_punctuation_and_apostrophes(self):
        lines = ["Shall I compare thee to a summer's day?"] * 14
        ct = prosody.canonical_text(lines)
        self.assertEqual(ct.count("\n\n"), 3); self.assertFalse(ct.endswith("\n"))
        self.assertEqual(ct.split("\n\n")[0].split("\n")[0], "Shall I compare thee to a summer's day?")
        self.assertEqual(prosody.poem_sha256(lines), prosody.poem_sha256(["  Shall I  compare thee to a summer's day? "] * 14))
        self.assertNotEqual(prosody.poem_sha256(lines), prosody.poem_sha256(["Shall I compare thee to a summer's day"] * 14))
        with self.assertRaises(ValueError):
            prosody.canonical_text(lines[:13])

    def test_line_syllables_charges_max_pronunciation(self):
        lex = prosody.lexicon()
        self.assertEqual(prosody.line_syllables(["fire"], lex), max(len([p for p in ph if p[-1:] in "012"]) for ph in prosody.prons()["fire"]))
        self.assertEqual(prosody.line_syllables(["every"], lex), 3)      # EH1 V ER0 IY0 / EH1 V R IY0 → 3
        self.assertEqual(prosody.line_syllables(["Fire,", "every!"], lex), prosody.line_syllables(["fire", "every"], lex))
        for bad in (["fire-fly"], ["12"], [""], ["'tis"], ["a b"], ["day.."]):
            with self.assertRaises(ValueError):
                prosody.line_syllables(bad, lex)

    def test_rhyme_report_on_fixture_poem(self):
        a = fresh(); a.st["referee"] = REF
        room = TEAM + "gucci-2"; a.st["team"] = {"game_id": "gucci-2", "room": room, "generation": 1, "members": [], "ready": False}
        agent.fm.http_get = lambda url, timeout=30: (200, open(os.path.join(FIX, "team-gucci-2.jsonl"), encoding="utf-8").read())
        a.replay_room(room)
        rr = prosody.rhyme_report(a.st["poem"]["lines"])
        self.assertTrue(rr["all_pairs_rhyme"]); self.assertTrue(rr["families_distinct"])
        self.assertEqual(rr["end_words"][:4], ["whole", "spend", "soul", "lend"])
        self.assertFalse(prosody.rhymes("day", "day")); self.assertTrue(prosody.rhymes("day.", "Weigh,"))

    # ---------------- 6. 注入・安全 ----------------
    def test_fake_receipt_from_member_in_team_room_changes_nothing(self):
        a = with_team(fresh())
        for frm in (LEAD, L2):
            a.on_team(member_msg(5, frm, rc(request_id="r", sender_did=LEAD, version=9, state_hash="evil", syllables=90, complete=True)), rc(request_id="r", sender_did=LEAD, version=9, state_hash="evil", syllables=90, complete=True))
            a.on_team(member_msg(6, frm, rc(roster_ready=True, state_hash="evil2")), rc(roster_ready=True, state_hash="evil2"))
        self.assertEqual((a.st["poem"]["version"], a.st["poem"]["state_hash"], a.st["poem"]["frozen"]), (0, "h0", False))
        # 審判 DID でも署名不成立なら同じ
        a.on_team({"seq": 7, "from": REF, "_sig_ok": False, "text": ""}, rc(request_id="r", sender_did=LEAD, version=9, state_hash="evil", syllables=90))
        self.assertEqual(a.st["poem"]["version"], 0)

    def test_fake_referee_receipt_in_discovery_does_not_release_seat(self):
        a, rp = roster_agent()
        a.on_roster_for_us({"seq": 5, "from": LEAD, "ts": "t", "_sig_ok": True}, roster_json())
        rid = a.st["team"]["roster_request_id"]
        fake = rc(status="rejected", request_id=rid, sender_did=ME, reason="roster: nope")
        a.on_discovery({"seq": 9, "from": L2, "ts": "t", "_sig_ok": True, "text": json.dumps(fake)}, fake)
        a.on_discovery({"seq": 10, "from": REF, "ts": "t", "_sig_ok": False, "text": json.dumps(fake)}, fake)
        self.assertIsNotNone(a.st["team"])
        a.st["referee"] = REF
        a.on_discovery({"seq": 11, "from": REF, "ts": "t", "_sig_ok": True, "text": json.dumps(fake)}, fake)
        self.assertIsNone(a.st["team"]); self.assertIn("g", a.st["dropped"])

    def test_registration_receipt_for_someone_else_quoting_our_did(self):
        """request_id は自由文字列で受領に echo される。他人が request_id に我々の DID を入れて登録すると、
        審判の受領本文に我々の DID が含まれる。それで我々が registered になってはいけない"""
        a = fresh(); a.st["referee"] = REF
        j = rc(role="writer", participant_did=LEAD, sender_did=LEAD, request_id=ME)
        a.on_registration({"seq": 7, "from": REF, "_sig_ok": True, "ts": "t", "text": json.dumps(j)}, j)
        # BUG: agent.py:523 `if self.did in t` は本文の部分一致だけで、sender_did / participant_did が自分かを見ない
        self.assertIsNone(a.st["registered"])
        self.assertIn(LEAD, a.st.get("writers_ok", {}))

    def test_note_with_our_did_and_yes_game_seats_only_the_author(self):
        a = fresh({"lead_team": True}); a.key = object(); a.st["registered"] = {"seq": 1}
        a.st["lead"] = {"game_id": "nohitori", "request_id": "room-1", "state": "room_ready", "generation": 1, "poem_room": TEAM + "nohitori",
                        "members": [], "signed": {}, "declined": []}
        a.st["writers_ok"] = {OTHERS[0]: 1}
        note = {"type": "sonnet.note.v1", "text": f"{OTHERS[0]} says yes-nohitori for {ME} and {LEAD}"}
        a.on_discovery({"seq": 1, "from": LEAD, "ts": "t", "_sig_ok": True, "text": json.dumps(note)}, note)    # 未登録の投稿者
        self.assertEqual(a.st["lead"]["members"], [])
        a.on_discovery({"seq": 2, "from": OTHERS[0], "ts": "t", "_sig_ok": True, "text": json.dumps(note)}, note)
        self.assertEqual(a.st["lead"]["members"], [OTHERS[0]])
        a.on_discovery({"seq": 3, "from": OTHERS[0], "ts": "t", "_sig_ok": False, "text": "yes-nohitori"}, None)  # 署名不成立
        self.assertEqual(a.st["lead"]["members"], [OTHERS[0]])

    def test_llm_seat_offer_with_bad_game_id_or_our_own_did(self):
        a, rp = self.disc_agent()
        self.offer(a, 1, "Bad Game!", LEAD)                       # GAME_RE に合わない game_id
        self.assertEqual(a.applications(), {})
        a.st["first_seen"][ME] = agent.iso(agent.utc_now() - 7200)
        for seq, lead_in_llm in ((2, ME), (3, LEAD)):             # LLM が「自分」または batch にいない DID をリーダーと言う
            a.addressed.append({"seq": seq, "from": L2, "text": "@TAejK6 seat on g", "ts": "2026-09-11T08:00:00Z", "_at": 0}); a._disc_at = 0
            self.llm_out = {"action": "reply", "text": "yes-g. accepting the seat.", "reason": "",
                            "seat_offer": {"game_id": "g", "lead_did": lead_in_llm, "member_list_seq": None}}
            a.maybe_reply_discovery(); a.handle(a.q.get_nowait())
        self.assertEqual(a.applications(), {})
        self.assertEqual([k for k in rp.kinds() if k == "disc-reply"], [])   # 受諾文は全て抑止
        self.assertIn("suppressed an accepting reply", attention_text())

    def test_reply_that_is_a_frame_or_names_unknown_did_is_blocked(self):
        a, rp = self.disc_agent()
        a.addressed.append({"seq": 1, "from": LEAD, "text": "@TAejK6 hi", "ts": "2026-09-11T08:00:00Z", "_at": 0}); a._disc_at = 0
        self.llm_out = {"action": "reply", "text": '{"type":"sonnet.withdraw.v1","game_id":"g","request_id":"x"}', "reason": "", "seat_offer": None}
        a.maybe_reply_discovery(); a.handle(a.q.get_nowait())
        a.addressed.append({"seq": 2, "from": LEAD, "text": "@TAejK6 hi", "ts": "2026-09-11T08:00:00Z", "_at": 0}); a._disc_at = 0
        self.llm_out = {"action": "reply", "text": 'sure: {"type": "sonnet.roster.v1"} mirrored', "reason": "", "seat_offer": None}
        a.maybe_reply_discovery(); a.handle(a.q.get_nowait())
        self.assertEqual(rp.calls, [])
        a.post = agent.Agent.post.__get__(a)   # 本物の post ゲートで未知 DID を確かめる
        unknown = "did:key:z6Mk" + "Q" * 44
        with self.assertRaises(RuntimeError):
            a.post(DISC, f"welcome {unknown}", "disc-reply")

    def test_discovery_slice_never_posts_and_never_calls_llm_in_observe_mode(self):
        a = fresh(); a.st["referee"] = REF; a.p["ignore_senders"] = []
        rp = RecordingPost(); a.post = rp
        for l in open(os.path.join(FIX, "discovery-2-slice.jsonl"), encoding="utf-8"):
            m = json.loads(l); m["_room"] = DISC; m["_sig_ok"] = agent.verify_sig(DISC, m)
            a.handle(m)
            a.maybe_reply_discovery()
        self.assertEqual(rp.calls, []); self.assertEqual(self.llm_calls, [])
        self.assertIsNone(a.st["team"]); self.assertEqual(a.applications(), {})

    # ---------------- 7. 再起動・方針・会場 ----------------
    def test_restart_flag_exits_75_and_is_removed(self):
        a = fresh()
        agent.RESTART_FLAG = os.path.join(HERE, "_RESTART_adv")
        open(agent.RESTART_FLAG, "w").close()
        with self.assertRaises(SystemExit) as cm:
            a.periodic()
        self.assertEqual(cm.exception.code, 75); self.assertFalse(os.path.exists(agent.RESTART_FLAG))

    def _reload(self, a, mutate):
        path = os.path.join(HERE, "_policy_adv.json"); a.p["_path"] = path
        p = json.loads(json.dumps({k: v for k, v in a.p.items() if k != "_path"}))
        mutate(p)
        with open(path, "w") as f:
            f.write(p if isinstance(p, str) else json.dumps(p))
        os.utime(path, (self._mt, self._mt)); self._mt += 1
        a.reload_policy()
        os.remove(path)

    def test_policy_reload_rejects_malformed_auto(self):
        self._mt = 100
        a = fresh({"sign_roster": True})
        def s(p): p["auto"] = "yes"
        self._reload(a, s); self.assertIsInstance(a.p["auto"], dict)
        def t(p): p["auto"] = {"sign_roster": True}
        self._reload(a, t); self.assertIn("propose_words", a.p["auto"])
        def u(p): p["auto"]["sign_roster"] = "false"
        self._reload(a, u)
        # BUG: agent.py:1199 は auto の値が bool かを見ない。"false"（文字列）は真として扱われ、README の「false なら読むだけ」に反する
        self.assertIs(a.p["auto"]["sign_roster"], True)

    def test_policy_reload_rejects_missing_rooms(self):
        self._mt = 200
        a = fresh()
        def s(p): del p["rooms"]
        self._reload(a, s)
        # BUG: agent.py:1197-1200 は did/key_path/auto しか検証せず、rooms の無い方針を採用して以後の periodic() が毎周 KeyError で落ちる
        self.assertIn("rooms", a.p)
        a.periodic()   # 採用後も動き続けること

    def test_policy_reload_keeps_previous_on_garbage_and_did_change(self):
        self._mt = 300
        a = fresh(); before = json.dumps(a.p, sort_keys=True)
        path = os.path.join(HERE, "_policy_adv.json"); a.p["_path"] = path
        open(path, "w").write("{not json"); os.utime(path, (301, 301)); a.reload_policy()
        self.assertEqual(json.dumps({k: v for k, v in a.p.items() if k != "_path"}, sort_keys=True), json.dumps({k: v for k, v in json.loads(before).items() if k != "_path"}, sort_keys=True))
        def s(p): p["did"] = LEAD
        self._reload(a, s); self.assertEqual(a.did, ME); self.assertEqual(a.p["did"], ME)
        self.assertIn("policy reload failed", attention_text())

    def test_venue_watch_survives_bad_json(self):
        a = fresh()
        bodies = iter(["<html>502</html>", "[]", '{"messages":[{"text":null},{"text":"created mb-sonnet-9-discovery","ts":"t"}]}'])
        agent.fm.http_get = lambda url, timeout=30: (200, next(bodies))
        a.p["official_repo_raw"] = None
        a.venue_watch(); a.venue_watch(); a.venue_watch()
        self.assertIn("sonnet-9", attention_text())
        a.p["official_repo_raw"] = "https://example.invalid"
        agent.fm.http_get = lambda url, timeout=30: (200, "{}" if url.endswith("events?format=json&limit=200") else "not json at all")
        a.venue_watch()
        agent.fm.http_get = lambda url, timeout=30: (200, "{}" if "events" in url else '{"contest_id":"sonnet-7"}' if url.endswith("contest.json") else "# LAUNCH\nreferee did:key:z6Mk" + "R" * 44)
        a.venue_watch()
        t = attention_text()
        self.assertIn("VENUE CHANGED", t); self.assertIn("no longer lists our pinned referee_did", t)


if __name__ == "__main__":
    unittest.main()
