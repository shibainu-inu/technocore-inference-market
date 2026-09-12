#!/usr/bin/env python3
"""
sonnet/audit.py — bot の品質・性能・セキュリティを一括で検査する（ネット不要。pip-audit だけ --online で有効）

  ~/technocore-env/bin/python sonnet/audit.py [--online] [--json out.json]

 品質      ruff（構文・未使用・バグ傾向）、単体テスト（韻律・本体・敵対入力）
 セキュリティ bandit、秘密のスキャン（鍵・パスフレーズ・鍵 PEM がリポジトリや実行時ファイルに無い）、鍵ファイルの権限、
           方針の不変条件（投稿先は sonnet-1 の部屋だけ、型は sonnet.* だけ、LLM 出力はゲートを通る）
 性能      辞書ロード、候補語検索、弱強判定、署名検証、メッセージ処理のスループット、読み取り予算（600/分/IP）の見積り、
           LLM の実測レイテンシと費用（llm.log）
終了コードは FAIL が 1 つでもあれば 1。
"""
import argparse, json, os, re, statistics, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable
RESULTS = []


def rec(section, name, ok, detail="", warn=False):
    status = "PASS" if ok else ("WARN" if warn else "FAIL")
    RESULTS.append({"section": section, "name": name, "status": status, "detail": detail})
    print(f"[{status}] {section}: {name}" + (f" — {detail}" if detail else ""), flush=True)


def run(cmd, timeout=600, cwd=ROOT):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
    return p.returncode, (p.stdout + p.stderr)


# ---------- 品質 ----------
def quality():
    rc, out = run([PY, "-m", "ruff", "check", "--select", "E,F,W,B,UP,S110,S112", "--ignore", "E401,E402,E501,E701,E702,E731,E741,UP015,UP031",
                   "--line-length", "130", "--output-format", "concise", "sonnet/agent.py", "sonnet/llm.py", "sonnet/prosody.py", "sonnet/audit.py", "sonnet/tests"])
    n = len([l for l in out.splitlines() if re.match(r"^sonnet/\S+:\d+:\d+: ", l)])
    rec("quality", "ruff", rc == 0, f"{n} findings" if n else "clean", warn=(rc != 0 and n <= 5))
    if n:
        print(out[:3000])
    t0 = time.time()
    rc, out = run([PY, "-m", "unittest", "discover", "-s", "sonnet/tests"], timeout=900)
    m = re.search(r"Ran (\d+) tests", out)
    rec("quality", "unit tests", rc == 0 and bool(m), f"{m.group(1) if m else '?'} tests in {time.time() - t0:.1f}s" + ("" if rc == 0 else " — " + out[-1500:]))
    pass  # テストの一時ファイルは各テストが自分で片付ける（並行実行中の他のテストを壊さない）
    rc, out = run([PY, "scripts/verify.py"], cwd=os.path.join(HERE, "pkg"))
    rec("quality", "official package integrity (manifest)", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")


# ---------- セキュリティ ----------
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (ENCRYPTED )?PRIVATE KEY-----"), "PEM private key"),
    (re.compile(r"\"private_key_pem\"\s*:\s*\"-----"), "key JSON body"),
    (re.compile(r"TC_PASS\s*=\s*['\"]?[^\s'\"$]{4,}"), "TC_PASS literal"),
    (re.compile(r"(passphrase|password)\s*[:=]\s*['\"][^'\"]{3,}", re.I), "password literal"),
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}"), "Anthropic API key"),
]


def security():
    rc, out = run([PY, "-m", "bandit", "-q", "-r", "sonnet", "-x", "sonnet/tests,sonnet/pkg", "-f", "json"])
    try:
        j = json.loads(out[out.index("{"):])
        issues = [i for i in j.get("results", []) if i["issue_severity"] in ("MEDIUM", "HIGH")]
        low = [i for i in j.get("results", []) if i["issue_severity"] == "LOW"]
        rec("security", "bandit", not issues, f"{len(issues)} medium/high, {len(low)} low" +
            ("".join(f"\n    {i['filename']}:{i['line_number']} {i['test_id']} {i['issue_text']}" for i in issues) if issues else ""))
        if low:
            for i in low:
                print(f"    low: {i['filename']}:{i['line_number']} {i['test_id']} {i['issue_text'][:100]}")
    except (ValueError, KeyError):
        rec("security", "bandit", False, out[:500])
    # 秘密のスキャン: リポジトリ内の sonnet/ と実行時ファイル
    hits = []
    scan = []
    for dp, dn, fn in os.walk(HERE):
        dn[:] = [d for d in dn if d not in ("__pycache__", "pkg")]
        for f in fn:
            if f.endswith((".py", ".json", ".md", ".log", ".txt", ".sh")):
                scan.append(os.path.join(dp, f))
    for path in scan:
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for pat, label in SECRET_PATTERNS:
            for _ in pat.finditer(txt):
                if "SECRET_PATTERNS" in txt and path.endswith("audit.py"):
                    continue
                if path.endswith("test_security.py"):
                    continue  # 敵対入力の fixture
                hits.append(f"{os.path.relpath(path, ROOT)}: {label}")
    rec("security", "no secrets in sonnet/ files, logs, state", not hits, "; ".join(hits) or f"{len(scan)} files scanned")
    # 鍵ファイルの権限
    p = json.load(open(os.path.join(HERE, "policy.json")))
    kp = p["key_path"]
    if os.path.exists(kp):
        mode = oct(os.stat(kp).st_mode & 0o777)
        rec("security", "key file permission 0600", mode == "0o600", f"{kp} {mode}")
        k = json.load(open(kp))
        rec("security", "key file DID matches policy", k.get("did") == p["did"], k.get("did", "")[-8:])
    else:
        rec("security", "key file present", False, kp)
    # git 追跡対象に実行時ファイルが無い
    runtime = ["sonnet/state.json", "sonnet/state-sonnet-2.json", "sonnet/agent.log", "sonnet/llm.log", "sonnet/ATTENTION.md", "sonnet/console.log"]
    rc, out = run(["git", "ls-files", "--", *runtime], cwd=ROOT)
    tracked = [l for l in out.splitlines() if l.strip()]
    rec("security", "runtime files are not git-tracked", not tracked, ", ".join(tracked) or "none tracked")
    rc, out = run(["git", "check-ignore", "sonnet/state.json", "sonnet/state-sonnet-2.json", "sonnet/agent.log", "sonnet/llm.log", "sonnet/ATTENTION.md"], cwd=ROOT)
    ignored = [l for l in out.splitlines() if l.strip()]
    rec("security", "runtime files are git-ignored", len(ignored) == 5, f"{len(ignored)}/5 ignored")
    # 方針の不変条件
    rooms_ok = all(r.startswith(("mb-sonnet-", "d-sonnet-")) for r in p["rooms"].values())
    rec("security", "policy rooms are contest rooms only", rooms_ok, ", ".join(p["rooms"].values()))
    src = open(os.path.join(HERE, "agent.py"), encoding="utf-8").read()
    rec("security", "agent has no shell/exec/eval on room text", not re.search(r"\b(eval|exec|os\.system|os\.popen|subprocess\.\w+)\s*\(", src))
    rec("security", "LLM adapter disables tools and MCP", all(s in open(os.path.join(HERE, "llm.py")).read() for s in ['"--tools", ""', "--strict-mcp-config"]))
    rec("security", "outgoing text gate present", all(s in src for s in ["FORBIDDEN_OUT", "ALLOWED_TYPES", "post refused: room"]))


def deps_online():
    rc, out = run([PY, "-m", "pip_audit", "--progress-spinner", "off"], timeout=600)
    vulns = [l for l in out.splitlines() if re.match(r"^\S+\s+\S+\s+(PYSEC|GHSA|CVE)", l)]
    rec("security", "pip-audit (installed packages)", rc == 0 and not vulns, f"{len(vulns)} vulnerable" + ("\n" + "\n".join(vulns[:20]) if vulns else ""), warn=bool(vulns))


# ---------- 性能 ----------
def performance():
    sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
    import prosody, agent
    t0 = time.time(); lex = prosody.lexicon(); prosody.prons(); t_load = time.time() - t0
    rec("perf", "lexicon + pronunciations load", t_load < 5, f"{t_load:.2f}s, {len(lex)} words", warn=t_load >= 5)
    t0 = time.time(); c = prosody.candidates(None, set("abcdefghijklmnopqrstuvwxyz"), 3); t1 = time.time() - t0
    rec("perf", "candidate search (all letters, ≤3 syl)", t1 < 2, f"{len(c)} words in {t1:.2f}s", warn=t1 >= 2)
    t0 = time.time(); c = prosody.candidates(None, prosody.did_letters("did:key:z6MkmG1MiumCr8Jk6vL5qt2A1XzEst6CVT5rwRHUHYwKPvqA"), 2, rhyme_with="light"); t2 = time.time() - t0
    rec("perf", "rhyme-constrained search", t2 < 2, f"{len(c)} words in {t2:.2f}s", warn=t2 >= 2)
    line = "Shall I compare thee to a summer's day".split()
    t0 = time.time(); n = 0
    while time.time() - t0 < 1.0:
        prosody.iambic_fit(line); n += 1
    rec("perf", "iambic_fit throughput", n > 500, f"{n}/s", warn=n <= 500)
    # 署名検証
    import base64
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    k = Ed25519PrivateKey.generate()
    did = agent.tc.did_from_pub(k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw))
    msg = {"from": did, "nonce": 1, "text": "x" * 300}
    msg["sig"] = base64.urlsafe_b64encode(k.sign(f"r|1|{msg['text']}".encode())).decode().rstrip("=")
    t0 = time.time(); n = 0
    while time.time() - t0 < 1.0:
        assert agent.verify_sig("r", msg); n += 1
    rec("perf", "signature verification throughput", n > 1000, f"{n}/s (registration room peaks ~4/s)", warn=n <= 1000)
    # メッセージ処理
    import tempfile
    tmp = tempfile.mkdtemp(prefix="sonnet-audit-")
    agent.STATE_PATH = os.path.join(tmp, "state.json"); agent.ATTENTION_PATH = os.path.join(tmp, "attention.md")
    agent.LOG_PATH = os.path.join(tmp, "agent.log"); agent.INBOX_DIR = os.path.join(tmp, "inbox")
    p = json.load(open(os.path.join(HERE, "policy.json"))); p["auto"] = {k: False for k in p["auto"]}
    a = agent.Agent(p); a.save = lambda: None
    disc = p["rooms"]["discovery"]
    texts = ['{"type":"sonnet.recruit.v1","contest_id":"sonnet-1","game_id":"g%d","request_id":"r","text":"seat open"}',
             "writer seeking seat, DID did:key:z6MkvBBoP3VST9xF833FLRLdZRG8d92uXahXgAW3BR9W9Uxu letters 26/26",
             '{"type":"sonnet.roster.v1","game_id":"g%d","poem_room":"d-sonnet-1-team-g","room_generation":0,"members":["did:key:z6MkvBBoP3VST9xF833FLRLdZRG8d92uXahXgAW3BR9W9Uxu"]}']
    t0 = time.time(); N = 3000
    for i in range(N):
        t = texts[i % 3]
        a.handle({"seq": i, "ts": "2026-09-11T08:00:00Z", "from": f"did:key:z6Mk{'A' * 40}{i % 97:04d}", "text": t % i if "%d" in t else t, "_room": disc, "_sig_ok": True})
    dt = time.time() - t0
    rec("perf", "message handling throughput", N / dt > 500, f"{N / dt:.0f} msg/s (rooms peak ~4 msg/s)", warn=N / dt <= 500)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    # 読み取り予算の見積り
    hot = len(agent.Agent.HOT) + 1  # チーム部屋
    wait, gap, cold_every = p.get("read_wait_s", 10), p.get("hot_poll_gap_s", 2), p.get("cold_poll_s", 120)
    worst = hot * 60 / gap  # long-poll が毎回即返る最悪ケース（登録部屋のような高流量）
    typical = hot * 60 / (wait + gap)
    cold = 4 * 60 / cold_every
    others = 60  # probe/validate/miner の実測（READSTAT: 各 13〜27/分）
    rec("perf", "read budget vs 600/min/IP", worst + cold + others < 600,
        f"worst {worst + cold:.0f}/min + other pollers ~{others} = {worst + cold + others:.0f}; typical {typical + cold:.0f}+{others}")
    # LLM 実測
    lp = os.path.join(HERE, "llm.log")
    if os.path.exists(lp):
        recs = [json.loads(l) for l in open(lp) if l.strip()]
        ok = [r for r in recs if not r.get("err")]
        secs = [r["sec"] for r in ok]
        cost = sum(r.get("cost_usd") or 0 for r in ok)
        if secs:
            rec("perf", "LLM latency (claude -p)", statistics.median(secs) < 30,
                f"n={len(ok)} median {statistics.median(secs):.1f}s max {max(secs):.1f}s, errors {len(recs) - len(ok)}, est. cost ${cost:.2f}", warn=statistics.median(secs) >= 30)
        else:
            rec("perf", "LLM latency", True, "no successful calls logged yet", warn=True)
    else:
        rec("perf", "LLM latency", True, "no llm.log yet", warn=True)
    # 常駐プロセスのメモリ
    rc, out = run(["bash", "-c", "pid=$(pgrep -f '^/[^ ]*python -u sonnet/agent.py run$' | head -1); [ -n \"$pid\" ] && ps -o rss=,etimes= -p \"$pid\""])
    m = re.search(r"(\d+)\s+(\d+)", out)
    if m:
        rss = int(m.group(1)) / 1024
        rec("perf", "running agent RSS", rss < 600, f"{rss:.0f} MB, uptime {int(m.group(2)) // 60} min", warn=rss >= 600)
    else:
        rec("perf", "running agent RSS", True, "agent not running (skipped)", warn=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--online", action="store_true", help="pip-audit も実行（ネット必要）")
    ap.add_argument("--json", help="結果を JSON で保存")
    a = ap.parse_args()
    quality(); security()
    if a.online:
        deps_online()
    performance()
    fails = [r for r in RESULTS if r["status"] == "FAIL"]
    warns = [r for r in RESULTS if r["status"] == "WARN"]
    print(f"\n{len(RESULTS)} checks: {len(RESULTS) - len(fails) - len(warns)} pass, {len(warns)} warn, {len(fails)} fail")
    if a.json:
        json.dump({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "results": RESULTS}, open(a.json, "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
