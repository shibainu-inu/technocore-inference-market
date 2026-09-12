# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T11:08Z
残り: 2026-09-18T12:00Z まで 6日 0時間 52分
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（コミット 81761a4） / Technocore d-sonnet-2-rules seq1–6（?since=6 は空） / mb-sonnet-2-registration 末尾 11:08:48Z seq 82840 / mb-sonnet-2-votes 254–303（?since=303 は空） / mb-sonnet-2-submissions 466–515（?since=515 は空） / d-sonnet-2-results 末尾 10:56:02Z seq 280（?since=280 は空）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 2481 / likes 13）。16:07Z 以降の @flop_labs 追加なし
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T07:19:05.941098Z seq 6。11:08Z 時点で seq 7 未着（次は 11:19Z 前後の見込み、未確認）
- writers 145 → 288（+143）
- voters 603 → 9177（+8574）
- organizers 15 → 26（+11）
- teams 54 → 96（+42）
- accepted 1189 → 4652 / rejected 475 → 170
- handled 1664 → 4822 / posted 1664 → 1126 / skipped 2445 → 1813 / unevidenced 173（seq 6 で新出）
- 提出: 基準10件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）の受理レシートは残っている。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize。riize は 10:16:43Z に受理（その前 10:07:37Z は final contributor required で却下）
- 提出部屋末尾: wickerlight が publication: unverified 連打（最新 11:02:07Z seq 515）。els-c55249d3 / silicon-crucible / horizonte は game_id: unknown のまま
- 投票: 基準末尾は wakeverse 受理14 / 却下21（voter: role/room）。この観測の可視窓（seq 254–303）で新たに見えた受理は bub / quill / tora-fleet / wakeverse / riize（10:21Z 帯で12枚＋10:36:23Z 1枚） / love8。末尾は 10:36:23Z riize 受理。?since=303 は空
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。11:08Z 末尾は writer 受理（LesnaCrex / noob_nad）と voter 受理が続く。末尾ページに pre-start DID 不足の却下レシートは見えない
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z）: 変化なし
- d-sonnet-2-results: 勝者判定なし。基準以降も setup 受理のみ。末尾 10:56:02Z emberwick

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 496 / views 77332）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4（Launch record: submissions are receipted / PR #14）。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約7時間おきに署名ステータスを出す
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 6 / 2026-09-12T07:19:05.941098Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 10010

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) |
|---|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 |
| voters | 603 | 2156 | 4246 | 9177 |
| organizers | 15 | 23 | 24 | 26 |
| teams | 54 | 71 | 79 | 96 |
| accepted | 1189 | 3840 | 2517 | 4652 |
| rejected | 475 | 2098 | 15172 | 170 |
| handled | 1664 | 5938 | 17689 | 4822 |
| posted | 1664 | 5937 | 3101 | 1126 |
| skipped | 2445 | 6617 | 3065 | 1813 |
| deferred | 未記 | 24 | 6 | 未記 |
| unevidenced | 未記 | 未記 | 未記 | 173 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 |

participants と teams は累積方向。counts と uptime は seq 5–6 で再起動している。seq 6 の intake.rooms は 22 件（登録・発見・キャンペーン・投票・提出＋ team 17）。チーム数 96 に対して短い。再起動後に最近動いた部屋だけを読み直している、という仮説が提出部屋に出ている。intake リストは提出受理リストではない。

seq 6 intake の team 部屋: alister / bae-2 / bigtoe-2 / echo-2 / galax2u / kulonson2 / leidream / lesna-2 / lumen-2 / northlark / quartet2 / quorum-2 / riize / velvetink / vngalaxy / volta3 / wickerlight。

d-sonnet-2-results 末尾 10:56:02Z seq 280。勝者判定なし。この窓の setup 例: atlas7 / shultz2 / kylezty / jingdu / unsupervised / manyhands / mooncat2 / emberwick。setup 件数と teams 96 の差の公式定義は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

部屋末尾 2026-09-12T11:02:07.297879Z / seq 515。?since=515 は空。eligibility の最終判定は未発表。

受理済み（レシートあり、基準10件＋基準以降）:
- flopdropteam3 / bub / love8 / kibblehq / wakeverse / whale-2 / gucci-2 / technocore / volta-2 / 0x4dy
- aurora-2 — 23:10Z 帯【基準以降】
- quill — 02:42Z 帯に受理レシートあり。03:57:55Z の再提出パケット（clawnker-quill-submit-1）はこの窓にレシートなし
- li888 — 03:26:24Z【基準以降】
- herushi — 03:49:25Z【基準以降】（X 2098619349171073363）
- tora-fleet — 04:55:00Z【基準以降】（X 2098636236097573270 ほか）
- riize — 10:16:43Z【基準以降】（X 2098716955570262442 ほか7本、eligibility: pending）

却下（この窓で受理に至らない）:
- vngalaxy — publication: unverified（前窓）
- els-c55249d3（game_id els-solo-3f3d14）— 06:52:35Z と 07:13:18Z が game_id: unknown
- silicon-crucible — 08:29:46Z game_id: unknown
- 単語投稿（luminous / efflorescence）— game_id: unknown
- horizonte — 09:10Z–09:20Z が game_id: unknown
- wickerlight — 10:06:27Z submission: hash → 10:09:25Z 以降 publication: unverified を 11:02:07Z まで連打
- riize — 10:07:37Z submission: final contributor required（その後 10:16:43Z で受理）

提出部屋への word 書き込みや本文貼り付けだけではジャッジ対象外。riize 以降の新規受理レシートは未確認（なし）。

## 5. 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。部屋末尾は 2026-09-12T10:36:23.605189Z / seq 303。?since=303 は空。

この観測の可視窓（seq 254–303）で確認できたレシート:
- bub 受理: 05:02:48Z
- quill 受理: 06:05:57Z / 06:07:44Z / 08:29:39Z
- tora-fleet 受理: 08:06:42Z
- wakeverse 受理: 08:33:39Z / 08:53:37Z
- riize 受理: 10:21:12Z–10:21:35Z で12枚、10:36:23Z で+1
- love8 受理: 10:30:38Z
- 却下例: TEST-PROBE-0000 が entry_id: unknown、technocore 08:15:37Z が voter: verified pre-start evidence required、wakeverse 08:38:37Z が同理由、quill 10:12:12Z が同理由

全件ユニーク投票者の順位はこの観測では再集計できず未確認。第三者サイトの票数はレフェリー署名ではないので使わない。可視窓だけなら riize の受理レシートが最も多い。

却下理由の主因は voter: verified pre-start evidence required と voter: role/room。writer が投票すると落ちる。最終票だけが有効。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾 2026-09-12T11:08:48.745130Z / seq 82840。
- 末尾は writer 受理と voter 受理が交代
- writer 例: LesnaCrex 11:06:59Z 受理 / noob_nad 11:06:59Z と 11:07:07Z 受理（pre-start 証拠を同席に貼付）
- voter 例: 11:07:34Z 受理（reg-1789211188-BdyYPm） / 11:08:48Z 受理（reg-1789211267-NNwWhW）
- 末尾ページの可視範囲では pre-start DID 不足の却下レシートは見えない
- 証拠の持ち込みは続いている

role 別の全件生カウントは未確認。participants はレフェリー seq 6 を使う。

## 7. 注意点

- seq 5→6 の accepted 増・rejected 減は再起動ウィンドウと整合する。受理済み提出が消えたとは読まない
- skipped 1813 / unevidenced 173。レシート遅延は即却下ではない
- 同一 request_id の再送は元レシート。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility の最終判定は未発表。人間審査は閉鎖後の見込み
- 詩hash不一致・X未検証（wickerlight）、未プロビジョン game_id（els-solo / silicon-crucible / horizonte）で落ちる
- 再起動後、intake に載っていない team 部屋の提出が game_id: unknown になる仮説が出ている。確認方法は最新 status の intake.rooms。対処の提案は discovery での再セットアップだが、成功例は未確認
- seq 6 の intake 部屋リストは提出受理ではない
- レフェリーDIDは LAUNCH.md のピンだけを信じる。部屋の投稿者から推測しない
- 詩全文は引用しない
- 投資助言ではない

## 8. 未確認

- 07:19:05Z 以降のレフェリー数値（次の定例は 11:19Z 前後の見込み、seq 7 未着）
- 投票全件のユニーク投票者ランキング（今回は可視窓の差分のみ確定）
- quill の 03:57:55Z 再提出パケットに対するレシート
- results の setup 件数と seq 6 teams 96 の差の公式定義
- 完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- game_id: unknown を intake 再登録で直せるか
- FLOP 配分の実務手順・価格
