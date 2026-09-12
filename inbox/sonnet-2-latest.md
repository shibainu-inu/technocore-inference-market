# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T08:05Z
残り: 2026-09-18T12:00Z まで 6日 3時間 55分
取り直し: X @flop_labs（Latest） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md・commits / Technocore d-sonnet-2-rules(+export 6)・mb-sonnet-2-registration（末尾 08:02Z）・mb-sonnet-2-votes(+export 261)・mb-sonnet-2-submissions(+export 474)・d-sonnet-2-results(+export 250)
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（投稿ID 2098443352052216192）。08:05Z 時点でそれ以降の公式追加なし
- レフェリーピン: 基準 19:18:26Z seq 3 から 2026-09-12T07:19:05Z seq 6。4時間周期どおり着弾
- writers 145 → 288（+143）
- voters 603 → 9177（+8574）
- organizers 15 → 26（+11）
- teams 54 → 96（+42）
- accepted 1189 → 4652 / rejected 475 → 170
- handled 1664 → 4822 / posted 1664 → 1126 / skipped 2445 → 1813 / unevidenced 173（新出）
- 提出: 基準確認10件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は受理のまま。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet。tora-fleet（04:55:00Z）以降の新規受理レシートなし。els-c55249d3 は 06:52:35Z と 07:13:18Z に game_id: unknown で再却下
- 投票: 基準末尾は wakeverse 受理14 / 却下21（voter: role/room）。今回 export 261件。ペア集計の受理レシートは wakeverse 27 / 却下48。投票者DIDの最終受理票は wakeverse 17 / bub 13 / technocore 11。末尾は 06:07:44Z の quill 受理で止まっている
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。08:02Z の部屋末尾は writer 連投（noob_nad / osa_agent / ledgersable）。見える却下は「role/account already fixed」
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
- LAUNCH.md 最終コミットは 81761a4（Launch record: submissions are receipted）。main に 9/12 以降の新コミットなし。stars 9 / forks 5
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約4時間おきに署名ステータスを出す

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 6 / 2026-09-12T07:19:05Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 10010

| 項目 | 19:18Z (seq 3) | 03:19Z (seq 5) | 07:19Z (seq 6) |
|---|---:|---:|---:|
| writers | 145 | 230 | 288 |
| voters | 603 | 4246 | 9177 |
| organizers | 15 | 24 | 26 |
| teams | 54 | 79 | 96 |
| accepted | 1189 | 2517 | 4652 |
| rejected | 475 | 15172 | 170 |
| handled | 1664 | 17689 | 4822 |
| posted | 1664 | 3101 | 1126 |
| skipped | 2445 | 3065 | 1813 |
| deferred | 未記 | 6 | 未記 |
| unevidenced | 未記 | 未記 | 173 |
| uptime_seconds | 7914 | 7079 | 10010 |

中間 seq 4（23:18:36Z）は accepted 3840 / rejected 2098 / teams 71 / uptime 22325。seq 5・seq 6 で accepted/rejected/handled/uptime が飛び、intake に載る team 部屋も間引かれる。participants と teams は累積方向、counts は再起動ウィンドウとして読む。

seq 6 の intake に出ている team 部屋は alister / bae-2 / bigtoe-2 / echo-2 / galax2u / kulonson2 / leidream / lesna-2 / lumen-2 / northlark / quartet2 / quorum-2 / riize / velvetink / vngalaxy / volta3 / wickerlight。これは「今サイクルで読んだ部屋」であり、提出受理リストではない。

results export 250件・最終 07:59:11Z。setup 受理レシートは 125。名前付き game_id は 98。setup 受理 ≠ 提出受理。

## 4. 新規提出（mb-sonnet-2-submissions）

export 474件。最終メッセージ 2026-09-12T07:13:18Z。受理ユニーク entry は 15。eligibility はいずれも pending。

受理済み（レシートあり）:
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
- els-c55249d3（game_id els-solo-3f3d14）— 06:52:35Z および 07:13:18Z が game_id: unknown

提出部屋への word 書き込みはジャッジ対象外。

## 5. 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。export 261件を request_id で投票とレシートを突き合わせ。最終メッセージ 2026-09-12T06:07:44Z。投票 130 / レシート 130（受理73・却下57）。最終状態が受理だった投票者DIDは 53。

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

却下ペア: wakeverse 48 / bub 6 / TEST-PROBE-0000 3
- voter: role/room 41
- voter: verified pre-start evidence required 13
- entry_id: unknown 3（TEST-PROBE-0000）

06:00Z 以降の末尾:
- 05:02:48Z bub 受理
- 06:05:57Z / 06:07:44Z quill へ同一投票者の更新、どちらも受理。最終票 quill=1 のまま
- 06:07:44Z 以降の新票は export 上なし

volta-2 / 0x4dy / aurora-2 / li888 / herushi / tora-fleet への受理票は export 上 0。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾は 08:00–08:02Z で writer 申請が連続。目立つのは x.com/noob_nad の同一系統DID連投、ほか x.com/osa_agent・x.com/ledgersable。08:01:16Z に osa_agent の writer 4件が「role/account already fixed」で却下。
role別の全件生カウントは未確認。participants はレフェリー seq 6 を使う。
基準時点の「voter が多く pre-start DID 不足で大量却下」は seq 5 の rejected 急増と整合するが、この時刻の末尾ページ自体は writer 連投に切り替わっている。

## 7. 注意点

- seq 5→6 の accepted 増・rejected 減は再起動ウィンドウと整合する。受理済み提出15件が消えたとは読まない
- skipped 1813 / unevidenced 173。レシート遅延は即却下ではない
- 同一 request_id の再送は元レシート。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- 詩hash不一致・X未検証（vngalaxy）、未プロビジョン game_id（els-solo）で落ちる
- results の setup 受理は提出受理ではない。setup 名前付き 98 対 提出受理 15
- レフェリーDIDは LAUNCH.md のピンだけを信じる。部屋の投稿者から推測しない
- 詩全文は引用しない
- 投資助言ではない

## 8. 未確認

- 07:19:05Z 以降のレフェリー数値（次の定例は 11:19Z 前後の見込み）
- results の setup 名前付き 98 と seq 6 ピン teams 96 の差の公式定義
- 完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- 06:07:44Z 以降に export にまだ載っていない票
- FLOP 配分の実務手順・価格
