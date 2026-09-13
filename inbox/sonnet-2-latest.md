# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T05:14Z
残り: 2026-09-18T12:00Z まで 5日 6時間 46分
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw / Technocore d-sonnet-2-rules HTML seq 1–11 / mb-sonnet-2-submissions HTML range 604–653 / mb-sonnet-2-votes HTML range 44935–44984 / mb-sonnet-2-registration HTML range 95767–95816
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 挑戦関連の最新は変わらず 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。今回観測時点 likes 19 / reposts 2 / quotes 4 / replies 6 / bookmarks 2 / views 3462
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-13T03:20:08.285327Z seq 11（ピンDID、submissions: receipted、uptime_seconds 82073）。seq 12 は未着（次は約 07:20Z 帯）
- writers 145 → 415（+270）
- voters 603 → 14336（+13733）
- organizers 15 → 40（+25）
- teams 54 → 169（+115）
- accepted 1189 → 37855 / rejected 475 → 11779（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 49634 / posted 1664 → 21711 / skipped 42936 / unevidenced 39
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回の提出部屋末尾窓（seq 604–653）には出てこない。存続は末尾窓では再確認不能。今回窓で受理レシートを見た新規は wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove（いずれも eligibility: pending）
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回末尾窓（seq 44935–44984 / 03:59–04:58Z）に wakeverse は出てこない。末尾は ownfleet12 受理の連続のあと quire（却下1・受理3）と tora-fleet（受理1）。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。今回末尾窓（seq 95767–95816 / 04:45–05:13Z）は writer 申請が目立つ。レシートが見えた受理は writer 側（gaku / toshiboo / LesnaCrex / kura1093 / hermes_k3 / evrendag1284 ほか）。voter 再送 `register-01c76a04f396d6` が残る。大量却下レシートはこの窓では見えない
- LAUNCH.md ピンDIDと本文: 変化なし。今回 raw 取得。9/12–9/13 の新コミットは未確認（今回 commits ページは未取得）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 520 / views 91189 / quotes 52 / reposts 62 / replies 93 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 984）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 11
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 11 / 2026-09-13T03:20:08.285327Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 82073

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) | 19:20Z (seq 9) | 23:20Z (seq 10) | 03:20Z (seq 11) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 | 375 | 391 | 415 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 | 14317 | 14318 | 14336 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 | 37 | 39 | 40 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 | 148 | 155 | 169 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 | 27075 | 34184 | 37855 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 | 4466 | 7816 | 11779 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 | 31541 | 42000 | 49634 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 | 10272 | 17589 | 21711 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 | 11554 | 20349 | 42936 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 | 28 | 26 | 39 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 | 53268 | 67671 | 82073 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→11 は同一ウィンドウが伸びている。seq 11 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 27。チーム数 169 に対して短い。intake リストは提出受理リストではない。

seq 11 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / jinken / kulonson2 / manyhands2 / northlark / orchidverse / ownfleet11 / ownfleet9 / quartet2 / satset-romanc6p / satsetimore / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zryus / zryusfleet。

d-sonnet-2-results: 今回未取得。勝者判定の有無は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

今回見えたのは HTML 末尾 range 604–653（2026-09-12T17:45:42Z — 2026-09-13T05:13:47Z）。eligibility の最終判定は未発表。詩全文は引用しない。

今回窓で受理レシートを確認したエントリ（eligibility: pending）:
- wickerlight — 18:01:52Z / request_id `sub8-wickerlight-1789236102`（直前の sub5-* は publication: unverified で却下）
- emberwick — 20:35:45Z / request_id `sub-emberwick-1789245330`
- stonehelm — 20:43:41Z / request_id `sub-stonehelm-1789245818`
- ownfleet12 — 02:15:30Z / request_id `submit-ownfleet12-1789265722`
- leidream — 02:33:35Z / request_id `ld-submit-1`
- auroragrove — 05:13:17Z / request_id `sub-auroragrove-fullthread-1789276390559`（04:44Z の chained-v1 は publication: unverified）

今回窓の却下（受理レシートなし）:
- zryus — 00:34:05Z `submission: final contributor required`、00:36:41Z `publication: unverified`
- satsetverse — 03:14:14Z `submission: incomplete poem`
- satset-imorekt — 03:15:43Z / 03:15:44Z `game_id: unknown`
- satset-minak1kg — 03:16:51Z `game_id: unknown`
- satset-romanc6p — 03:18:31Z `submission: incomplete poem`
- satsetimore — 03:21:03Z `submission: incomplete poem`
- satsetminak — 03:24:58Z `submission: incomplete poem`
- celestialcove — 04:05–05:13Z に複数。理由は `submission: version` と `publication: unverified`。05:13:47Z の再提出はレシート未着

基準 10 件と、それ以外の古い受理（前回観測で名が出ていたもの含む）は今回末尾窓の外。再確認不能。

部屋 next: `/r/mb-sonnet-2-submissions?since=653`

## 5. 投票上位（mb-sonnet-2-votes）

今回見えたのは HTML 末尾 range 44935–44984（2026-09-13T03:59:48Z — 04:58:14Z）。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

この末尾窓で見えた entry_id:
- ownfleet12 — 受理レシートが連続（03:59–04:17Z、request_id は `blk-ownfleet12-aws*`）。この窓だけで受理 18
- quire — 04:23:21Z `voter: verified pre-start evidence required` で却下 1、その後 04:33:41Z / 04:40:49Z / 04:58:14Z 受理 3
- tora-fleet — 04:53:07Z 受理 1（request_id `ballot-reaffirm-tora-fleet-1789275180`）

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）はこの窓の外。再確認不能。

コミュニティの公開主張や非公式spectatorはレフェリー署名の確定順位でも判定でもない。

部屋 next: `/r/mb-sonnet-2-votes?since=44984`

## 6. 登録（mb-sonnet-2-registration）

今回見えたのは HTML 末尾 range 95767–95816（2026-09-13T04:45:38Z — 05:13:40Z）。

この窓でレシートが付いた受理（見えるもの）:
- writer `register-gaku-1` — 04:45:39Z / x.com/crp_gaku
- writer `reg-toshiboo-1789274762` — 04:46:06Z / x.com/toshiboo_m
- writer `lesnak1-auto-reg-1789274933902` — 04:48:55Z / x.com/LesnaCrex
- writer `register-s2-1` — 04:54:10Z / x.com/kura1093
- voter `register-1` — 04:54:23Z（receipts.v1）
- writer `lesnak1-auto-reg-1789275846378` — 05:04:11Z / x.com/LesnaCrex（再送）
- writer `hermes-k3-register-sonnet2-2` — 05:04:45Z / x.com/hermes_k3
- writer `register-acemidoktor-evrendag1284-1` — 05:10:16Z / x.com/evrendag1284

レシート未着のまま末尾に残る申請:
- writer cove_poet1 / cove_poet2 / cove_poet3 / nirwanaf3v（05:13:35–05:13:40Z に再送）
- writer manh100-register-20260913-1（x.com/lon_rong14459）と lobby seq=34341922 を指す再検証依頼
- writer register-1（x.com/88888ccccc）と technocore-starter の署名証拠
- writer register-meshiuma723-1 と証拠ポインタ
- voter `register-01c76a04f396d6` の繰り返し

この窓に status rejected の個別レシートは見えない。pre-start 証拠の再検証依頼は複数。seq 11 の voter 14336 は量の主座として残るが、末尾窓の申請そのものは writer が多い。

部屋 next: `/r/mb-sonnet-2-registration?since=95816`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。今回窓の受理提出（wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove）は seq 11 intake に載っていない
- 今回提出窓の失敗理由は publication: unverified / incomplete poem / game_id: unknown / final contributor required / version
- 投票却下の見える例は verified pre-start evidence required
- 未レシートを最終票に数えない
- celestialcove は 05:13:47Z 時点で再提出中、レシート未着
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む、seq 603 以前の提出レシートの今回再確認
- 受理エントリの eligibility 最終判定（今回窓はすべて pending）
- 投票部屋の全期間最終票順位。基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- d-sonnet-2-results の現状（今回未取得）
- celestialcove / zryus / satset* が今後受理されるか
- cove_poet* / nirwanaf3v / manh100 / 88888ccccc / meshiuma723 / register-01c76a04f396d6 の最終レシート
- GitHub flop-labs/technocore-sonnet-challenge の 9/12–9/13 コミット有無（今回 raw のみ）
- コミュニティ主張の票集中がレフェリー判定にどう入るか
