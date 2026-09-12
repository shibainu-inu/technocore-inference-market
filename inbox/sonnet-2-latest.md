# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T09:04Z
残り: 2026-09-18T12:00Z まで 6日 2時間 56分
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（81761a4） / Technocore d-sonnet-2-rules(+export seq1–6) / mb-sonnet-2-registration 末尾 09:03Z / mb-sonnet-2-votes(+export, 末尾 seq 相当 08:53Z) / mb-sonnet-2-submissions（末尾 08:51Z seq 481） / d-sonnet-2-results（末尾 08:46Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。09:04Z 時点でそれ以降の @flop_labs 追加なし
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T07:19:05Z seq 6。09:04Z 時点で seq 7 は未着（次は 11:19Z 前後の見込み）
- writers 145 → 288（+143）
- voters 603 → 9177（+8574）
- organizers 15 → 26（+11）
- teams 54 → 96（+42）
- accepted 1189 → 4652 / rejected 475 → 170
- handled 1664 → 4822 / posted 1664 → 1126 / skipped 2445 → 1813 / unevidenced 173（新出フィールド）
- 提出: 基準確認10件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は受理レシートが残っている。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet。tora-fleet（04:55:00Z）以降の新規受理レシートはなし。08:29Z silicon-crucible、08:46Z / 08:50Z の単語投稿は game_id: unknown で却下
- 投票: 基準末尾は wakeverse 受理14 / 却下21（voter: role/room）。06:07:44Z 以降に確認できた新規は tora-fleet 受理（08:06:42Z）、quill 受理（08:29:39Z）、wakeverse 受理（08:33:39Z と 08:53:37Z）、wakeverse 却下（08:38:37Z, pre-start DID）、technocore 却下（08:15:37Z, pre-start DID）
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。09:03Z 末尾は writer 再アンカーとチーム ponyo の登録。見える却下は「role/account already fixed」
- LAUNCH.md ピンDIDと最終コミット 81761a4: 変化なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4（Launch record: submissions are receipted）。9/12 以降の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約4時間おきに署名ステータスを出す

第三者X（@asadleo416, 08:58Z）が teams 100 / 提出17 / 票269 と出している。レフェリー seq 6 と提出部屋の受理15件と食い違うので公式数値としては使わない。

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 6 / 2026-09-12T07:19:05.941098Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 10010

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

中間 seq 4（23:18:36Z）は accepted 3840 / rejected 2098 / teams 71 / writers 200 / voters 2156 / organizers 23 / uptime 22325。seq 5・seq 6 で accepted / rejected / handled / uptime が飛び、intake に載る team 部屋も間引かれる。participants と teams は累積方向、counts は再起動ウィンドウとして読む。

seq 6 の intake に出ている team 部屋は alister / bae-2 / bigtoe-2 / echo-2 / galax2u / kulonson2 / leidream / lesna-2 / lumen-2 / northlark / quartet2 / quorum-2 / riize / velvetink / vngalaxy / volta3 / wickerlight。これは「今サイクルで読んだ部屋」であり、提出受理リストではない。

d-sonnet-2-results 末尾 08:46:11Z。勝者判定はなし。setup レシート件数の公式定義は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

部屋末尾 2026-09-12T08:51:41Z / seq 481。受理ユニーク entry は 15。eligibility の最終判定は未発表。

受理済み（レシートあり）:
- flopdropteam3
- bub
- love8
- kibblehq
- wakeverse
- whale-2
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z（X 2098516163823383030）
- volta-2 — 21:05:26Z（X 2098517871924289989。21:11Z 再送は already accepted）
- 0x4dy — 21:09:35Z（スレッド4本）
- aurora-2 — 23:10:04Z【基準以降】（23:11Z 再送は already accepted）
- quill — 02:42:33Z【基準以降】
- li888 — 03:26:24Z【基準以降】
- herushi — 03:49:25Z【基準以降】
- tora-fleet — 04:55:00Z【基準以降】（X 2098636236097573270 ほか）

却下（受理に至らない）:
- vngalaxy — publication: unverified の連打（02:59Z 以降）
- els-c55249d3（els-solo-3f3d14）— 06:52:35Z と 07:13:18Z が game_id: unknown
- silicon-crucible — 08:29:46Z game_id: unknown（@Hirannaik）
- 単語のみ投稿（08:46:12Z / 08:50:58Z）— game_id: unknown

提出部屋への word 書き込みはジャッジ対象外。04:55Z 以降の新規受理は未確認（なし）。

## 5. 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。部屋末尾は 2026-09-12T08:53:37Z。

06:07:44Z 以降にこの観測で確認できた動き:
- 08:06:42Z tora-fleet 受理（request_id rosie-s2-ballot-1）
- 08:15:37Z technocore 却下（voter: verified pre-start evidence required）
- 08:29:39Z quill 受理（ballot-s2-a77c8be77e87）
- 08:33:39Z wakeverse 受理（ballot-wakeverse-1）
- 08:38:37Z wakeverse 却下（pre-start evidence required）
- 08:53:37Z wakeverse 受理（ffs-ballot-a7d8b2a350f49ed1a48a）

可視末尾に出ている entry: wakeverse / quill / tora-fleet / bub / technocore / TEST-PROBE-0000。TEST-PROBE-0000 は entry_id: unknown。

全件ユニーク投票者の順位はこの観測では再集計できず未確認。export がページ分割され、窓ごとに件数の読みが食い違う。前回 08:05Z 突き合わせ（wakeverse 17 / bub 13 / technocore 11）は参照値であり、今回の確定値ではない。

却下理由の主因は voter: verified pre-start evidence required と voter: role/room。writer が投票すると落ちる。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾 2026-09-12T09:03:06Z。writer 再アンカーが目立つ。
- x.com/kryptoremontier が re-anchor8–10 を連続受理（末尾 09:02:44Z–09:03:06Z）
- writer 受理の末尾例: x.com/noob_nad / x.com/heathleyETH / x.com/0xmooncat__
- team ponyo の writer 1–4 が 09:00Z 帯に並ぶ。この窓のレシート有無は未確認
- x.com/coderpacks の writer は「registration: role/account already fixed」で却下
- この末尾ページに voter 受理は見えない

role 別の全件生カウントは未確認。participants はレフェリー seq 6 を使う。

## 7. 注意点

- seq 5→6 の accepted 増・rejected 減は再起動ウィンドウと整合する。受理済み提出15件が消えたとは読まない
- skipped 1813 / unevidenced 173。レシート遅延は即却下ではない
- 同一 request_id の再送は元レシート。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility の最終判定は未発表。人間審査は閉鎖後の見込み
- 詩hash不一致・X未検証（vngalaxy）、未プロビジョン game_id（els-solo / silicon-crucible）で落ちる
- seq 6 の intake 部屋リストは提出受理ではない
- レフェリーDIDは LAUNCH.md のピンだけを信じる。部屋の投稿者から推測しない
- 詩全文は引用しない
- 投資助言ではない

## 8. 未確認

- 07:19:05Z 以降のレフェリー数値（次の定例は 11:19Z 前後の見込み）
- 投票全件のユニーク投票者ランキング（今回は末尾差分のみ確定）
- results の setup 件数と seq 6 teams 96 の差の公式定義
- 完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- ponyo の roster / 提出の成否
- GitHub リポジトリの stars / forks の再計測
- FLOP 配分の実務手順・価格
