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

  // 公式デコーダを優先。未知フィールド／必須欠落で拒否された場合のみ、JSON を直接読んで補完する。
  // tclk/1 の offer 必須項目は 12（frame-fields.generated）。probe の offer は 5 項目しかないため、
  // 応答するには残りを創作するほかない。何を創作したかは fabricated として呼び出し元に返し、
  // 呼び出し元が平文で先に明示してから accept を投稿する。値の書き換えはしない。
  const OFFER_ALLOWED = ["type", "from", "role", "amount", "asset", "lock", "rails",
    "claimByMs", "refundAfterMs", "expiresMs", "paymentKey", "job", "nonce", "id"];
  let offer = null, ignored = [], fabricated = [];
  const hl = generateHashLock();   // statement 用。offer に lock が無い場合はその lock にも使う
  try {
    offer = core.decodeFrame(input.text);
  } catch (e) {
    const raw = JSON.parse(input.text.replace(/^\s*tclk1\s+/, ""));
    if (raw.type !== "offer") out({ ok: false, error: `not an offer: ${e.message}` });
    ignored = Object.keys(raw).filter((k) => !OFFER_ALLOWED.includes(k));
    offer = {};
    for (const k of OFFER_ALLOWED) if (k in raw) offer[k] = raw[k];
    const now = Date.now();
    const fill = {
      from: input.signer_did,                       // 署名から自明（創作ではないが欠落なので補う）
      role: "payer",                                // offer を出す側。列挙は payer|payee の2値
      lock: hl.hash,                                // 本来は offer 側が提示するもの
      claimByMs: now + 10 * 60_000,
      refundAfterMs: now + 20 * 60_000,
      expiresMs: now + 30 * 60_000,
      nonce: Math.floor(Math.random() * 2 ** 48).toString(16),
    };
    for (const [k, v] of Object.entries(fill)) {
      if (offer[k] === undefined) { offer[k] = v; fabricated.push(k); }
    }
  }
  if (!offer || offer.type !== "offer") out({ ok: false, error: "not an offer" });
  if (input.probe_only) out({ ok: true, probe_only: true, ignored_fields: ignored, fabricated_fields: fabricated });

  // accept を組む（statement はハッシュロック。支払いゼロだが形式上必要なので鋳造し、0600 で保存）
  const dir = path.join(homedir(), "tclk-ours");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `probe_secret_${hl.hash.slice(2, 18)}.json`),
    JSON.stringify({ ...hl, offer_id: offer.id }), { mode: 0o600 });
  const accept = makeAccept(offer, { from: me.did, statement: hl.hash });

  // 投稿（payee.mjs の post と同じ本文形式・署名。再送はしない: 1回失敗なら失敗として返す）
  const text = sweep(encodeFrame(accept));
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
  out({ ok: true, contract: accept.contract, room, text, ignored_fields: ignored, fabricated_fields: fabricated });
} catch (e) {
  out({ ok: false, error: `${e.name}: ${e.message}` });
}
