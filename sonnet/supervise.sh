#!/usr/bin/env bash
# sonnet/supervise.sh — bot の監督ループ。利用者が tmux で一度だけ起動する（TC_PASS はこのシェルの環境にだけ置く）。
#   - bot が終了コード 75 で終わったら即再起動（sonnet/RESTART ファイルを置くと bot がそのコードで終了する）
#   - 異常終了なら 15 秒待って再起動。Ctrl-C（130）や通常終了（0）なら止まる
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-$HOME/technocore-env/bin/python}
while true; do
  "$PY" -u sonnet/agent.py run 2>&1 | tee -a sonnet/console.log
  rc=${PIPESTATUS[0]}
  if [ "$rc" -eq 75 ]; then echo "$(date -u +%FT%TZ) supervise: restart requested"; continue; fi
  if [ "$rc" -eq 0 ] || [ "$rc" -eq 130 ]; then echo "$(date -u +%FT%TZ) supervise: exit $rc"; break; fi
  echo "$(date -u +%FT%TZ) supervise: crash rc=$rc; restarting in 15s"; sleep 15
done
