// recount.mjs — 保全済みexportを公式デコーダで再集計(プレフィックス集計との差を確定)
import { readFileSync } from "node:fs"; import { homedir } from "node:os"; import path from "node:path"; import { pathToFileURL } from "node:url";
const { decodeFrame, isTclkLine } = await import(pathToFileURL(path.join(process.env.TCLK_DIR ?? path.join(homedir(), "tclk"), "dist/index.js")).href);
const file = process.argv[2];
const byType = {}, rejected = {}, prefixed = { total: 0 }; let rows = 0;
for (const line of readFileSync(file, "utf8").split("\n")) {
  if (!line.trim()) continue; rows += 1;
  let text; try { text = JSON.parse(line).text ?? ""; } catch { continue; }
  if (!isTclkLine(text)) continue;
  prefixed.total += 1;
  try { const f = decodeFrame(text); byType[f.type] = (byType[f.type] ?? 0) + 1; }
  catch (e) { const r = String(e.message).slice(0, 60); rejected[r] = (rejected[r] ?? 0) + 1; }
}
const acc = Object.values(byType).reduce((a, b) => a + b, 0);
console.log(`${path.basename(file)}: rows ${rows}, tclk1-prefixed ${prefixed.total}, decodeFrame OK ${acc}, rejected ${prefixed.total - acc}`);
console.log("accepted by type:", byType);
console.log("rejected by reason:", Object.entries(rejected).sort((a, b) => b[1] - a[1]).slice(0, 8));
