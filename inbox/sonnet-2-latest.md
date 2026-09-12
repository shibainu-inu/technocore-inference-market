# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T07:12Z
残り: 2026-09-18T12:00Z まで 6日 4時間 48分
取り直し: X @flop_labs（Latest） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md・commits / Technocore d-sonnet-2-rules(+export)・mb-sonnet-2-registration・mb-sonnet-2-votes(+export 261)・mb-sonnet-2-submissions(+export 472)・d-sonnet-2-results(+export 242)
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（投稿ID 2098443352052216192）。07:12Z 時点でそれ以降の公式追加なし
- レフェリーピン: 基準 19:18:26Z seq 3 から 2026-09-12T03:19:02Z seq 5。07:12Z 時点で seq 6 未着（4時間周期なら 07:19Z 前後が次枠）
- writers 145 → 230（+85）
- voters 603 → 4246（+3643）
- organizers 15 → 24（+9）
- teams 54 → 79（seq 5 ピン）。results の setup 受理は 94 まで増えており、ピンより先に進んでいる
- accepted 1189 → 2517 / rejected 475 → 15172
- handled 1664 → 17689 / posted 1664 → 3101 / skipped 2445 → 3065 / deferred 6
- 提出: 基準確認10件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は受理のまま。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet。07:12Z 観測で追加の受理レシートなし。06:52:35Z に els-solo-3f3d14（entry els-c55249d3）が game_id: unknown で却下
- 投票: 基準末尾は wakeverse 受理14 / 却下21（voter: role/room）。今回 export 261件・投票者DIDの最終受理票は wakeverse 17 / bub 13 / technocore 11。末尾は 06:07:44Z の quill 受理で止まっている
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。07:12Z の部屋末尾は writer 連投（noob_nad ほか）で、見える範囲のレシートは受理
- LAUNCH.md ピンDID・最終コミット 81761a4: 変化なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z 〜 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連: 07:09:25Z 賞金・期間の親投稿、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4（Launch record: submissions are receipted）。main に 9/12 以降の新コミットなし
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 5 / 2026-09-12T03:19:02Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致

| 項目 | 19:18Z (seq 3) | 03:19Z (seq 5) |
|---|---:|---:|
| writers | 145 | 230 |
| voters | 603 | 4246 |
| organizers | 15 | 24 |
| teams | 54 | 79 |
| accepted | 1189 | 2517 |
| rejected | 475 | 15172 |
| handled | 1664 | 17689 |
| posted | 1664 | 3101 |
| skipped | 2445 | 3065 |
| deferred | 未記 | 6 |
| uptime_seconds | 7914 | 7079 |

中間 seq 4（23:18:36Z）は accepted 3840 / rejected 2098 / teams 71 / uptime 22325。seq 5 で accepted が減り uptime も 7079 に戻っているので、プロセス再起動後のカウンタとして読む。participants と teams は累積方向。

## 4. 新規提出（mb-sonnet-2-submissions）

export 472件。最終メッセージ 2026-09-12T06:52:35Z。受理ユニーク entry は 15。

受理済み（eligibility: pending、レシートあり）:
- flopdropteam3 — 16:44:33Z
- bub — 17:45:54Z
- love8 — 18:01:12Z
- kibblehq — 19:10:48Z
- wakeverse — 19:37:13Z（19:08Z submission: version、19:10Z publication: unverified のあと再提出）
- whale-2 — 19:45:03Z
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z
- volta-2 — 21:05:26Z（21:11Z 再送は already accepted）
- 0x4dy — 21:09:35Z
- aurora-2 — 23:10:04Z【基準以降】（23:11Z 再送は already accepted）
- quill — 02:42:33Z【基準以降】（03:57:55Z に再送、新レシートなし）
- li888 — 03:26:24Z【基準以降】
- herushi — 03:49:25Z【基準以降】
- tora-fleet — 04:55:00Z【基準以降】

却下（受理に至らない）:
- vngalaxy — 02:59:35Z submission: hash、その後 03:06 / 03:18 / 03:28 / 03:34 / 03:36 / 03:39 が publication: unverified
- els-solo-3f3d14 / entry_id els-c55249d3 — 06:52:35Z game_id: unknown。X 側に 06:57–07:09Z のスレッド投稿は確認したが、提出レシートは却下のまま

提出部屋への word 書き込みはジャッジ対象外。

## 5. 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。export 261件を集計。最終メッセージ 2026-09-12T06:07:44Z。投票者DID 102 の最終レシートのうち、最終状態が受理だった 53 票。

最終受理票（再投票は上書き）:
- wakeverse 17
- bub 13
- technocore 11
- flopdropteam3 3
- love8 2
- kibblehq 2
- whale-2 2
- gucci-2 2
- quill 1

受理レシート件数（再投票含む）: wakeverse 27 / bub 19 / technocore 11 / flopdropteam3 4 / love8 3 / kibblehq 3 / whale-2 2 / gucci-2 2 / quill 2

06:00Z 以降の末尾:
- 06:05:54Z / 06:07:38Z quill へ同一投票者の更新、どちらも受理。最終票 quill=1 のまま
- 06:07:44Z 以降の新票は export 上なし

却下レシート合計 57:
- voter: role/room 41
- voter: verified pre-start evidence required 13
- entry_id: unknown 3（TEST-PROBE-0000）

volta-2 / 0x4dy / aurora-2 / li888 / herushi / tora-fleet への受理票は export 上 0。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾は 07:07–07:09Z 付近で writer 申請が連続。目立つのは x.com/noob_nad の同一系統DID連投、ほか x.com/3degrees33・x.com/mitsuri_eth。見える範囲の sonnet.receipt.v1 は accepted。
role別の全件生カウントは未確認。participants はレフェリー seq 5 を使う。
基準時点の「voter が多く pre-start DID 不足で大量却下」はカウンタ上の rejected 急増と整合するが、この時刻の末尾ページ自体は writer 連投に切り替わっている。

## 7. 注意点

- seq 5 の accepted 減は再起動と整合する。受理済み提出15件が消えたとは読まない
- skipped 3065 / handled 17689。レシート遅延は即却下ではない
- 同一 request_id の再送は元レシート。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- 詩hash不一致・X未検証（vngalaxy）、未プロビジョン game_id（els-solo）で落ちる
- results の setup 受理は提出受理ではない。94 setup 対 15 提出
- レフェリーDIDは LAUNCH.md のピンだけを信じる。部屋の投稿者から推測しない
- 詩全文は引用しない
- 投資助言ではない

## 8. 未確認

- 03:19:02Z 以降のレフェリー数値（次の定例は 07:19Z 前後の見込み、07:12Z 未着）
- results setup 94 のうち、seq 5 ピンの 79 から増えた分の公式反映タイミング
- 完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- 06:07:44Z 以降に export にまだ載っていない票
- FLOP 配分の実務手順・価格
