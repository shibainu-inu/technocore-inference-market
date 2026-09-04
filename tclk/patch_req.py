#!/usr/bin/env python3
# patch_req.py — ~/tclk-ours/{payer,payee,refund}.mjs の会場I/Oを強化する(アンカー検証付き・冪等)
# 1) req(): 5xx を指数バックオフで再試行(3回)、1試行ごとに AbortSignal.timeout(REQ_TIMEOUT_MS 既定25s)
# 2) post(): 再送後の nonce 拒否 / 422 は「初回が着地済み」として成功扱い
# 3) notes.set(): 409 の本文にある現在値が自分の値と一致なら成功扱い
import os, re, sys
DIR = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/tclk-ours")

NEW_REQ = '''const REQ_TIMEOUT_MS = Number(process.env.REQ_TIMEOUT_MS ?? 25_000);
async function req(url, init, what) {
  // 再試行の原則: 同一リクエストの再送のみ(署名投稿は nonce で at-most-once)。1試行ごとに時間上限。
  for (let attempt = 0; ; attempt += 1) {
    let res;
    try {
      res = await fetch(url, { ...init, signal: AbortSignal.timeout(REQ_TIMEOUT_MS) });
    } catch (e) {
      if (attempt >= 3) throw new Error(`${what}: venue unreachable or silent after ${attempt} retries (${e.name})`);
      const waitMs = Math.min(2 ** attempt, 10) * 1000;
      log("", `${what}: ${e.name} — ${waitMs / 1000}s 待機して同一リクエストを再送`);
      await sleep(waitMs); continue;
    }
    if (res.status !== 429 && res.status < 500) { res.attempts = attempt; return res; }
    if (attempt >= 3) throw new Error(`${what}: gave up after ${attempt} retries (${res.status})`);
    const stated = Number(res.headers.get("retry-after"));
    const waitMs = res.status === 429
      ? (Number.isFinite(stated) && stated > 0 ? stated : 5) * 1000
      : Math.min(2 ** attempt, 10) * 1000;
    log("", `${what}: ${res.status} — ${waitMs / 1000}s 待機`);
    await sleep(waitMs);
  }
}
'''
OLD_POST_FAIL = "  if (!res.ok) throw await refusal(`post to ${room}`, res);\n"
NEW_POST_FAIL = '''  if (!res.ok) {
    const body = await res.text();
    const first = body.split("\\n").filter((l) => l.trim())[0] ?? "";
    // 再送後の nonce 拒否 / 422 重複拒否は「初回の書き込みが着地していた」印
    if (res.attempts > 0 && (res.status === 422 || /nonce/i.test(first))) {
      log("", `再送が拒否 (${res.status}: ${first}) — 初回の書き込みが着地済みとみなす`);
      return text;
    }
    throw new Error(`post to ${room}: ${res.status} ${first}`);
  }
'''
OLD_409 = "    if (res.status === 409) return false;\n"
NEW_409 = '''    if (res.status === 409) {
      // 自分の前回試行が着地していれば「現在値 = 書こうとした値」→ 成功扱い(会場の 409 本文が現在値を運ぶ)
      const lines = (await res.text()).split("\\n");
      const i = lines.findIndex((l) => l.startsWith("current value follows"));
      const current = i >= 0 ? (lines[i + 1] ?? "").trimEnd() : null;
      if (current !== null && current === value) {
        log("", `kv set ${ns}/${key}: 409 だが現在値が自分の値と一致 — 着地済み`);
        return true;
      }
      return false;
    }
'''
REQ_RE = re.compile(r"async function req\(url, init, what\) \{\n.*?\n\}\n", re.S)

for name in ("payer.mjs", "payee.mjs", "refund.mjs"):
    p = os.path.join(DIR, name)
    if not os.path.exists(p): print("skip (absent):", name); continue
    s = open(p, encoding="utf-8").read()
    if "REQ_TIMEOUT_MS" in s: print("already patched:", name); continue
    assert len(REQ_RE.findall(s)) == 1, f"{name}: req() anchor"
    assert s.count(OLD_POST_FAIL) == 1, f"{name}: post fail anchor"
    assert s.count(OLD_409) == 1, f"{name}: 409 anchor"
    s = REQ_RE.sub(lambda m: NEW_REQ, s, count=1)
    s = s.replace(OLD_POST_FAIL, NEW_POST_FAIL).replace(OLD_409, NEW_409)
    open(p, "w", encoding="utf-8").write(s)
    print("patched:", name)
print("done")
