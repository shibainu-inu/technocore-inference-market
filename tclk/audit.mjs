#!/usr/bin/env node
// audit.mjs — 第三者監査: 会場の公開データ(export)だけからディールを再構成する(読み取り専用・鍵不要)
// 用法: node audit.mjs 0x<contract id(先頭16hex以上で可)>
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const TCLK = process.env.TCLK_DIR ?? path.join(homedir(), "tclk");
const { OFFER_ROOM, dealRoom, findContractHandshake, foldTranscript, transcriptRecord, tryDecodeFrame } =
  await import(pathToFileURL(path.join(TCLK, "dist/index.js")).href);
const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
const prefix = (process.argv[2] ?? "").toLowerCase();
if (!prefix.startsWith("0x") || prefix.length < 18) {
  console.error("usage: node audit.mjs 0x<contract id (先頭16hex以上)>"); process.exit(2);
}
const get = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(`${u}: ${r.status}`); return r.text(); };

// 寛容パーサー: 行単位で検証し、不正行は数えて除外(公式parseTranscriptExportは1行でも不正なら全拒否)
function parseLenient(room, jsonl) {
  const recs = []; let bad = 0;
  for (const line of jsonl.split("\n")) {
    if (!line.trim()) continue;
    try { recs.push(transcriptRecord(room, JSON.parse(line))); } catch { bad += 1; }
  }
  return { recs, bad };
}
const { recs: board, bad: boardBad } = parseLenient(OFFER_ROOM, await get(`${BASE}/r/${OFFER_ROOM}/export`));
let contract = null;
for (const rec of board) {
  const f = tryDecodeFrame(rec.line);
  if (f && f.type === "accept" && f.contract.startsWith(prefix)) contract = f.contract;
}
if (contract === null) { console.error("board export上に該当acceptなし(掲示板から流れた可能性)"); process.exit(1); }
const room = dealRoom(contract);
const { recs: deal, bad: dealBad } = parseLenient(room, await get(`${BASE}/r/${room}/export`));
const hs = findContractHandshake(board, contract);
if (hs === null) { console.error("handshake(offer+accept)が見つからない"); process.exit(1); }

// 署名・送信者・会場時刻を検証しながら状態機械に畳み込む(当事者を一切信用しない)
const folded = foldTranscript([hs.offer, hs.accept, ...deal]);
const st = folded.state;
const applied = folded.steps.filter((s) => s.ok).length;
console.log(`contract     ${contract}`);
console.log(`records      board ${board.length} (malformed skipped ${boardBad}) / deal room ${deal.length} (malformed skipped ${dealBad})`);
console.log(`replayed     ${applied} frames applied, ${folded.steps.length - applied} ignored`);
for (const s of folded.steps) {
  console.log(`  ${s.ok ? "ok  " : "skip"} ${s.room} seq=${s.seq} ${s.type ?? "(non-frame)"}${s.reason ? " — " + s.reason : ""}`);
}
console.log(`final status ${st?.status}`);
console.log(`payer        ${st?.payerDid}`);
console.log(`payee        ${st?.payeeDid}`);
console.log(`statement    ${st?.statement}`);
console.log(`secret       ${st?.secret ?? "(未公開)"}`);
console.log(`rail / ref   ${st?.rail ?? "-"} ${st?.railRef ?? ""}`);
console.log(`amount       ${st?.offer.amount} ${st?.offer.asset}   job ${st?.offer.job?.id ?? "-"}`);
console.log(`refundAfter  ${new Date(st?.offer.refundAfterMs ?? 0).toISOString()}`);
const delivery = deal.map((r) => r.line).find((l) => l.startsWith("deliverable "));
console.log(`deliverable  ${delivery ?? "(なし)"}`);
