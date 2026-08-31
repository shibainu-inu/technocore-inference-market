#!/usr/bin/env python3
"""
flopmarket.py — Technocore 上の推論市場プロトタイプ（FLOPティーザーのセッション要求形式に準拠）

 役割
   request   発注エージェント: REQ を署名付きで投稿し、模擬FLOPの手数料をエスクロー
   miner     マイナー:         部屋を監視し REQ に Ollama で応答（RES）。手数料の85%を受領
   validate  バリデーター:     RES を再実行して照合し VER を投稿。手数料の15%をプールへ

 前提
   - technocore_did.py と同じディレクトリに置く（署名関数を流用）
   - Ollama が 127.0.0.1:11434 で稼働中
   - 台帳(ledger.db)はローカルSQLite。実トークンは存在しない「模擬FLOP」

 使い方
   python flopmarket.py request --key did_key.json  --model qwen2.5:1.5b --fee 30 "prompt text"
   python flopmarket.py miner   --key did_miner.json --model qwen2.5:1.5b
   python flopmarket.py validate --key did_key.json --model qwen2.5:1.5b
   python flopmarket.py ledger

 パスフレーズは起動時に1回入力（常駐用に環境変数 TC_PASS も可。ただし平文保存は避けること）
"""
import argparse, getpass, hashlib, json, os, re, sqlite3, sys, time, urllib.parse, urllib.request
from cryptography.hazmat.primitives import serialization
import technocore_did as tc

ROOM = "inference-agents"
BASE = "https://technocore.chat"
OLLAMA = "http://127.0.0.1:11434"
LEDGER = "ledger.db"
STATE = "state.json"
LINE = re.compile(r"^\[(\d+)\] (\S+) <([^>]+)> (.*)$")
MINER_SHARE = 0.85      # ティーザー: 推論手数料の85%はマイナー、15%はバリデーター
INITIAL_BALANCE = 1000  # 模擬FLOPの初期残高（新規DIDに付与）
READ_WAIT = 10          # long-poll の待ち秒数（--wait で変更可。接続を占有する時間でもある）
ERR_SLEEP = 15          # 読み取り失敗後の待機秒数（--err-sleep）
READSTAT_WIN = 300      # 読み取り成功/失敗の集計窓（秒）。この間隔で READSTAT 行を台帳に書く

# ---------- 共通 ----------
def load_key(path):
    pem = json.load(open(path))["private_key_pem"].encode()
    pw = os.environ.get("TC_PASS") or getpass.getpass(f"パスフレーズ ({path}): ")
    return serialization.load_pem_private_key(pem, password=pw.encode())

def did_of(key):
    pub = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return tc.did_from_pub(pub)

def short(did):  # 部屋の表示形式 <z6Mk…PvqA> に合わせる
    return did.replace("did:key:", "")[:4] + "…" + did[-4:]

def http_get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "flopmarket/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")

def post_signed(key, text, nonce=None):
    """署名付き投稿。nonce は単調増加（ミリ秒）"""
    nonce = nonce or int(time.time() * 1000)
    url = tc.sign_url(key, "say", [ROOM], text, nonce)
    st, body = http_get(url)
    m = re.search(r"\[(\d+)\] \S+ <([^>]+)> " + re.escape(" ".join(text.split()))[:60], body)
    seq = int(m.group(1)) if m else None
    return st, seq, body

def read_room(since, wait=10):
    st, body = http_get(f"{BASE}/r/{ROOM}?since={since}&wait={wait}", timeout=wait + 20)
    msgs = []
    for ln in body.splitlines():
        m = LINE.match(ln)
        if m:
            msgs.append({"seq": int(m[1]), "ts": m[2], "from": m[3], "text": m[4]})
    nxt = re.search(r"next: /r/[^?]+\?since=(\d+)", body)
    return msgs, int(nxt[1]) if nxt else since

def err_kind(e):
    """読み取りエラーの分類。503(入口での即時拒否) と timeout(受理後に遅い) を分けて数える"""
    s = str(e)
    if "503" in s: return "503"
    if "502" in s: return "502"
    if "timed out" in s or "timeout" in s.lower(): return "timeout"
    if "name resolution" in s: return "dns"
    if "Connection refused" in s or "Connection reset" in s: return "conn"
    return "other"

class ReadMeter:
    """読み取りの成功数・失敗数・応答時間を集計し、READSTAT_WIN 秒ごとに台帳へ1行書く。
    成功を1件ずつ記録すると台帳が肥大化するため窓で集計する。失敗は従来どおり ERR 行にも残す（ms付き）。
    2026-08-29〜30 の 503 障害（Issue #588 コメント）で「正確な失敗率」と「503(速い) vs timeout(遅い)」の分離が必要になり追加。"""
    def __init__(self, c, role, wait, win=None):
        self.c, self.role, self.wait, self.win = c, role, wait, win or READSTAT_WIN
        self.reset()
    def reset(self):
        self.t0 = time.time(); self.ok = 0; self.err = {}; self.ok_ms = []; self.err_ms = {}
    def record(self, ok, ms, e=None):
        if ok:
            self.ok += 1; self.ok_ms.append(ms)
        else:
            k = err_kind(e); self.err[k] = self.err.get(k, 0) + 1; self.err_ms.setdefault(k, []).append(ms)
            log(self.c, "ERR", {"e": str(e)[:120], "kind": k, "ms": ms, "role": self.role})
        if time.time() - self.t0 >= self.win:
            self.flush()
    def flush(self):
        import statistics
        n_err = sum(self.err.values())
        if self.ok + n_err == 0:
            self.reset(); return
        med = lambda xs: int(statistics.median(xs)) if xs else None
        p90 = lambda xs: int(sorted(xs)[int(len(xs) * 0.9)]) if xs else None
        log(self.c, "READSTAT", {"role": self.role, "wait": self.wait, "win_s": int(time.time() - self.t0),
                                 "ok": self.ok, "err": self.err,
                                 "ok_ms_med": med(self.ok_ms), "ok_ms_p90": p90(self.ok_ms),
                                 "err_ms_med": {k: med(v) for k, v in self.err_ms.items()}})
        self.reset()

def read_room_metered(meter, since, wait):
    """read_room に計測を付けたもの。失敗時は ERR 記録の上で例外を投げ直す"""
    t0 = time.time()
    try:
        r = read_room(since, wait=wait)
    except Exception as e:
        meter.record(False, int((time.time() - t0) * 1000), e); raise
    meter.record(True, int((time.time() - t0) * 1000))
    return r

def parse_msg(text, kind):
    if not text.startswith(kind + " "):
        return None
    try:
        return json.loads(text[len(kind) + 1:])
    except json.JSONDecodeError:
        return None

def load_state():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}

def save_state(s):
    json.dump(s, open(STATE, "w"), indent=1)

# ---------- Ollama ----------
def ollama_model_digest(model):
    """Ollama の /api/tags からモデルのダイジェスト（`ollama list` の ID と同じ sha256）を取得"""
    with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=30) as r:
        tags = json.load(r)
    for m in tags.get("models", []):
        if m.get("name") == model or m.get("model") == model:
            return m.get("digest", "")
    return "unknown:" + model

def ollama_generate(model, prompt, max_tokens=120):
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0, "seed": 42, "num_predict": max_tokens}}
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        out = json.load(r)
    ms = int((time.time() - t0) * 1000)
    return out.get("response", ""), out.get("eval_count", 0), ms

def ollama_generate_steady(model, prompt, max_tokens=120):
    """同じプロンプトを2回生成し、2回目（プロンプトキャッシュ再利用後の定常状態）を採用する。
    実測: キャッシュ有無でtemp=0でも出力が分岐する（2026-08-28, N100とXeon Broadwellで同一挙動）。
    1回目のsha256も返し、コールド/ウォーム差を記録する。"""
    out1, _, ms1 = ollama_generate(model, prompt, max_tokens)
    out2, tokens2, ms2 = ollama_generate(model, prompt, max_tokens)
    return out2, tokens2, ms1 + ms2, hashlib.sha256(out1.encode()).hexdigest()

# ---------- 台帳（模擬FLOP） ----------
def db():
    c = sqlite3.connect(LEDGER)
    c.execute("CREATE TABLE IF NOT EXISTS bal (did TEXT PRIMARY KEY, amt REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS escrow (req_id TEXT PRIMARY KEY, did TEXT, fee REAL, state TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS log (ts TEXT, event TEXT, detail TEXT)")
    return c

def ensure(c, did):
    if c.execute("SELECT 1 FROM bal WHERE did=?", (did,)).fetchone() is None:
        c.execute("INSERT INTO bal VALUES (?,?)", (did, INITIAL_BALANCE))

def log(c, event, detail):
    c.execute("INSERT INTO log VALUES (?,?,?)", (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), event, json.dumps(detail, ensure_ascii=False)))
    c.commit()

# ---------- 役割 ----------
def cmd_request(a):
    key = load_key(a.key); me = did_of(key); c = db(); ensure(c, me)
    bal = c.execute("SELECT amt FROM bal WHERE did=?", (me,)).fetchone()[0]
    if bal < a.fee:
        sys.exit(f"残高不足: {bal} < {a.fee}")
    req_id = hashlib.sha256(f"{me}{time.time()}{a.prompt}".encode()).hexdigest()[:12]
    try:
        mh = ollama_model_digest(a.model)
    except Exception:
        mh = "unset"   # 発注側に Ollama は不要（マイナー/バリデーターはモデル名で照合する）
    req = {"id": req_id, "model": a.model, "model_hash": mh,
           "max_latency_ms": a.max_latency, "flops_est": a.flops, "confidential": False,
           "fee": a.fee, "prompt": a.prompt[:400]}
    c.execute("UPDATE bal SET amt=amt-? WHERE did=?", (a.fee, me))
    c.execute("INSERT INTO escrow VALUES (?,?,?,?)", (req_id, me, a.fee, "open"))
    log(c, "REQ", req)
    st, seq, _ = post_signed(key, "REQ " + json.dumps(req, ensure_ascii=False, separators=(",", ":")))
    print(f"REQ {req_id} posted seq={seq} fee={a.fee} escrowed. balance={bal - a.fee}")
    print(f"watch RES/VER: {BASE}/r/{ROOM}?since={seq}")

def cmd_join(a):
    """外部参加者向けの最小導線: DID がなければ生成し、Ollama なしで REQ を1件投稿する。"""
    if not os.path.exists(a.key):
        print(f"{a.key} が見つからないため、新しい DID を生成します（パスフレーズを決めてください）")
        tc.gen(a.key)
        print("生成した鍵ファイルは共有・コミットしないでください。")
    cmd_request(a)

def cmd_miner(a):
    key = load_key(a.key); me = did_of(key); c = db(); ensure(c, me)
    st = load_state(); since = st.get("miner_since", 0)
    if since == 0:  # 初回は現在位置から（過去の山を処理しない）
        _, since = read_room(0, wait=0)
    print(f"miner {short(me)} watching /r/{ROOM} from seq {since} model={a.model} wait={a.wait}s")
    log(c, "START", {"role": "miner", "me": me[-8:], "since": since, "wait": a.wait})
    meter = ReadMeter(c, "miner", a.wait)
    while True:
        try:
            msgs, since = read_room_metered(meter, since, a.wait)
        except Exception as e:
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "read error:", e); time.sleep(a.err_sleep); continue
        for m in msgs:
            req = parse_msg(m["text"], "REQ")
            if not req or req.get("model") != a.model:
                continue
            if not m["from"].startswith("z6Mk"):   # 署名なし（~nick）の要求は受けない
                continue
            print(f"[{m['seq']}] REQ {req['id']} from {m['from']} fee={req['fee']}")
            try:
                out, tokens, ms, sha1 = ollama_generate_steady(a.model, req["prompt"])
            except Exception as e:
                print("ollama error:", e); continue
            res = {"req_id": req["id"], "req_seq": m["seq"], "miner": me[-8:], "model_hash": ollama_model_digest(a.model),
                   "output_sha256": hashlib.sha256(out.encode()).hexdigest(), "first_run_sha256": sha1, "runs": 2, "req_from": m["from"],
                   "output_head": out[:200], "tokens": tokens, "latency_ms": ms,
                   "within_latency": ms <= req.get("max_latency_ms", 10**9)}
            log(c, "RES", res)
            try:
                _, seq, _ = post_signed(key, "RES " + json.dumps(res, ensure_ascii=False, separators=(",", ":")))
                print(f"  -> RES posted seq={seq} {ms}ms {tokens}tok sha={res['output_sha256'][:12]}")
            except Exception as e:
                print("post error:", e)
        st["miner_since"] = since; save_state(st)

def cmd_validate(a):
    key = load_key(a.key); me = did_of(key); c = db(); ensure(c, me)
    st = load_state(); since = st.get("val_since", 0)
    if since == 0:
        _, since = read_room(0, wait=0)
    reqs = {}
    print(f"validator {short(me)} watching from seq {since} wait={a.wait}s")
    log(c, "START", {"role": "validator", "me": me[-8:], "since": since, "wait": a.wait})
    meter = ReadMeter(c, "validator", a.wait)
    while True:
        try:
            msgs, since = read_room_metered(meter, since, a.wait)
        except Exception as e:
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "read error:", e); time.sleep(a.err_sleep)
            maybe_daily_report(key, c, st); continue
        for m in msgs:
            r = parse_msg(m["text"], "REQ")
            if r: reqs[r["id"]] = r; continue
            res = parse_msg(m["text"], "RES")
            if not res or res["req_id"] not in reqs or reqs[res["req_id"]]["model"] != a.model:
                continue
            req = reqs[res["req_id"]]
            out, _, ms, sha1 = ollama_generate_steady(a.model, req["prompt"])
            sha = hashlib.sha256(out.encode()).hexdigest()
            verdict = "match" if sha == res["output_sha256"] else ("similar" if out[:60] == res.get("output_head", "")[:60] else "mismatch")
            ver = {"res_seq": m["seq"], "req_id": req["id"], "verdict": verdict,
                   "recomputed_sha256": sha, "validator_latency_ms": ms, "first_run_sha256": sha1, "runs": 2}
            # 決済: match/similar ならエスクロー解放（85%マイナー・15%バリデーター）
            row = c.execute("SELECT fee,state FROM escrow WHERE req_id=?", (req["id"],)).fetchone()
            if row and row[1] == "open":
                fee = row[0]
                if verdict in ("match", "similar"):
                    miner_did = None
                    for d, in c.execute("SELECT did FROM bal"):
                        if d.endswith(res["miner"]): miner_did = d
                    if miner_did is None:
                        miner_did = "did:key:?" + res["miner"]; ensure(c, miner_did)
                    c.execute("UPDATE bal SET amt=amt+? WHERE did=?", (fee * MINER_SHARE, miner_did))
                    c.execute("UPDATE bal SET amt=amt+? WHERE did=?", (fee * (1 - MINER_SHARE), me))
                    c.execute("UPDATE escrow SET state='settled' WHERE req_id=?", (req["id"],))
                    ver["settlement"] = {"miner": round(fee * MINER_SHARE, 2), "validator": round(fee * (1 - MINER_SHARE), 2)}
                else:
                    requester = c.execute("SELECT did FROM escrow WHERE req_id=?", (req["id"],)).fetchone()[0]
                    c.execute("UPDATE bal SET amt=amt+? WHERE did=?", (fee, requester))
                    c.execute("UPDATE escrow SET state='refunded' WHERE req_id=?", (req["id"],))
                    ver["settlement"] = "refund"
            log(c, "VER", ver)
            try:
                _, seq, _ = post_signed(key, "VER " + json.dumps(ver, ensure_ascii=False, separators=(",", ":")))
                print(f"[{m['seq']}] {verdict} -> VER posted seq={seq}")
            except Exception as e:
                print("post error:", e)
        st["val_since"] = since; save_state(st)
        maybe_daily_report(key, c, st)

def cmd_ledger(a):
    c = db()
    print("== balances (mock FLOP)")
    for d, amt in c.execute("SELECT did, amt FROM bal"): print(f"  {short(d) if d.startswith('did:key:z') else d}: {amt:.2f}")
    print("== escrow")
    for row in c.execute("SELECT * FROM escrow"): print("  ", row)
    print("== last events")
    for row in c.execute("SELECT * FROM log ORDER BY rowid DESC LIMIT 10"): print("  ", row[0], row[1], row[2][:100])

REPORT_UTC_HOUR = 8   # 毎日この時刻(UTC)以降の最初のループで日次報告を自動投稿 (08:00 UTC = 17:00 JST)
REPORT_RETRY_SEC = 600  # 初回投稿が失敗したとき、この秒数後に1回だけ再試行

def compute_stats(c, hours, own_csv="PvqA,88xr,hE3T"):
    import statistics
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - hours * 3600))
    rows = [(ts, ev, json.loads(d)) for ts, ev, d in
            c.execute("SELECT ts,event,detail FROM log WHERE ts>=? ORDER BY ts", (cutoff,))]
    req  = [d for _, e, d in rows if e == "REQ"]
    res  = [d for _, e, d in rows if e == "RES"]
    ver  = [d for _, e, d in rows if e == "VER"]
    errs = [d for _, e, d in rows if e == "ERR"]
    starts = [(ts, d) for ts, e, d in rows if e == "START"]
    own = tuple(x.strip() for x in own_csv.split(","))
    n_match = sum(1 for d in ver if d.get("verdict") == "match")
    by_miner = {}
    for d in res: by_miner[d.get("miner", "?")] = by_miner.get(d.get("miner", "?"), 0) + 1
    ext = sorted({d.get("req_from", "") for d in res
                  if d.get("req_from") and not d["req_from"].endswith(own)})
    med = lambda xs: int(statistics.median(xs)) if xs else 0
    lat_m = med([d.get("latency_ms", 0) for d in res])
    lat_v = med([d.get("validator_latency_ms", 0) for d in ver])
    ebd = {}
    for d in errs:
        k = d.get("kind") or err_kind(d.get("e", ""))
        ebd[k] = ebd.get(k, 0) + 1
    estr = " ".join(f"{k}:{v}" for k, v in sorted(ebd.items())) or "none"
    mstr = " ".join(f"{k}:{v}" for k, v in sorted(by_miner.items())) or "-"
    # READSTAT（集計窓）があれば成功数と失敗率を出す。無い期間（旧版）は errors のみ
    rstat = [d for _, e, d in rows if e == "READSTAT"]
    read_ok = sum(d.get("ok", 0) for d in rstat)
    read_err = sum(sum(d.get("err", {}).values()) for d in rstat)
    fail_pct = round(100 * read_err / (read_ok + read_err), 1) if (read_ok + read_err) else None
    rstr = f" | reads ok {read_ok} fail {fail_pct}%" if fail_pct is not None else ""
    room = (f"STATS last {hours}h: REQ {len(req)} | RES {len(res)} ({mstr}) | "
            f"VER {len(ver)} match {n_match} | external REQ DIDs {len(ext)} | "
            f"median latency ms miner {lat_m} / validator {lat_v} | read errors {len(errs)} ({estr}){rstr}")
    return {"rows": rows, "req": req, "res": res, "ver": ver, "errs": errs, "starts": starts,
            "n_match": n_match, "ext": ext, "lat_m": lat_m, "lat_v": lat_v, "estr": estr, "room": room,
            "read_ok": read_ok, "fail_pct": fail_pct}

def maybe_daily_report(key, c, st):
    """バリデーター常駐プロセスから毎日1回、直近24hのSTATSを部屋へ自動投稿する。
    イベントゼロの日はスキップ（心拍投稿にしない）。鍵は起動時に復号済みのものを使う。
    投稿済み記録は台帳に持つ（再起動しても同日に二重投稿しない）。"""
    now = time.gmtime()
    if now.tm_hour < REPORT_UTC_HOUR:
        return
    day = time.strftime("%Y-%m-%d", now)
    like = f'%\"day\": \"{day}\"%'
    row = c.execute("SELECT ts, detail FROM log WHERE event='REPORT' AND detail LIKE ?", (like,)).fetchone()
    if row:
        rep = json.loads(row[1])
        # 失敗済みなら REPORT_RETRY_SEC 経過後に1回だけ再試行（2026-08-28 DNS障害、8/30 503障害の教訓）
        if rep.get("seq") is not None or rep.get("tries", 1) >= 2:
            return
        import calendar
        if time.time() - calendar.timegm(time.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ")) < REPORT_RETRY_SEC:
            return
        tries = 2
    else:
        tries = 1
        log(c, "REPORT", {"day": day, "seq": None, "tries": 1})   # 先に記録（連投防止を優先）
    d = compute_stats(c, 24)
    if not (d["req"] or d["res"] or d["ver"] or d["errs"]):
        print(f"[daily report {day}] no events in 24h - skipped"); return
    try:
        _, seq, _ = post_signed(key, d["room"])
        c.execute("UPDATE log SET detail=? WHERE event='REPORT' AND detail LIKE ?",
                  (json.dumps({"day": day, "seq": seq, "tries": tries}), like)); c.commit()
        print(f"[daily report {day}] posted seq={seq} (try {tries})")
    except Exception as e:
        c.execute("UPDATE log SET detail=? WHERE event='REPORT' AND detail LIKE ?",
                  (json.dumps({"day": day, "seq": None, "tries": tries}), like)); c.commit()
        print(f"[daily report {day}] post error (try {tries}):", e,
              f"- retry in {REPORT_RETRY_SEC}s" if tries == 1 else "- giving up for today")

def cmd_stats(a):
    """直近 --hours の運用サマリ。--room で部屋投稿用1行、--x でX用テンプレを出力"""
    c = db()
    d = compute_stats(c, a.hours, a.own)
    rows, req, res, ver, errs, starts = d["rows"], d["req"], d["res"], d["ver"], d["errs"], d["starts"]
    n_match, ext, lat_m, lat_v, estr, room = d["n_match"], d["ext"], d["lat_m"], d["lat_v"], d["estr"], d["room"]
    if a.room:
        print(room); return
    if a.x:
        # X日誌の確定テンプレ（2026-08-28）。日付は JST。「今日の学び」「Todo」は無ければ行ごと削除して投稿
        day = time.strftime("%Y.%m.%d", time.gmtime(time.time() + 9 * 3600))
        fail = f"、失敗率 {d['fail_pct']}%" if d.get("fail_pct") is not None else ""
        print("Technocore💠自作デモ市場（トークンもデモ）")
        print(f"運用日誌{day}✍")
        print("・マイナー、バリデーター2台稼働中")
        print("・サーバー: ローカル＋GCP東京")
        print(f"・直近{a.hours}hステータス: REQ{len(req)}/RES{len(res)}/VER{len(ver)}（match {n_match}）")
        print(f"　外部DIDからのREQ: {len(ext)}")
        print(f"・レイテンシ中央値: マイナー {lat_m}ms、検証 {lat_v}ms")
        print(f"・読み取りエラー: {len(errs)}（{estr}{fail}）")
        print("・今日の学び: ")
        print("・Todo: ")
        print("・詳細、参加方法は固定スレへ👉")
        print("　あなたのREQお待ちしております！")
        return
    print(room)
    for ts, d in starts[-4:]: print("start:", ts, d.get("role"), d.get("me"))
    if ext: print("external DIDs:", ", ".join(ext))
    if not rows: print(f"(no events in last {a.hours}h)")

def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("request"); r.add_argument("prompt"); r.add_argument("--key", default="did_key.json")
    r.add_argument("--model", default="qwen2.5:1.5b"); r.add_argument("--fee", type=float, default=30)
    r.add_argument("--max-latency", type=int, default=60000); r.add_argument("--flops", type=int, default=3_000_000_000_000)
    m = s.add_parser("miner"); m.add_argument("--key", default="did_miner.json"); m.add_argument("--model", default="qwen2.5:1.5b")
    v = s.add_parser("validate"); v.add_argument("--key", default="did_key.json"); v.add_argument("--model", default="qwen2.5:1.5b")
    for x in (m, v):
        x.add_argument("--wait", type=int, default=READ_WAIT, help="long-poll 待ち秒（接続を占有する時間。実験用）")
        x.add_argument("--err-sleep", type=int, default=ERR_SLEEP, help="読み取り失敗後の待機秒")
    j = s.add_parser("join", help="DIDがなければ生成してREQを1件投稿（Ollama不要）")
    j.add_argument("prompt"); j.add_argument("--key", default="did_key.json")
    j.add_argument("--model", default="qwen2.5:1.5b"); j.add_argument("--fee", type=float, default=10)
    j.add_argument("--max-latency", type=int, default=60000); j.add_argument("--flops", type=int, default=3_000_000_000_000)
    s.add_parser("ledger")
    t = s.add_parser("stats"); t.add_argument("--hours", type=int, default=24)
    t.add_argument("--room", action="store_true"); t.add_argument("--x", action="store_true")
    t.add_argument("--own", default="PvqA,88xr,hE3T", help="自分のDID末尾（カンマ区切り、対向数から除外）")
    a = p.parse_args()
    {"request": cmd_request, "miner": cmd_miner, "validate": cmd_validate, "ledger": cmd_ledger, "stats": cmd_stats, "join": cmd_join}[a.cmd](a)

if __name__ == "__main__":
    main()
