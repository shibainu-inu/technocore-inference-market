#!/usr/bin/env python3
"""accepted-word history の母数を広げる: 提出部屋の受理レシート → 各 team 部屋の /export → 受理された語の数を DID ごとに数え、
sonnet/proven_contributors.json に書く（既存ファイルとマージ、読むだけで投稿しない）。bot は policy `proven_file` で参照する。

使い方: ~/technocore-env/bin/python sonnet/tools/proven_contributors.py [--out sonnet/proven_contributors.json] [--state sonnet/state-sonnet-2.json]
"""
import argparse, collections, json, os, re, sys, time, urllib.request

BASE = "https://technocore.chat"
DID_RE = re.compile(r"did:key:z6Mk[1-9A-HJ-NP-Za-km-z]{44}")
HERE = os.path.dirname(os.path.abspath(__file__))


def get(path, timeout=120):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "nohitori-proven/1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def ndjson(body):
    for ln in body.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            yield json.loads(ln)
        except ValueError:
            continue


def parse(text):
    try:
        j = json.loads(text)
        return j if isinstance(j, dict) else None
    except Exception:
        return None


def accepted_games(contest):
    """提出部屋の export から (game_id, submitter) を集める: submit.v1 の request_id に accepted receipt が付いたもの"""
    body = get(f"/r/mb-{contest}-submissions/export")
    subs, out = {}, {}
    for m in ndjson(body):
        j = parse(m.get("text", ""))
        if not j:
            continue
        if j.get("type") == "sonnet.submit.v1" and isinstance(j.get("game_id"), str) and isinstance(j.get("request_id"), str):
            subs[j["request_id"]] = (j["game_id"], m.get("from"))
        elif j.get("type") == "sonnet.receipt.v1" and j.get("status") == "accepted" and j.get("request_id") in subs:
            gid, frm = subs[j["request_id"]]
            out[gid] = frm
    return out


def room_history(contest, gid):
    body = get(f"/r/d-{contest}-team-{gid}/export")
    by_req, acc = {}, collections.Counter()
    for m in ndjson(body):
        j = parse(m.get("text", ""))
        frm = m.get("from", "")
        if not j or not DID_RE.fullmatch(frm):
            continue
        if j.get("type") == "sonnet.word.v1" and isinstance(j.get("request_id"), str):
            by_req[j["request_id"]] = frm
        elif j.get("type") == "sonnet.receipt.v1" and j.get("status") == "accepted" and j.get("request_id") in by_req and "version" in j:
            acc[by_req[j["request_id"]]] += 1
    return acc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contest", default="sonnet-2")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "proven_contributors.json"))
    ap.add_argument("--state", default=os.path.join(HERE, "..", "state-sonnet-2.json"))
    ap.add_argument("--sleep", type=float, default=0.3)
    a = ap.parse_args()
    existing = {}
    if os.path.exists(a.out):
        try:
            existing = json.load(open(a.out)).get("dids", {})
        except (OSError, ValueError):
            existing = {}
    dids = {d: dict(v) for d, v in existing.items() if DID_RE.fullmatch(d)}
    games = accepted_games(a.contest)
    print(f"accepted games in the submissions ring: {len(games)}", file=sys.stderr)
    for gid, submitter in sorted(games.items()):
        try:
            acc = room_history(a.contest, gid)
        except Exception as e:
            print(f"  {gid}: {e!r}", file=sys.stderr); continue
        for d, n in acc.items():
            rec = dids.setdefault(d, {"words": 0, "games": [], "submitted": 0})
            if gid not in rec["games"]:
                rec["games"].append(gid); rec["words"] += n
        if isinstance(submitter, str) and DID_RE.fullmatch(submitter):
            rec = dids.setdefault(submitter, {"words": 0, "games": [], "submitted": 0})
            if gid not in rec.get("submitted_games", []):
                rec.setdefault("submitted_games", []).append(gid); rec["submitted"] += 1
        time.sleep(a.sleep)
    if os.path.exists(a.state):
        try:
            st = json.load(open(a.state))
            for d in (st.get("proven_submitters") or {}):
                rec = dids.setdefault(d, {"words": 0, "games": [], "submitted": 0})
                rec["submitted"] = max(rec.get("submitted", 0), 1)
            for d in (st.get("proven_contributors") or {}):
                rec = dids.setdefault(d, {"words": 0, "games": [], "submitted": 0})
                rec["words"] = max(rec.get("words", 0), 1)
        except (OSError, ValueError):
            pass
    data = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "contest": a.contest, "games_scanned": sorted(games),
            "dids": dict(sorted(dids.items()))}
    tmp = a.out + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=1)
    os.replace(tmp, a.out)
    print(f"wrote {a.out}: {len(dids)} DIDs, {sum(1 for v in dids.values() if v.get('words', 0) >= 1)} with accepted words, "
          f"{sum(1 for v in dids.values() if v.get('submitted', 0) >= 1)} submitters", file=sys.stderr)


if __name__ == "__main__":
    main()
