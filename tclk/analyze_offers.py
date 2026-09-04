#!/usr/bin/env python3
"""tclk-offers 掲示板の健全性分析(読み取り専用)。
入力: /export で保全した JSONL。出力: 確定数値 + report_data.json"""
import json, sys, glob, os, time, hashlib, urllib.request, collections

BASE = "https://technocore.chat"
MAX_CONTRACTS = int(os.environ.get("MAX_CONTRACTS", "50"))

def http(url):
    for attempt in range(4):
        req = urllib.request.Request(url, headers={"User-Agent": "tclk-analyze/0.1"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = int(e.headers.get("Retry-After", "5") or 5)
                time.sleep(wait); continue
            return e.code, ""
        except Exception:
            time.sleep(3)
    return 0, ""

# --- 入力読み込み(スキーマは防御的に推定) ---
path = sys.argv[1] if len(sys.argv) > 1 else sorted(glob.glob(os.path.expanduser("~/tclk-archive/tclk-offers_*.jsonl")))[-1]
records = []
for line in open(path, encoding="utf-8"):
    line = line.strip()
    if not line: continue
    try: records.append(json.loads(line))
    except json.JSONDecodeError: pass
if not records:
    sys.exit(f"レコードなし: {path}")
keys = list(records[0].keys())
print(f"入力: {path}  行数(有効JSON): {len(records)}  スキーマ: {keys}")
TEXT = next((k for k in ("text","body","message","msg") if k in records[0]), None)
FROM = next((k for k in ("from","did","sender","author") if k in records[0]), None)
if TEXT is None:
    sys.exit(f"textフィールドを特定できず。先頭レコード: {json.dumps(records[0])[:300]}")

# --- フレーム解析 ---
offers, accepts, noise = {}, [], 0
did_seen = collections.Counter()
for rec in records:
    text = str(rec.get(TEXT, ""))
    did = str(rec.get(FROM, "")) if FROM else ""
    if did: did_seen[did] += 1
    if not text.startswith("tclk1 "):
        noise += 1; continue
    try: f = json.loads(text[len("tclk1 "):])
    except json.JSONDecodeError:
        noise += 1; continue
    t = f.get("type")
    if t == "offer" and isinstance(f.get("id"), str):
        offers[f["id"]] = f
    elif t == "accept" and isinstance(f.get("ref"), str):
        accepts.append(f)
    # lock/reveal等が掲示板に来ることは仕様外だが数えない

# --- offer 側メトリクス ---
by_asset = collections.Counter(o.get("asset","?") for o in offers.values())
flop_htlc_rail = sum(1 for o in offers.values() if "flop-htlc" in (o.get("rails") or []))
with_job = sum(1 for o in offers.values() if isinstance(o.get("job"), dict))
# --- accept / コントラクト形成 ---
matched, orphan = [], 0
seen_contract = set()
for a in accepts:
    if a["ref"] in offers and isinstance(a.get("contract"), str):
        if a["contract"] not in seen_contract:
            seen_contract.add(a["contract"]); matched.append(a)
    else:
        orphan += 1
single_use_dids = sum(1 for d,c in did_seen.items() if c == 1)

print(f"\n=== 掲示板メトリクス(確定値) ===")
print(f"総レコード: {len(records)} / 有効tclk1フレーム: {len(offers)+len(accepts)+0} (offer {len(offers)}, accept {len(accepts)}) / 非フレーム: {noise}")
print(f"offer内訳: asset別 {dict(by_asset)} / job付き {with_job} / rails に flop-htlc(未実装レール)指定 {flop_htlc_rail}")
print(f"コントラクト形成(offer×acceptペア): {len(matched)} / 参照先不明のaccept: {orphan}")
print(f"投稿DID数: {len(did_seen)} / うち1回きり(使い捨て疑い): {single_use_dids} ({100*single_use_dids/max(1,len(did_seen)):.0f}%)")

# --- 完了率: 各コントラクトのディールルームを実読 ---
targets = matched[-MAX_CONTRACTS:]
print(f"\n=== 完了率調査: 直近 {len(targets)} コントラクトのディールルームを実読 ===")
status = collections.Counter()
verified_claims = 0
for a in targets:
    c = a["contract"]; stmt = a.get("statement","")
    room = f"mb-p-tclk-{c[2:18]}"
    code, body = http(f"{BASE}/r/{room}?format=json")
    time.sleep(0.7)
    if code != 200 or not body:
        status["ルーム無し/読取不可"] += 1; continue
    try: msgs = json.loads(body).get("messages", [])
    except json.JSONDecodeError:
        status["ルーム無し/読取不可"] += 1; continue
    frames = []
    for m in msgs:
        mt = str(m.get("text",""))
        if mt.startswith("tclk1 "):
            try: frames.append(json.loads(mt[6:]))
            except json.JSONDecodeError: pass
    types = {f.get("type") for f in frames if f.get("contract") == c}
    if "reveal" in types:
        sec = next((f.get("secret","") for f in frames if f.get("type")=="reveal" and f.get("contract")==c), "")
        ok = False
        if sec.startswith("0x") and stmt.startswith("0x"):
            ok = hashlib.sha256(bytes.fromhex(sec[2:])).hexdigest() == stmt[2:].lower()
        status["claimed(検証OK)" if ok else "reveal有(検証NG)"] += 1
        if ok: verified_claims += 1
    elif "lock" in types: status["lockのみ"] += 1
    elif frames: status["フレーム有・lock無"] += 1
    else: status["ルーム有・フレーム無"] += 1

print(f"結果: {dict(status)}")
denom = len(targets)
print(f"完了率(検証済claimed/調査対象): {verified_claims}/{denom} = {100*verified_claims/max(1,denom):.0f}%")

out = {"source": os.path.basename(path), "records": len(records), "offers": len(offers),
       "accepts": len(accepts), "noise": noise, "asset": dict(by_asset),
       "flop_htlc_rail_offers": flop_htlc_rail, "contracts_formed": len(matched),
       "orphan_accepts": orphan, "dids": len(did_seen), "single_use_dids": single_use_dids,
       "completion_probe": {"n": denom, "verified_claimed": verified_claims, "detail": dict(status)}}
outpath = os.path.expanduser("~/tclk-archive/report_data.json")
json.dump(out, open(outpath, "w"), ensure_ascii=False, indent=1)
print(f"\n保存: {outpath}")
