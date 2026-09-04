// recount2.mjs — 公式decodeFrame基準で、レポートの主要比率を再計算
import { readFileSync } from "node:fs"; import { homedir } from "node:os"; import path from "node:path"; import { pathToFileURL } from "node:url";
const { decodeFrame, isTclkLine } = await import(pathToFileURL(path.join(process.env.TCLK_DIR ?? path.join(homedir(), "tclk"), "dist/index.js")).href);
const offers = new Map(), accepted = new Set();
for (const line of readFileSync(process.argv[2], "utf8").split("\n")) {
  if (!line.trim()) continue;
  let text; try { text = JSON.parse(line).text ?? ""; } catch { continue; }
  if (!isTclkLine(text)) continue;
  let f; try { f = decodeFrame(text); } catch { continue; }
  if (f.type === "offer") offers.set(f.id, f);
  else if (f.type === "accept") accepted.add(f.ref);
}
const b = (pred) => { const ids = [...offers.entries()].filter(([, o]) => pred(o)).map(([i]) => i); const a = ids.filter((i) => accepted.has(i)).length; return `${ids.length} offers, ${a} accepted (${ids.length ? Math.round(100 * a / ids.length) : 0}%)`; };
const formed = [...offers.keys()].filter((i) => accepted.has(i)).length;
console.log(`offers ${offers.size}, contracts formed ${formed} (${Math.round(100 * formed / offers.size)}%)`);
console.log(`FLOP + flop-htlc rail : ${b((o) => o.asset === "FLOP" && o.rails.includes("flop-htlc"))}`);
console.log(`PAPER                 : ${b((o) => o.asset === "PAPER")}`);
console.log(`FLOP (any rails)      : ${b((o) => o.asset === "FLOP")}`);
