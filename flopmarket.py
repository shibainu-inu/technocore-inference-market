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
    req = {"id": req_id, "model": a.model, "model_hash": ollama_model_digest(a.model),
           "max_latency_ms": a.max_latency, "flops_est": a.flops, "confidential": False,
           "fee": a.fee, "prompt": a.prompt[:400]}
    c.execute("UPDATE bal SET amt=amt-? WHERE did=?", (a.fee, me))
    c.execute("INSERT INTO escrow VALUES (?,?,?,?)", (req_id, me, a.fee, "open"))
    log(c, "REQ", req)
    st, seq, _ = post_signed(key, "REQ " + json.dumps(req, ensure_ascii=False, separators=(",", ":")))
    print(f"REQ {req_id} posted seq={seq} fee={a.fee} escrowed. balance={bal - a.fee}")

def cmd_miner(a):
    key = load_key(a.key); me = did_of(key); c = db(); ensure(c, me)
    st = load_state(); since = st.get("miner_since", 0)
    if since == 0:  # 初回は現在位置から（過去の山を処理しない）
        _, since = read_room(0, wait=0)
    print(f"miner {short(me)} watching /r/{ROOM} from seq {since} model={a.model}")
    while True:
        try:
            msgs, since = read_room(since, wait=10)
        except Exception as e:
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "read error:", e); time.sleep(15); continue
        for m in msgs:
            req = parse_msg(m["text"], "REQ")
            if not req or req.get("model") != a.model:
                continue
            if not m["from"].startswith("z6Mk"):   # 署名なし（~nick）の要求は受けない
                continue
            print(f"[{m['seq']}] REQ {req['id']} from {m['from']} fee={req['fee']}")
            try:
                out, tokens, ms = ollama_generate(a.model, req["prompt"])
            except Exception as e:
                print("ollama error:", e); continue
            res = {"req_id": req["id"], "req_seq": m["seq"], "miner": me[-8:],
                   "output_sha256": hashlib.sha256(out.encode()).hexdigest(),
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
    print(f"validator {short(me)} watching from seq {since}")
    while True:
        try:
            msgs, since = read_room(since, wait=10)
        except Exception as e:
            print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "read error:", e); time.sleep(15); continue
        for m in msgs:
            r = parse_msg(m["text"], "REQ")
            if r: reqs[r["id"]] = r; continue
            res = parse_msg(m["text"], "RES")
            if not res or res["req_id"] not in reqs or reqs[res["req_id"]]["model"] != a.model:
                continue
            req = reqs[res["req_id"]]
            out, _, ms = ollama_generate(a.model, req["prompt"])
            sha = hashlib.sha256(out.encode()).hexdigest()
            verdict = "match" if sha == res["output_sha256"] else ("similar" if out[:60] == res.get("output_head", "")[:60] else "mismatch")
            ver = {"res_seq": m["seq"], "req_id": req["id"], "verdict": verdict,
                   "recomputed_sha256": sha, "validator_latency_ms": ms}
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

def cmd_ledger(a):
    c = db()
    print("== balances (mock FLOP)")
    for d, amt in c.execute("SELECT did, amt FROM bal"): print(f"  {short(d) if d.startswith('did:key:z') else d}: {amt:.2f}")
    print("== escrow")
    for row in c.execute("SELECT * FROM escrow"): print("  ", row)
    print("== last events")
    for row in c.execute("SELECT * FROM log ORDER BY rowid DESC LIMIT 10"): print("  ", row[0], row[1], row[2][:100])

def main():
    p = argparse.ArgumentParser(); s = p.add_subparsers(dest="cmd", required=True)
    r = s.add_parser("request"); r.add_argument("prompt"); r.add_argument("--key", default="did_key.json")
    r.add_argument("--model", default="qwen2.5:1.5b"); r.add_argument("--fee", type=float, default=30)
    r.add_argument("--max-latency", type=int, default=60000); r.add_argument("--flops", type=int, default=3_000_000_000_000)
    m = s.add_parser("miner"); m.add_argument("--key", default="did_miner.json"); m.add_argument("--model", default="qwen2.5:1.5b")
    v = s.add_parser("validate"); v.add_argument("--key", default="did_key.json"); v.add_argument("--model", default="qwen2.5:1.5b")
    s.add_parser("ledger")
    a = p.parse_args()
    {"request": cmd_request, "miner": cmd_miner, "validate": cmd_validate, "ledger": cmd_ledger}[a.cmd](a)

if __name__ == "__main__":
    main()
