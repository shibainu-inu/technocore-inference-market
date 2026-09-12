# READSTAT/ERR/CONFIG を版境界（0.12.1 / 0.13.0 初観測）で区切って集計する。読み取り専用・ネットワークなし。usage: python3 extract_periods.py > extract_$(hostname)_$(date -u +%Y%m%d).txt
import sqlite3, json, statistics as st
c=sqlite3.connect('ledger.db')
def rows(sql,*a): return c.execute(sql,a).fetchall()
import socket; print("host", socket.gethostname(), "; ledger max ts", rows("select max(ts) from log")[0][0])
print("\n## START rows since 09-04")
for ts,d in rows("select ts, detail from log where event='START' and ts>='2026-09-04' order by ts"): print(" ", ts, d[:80])
print("\n## CONFIG version transitions since 09-04 (rowid, ts, version, changed)")
prev=None
for rid,ts,d in rows("select rowid, ts, detail from log where event='CONFIG' and ts>='2026-09-04' order by ts"):
    j=json.loads(d); v=j.get('version')
    if v!=prev or j.get('changed'): print(" ", rid, ts, v, "changed=", j.get('changed')); prev=v
P=[("pre-0.12.1","2026-09-04T08:00:00Z","2026-09-05T18:11:57Z"),("0.12.1","2026-09-05T18:11:57Z","2026-09-07T07:49:25Z"),("0.13.0 to 09-11 12:33:57Z","2026-09-07T07:49:25Z","2026-09-11T12:33:57Z"),("0.13.0 to now","2026-09-07T07:49:25Z","2099-01-01T00:00:00Z")]
print("\n## per-period: requests (READSTAT sums), 503 / timeout / 502 counts (ERR rows), rates")
for label,lo,hi in P:
    rs=[json.loads(d) for (d,) in rows("select detail from log where event='READSTAT' and ts>? and ts<=?",lo,hi)]
    req=sum(r['ok']+sum(r['err'].values()) for r in rs)
    cnt={k: rows("select count(*) from log where event='ERR' and json_extract(detail,'$.kind')=? and ts>=? and ts<?",k,lo,hi)[0][0] for k in ('503','timeout','502')}
    print(f"  {label:26s} windows {len(rs):5d} requests {req:7d} 503 {cnt['503']:4d} ({100*cnt['503']/req if req else 0:.4f}%) timeout {cnt['timeout']:4d} ({100*cnt['timeout']/req if req else 0:.4f}%) 502 {cnt['502']}")
print("\n## per-period error latency ms (ERR rows): n / min / p50 / p90 / max")
for label,lo,hi in P:
    for k in ('503','timeout','502'):
        ms=sorted(m for (m,) in rows("select json_extract(detail,'$.ms') from log where event='ERR' and json_extract(detail,'$.kind')=? and ts>=? and ts<?",k,lo,hi) if m is not None)
        if ms: print(f"  {label:26s} {k:8s} n {len(ms):4d} min {ms[0]:6d} p50 {int(st.median(ms)):6d} p90 {ms[int(len(ms)*0.9)] if len(ms)>1 else ms[0]:6d} max {ms[-1]:6d}")
print("\n## per-period successful-read latency (median of window ok_ms_med / median of window p90) and probe_ms median")
for label,lo,hi in P:
    rs=[json.loads(d) for (d,) in rows("select detail from log where event='READSTAT' and ts>? and ts<=?",lo,hi)]
    med=[r['ok_ms_med'] for r in rs if r.get('ok_ms_med') is not None]; p90=[r['ok_ms_p90'] for r in rs if r.get('ok_ms_p90') is not None]; pr=[r['probe_ms'] for r in rs if r.get('probe_ms') is not None]
    print(f"  {label:26s} ok_ms_med {int(st.median(med)) if med else None} p90 {int(st.median(p90)) if p90 else None} probe_ms {int(st.median(pr)) if pr else None} wait {sorted(set(r.get('wait') for r in rs))}")
print("\n## fingerprints since 09-04 08:00Z: (status, body32 class, cl, conn) -> count")
from collections import Counter
fp=Counter()
for (d,) in rows("select detail from log where event='ERR' and ts>='2026-09-04T08:00:00Z' and json_extract(detail,'$.http') is not null"):
    h=json.loads(d)['http']; b=h.get('body32') or ''
    cls='Service Unavailable' if b.startswith('Service Unavailable') else 'origin unavailable' if b.startswith('origin unavailable') else 'error code: 502' if b.startswith('error code: 502') else 'other:'+repr(b[:20])
    fp[(h.get('status'),cls,h.get('cl'),h.get('conn'))]+=1
for k,v in sorted(fp.items(), key=lambda x:-x[1]): print("  ",k,v)
print("\n## per-day since 09-04: 503 / requests / rate")
for (d,) in rows("select distinct substr(ts,1,10) from log where ts>='2026-09-04' order by 1"):
    lo,hi=d+"T00:00:00Z",d+"T23:59:59Z"
    rs=[json.loads(x) for (x,) in rows("select detail from log where event='READSTAT' and ts>? and ts<=?",lo,hi)]
    req=sum(r['ok']+sum(r['err'].values()) for r in rs); n=rows("select count(*) from log where event='ERR' and json_extract(detail,'$.kind')='503' and ts>=? and ts<=?",lo,hi)[0][0]
    print(f"  {d}: 503 {n:4d} requests {req:6d} rate {100*n/req if req else 0:.4f}%")
