# 0.11.2 前後比較（#588 用）。ledger.db のあるディレクトリで実行。
import sqlite3, json, statistics

B_START = "2026-08-31T08:56:00Z"
BOUND_A = "2026-09-01T07:04:00Z"
BOUND_B = "2026-09-01T07:12:00Z"
A_END   = "2026-09-02T07:04:25Z"
BURSTS  = [("2026-09-01T17:15:00Z","2026-09-01T17:40:00Z"),
           ("2026-09-01T18:30:00Z","2026-09-01T19:00:00Z")]

def win_start(ts, win_s):
    import datetime as dt
    t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ") - dt.timedelta(seconds=win_s)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

rows = []
c = sqlite3.connect("ledger.db")
for ts, d in c.execute("select ts, detail from log where event='READSTAT' and ts>=? and ts<=? order by ts", (B_START, A_END)):
    d = json.loads(d)
    err = dict(d.get("err") or {})
    cfg = err.pop("config", 0)
    rows.append({"ts": ts, "start": win_start(ts, int(d.get("win_s") or 300)), "role": d.get("role"),
                 "ok": int(d.get("ok") or 0), "err": err, "cfg": cfg,
                 "ok_med": d.get("ok_ms_med"), "err_med": (d.get("err_ms_med") or {})})

def in_burst(r):
    return any(not (r["ts"] <= s or r["start"] >= e) for s, e in BURSTS)

def agg(rs, label):
    ok = sum(r["ok"] for r in rs); e503 = sum(r["err"].get("503",0) for r in rs)
    eto = sum(r["err"].get("timeout",0) for r in rs)
    eoth = sum(sum(v for k,v in r["err"].items() if k not in ("503","timeout")) for r in rs)
    errs = e503 + eto + eoth; tot = ok + errs; cfg = sum(r["cfg"] for r in rs)
    okm = [r["ok_med"] for r in rs if r["ok_med"] is not None]
    e5m = [r["err_med"].get("503") for r in rs if r["err_med"].get("503") is not None]
    tom = [r["err_med"].get("timeout") for r in rs if r["err_med"].get("timeout") is not None]
    med = lambda v: round(statistics.median(v)) if v else None
    cov = sum(300 for _ in rs) / 3600
    print(f"[{label}] windows={len(rs)} (~{cov:.1f}h) req={tot} ok={ok}")
    if tot:
        print(f"  per-request: 503 {e503} ({100*e503/tot:.1f}%) | timeout {eto} ({100*eto/tot:.2f}%) | other {eoth} | fail {100*(errs)/tot:.1f}%")
    if errs:
        print(f"  timeout share of errors: {100*eto/errs:.1f}%")
    print(f"  medians of window medians: ok {med(okm)} ms | 503 {med(e5m)} ms | timeout {med(tom)} ms | config-errors excluded: {cfg}")

roles = sorted(set(r["role"] for r in rows))
print("roles in this ledger:", roles)
before = [r for r in rows if r["ts"] <= BOUND_A]
after  = [r for r in rows if r["start"] >= BOUND_B]
after_base  = [r for r in after if not in_burst(r)]
after_burst = [r for r in after if in_burst(r)]
agg(before, "0.11.1  (08-31 08:56Z -> 09-01 07:04Z)")
agg(after,  "0.11.2  (09-01 07:12Z -> 09-02 07:04Z) ALL")
agg(after_base,  "0.11.2  baseline (burst windows excluded)")
agg(after_burst, "0.11.2  burst windows only (17:15-17:40Z, 18:30-19:00Z)")
for role in roles:
    agg([r for r in before if r["role"]==role], f"0.11.1 role={role}")
    agg([r for r in after  if r["role"]==role], f"0.11.2 role={role}")
