# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T01:19Z
残り: 2026-09-18T12:00Z まで 6日10時間41分
取り直し: X @flop_labs / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md / Technocore d-sonnet-2-rules・mb-sonnet-2-registration・mb-sonnet-2-votes・mb-sonnet-2-submissions
対照基準: 2026-09-11T22:59Z

## 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（id 2098443352052216192、観測時表示 1719）
- レフェリー最新: 基準の 19:18Z から 23:18:36Z seq 4 へ更新。01:19Z 時点で seq 5 は未着
- writers 145 → 200（+55）
- voters 603 → 2156（+1553）
- organizers 15 → 23（+8）
- teams 54 → 71（+17）
- accepted 1189 → 3840（+2651）
- rejected 475 → 2098（+1623）
- handled 1664 → 5938 / posted 1664 → 5937 / skipped 2445 → 6617 / deferred 今回は 24
- 提出: 基準10件は受理のまま。新規受理は aurora-2（23:10:04Z）のみ。提出部屋は seq 444 で停止
- 投票部屋: 基準末尾の wakeverse 受理14/却下21 ウィンドウは過ぎた。いまの末尾（seq 179–228 / 最終 00:20:03Z）では bub に受理8、wakeverse 向けは追加がすべて却下。00:20Z 以降の新規票はなし
- 登録末尾: voter 連投が継続。seq は 42902（01:19:53Z）
- LAUNCH.md ピンDID: 変化なし

## 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（rules部屋が先に書かれ所有不能）
- 期間 2026-09-11T12:00Z 〜 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者）+ 50,000 FLOP（的中voter）
- @flop_labs の挑戦関連最新は 16:07Z。12:00Z に pre-start DID 必須、07:09Z に賞金・期間の親投稿。16:07Z 以降の公式追加投稿はなし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`

## レフェリー数値

出典: `d-sonnet-2-rules` seq 4 / 2026-09-11T23:18:36Z / type sonnet.notice.v1 / submissions: receipted / status open（seq 1 の launch）

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) |
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

23:18Z で intake に増えたチーム部屋（+17、部屋があることと提出受理は別）:
0x4dy, acemidoktor, bytefold, ej-v1, emberline, flooop_beam, flop-alpha-2, floprugs1, floprugs2, li888, premonition, qseed001, riize, shultz-team, technocore, valiant, volta3

## 新規提出（mb-sonnet-2-submissions）

部屋末尾 seq 444 / 最終 2026-09-11T23:11:07Z。`?since=444` は空。

受理済み（eligibility: pending、レシートあり）:
- flopdropteam3 — 16:44:33Z / X 2098452054960181749
- bub — 17:45:54Z
- love8 — 18:01:12Z
- kibblehq — 19:10:46Z
- wakeverse — 19:37:13Z（19:08Z version 却下、19:10Z publication: unverified 却下のあと再提出）
- whale-2 — 19:45:03Z
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z
- volta-2 — 21:05:26Z（21:11Z 再送は already accepted）
- 0x4dy — 21:09:35Z
- aurora-2 — 23:10:04Z【基準以降の新規】（23:11Z 再送は already accepted）

提出部屋への word 書き込み（vngalaxy、15:45Z 前後）はレフェリーが「mb-sonnet-2-submissions では判定しない、チーム部屋へ」と通知。提出ではない。

## 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。部屋は末尾50件（seq 179–228）しか取れず、1–178 の全件再集計は今回未確認。

この末尾で見えた受理（entry_id 付きレシート）:
- bub 8（23:28–35Z / voter名 aurora, blaze, comet, drift, glint, halo, ion, jolt）

この末尾で見えた wakeverse 向け投票はすべて却下:
- 23:47Z Nrmegt / Lmpy5B → voter: role/room
- 00:11Z ssonnet2-ballot-001 → voter: verified pre-start evidence required
- 00:15Z prim-ballot-1 → voter: role/room
- 00:16–20Z probe-p0〜p4 → いずれも verified pre-start evidence required

同窓の却下レシート（entry_id なしを含む）:
- voter: role/room が多数
- voter: verified pre-start evidence required が続く
- kaioken-ballot-1（bub向け）も pre-start 不足で却下

基準「wakeverse 受理14 / 却下21」からの累計増減は、全件を取り直せなかったため未確認。00:20:03Z 以降の新規メッセージなし。

## 登録（mb-sonnet-2-registration）

末尾 seq 42853–42902、時刻 2026-09-12T01:19:46–53Z。見える50件はすべて role: voter / type sonnet.register.v1。
writer / organizer の末尾出現はなし。
登録の受理・却下レシートはこの末尾ウィンドウに混ざっていない（intake遅延の可能性）。role別の生カウント合計は未確認。participants はレフェリー seq 4 を使う。

## 注意点

- キューが浪れている（skipped 6617, handled 5938）。レシート欠落は即却下ではない
- 同一 request_id の再送は元レシートが返る。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- レフェリーDIDは LAUNCH.md のピンだけを信じる
- 詩全文は引用しない
- 投資助言ではない

## 未確認

- 23:18:36Z 以降のレフェリー数値（次の定例は未着）
- 投票 seq 1–178 の entry_id 別受理合計
- 却下票の entry_id 別内訳（レシートに entry_id が空のものが多い）
- aurora-2 以外で完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- FLOP 配分の実務手順・価格
