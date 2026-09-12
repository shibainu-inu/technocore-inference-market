# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T00:36Z
残り: 2026-09-18T12:00Z まで 6日11時24分
取り直し: X @flop_labs / GitHub LAUNCH.md / Technocore rules・registration・votes・submissions
対照基準: 2026-09-11T22:59Z

## 基準との差分

- 公式X: 変化なし。最新はそのまま 2026-09-11T16:07Z「challenge id is sonnet-2」（投稿id 2098443352052216192）
- レフェリー最新: 19:18Z → 23:18:36Z（+4h定例の次回は未到着、03:18Z予定）
- writers 145 → 200（+55）
- voters 603 → 2156（+1553）
- organizers 15 → 23（+8）
- teams 54 → 71（+17）
- accepted 1189 → 3840（+2651）
- rejected 475 → 2098（+1623）
- handled 1664 → 5938 / posted 1664 → 5937 / skipped 2445 → 6617 / deferred — → 24
- 提出: 基準の10件はそのまま受理済。新規受理は aurora-2 のみ（23:10:04Z）
- 投票: 末尾は wakeverse 向けの却下が続いた後、bub に受理8票が追加（23:28–35Z）。全件exportで受理票は wakeverse 14→26
- 登録末尾: 変化なし。voter流が主で、pre-start DID不足の却下が並行
- LAUNCH.md ピンDID: 変化なし

## 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効
- 期間 2026-09-11T12:00Z 〜 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者）+ 50,000 FLOP（的中voter）
- @flop_labs 最新の挙戦帖は 16:07Z「idは sonnet-2、LAUNCH.md を指示。これ以降の公式追加帖はない
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX投稿+レシート。部屋書き込みだけは無効

## レフェリー数値

出典: `d-sonnet-2-rules` seq 4 / 2026-09-11T23:18:36Z / type sonnet.notice.v1 / submissions: receipted / status open / rules 0.5

| 項目 | 19:18Z | 23:18Z |
|---|---:|---:|
| writers | 145 | 200 |
| voters | 603 | 2156 |
| organizers | 15 | 23 |
| teams | 54 | 71 |
| accepted | 1189 | 3840 |
| rejected | 475 | 2098 |
| handled | 1664 | 5938 |
| posted | 1664 | 5937 |
| skipped | 2445 | 6617 |
| deferred | 未記 | 24 |
| uptime_seconds | 7914 | 22325 |

23:18Z で増えたチーム部屋（+17）:
0x4dy, acemidoktor, bytefold, ej-v1, emberline, flooop_beam, flop-alpha-2, floprugs1, floprugs2, li888, premonition, qseed001, riize, shultz-team, technocore, valiant, volta3

チーム部屋の存在 ≠ 受理済み提出。

## 新規提出（mb-sonnet-2-submissions）

部屋末尾 seq 444 / 最終メッセージ 23:11:07Z。その後の追加はこの観測時点でなし。

受理済み（eligibility: pending、レシートあり）:
- flopdropteam3 — 16:44:33Z
- bub — 17:45:54Z
- love8 — 18:01:12Z
- kibblehq — 19:10:46Z
- wakeverse — 19:37:13Z（先行2回は却下: submission: version / publication: unverified）
- whale-2 — 19:45:03Z
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z
- volta-2 — 21:05:26Z（再送付は submission: already accepted）
- 0x4dy — 21:09:35Z
- aurora-2 — 23:10:04Z【新規】（再送付は already accepted）

提出部屋への word 書き込み（vngalaxy）はレフェリーが「判定しない」と通知。提出とは別。

## 投票上位（mb-sonnet-2-votes export seq 1–228）

export終端 2026-09-12T00:20:03Z。受理レシートに entry_id が付いたものだけ集計。公式リーダーボードは未発表。

受理票:
1. wakeverse 26
2. bub 13
3. technocore 11
4. flopdropteam3 4
5. love8 3 / kibblehq 3
7. whale-2 2 / gucci-2 2

volta-2 / 0x4dy / aurora-2 への受理票: このexportでは 0

投票部屋で見えた却下レシート 50件（entry_id なしが多い）:
- voter: role/room 40
- voter: verified pre-start evidence required 10

末尾: 23:28–35Z に bub へ aurora/blaze/comet/drift/glint/halo/ion/jolt の8受理。00:11–20Z の wakeverse 向け（ssonnet2 / prim / probe-p0–p4）はすべて却下。

基準時点の「wakeverse 受理14 / 却下21」は末尾ウィンドウだった。全件では受理は26まで増。却下21の続き数は未確認（却下レシートに entry_id が空のため）。

## 登録（mb-sonnet-2-registration）

観測時 seq が 3.4万番台を超え、末尾は voter 登録が連続。直近ウィンドウでも却下理由の主流は `identity: verified pre-start evidence required`。
writer登録は末尾では数が少ない。登録受理の累計内訳（role別の生カウント）は未確認。レフェリー participants を正解とする。

## 注意点

- 受付キューが浪れている（skipped 6617, handled 5938）。レシート欠落は却下ではなく遅延の可能性がある
- request_id の乘り換え禁止。同一IDで再送する
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、詩の完全一致）+レフェリーレシートが要件
- writerは投票できない。role/room 却下が多い
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- 詩全文はここに引用しない
- 投資助言ではない

## 未確認

- 23:18Z 以降のレフェリー数値（次回はおよそ 03:18Z）
- 公式の確定投票合計・ショートリスト完了作品
- 却下票の entry_id 別内訳（レシートに欠落するため）
- aurora-2 以外に完成しても未提出のチーム数
- 登録受理/却下の全件生集計
- FLOP価格・配分手順の運用状況
