#!/usr/bin/env python3
"""
sonnet/llm.py — LLM アダプタ。Claude Code のヘッドレス実行（`claude -p`）を使う。

 - API 鍵は不要（Claude Code のログインを使う）。ツールは全て無効化し、JSON Schema で出力を固定する
 - 部屋の文章は「データ」として user メッセージに入れる。行動条件は system プロンプト（固定文）だけが持つ
 - 呼び出しごとに費用・所要時間・入出力の要約を llm.log に残す
"""
import json, os, subprocess, time

CLAUDE_BIN = os.environ.get("SONNET_CLAUDE_BIN", "claude")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "llm.log")


class LLMError(Exception):
    pass


def ask(system: str, user: str, schema: dict, *, model: str = "opus", timeout_s: int = 150, task: str = "",
        retries: int = 1) -> dict:
    """system/user を渡し、schema に従う dict を返す。失敗時は LLMError"""
    cmd = [CLAUDE_BIN, "-p", "--model", model, "--output-format", "json", "--no-session-persistence",
           "--tools", "", "--system-prompt", system, "--json-schema", json.dumps(schema, ensure_ascii=False),
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
    # 子プロセスに渡す環境は白リストのみ（TC_PASS 等の秘密と、入れ子セッション判定の CLAUDECODE を渡さない）
    env = {k: v for k, v in os.environ.items() if k in ("HOME", "PATH", "TERM", "LANG", "LC_ALL", "USER", "SHELL", "TMPDIR")
           or k.startswith("XDG_")}
    last = None
    for _ in range(retries + 1):
        t0 = time.time()
        try:
            p = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=timeout_s, env=env)  # プロンプトは stdin
        except subprocess.TimeoutExpired:
            last = LLMError(f"timeout after {timeout_s}s")
            _log(task, model, t0, None, str(last)); continue
        except OSError as e:
            last = LLMError(f"spawn failed: {e}")
            _log(task, model, t0, None, str(last)); continue
        try:
            d = json.loads(p.stdout)
        except json.JSONDecodeError:
            last = LLMError(f"non-json output rc={p.returncode}: {p.stdout[:200]!r} {p.stderr[:200]!r}")
            _log(task, model, t0, None, str(last)); continue
        out = d.get("structured_output")
        if d.get("is_error") or out is None:
            last = LLMError(f"no structured output: {str(d.get('result'))[:300]}")
            _log(task, model, t0, d, str(last)); continue
        _log(task, model, t0, d, None)
        return out
    raise last


def _log(task, model, t0, d, err):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "task": task, "model": model,
           "sec": round(time.time() - t0, 1), "err": err}
    if d:
        rec.update({"cost_usd": d.get("total_cost_usd"), "api_ms": d.get("duration_api_ms"),
                    "out": json.dumps(d.get("structured_output"), ensure_ascii=False)[:400]})
    with open(LOG, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


if __name__ == "__main__":  # 動作確認: python3 sonnet/llm.py
    print(ask("Answer only via the schema.", "Which of bright, night, dog rhyme?",
              {"type": "object", "properties": {"pair": {"type": "array", "items": {"type": "string"}}},
               "required": ["pair"], "additionalProperties": False}, task="selftest"))
