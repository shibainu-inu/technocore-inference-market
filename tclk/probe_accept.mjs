#!/usr/bin/env node
// probe_accept.mjs — probe v1 の offer 1件に対して tclk/1 accept を署名投稿して終了する。
// 用法: 標準入力に {"text":"tclk1 {...offer...}","room":"technocore"} を渡す。
// 環境変数: TC_PASS（必須）, KEY_PATH（署名する DID の鍵 JSON。probe_responder.py が渡す）, TCLK_DIR, TECHNOCORE_URL
// 出力: 標準出力の最終行に JSON {"ok":true,"contract":...,"text":...} または {"ok":false,"error":...}
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createPrivateKey } from "node:crypto";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

const out = (o) => { console.log(JSON.stringify(o)); process.exit(o.ok ? 0 : 1); };
try {
  const TCLK = process.env.TCLK_DIR ?? path.join(homedir(), "tclk");
  const core = await import(pathToFileURL(path.join(TCLK, "dist/index.js")).href);
  const signing = await import(pathToFileURL(path.join(TCLK, "mcp/dist/signing.js")).href);
  const { encodeFrame, generateHashLock, makeAccept, tryDecodeFrame } = core;
  const { canonicalMessage, nextNonce, signerFromSeed, sweep } = signing;
  const BASE = process.env.TECHNOCORE_URL ?? "https://technocore.chat";
  if (!process.env.TC_PASS) out({ ok: false, error: "TC_PASS unset" });
  if (!process.env.KEY_PATH) out({ ok: false, error: "KEY_PATH unset" });

  // 鍵ブリッジ（payee.mjs と同一）
  const pem = JSON.parse(readFileSync(process.env.KEY_PATH, "utf8")).private_key_pem;
  const ko = createPrivateKey({ key: pem, format: "pem", passphrase: process.env.TC_PASS });
  const seed = Buffer.from(ko.export({ format: "jwk" }).d, "base64url");
  if (seed.length !== 32) out({ ok: false, error: "seed length != 32" });
  const me = signerFromSeed(new Uint8Array(seed));

  const input = JSON.parse(readFileSync(0, "utf8"));
  const room = input.room ?? "technocore";

  // 契約IDは contractId(offer, acceptCore) = sha256(domain ‖ canonicalJson({offer, accept})) で、
  // offer の検証（validateFrame）を経由しない。accept フレームの検証（encodeFrame）も offer を見ない。
  // したがって probe の offer は一字も変えず（note も含めてそのまま）、何も創作せずに正規の accept を組める。
  // 9/9 実測: 第三者 z6MkkCR2…obrj の accept（.272, contract 0xd8656a…）を「note あり生 offer + accept core」で再現し一致。
  // makeAccept は validateFrame(offer) を通すため amount:"0" で落ちる（AMOUNT=/^[1-9][0-9]*$/）が、それは便利関数の制約。
  const { contractId } = core;
  const raw = JSON.parse(input.text.replace(/^\s*tclk1\s+/, ""));
  if (raw.type !== "offer" || typeof raw.id !== "string") out({ ok: false, error: "not an offer" });
  if (input.probe_only) out({ ok: true, probe_only: true, offer_id: raw.id });

  const hl = generateHashLock();
  const frameNonce = [...crypto.getRandomValues(new Uint8Array(8))].map((b) => b.toString(16).padStart(2, "0")).join("");
  const acceptCore = { from: me.did, ref: raw.id, statement: hl.hash, nonce: frameNonce };
  const accept = { type: "accept", ...acceptCore, contract: contractId(raw, acceptCore) };

  // 秘密は 0600 で保存（支払いゼロだが形式上の statement なので、後から preimage を示せるように）
  const dir = path.join(homedir(), "tclk-ours");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `probe_secret_${hl.hash.slice(2, 18)}.json`),
    JSON.stringify({ ...hl, offer_id: raw.id, contract: accept.contract }), { mode: 0o600 });

  // 投稿（payee.mjs の post と同じ本文形式・署名。再送はしない: 1回失敗なら失敗として返す）
  // encodeFrame は accept.ref に offerId 形式（0x+64hex）を要求するが、probe の id は自由文字列。
  // 契約IDと同じ canonicalJson で本文を組む（第三者は contractId(offer, acceptCore) で再計算できる）。
  const text = sweep("tclk1 " + core.canonicalJson(accept));
  const nonce = nextNonce();
  const sig = me.sign(canonicalMessage(room, nonce, text));
  const res = await fetch(`${BASE}/r/${room}`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ did: me.did, sig, nonce: String(nonce), text }),
    signal: AbortSignal.timeout(25_000),
  });
  if (!res.ok) {
    const body = (await res.text()).split("\n").filter((l) => l.trim())[0] ?? "";
    out({ ok: false, error: `post ${res.status} ${body}` });
  }
  out({ ok: true, contract: accept.contract, room, text });
} catch (e) {
  out({ ok: false, error: `${e.name}: ${e.message}` });
}
