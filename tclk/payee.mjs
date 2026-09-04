#!/usr/bin/env node
// payee.mjs — GCP側マイナーエージェント(受注→納品→claim)
// 用法: TC_PASS=... PAYER_DID=did:key:z6Mk... node payee.mjs
// 環境変数: KEY_PATH (既定 ~/technocore-inference-market/did_miner2.json),
//   TCLK_DIR (既定 ~/tclk), TECHNOCORE_URL, REPORT_CMD, JOB_PREFIX (既定 boardhealth-)
import { readFileSync } from "node:fs";
import { createPrivateKey } from "node:crypto";
import { execFileSync } from "node:child_process";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const TCLK = process.env.TCLK_DIR ?? path.join(homedir(), "tclk");
const core = await import(pathToFileURL(path.join(TCLK, "dist/index.js")).href);
const signing = await import(pathToFileURL(path.join(TCLK, "mcp/dist/signing.js")).href);
const {
  OFFER_ROOM, PaperRail, applyFrame, dealRoom, encodeFrame, generateHashLock,
  lockTerms, makeAccept, openContract, stateNote, stateNoteValue, tryDecodeFrame,
} = core;
const { canonicalMessage, nextNonce, signerFromSeed, sweep } = signing;

const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
const KEY_PATH = process.env.KEY_PATH ?? path.join(homedir(), "technocore-inference-market/did_miner2.json");
const PAYER_DID = process.env.PAYER_DID;
const JOB_PREFIX = process.env.JOB_PREFIX ?? "boardhealth-";
const REPORT_CMD = process.env.REPORT_CMD ?? `python3 ${path.join(homedir(), "tclk-archive/make_report.py")}`;
if (!process.env.TC_PASS) { console.error("TC_PASS(パスフレーズ)が未設定です"); process.exit(2); }
if (!PAYER_DID) { console.error("PAYER_DID(発注側DID)が未設定です"); process.exit(2); }

const log = (s, d) => console.log(`${String(s).padEnd(3)} ${d}`);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const POLL = Number(process.env.POLL_MS ?? 8000);

// ── 鍵ブリッジ: パスフレーズ付きPEM(JSON格納) → 32バイトseed → tclk署名器 ──
function loadSigner(file, pass) {
  const pem = JSON.parse(readFileSync(file, "utf8")).private_key_pem;
  const ko = createPrivateKey({ key: pem, format: "pem", passphrase: pass });
  const seed = Buffer.from(ko.export({ format: "jwk" }).d, "base64url");
  if (seed.length !== 32) throw new Error("seed length != 32");
  return signerFromSeed(new Uint8Array(seed));
}

// ── 会場I/O(stock live-deal.mjs と同一挙動) ──
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
log("", `payee  ${me.did} (miner)`);
log("", `payer  ${PAYER_DID} を待機`);
if (process.env.EXPECT_DID && process.env.EXPECT_DID !== me.did) {
  console.error(`鍵から導出したDIDが期待値と不一致: ${me.did}`); process.exit(2);
}

// 1 — 掲示板をポーリングし、発注DIDからの対象offerを待つ
let offer = null;
const offerDeadline = Date.now() + 60 * 60_000;
while (offer === null) {
  if (Date.now() > offerDeadline) { console.error("offer待機タイムアウト(60分)"); process.exit(1); }
  for (const m of await readTail(OFFER_ROOM)) {
    const f = tryDecodeFrame(String(m.text ?? ""));
    if (f && f.type === "offer" && f.from === PAYER_DID && f.lock === "hash"
        && f.asset === "PAPER" && f.rails.includes("paper")
        && f.job && typeof f.job.id === "string" && f.job.id.startsWith(JOB_PREFIX)
        && Date.now() < f.expiresMs && f.claimByMs > Date.now() + 10 * 60_000) {
      offer = f; break;
    }
  }
  if (offer === null) await sleep(POLL);
}
log(1, `offer検知  id ${offer.id.slice(0, 18)}…  job ${offer.job.id}`);
const spec = offer.job.context ? await notes.get(...offer.job.context.replace(/^\/kv\//, "").split("/")) : null;
log("", `job spec   ${spec ?? "(取得不可)"}`);

// 2 — 秘密を鋳造し、statementだけを公開してaccept
const hl = generateHashLock();
// クラッシュ対策: 秘密を即座に0600で保存(公開前に落ちても復旧できる)
const { writeFileSync } = await import("node:fs");
writeFileSync(path.join(homedir(), `tclk-ours/secret_${hl.hash.slice(2, 18)}.json`), JSON.stringify(hl), { mode: 0o600 });
const accept = makeAccept(offer, { from: me.did, statement: hl.hash });
await post(me, OFFER_ROOM, accept);
const contract = accept.contract;
const room = dealRoom(contract);
const sn = stateNote(contract);
log(2, `accept投稿  contract ${contract.slice(0, 18)}…`);
log("", `deal room  /r/${room}`);
let view = applyFrame(openContract(offer), accept, Date.now()).state;
await notes.set(sn.ns, sn.key, stateNoteValue("accepted"), { ifAbsent: true });

// 3 — lockフレームを待ち、レール自体を検証(相手の言葉は信じない)
let lockFrame = null;
const lockDeadline = Date.now() + 30 * 60_000;
while (lockFrame === null) {
  if (Date.now() > lockDeadline) { console.error("lock待機タイムアウト(30分)"); process.exit(1); }
  for (const m of await readTail(room)) {
    const f = tryDecodeFrame(String(m.text ?? ""));
    if (f && f.type === "lock" && f.contract === contract && f.rail === "paper") { lockFrame = f; break; }
  }
  if (lockFrame === null) await sleep(POLL);
}
view = applyFrame(view, lockFrame, Date.now()).state;
const rail = new PaperRail(notes);
const held = await rail.verifyLock(lockTerms(view), lockFrame.ref);
log(3, `lock検知   rail自己検証 verifyLock=${held}`);
if (!held) { console.error("レール記録がlockフレームの主張と不一致"); process.exit(1); }

// 4 — 実ジョブ: レポートを生成し(qwen2.5:1.5b要約を含む)、sha256を納品
log(4, `レポート生成中: ${REPORT_CMD} ${contract.slice(0, 12)}…`);
const [cmd, ...args] = REPORT_CMD.split(" ");
const out = execFileSync(cmd, [...args, contract], { encoding: "utf8", timeout: 600_000 });
const mh = out.match(/sha256\(report\): 0x([0-9a-f]{64})/);
if (!mh) { console.error("レポート生成出力にsha256が見つからない"); process.exit(1); }
const reportHash = `0x${mh[1]}`;
const delivery = `deliverable ${offer.job.id} contract=${contract} report_sha256=${reportHash} model=qwen2.5:1.5b generated_on=payee-node`;
await post(me, room, delivery);
log("", `納品投稿   report_sha256=${reportHash.slice(0, 18)}…`);

// 5 — 秘密の公開がclaimそのもの
const reveal = { type: "reveal", from: me.did, contract, ref: lockFrame.ref, secret: hl.preimage };
await post(me, room, reveal);
await rail.claim(lockFrame.ref, hl.preimage);
await notes.set(sn.ns, sn.key, stateNoteValue("claimed", lockFrame.ref),
  { if: stateNoteValue("locked", lockFrame.ref) });
view = applyFrame(view, reveal, Date.now()).state;
log(5, `reveal投稿 → レール記録 claimed  最終状態: ${view.status}`);
log("", `report: ~/tclk-archive/report_${contract.slice(0, 10)}.md (公開リポジトリへコミット予定)`);
