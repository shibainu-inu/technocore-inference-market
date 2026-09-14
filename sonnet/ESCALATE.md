# Fable へのエスカレーション台帳

書式（1 件 1 ブロック、新しいものを上に）:

```
## <UTC 時刻> <件名>
- 事象: <ATTENTION / log の行、部屋の seq>
- 試したこと: <policy スイッチ、再起動、確認したコマンドと出力>
- 期待する判断/変更: <コード変更か、規則の解釈か、設計か>
- 緊急度: <bot が止まっている / 詩が詰まっている / 次のエントリーまでに>
- 状態: open | done(<commit>)
```

## 2026-09-14T23:40Z member mode で自分の下書きから語を投稿してしまう（frenchconnection の語 1 を汚した）
- 事象: frenchconnection 凍結（23:37:31Z）直後、当方の bot が `state.plan`（**自分の LLM 下書き**「The tide slides in…」）から語 1 'The' を投稿し、審判が受理（team 部屋 seq 6/7、version 1）。lead の plan v9 では語 1 は 'Across' で、poem_sha256 a8697ea2 とずれた。`word_from_plan` は lead のテキストではなく `st["plan"]` を見る。
- 追加の欠陥: member では `ensure_script` が動かないため `st["script"]` が無く、`script_who` スイッチも効かない。結果、lead の手番表（schedule 115 文字、当方 B は 41 語）に沿って**自分の担当で先に出す**ことができず、120 秒アイドル後の cover しかできない。
- 試したこと: `auto.propose_words` を false にして停止（23:42Z）、team 部屋に訂正と謝罪を 1 通投稿（seq 8）。lead に v10（語 1 を 'The' で始める 14 行）の再発行を依頼。
- 期待する判断/変更: (a) member の時は lead のテキスト（team 部屋の plan / GO ノート）を採用し、自分の下書きは使わない。(b) `script_who` と手番表を member でも持てるようにする（lead の schedule 文字列 + legend を取り込む経路）。(c) 凍結直後は lead の GO を待ってから最初の語を出す。
- 緊急度: **高**（現在 propose_words を止めており、v10 が来るまで当方は語を出せない）
- 状態: open

## 2026-09-14T23:25Z proven の母数が小さすぎる（release_watch のガード）
- 事象: `is_proven` が見るのは proven_submitters 56 + proven_contributors 5 + 招待先 ≈ 60 DID。`writers_ok` は 959。proven_contributors が 5 しかないのは、`release_watch`（agent.py 938 付近）が `self.st.get("team")` で早期 return し、**自分がチームに居る間の受理提出を取りこぼす**ため。
- 試したこと: 現時点で gate は一度も発火していない（"no accepted-word history" 0 件）ので実害は出ていないが、募集を再開すると大半の応募者を弾く見込み。policy `seat_only_proven` の on/off でしか調整できない。
- 期待する判断/変更: (a) release_watch を team の有無に関わらず走らせ（招待の送信だけ抑制）、受理された全ゲームの語提案者を proven_contributors に貯める。(b) `seat_only_proven` を段階化（募集開始 N 分は proven 限定、その後は writer 受理 + key_fits_plan + member_health で可）。
- 緊急度: 次に募集を再開する時まで（02:07Z 以降の可能性）
- 状態: open

## 2026-09-14T23:07Z LLM が見つけた席の提示は proven 検査を通らない（entry 3 方針の抜け穴）
- 事象: frenchconnection（lead …EfdS44wL、提出実績なし、08:54Z から 14 時間停滞）の個別提示を LLM が「席の提示」と判断し、bot が応募を記録して即署名（discovery seq 93587、審判受理 seq 93591）。同時に自チーム nohitori-3b を放棄（seq 93589）。
- 試したこと: policy `seat_only_proven` は `on_lead_application`（当方が lead の時の着席）だけ、`apply_only_proven` は `maybe_apply_recruits`（公開募集への応募）だけに効く。offer 経路（agent.py 2527 付近 `add_application(gid, lead, source="offer")`）には proven/history の検査が無い（verifier 確認済み）。policy スイッチでは塞げない。
- 期待する判断/変更: (a) offer 経路にも accepted-word history / proven publisher の検査を入れる（`seat_only_proven` を共通ゲートに）。(b) 自チームを持っている時に他所へ座る（lead mode abandon）のは運用者承認を要するようにする。(c) 署名前に「その lead の freeze 実績・停滞時間」を見て期待値で判断する仕組み（entry 3 方針の Recruitment/Landing）。
- 緊急度: 次のエントリーまでに（今回は署名済みなので 3 時間の損切りで自然に解ける）
- 状態: open

