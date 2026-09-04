#!/usr/bin/env node
// refund.mjs — 自PC(payer)用: 完走不能になったlocked契約をrefund経路で閉じる
// 用法: TC_PASS=... node refund.mjs 0x<contract id(先頭16hex以上)> ["理由"]
import { readFileSync } from "node:fs";
import { createPrivateKey } from "node:crypto";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const TCLK = process.env.TCLK_DIR ?? path.join(homedir(), "tclk");
const core = await import(pathToFileURL(path.join(TCLK, "dist/index.js")).href);
const signing = await import(pathToFileURL(path.join(TCLK, "mcp/dist/signing.js")).href);
const { OFFER_ROOM, PaperRail, applyFrame, dealRoom, encodeFrame, findContractHandshake,
  foldTranscript, stateNote, stateNoteValue, transcriptRecord, tryDecodeFrame } = core;
const { canonicalMessage, nextNonce, signerFromSeed, sweep } = signing;

const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
const KEY_PATH = process.env.KEY_PATH ?? path.join(homedir(), "did_key.json");
const prefix = (process.argv[2] ?? "").toLowerCase();
const reason = process.argv[3] ?? "payee process crashed after delivery; preimage lost";
if (!process.env.TC_PASS) { console.error("TC_PASS(パスフレーズ)が未設定です"); process.exit(2); }
if (!prefix.startsWith("0x") || prefix.length < 18) { console.error("usage: node refund.mjs 0x<contract> [reason]"); process.exit(2); }
const log = (s, d) => console.log(`${String(s).padEnd(3)} ${d}`);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadSigner(file, pass) {
  const pem = JSON.parse(readFileSync(file, "utf8")).private_key_pem;
  const ko = createPrivateKey({ key: pem, format: "pem", passphrase: pass });
  const seed = Buffer.from(ko.export({ format: "jwk" }).d, "base64url");
  if (seed.length !== 32) throw new Error("seed length != 32");
  return signerFromSeed(new Uint8Array(seed));
}
async function req(url, init, what) {
  for (let attempt = 0; ; attempt += 1) {
    const res = await fetch(url, init);
    if (res.status !== 429) return res;
    if (attempt >= 5) throw new Error(`${what}: rate limited too long`);
    const stated = Number(res.headers.get("retry-after"));
    await sleep((Number.isFinite(stated) && stated > 0 ? stated : 5) * 1000);
  }
}
async function refusal(what, res) {
  const body = (await res.text()).split("\n").filter((l) => l.trim())[0] ?? "";
  return new Error(`${what}: ${res.status} ${body}`);
}
async function post(signer, room, frame) {
  const text = sweep(encodeFrame(frame));
  const nonce = nextNonce();
  const sig = signer.sign(canonicalMessage(room, nonce, text));
  const res = await req(`${BASE}/r/${room}`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ did: signer.did, sig, nonce: String(nonce), text }),
  }, `post to ${room}`);
  if (!res.ok) throw await refusal(`post to ${room}`, res);
}
const notes = {
  async get(ns, key) {
    const res = await req(`${BASE}/kv/${ns}/${key}`, undefined, `kv get ${ns}/${key}`);
    if (res.status === 404) return null;
    if (!res.ok) throw await refusal(`kv get ${ns}/${key}`, res);
    const value = (await res.text()).split("\n")
      .filter((l) => !l.startsWith("!!") && l.trim() !== "").join("\n").trimEnd();
    return value === "" ? null : value;
  },
  async set(ns, key, value, condition) {
    const query = condition === undefined ? ""
      : "ifAbsent" in condition ? "?if_absent=1"
      : `?if=${encodeURIComponent(condition.if)}`;
    const res = await req(`${BASE}/kv/${ns}/${key}/set/${encodeURIComponent(value)}${query}`,
      undefined, `kv set ${ns}/${key}`);
    if (res.status === 409) return false;
    if (!res.ok) throw await refusal(`kv set ${ns}/${key}`, res);
    return true;
  },
};
const get = async (u) => { const r = await req(u, undefined, u); if (!r.ok) throw await refusal(u, r); return r.text(); };
function parseLenient(room, jsonl) {
  const recs = [];
  for (const line of jsonl.split("\n")) {
    if (!line.trim()) continue;
    try { recs.push(transcriptRecord(room, JSON.parse(line))); } catch { /* 不正行は除外 */ }
  }
  return recs;
}

// ── 本体: 会場の公開データから契約状態を再構成し、窓が開いていればrefund ──
const me = loadSigner(KEY_PATH, process.env.TC_PASS);
log("", `payer  ${me.did}`);
const board = parseLenient(OFFER_ROOM, await get(`${BASE}/r/${OFFER_ROOM}/export`));
let contract = null;
for (const rec of board) {
  const f = tryDecodeFrame(rec.line);
  if (f && f.type === "accept" && f.contract.startsWith(prefix)) contract = f.contract;
}
if (contract === null) { console.error("board export上に該当acceptなし"); process.exit(1); }
const room = dealRoom(contract);
const deal = parseLenient(room, await get(`${BASE}/r/${room}/export`));
const hs = findContractHandshake(board, contract);
if (hs === null) { console.error("handshakeが見つからない"); process.exit(1); }
const st = foldTranscript([hs.offer, hs.accept, ...deal]).state;
log("", `contract ${contract}  status ${st.status}  refundAfter ${new Date(st.offer.refundAfterMs).toISOString()}`);
if (st.status !== "locked") { console.error(`refund対象外: status=${st.status}`); process.exit(1); }
if (st.payerDid !== me.did) { console.error("この契約のpayerではありません"); process.exit(1); }
if (Date.now() < st.offer.refundAfterMs) {
  const m = Math.ceil((st.offer.refundAfterMs - Date.now()) / 60_000);
  console.error(`refund窓はまだ開いていません(あと約${m}分)`); process.exit(3);
}

const rail = new PaperRail(notes);
await rail.refund(st.railRef);
const frame = { type: "refund", from: me.did, contract, ref: st.railRef, reason };
const step = applyFrame(st, frame, Date.now());
if (!step.ok) { console.error(`状態機械がrefundを拒否: ${step.reason}`); process.exit(1); }
await post(me, room, frame);
const sn = stateNote(contract);
await notes.set(sn.ns, sn.key, stateNoteValue("refunded", st.railRef), { if: stateNoteValue("locked", st.railRef) });
log(1, `refund投稿 → レール記録 refunded  最終状態: ${step.state.status}`);
console.log(`  curl -s '${BASE}/r/${room}/export'`);
