#!/usr/bin/env node
// payer.mjs — 自PC側発注エージェント(offer掲示→lock→検収→receipt)
// 用法: TC_PASS=... PAYEE_DID=did:key:z6Mk... node payer.mjs
// 環境変数: KEY_PATH (既定 ~/did_key.json), TCLK_DIR (既定 ~/tclk), TECHNOCORE_URL
import { readFileSync } from "node:fs";
import { createPrivateKey, randomBytes } from "node:crypto";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const TCLK = process.env.TCLK_DIR ?? path.join(homedir(), "tclk");
const core = await import(pathToFileURL(path.join(TCLK, "dist/index.js")).href);
const signing = await import(pathToFileURL(path.join(TCLK, "mcp/dist/signing.js")).href);
const {
  OFFER_ROOM, PaperRail, applyFrame, contractId, dealRoom, encodeFrame,
  lockTerms, makeOffer, openContract, paperNote, stateNote, stateNoteValue, tryDecodeFrame,
} = core;
const { canonicalMessage, nextNonce, signerFromSeed, sweep } = signing;

const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
const KEY_PATH = process.env.KEY_PATH ?? path.join(homedir(), "did_key.json");
const PAYEE_DID = process.env.PAYEE_DID;
if (!process.env.TC_PASS) { console.error("TC_PASS(パスフレーズ)が未設定です"); process.exit(2); }
if (!PAYEE_DID) { console.error("PAYEE_DID(マイナーDID)が未設定です"); process.exit(2); }

const log = (s, d) => console.log(`${String(s).padEnd(3)} ${d}`);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const POLL = Number(process.env.POLL_MS ?? 8000);

function loadSigner(file, pass) {
  const pem = JSON.parse(readFileSync(file, "utf8")).private_key_pem;
  const ko = createPrivateKey({ key: pem, format: "pem", passphrase: pass });
  const seed = Buffer.from(ko.export({ format: "jwk" }).d, "base64url");
  if (seed.length !== 32) throw new Error("seed length != 32");
  return signerFromSeed(new Uint8Array(seed));
}
const REQ_TIMEOUT_MS = Number(process.env.REQ_TIMEOUT_MS ?? 25_000);
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
async function refusal(what, res) {
  const body = (await res.text()).split("\n").filter((l) => l.trim())[0] ?? "";
  return new Error(`${what}: ${res.status} ${body}`);
}
async function readTail(room) {
  const res = await req(`${BASE}/r/${room}?format=json`, undefined, `read ${room}`);
  if (res.status === 404) return [];
  if (!res.ok) throw await refusal(`read ${room}`, res);
  const view = await res.json();
  if (!view || !Array.isArray(view.messages)) return [];
  return view.messages;
}
async function post(signer, room, frameOrText) {
  const text = sweep(typeof frameOrText === "string" ? frameOrText : encodeFrame(frameOrText));
  const nonce = nextNonce();
  const sig = signer.sign(canonicalMessage(room, nonce, text));
  const res = await req(`${BASE}/r/${room}`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ did: signer.did, sig, nonce: String(nonce), text }),
  }, `post to ${room}`);
  if (!res.ok) {
    const body = await res.text();
    const first = body.split("\n").filter((l) => l.trim())[0] ?? "";
    // 再送後の nonce 拒否 / 422 重複拒否は「初回の書き込みが着地していた」印
    if (res.attempts > 0 && (res.status === 422 || /nonce/i.test(first))) {
      log("", `再送が拒否 (${res.status}: ${first}) — 初回の書き込みが着地済みとみなす`);
      return text;
    }
    throw new Error(`post to ${room}: ${res.status} ${first}`);
  }
  return text;
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
    if (res.status === 409) {
      // 自分の前回試行が着地していれば「現在値 = 書こうとした値」→ 成功扱い(会場の 409 本文が現在値を運ぶ)
      const lines = (await res.text()).split("\n");
      const i = lines.findIndex((l) => l.startsWith("current value follows"));
      const current = i >= 0 ? (lines[i + 1] ?? "").trimEnd() : null;
      if (current !== null && current === value) {
        log("", `kv set ${ns}/${key}: 409 だが現在値が自分の値と一致 — 着地済み`);
        return true;
      }
      return false;
    }
    if (!res.ok) throw await refusal(`kv set ${ns}/${key}`, res);
    return true;
  },
};

// ── 本体 ──
const me = loadSigner(KEY_PATH, process.env.TC_PASS);
log("", `venue  ${BASE}`);
log("", `payer  ${me.did} (requester)`);
log("", `payee  ${PAYEE_DID} (miner, 期待値)`);
if (process.env.EXPECT_DID && process.env.EXPECT_DID !== me.did) {
  console.error(`鍵から導出したDIDが期待値と不一致: ${me.did}`); process.exit(2);
}
const now = Date.now();

// 0 — ジョブ仕様はKVノートに置き、offerはそれを指すだけ
const taskId = `boardhealth-${randomBytes(3).toString("hex")}`;
const specNote = { ns: `tclk-job-${taskId.slice(-2)}`, key: taskId.slice(0, 14) };
const spec = "board health report of /r/tclk-offers | checkable: report_sha256 posted in deal room before claimBy; counts included for offers, contracts formed, rail split, FLOP follow-up; summary model qwen2.5:1.5b disclosed verbatim; full report published to operator repo within 24h";
await notes.set(specNote.ns, specNote.key, spec, { ifAbsent: true });
log(0, `job spec   /kv/${specNote.ns}/${specNote.key}`);

// 1 — offer掲示(見せ球はしない: 決済可能なPAPER建てのみ)
const offer = makeOffer({
  from: me.did, role: "payer", lock: "hash",
  amount: "727", asset: "PAPER", rails: ["paper"],
  claimByMs: now + 45 * 60_000, refundAfterMs: now + 90 * 60_000, expiresMs: now + 20 * 60_000,
  job: { proto: "a2a", id: taskId, context: `/kv/${specNote.ns}/${specNote.key}` },
});
await post(me, OFFER_ROOM, offer);
log(1, `offer投稿  id ${offer.id.slice(0, 18)}…  amount 727 PAPER  job ${taskId}`);

// 2 — マイナーDIDのacceptを待つ(contract idも自分で再計算して照合)
let accept = null;
const acceptDeadline = offer.expiresMs;
while (accept === null) {
  if (Date.now() > acceptDeadline) { console.error("accept待機タイムアウト(offer失効)"); process.exit(1); }
  for (const m of await readTail(OFFER_ROOM)) {
    const f = tryDecodeFrame(String(m.text ?? ""));
    if (f && f.type === "accept" && f.ref === offer.id && f.from === PAYEE_DID) {
      const expect = contractId(offer, { from: f.from, ref: f.ref, statement: f.statement,
        paymentKey: f.paymentKey, nonce: f.nonce });
      if (expect !== f.contract) { log("", "contract id不一致のacceptを無視"); continue; }
      accept = f; break;
    }
  }
  if (accept === null) await sleep(POLL);
}
const contract = accept.contract;
const room = dealRoom(contract);
const sn = stateNote(contract);
log(2, `accept検知 contract ${contract.slice(0, 18)}…  deal room /r/${room}`);
let view = applyFrame(openContract(offer), accept, Date.now()).state;

// 3 — レールにロックし、ディールルームで宣言
const rail = new PaperRail(notes);
const ref = await rail.lock(lockTerms(view));
const lockFrame = { type: "lock", from: me.did, contract, rail: "paper", ref };
await post(me, room, lockFrame);
view = applyFrame(view, lockFrame, Date.now()).state;
await notes.set(sn.ns, sn.key, stateNoteValue("locked", ref), { if: stateNoteValue("accepted") });
const pn = paperNote(contract);
log(3, `lock投稿   rail record /kv/${pn.ns}/${pn.key}`);

// 4 — 納品(deliverable行)とrevealを待ち、検収する
let delivery = null, reveal = null;
const claimDeadline = offer.claimByMs + 60_000;
while (reveal === null) {
  if (Date.now() > claimDeadline) break;
  for (const m of await readTail(room)) {
    const text = String(m.text ?? "");
    if (delivery === null && text.startsWith(`deliverable ${taskId} `)) delivery = text;
    const f = tryDecodeFrame(text);
    if (f && f.type === "reveal" && f.contract === contract) reveal = f;
  }
  if (reveal === null) await sleep(POLL);
}
if (reveal === null) {
  console.error("claim期限までにrevealなし — refundAfter以降にrefund可能です"); process.exit(1);
}
const step = applyFrame(view, reveal, Date.now());
if (!step.ok) { console.error(`reveal却下: ${step.reason}`); process.exit(1); }
view = step.state;
const dh = delivery === null ? null : (delivery.match(/report_sha256=(0x[0-9a-f]{64})/) ?? [])[1];
log(4, `検収: 納品行=${delivery !== null} report_sha256=${dh ? dh.slice(0, 18) + "…" : "なし"} / 秘密がstatementを開く=${view.status === "claimed"}`);
if (delivery === null) log("", "警告: 納品行なしでのreveal(HTLCの正直な限界のデモとして記録)");

// 5 — receipt(検収完了の記録)
const receipt = { type: "receipt", from: me.did, contract, outcome: "claimed", rail: "paper", ref };
await post(me, room, receipt);
log(5, `receipt投稿  最終状態: ${view.status}`);
console.log();
console.log("Deal complete. Read it back yourself:");
console.log(`  curl -s '${BASE}/r/${room}/export'`);
console.log(`  curl -s '${BASE}/kv/${pn.ns}/${pn.key}'`);
console.log(`  curl -s '${BASE}/kv/${sn.ns}/${sn.key}'`);
