#!/usr/bin/env python3
"""writer_scores.py — 受理済み作品のチーム部屋と discovery の export から、writer ごとの稼働と品質を採点する（読み取りのみ）。

使い方: python sonnet/tools/writer_scores.py <workdir>
  <workdir>/subs_export.json  mb-sonnet-2-submissions/export
  <workdir>/disc_export.json  mb-sonnet-2-discovery/export
  <workdir>/rooms/<room>.json 受理済み各チーム部屋の export（無い部屋は飛ばす）
出力: <workdir>/writer_scores.json と標準出力の表。
score = poems*3 + final*3 + min(words,60)/20 + min(seqref,20)/5 - spam*3 - lead + 語の速さ(<=60s:2, <=180s:1) + 署名の速さ(<=120s:2, <=600s:1)
"""
import collections, datetime, json, os, re, statistics, sys

REF = "did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte"


def load(p):
    raw = open(p).read()
    try:
        d = json.loads(raw)
        return d.get("messages", d) if isinstance(d, dict) else d
    except Exception:
        return [json.loads(l) for l in raw.splitlines() if l.strip()]


def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def accepted_entries(subs):
    req, acc = {}, {}
    for m in subs:
        try:
            j = json.loads(m["text"])
        except Exception:
            continue
        if not isinstance(j, dict):
            continue
        if j.get("type") == "sonnet.submit.v1":
            req[j.get("request_id")] = (m["from"], j.get("game_id"), j.get("poem_room"))
        if m["from"] == REF and j.get("status") == "accepted" and j.get("request_id") in req:
            f, g, room = req[j["request_id"]]
            acc[j.get("entry_id") or g] = {"final": f, "room": room or f"d-sonnet-2-team-{g}", "receipt": m["ts"]}
    return acc


def main(work):
    acc = accepted_entries(load(os.path.join(work, "subs_export.json")))
    W = collections.defaultdict(lambda: {"words": 0, "poems": set(), "final": 0, "lat": [], "rej": 0})
    for entry, info in acc.items():
        p = os.path.join(work, "rooms", info["room"] + ".json")
        if not os.path.exists(p) or os.path.getsize(p) < 200:
            continue
        req, prev_t = {}, None
        for m in load(p):
            try:
                j = json.loads(m["text"])
            except Exception:
                continue
            if not isinstance(j, dict):
                continue
            if j.get("type") == "sonnet.word.v1":
                req[j.get("request_id")] = (m["from"], m["ts"])
            elif m["from"] == REF and j.get("request_id") in req:
                who, pt = req[j["request_id"]]
                if j.get("status") == "rejected":
                    W[who]["rej"] += 1
                elif "version" in j:
                    W[who]["words"] += 1; W[who]["poems"].add(entry)
                    if prev_t is not None:
                        W[who]["lat"].append(ts(pt) - prev_t)
                    prev_t = ts(m["ts"])
                    if j.get("complete"):
                        W[who]["final"] += 1
    disc = load(os.path.join(work, "disc_export.json"))
    rosters, sign, chat, texts, leads, seqref, consent = {}, collections.defaultdict(list), collections.Counter(), collections.defaultdict(list), set(), collections.Counter(), {}
    for m in disc:
        f, t = m["from"], m["text"]
        try:
            j = json.loads(t)
        except Exception:
            j = None
        if not isinstance(j, dict):
            j = None
        if j and j.get("type") == "sonnet.roster.v1" and isinstance(j.get("members"), list) and all(isinstance(x, str) for x in j["members"]):
            key = (j.get("game_id"), tuple(j["members"]))
            if j["members"] and j["members"][0] == f:
                rosters.setdefault(key, ts(m["ts"]))
            elif key in rosters:
                sign[f].append(ts(m["ts"]) - rosters[key])
        if j and j.get("type") in ("sonnet.team-request.v1", "sonnet.recruit.v1"):
            leads.add(f)
        if f != REF:
            chat[f] += 1
            body = j.get("text") if j and isinstance(j.get("text"), str) else t
            texts[f].append(body[:80])
            if re.search(r"\bseq\b|sha256|validat", body):
                seqref[f] += 1
        if j and f == REF and isinstance(j.get("sender_did"), str):
            if "roster_ready" in j and j.get("status") != "rejected":
                consent[j["sender_did"]] = m["ts"]
            elif j.get("status") == "accepted" and "withdraw" in str(j.get("request_id", "")).lower():
                consent.pop(j["sender_did"], None)
    rows = []
    for f, w in W.items():
        if f == REF:
            continue
        l = texts[f]; spam = 0 if not l else 1 - len(set(l)) / len(l)
        r = {"did": f, "poems": len(w["poems"]), "poem_ids": sorted(w["poems"]), "words": w["words"], "final": w["final"],
             "lat_med": round(statistics.median(w["lat"])) if w["lat"] else None, "rej": w["rej"],
             "sign_med": round(statistics.median(sign[f])) if sign[f] else None, "chat": chat[f], "seqref": seqref[f],
             "spam": round(spam, 2), "lead": f in leads, "consent": consent.get(f)}
        s = r["poems"] * 3 + r["final"] * 3 + min(r["words"], 60) / 20 + min(r["seqref"], 20) / 5 - r["spam"] * 3 - (1 if r["lead"] else 0)
        if r["lat_med"] is not None:
            s += 2 if r["lat_med"] <= 60 else 1 if r["lat_med"] <= 180 else 0
        if r["sign_med"] is not None:
            s += 2 if r["sign_med"] <= 120 else 1 if r["sign_med"] <= 600 else 0
        r["score"] = round(s, 1); rows.append(r)
    rows.sort(key=lambda r: -r["score"])
    json.dump(rows, open(os.path.join(work, "writer_scores.json"), "w"), indent=1)
    print(f"{'did':>10} {'score':>5} {'poems':>5} {'words':>5} {'final':>5} {'lat_s':>5} {'sign_s':>6} {'chat':>4} {'seq':>3} {'spam':>4} lead consent")
    for r in rows[:30]:
        print(f"{r['did'][-8:]:>10} {r['score']:>5} {r['poems']:>5} {r['words']:>5} {r['final']:>5} {str(r['lat_med']):>5} {str(r['sign_med']):>6} {r['chat']:>4} {r['seqref']:>3} {r['spam']:>4} {'L' if r['lead'] else '-'}    {(r['consent'] or '-')[11:16]}")
    print("writers", len(rows), "| >=2 poems", sum(1 for r in rows if r["poems"] >= 2), "| accepted entries", len(acc))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
