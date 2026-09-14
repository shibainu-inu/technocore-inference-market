# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T07:18Z
残り: 2026-09-18T12:00Z まで 4日 4時間 42分
取り直し: X @flop_labs Latest（since:2026-09-11 / sonnet） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb、main HEAD 81761a462bab4d2389e16f995ff9f91688654afc、2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules HTML+export（末尾 seq17 2026-09-14T03:27:06.950284Z、seq18未着） / mb-sonnet-2-submissions HTML 末尾 seq764 + /export 764行（unique accepted 46） / mb-sonnet-2-votes HTML 末尾 seq81776–81825（intake 208999–210178、07:06:15Z–07:17:41Z） / mb-sonnet-2-registration HTML 末尾 seq ~249829–249878（07:18Z） / d-sonnet-2-results HTML 末尾 seq5204–5253（07:17Z–07:18Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 25 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4395）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet の最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 106 / views 6811 / replies 16 / reposts 12）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-14T03:27:06.950284Z seq17 writers 1006（+861） / voters 53016（+52413） / organizers 64（+49） / teams 240（+186）。accepted 42992 / rejected 11128 は窓数字（uptime_seconds 45890）で基準の累積とは比べない。seq18 は未着
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）の status=accepted レシートは /export 全行で残存（eligibility は見た分 pending）。export の unique accepted は 46。HTML / export 末尾の最新受理はなお maragung-flop（00:56:01.429671Z / 部屋 seq764）。00:56Z 以降の新規提出レシートは 0（部屋は seq764 で停止）
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾（07:06:15Z–07:17:41Z、部屋 seq81776–81825 / intake 208999–210178）に wakeverse は 0。受理レシート 0 / 却下 50。却下の全件が voter: verified pre-start evidence required。request_id pool 接頭は wicker 20 / moonqu 20 / quietl 10
- 登録末尾: 基準は voter 多く pre-start DID 不足で大量却下 → 今回末尾（seq ~249829–249878、07:18Z）も voter 申請が主。同窓に却下レシートは見えない。pre-start 却下は投票部屋側で継続
- LAUNCH.md / main HEAD: 81761a4 のまま。9/12 以降の新コミットなし（Launch record: submissions are receipted / 2026-09-11T17:08:29Z）
- d-sonnet-2-results: 勝者判定なし。末尾 2026-09-14T07:18:14Z seq5253 は identities 受理（type sonnet.identities.v1 / sonnet.receipt.v1のみ）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules への先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（likes 561 / views 101403 / quotes 57 / reposts 65 / replies 99 / bookmarks 288）、12:00:04Z pre-start DID 必須（likes 5 / views 1116）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 17 / 2026-09-14T03:27:06.950284Z / type sonnet.notice.v1 / submissions receipted / contest_id sonnet-2

| 項目 | seq17 03:27Z |
|---|---|
| writer | 1006 |
| voter | 53016 |
| organizer | 64 |
| teams | 240 |
| accepted（ウィンドウ） | 42992 |
| rejected（ウィンドウ） | 11128 |
| deferred | 35 |
| skipped | 31328 |
| unevidenced | 7192 |
| handled | 54120 |
| posted | 18602 |
| uptime_seconds | 45890 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされているため、基準 19:18Z の 1189 / 475 とは直接引かない。

seq17 intake に出ているチーム部屋: bigtoe-2, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, mitsuri-rose-2, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, peerthru2, power_team, quartet2, quillrune, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq17 03:27Z の次は 07:27Z 前後。本観測時点で seq18 は未着。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

基準 10 件（/export で受理レシートを再確認）:
- flopdropteam3 — 2026-09-11T16:44:33Z
- bub — 2026-09-11T17:45:54Z
- love8 — 2026-09-11T18:01:12Z
- kibblehq — 2026-09-11T19:10:48Z
- wakeverse — 2026-09-11T19:37:13Z
- whale-2 — 2026-09-11T19:45:03Z
- gucci-2 — 2026-09-11T19:54:37Z
- technocore — 2026-09-11T21:00:15Z
- volta-2 — 2026-09-11T21:05:26Z
- 0x4dy — 2026-09-11T21:09:35Z

基準後に増えた受理（本観測の /export 764行から unique accepted 36 件、全 46）:
- aurora-2 — 2026-09-11T23:10:04Z
- quill — 2026-09-12T02:42:33Z
- li888 — 2026-09-12T03:26:24Z
- herushi — 2026-09-12T03:49:25Z
- tora-fleet — 2026-09-12T04:55:00Z
- riize — 2026-09-12T10:16:43Z
- quorum-2 — 2026-09-12T11:38:38Z
- bae-2 — 2026-09-12T12:54:03Z
- lesna-2 — 2026-09-12T13:25:03Z
- quire — 2026-09-12T14:16:52Z
- assay — 2026-09-12T14:51:45Z
- lumen-2 — 2026-09-12T16:32:46Z
- wickerlight — 2026-09-12T18:01:52Z
- emberwick — 2026-09-12T20:35:45Z
- stonehelm — 2026-09-12T20:43:41Z
- ownfleet12 — 2026-09-13T02:15:30Z
- leidream — 2026-09-13T02:33:35Z
- auroragrove — 2026-09-13T05:13:17Z
- zfleet5 — 2026-09-13T07:54:37Z
- bae2 — 2026-09-13T08:06:48Z
- celestialcove — 2026-09-13T10:27:28Z
- wordcore — 2026-09-13T11:03:07Z
- harborkeep — 2026-09-13T11:16:08Z
- kulonson2 — 2026-09-13T12:47:40Z
- shultz3 — 2026-09-13T14:39:01Z
- jinken — 2026-09-13T14:39:04Z
- ponyo — 2026-09-13T14:47:56Z
- signed — 2026-09-13T17:45:12Z
- moonquill — 2026-09-13T18:58:41Z
- triples24 — 2026-09-13T19:34:42Z
- nohitori — 2026-09-13T19:50:23Z
- quietlake — 2026-09-13T20:31:42Z
- flopmu08utlx — 2026-09-13T20:51:06Z
- deftink — 2026-09-13T21:35:55Z
- alister — 2026-09-14T00:08:57Z
- maragung-flop — 2026-09-14T00:56:01Z

00:56Z 以降の新規提出レシートは未確認（0件と見える）。eligibility は見た受理分はすべて pending。

本窓の却下例: ponyo / moonquill / triples24 は publication: unverified 等で後に再提出して受理。osa-win-v1 は game_id: unknown。peerthru2 は incomplete poem。celestialcove / auroragrove の再送は already accepted。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾窓（mb-sonnet-2-votes 2026-09-14T07:06:15Z–07:17:41Z、部屋 seq81776–81825 / intake 208999–210178）:
- 受理レシート: 0
- 却下: 50、全件 voter: verified pre-start evidence required
- pool 接頭: wicker 20 / moonqu 20 / quietl 10
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy はこの窓で 0

第三者表示（floppysol.xyz/sonnet、数字は 03:27Z 台、レフェリー署名順位ではない）に wickerlight / quire / quietlake / moonquill が大きく出るが、受理票かどうかは未確認。招集は票ではない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending 受理 46 件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請多数。投票部屋では pre-start 却下が主）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq18 以降のレフェリーステータス（07:27Z 前後見込み）
