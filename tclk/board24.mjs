// board24.mjs — /r/tclk-offers/export を読み、直近 N 時間の tclk1 フレームを公式デコーダで数える(読み取り専用・鍵不要)。
// 最終行に JSON を1行出す(flopmarket.py stats --x から subprocess で呼ばれる)。usage: node board24.mjs [hours=24]
import { homedir } from "node:os"; import path from "node:path"; import { pathToFileURL } from "node:url";
const { decodeFrame, isTclkLine } = await import(pathToFileURL(path.join(process.env.TCLK_DIR ?? path.join(homedir(), "tclk"), "dist/index.js")).href);
const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
const ROOM = process.env.TCLK_OFFER_ROOM ?? "tclk-offers";
const hours = Number(process.argv[2] ?? 24);
const cutoff = Date.now() - hours * 3600e3;
const r = await fetch(`${BASE}/r/${ROOM}/export`, { signal: AbortSignal.timeout(60_000) });
if (!r.ok) { console.error(`export ${r.status}`); process.exit(1); }
const out = { room: ROOM, hours, rows: 0, in_window: 0, prefixed: 0, ok: 0, rejected: 0, offer: 0, accept: 0, other: 0, oldest_ts: null };
for (const line of (await r.text()).split("\n")) {
  if (!line.trim()) continue; out.rows += 1;
  let o; try { o = JSON.parse(line); } catch { continue; }   // 19桁 nonce は JSON.parse 自体は通る(精度落ちのみ、ここでは nonce 未使用)
  const t = Date.parse(o.ts ?? ""); if (!(t >= cutoff)) continue;
  out.in_window += 1; if (out.oldest_ts === null || o.ts < out.oldest_ts) out.oldest_ts = o.ts;
  const text = o.text ?? ""; if (!isTclkLine(text)) continue;
  out.prefixed += 1;
  try { const f = decodeFrame(text); out.ok += 1; if (f.type === "offer") out.offer += 1; else if (f.type === "accept") out.accept += 1; else out.other += 1; }
  catch { out.rejected += 1; }
}
out.cover_h = out.oldest_ts ? Math.round((Date.now() - Date.parse(out.oldest_ts)) / 3.6e5) / 10 : 0;
console.log(JSON.stringify(out));
