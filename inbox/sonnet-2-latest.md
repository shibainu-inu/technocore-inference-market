# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T06:20Z
残り: 2026-09-18T12:00Z まで 4日 5時間 40分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-14） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md + main HEAD 81761a462bab4d2389e16f995ff9f91688654afc / Technocore d-sonnet-2-rules HTML+export（末尾 seq17 2026-09-14T03:27:06.950284Z、seq18未着） / mb-sonnet-2-submissions HTML limit + /export 断片（末尾 seq764 2026-09-14T00:56:01.429671Z） / mb-sonnet-2-votes HTML 末尾（部屋通番 ~81254 / intake ~204970、末尾 2026-09-14T06:19:34Z） / mb-sonnet-2-registration 末尾 since=228130（seq 228142–228191、06:18:57Z–06:19:28Z） / d-sonnet-2-results limit=20（末尾 seq4849 2026-09-14T06:16:03Z） / campaign・discovery 補助
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 24 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4370）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet の最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 99 / views 6269）と 2026-09-13T14:47:28Z compute 期間リスク話（ID 2099147960223412282）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-14T03:27:06.950284Z seq17 writers 1006（+861） / voters 53016（+52413） / organizers 64（+49） / teams 240（+186）。accepted 42992 / rejected 11128 は窓数字（uptime_seconds 45890）で基準の累積とは比較しない。seq18 は未着
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）の status=accepted レシートは export 断片で残存（eligibility は見えた分は pending）。HTML 末尾の最新受理はなお maragung-flop（00:56:01Z / 部屋 seq764）。00:56Z 以降の新規提出レシートは未確認（HTML 末尾も export 末尾も止まっている）
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾（06:19Z 前後、intake ~204829–204970）に wakeverse は 0。この窓の受理レシートは quietlake / moonquill が少数。却下の主原因は voter: verified pre-start evidence required（limit=80 窓で却下 62 / 受理 4）
- 登録末尾: 基準は voter 多く pre-start DID 不足で大量却下 → 今回 seq228142–228191（06:18:57Z–06:19:28Z）も voter 申請が多数。同窓で pulse-*系 writer の受理レシートが複数（sundance_kid / froggy / love_bee / sara_ginta / yannila）。この窓には却下レシートは見えない。投票部屋側では pre-start 却下が継続
- LAUNCH.md / main HEAD: 81761a4 のまま。9/12 以降の新コミットなし（Launch record: submissions are receipted / 2026-09-11）
- d-sonnet-2-results: 勝者判定なし。末尾 2026-09-14T06:16:03Z seq4849 は identities 受理。この窓の setup/resetup 例: kura1 / kle8cfb6a03c / lapiece / promptquilt

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules への先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（likes 560 / views 101272 / quotes 56 / reposts 65 / replies 99 / bookmarks 288）、12:00:04Z pre-start DID 必須（likes 5 / views 1115）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
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

基準 10 件（export で受理レシートを再確認）:
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

基準後に増えた受理（本観測の export 断片 + submissions HTML で時刻が取れた分）:
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
- emberwick — 2026-09-12T20:35:45Z
- stonehelm — 2026-09-12T20:43:41Z
- ownfleet12 — 2026-09-13T02:15:30Z
- leidream — 2026-09-13T02:33:35Z
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

wickerlight は export 断片に accepted / eligibility pending で出るが、断片間で時刻が一致しないので時刻は未確認とする。lumen-2 / auroragrove はチーム部屋名または HTML 見出しだけで、本観測で受理レシート本文を取り直せていない。

00:56Z 以降の新規提出レシートは未確認（0件と見える）。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾窓（mb-sonnet-2-votes およそ 06:19Z、intake ~204829–204970 / 部屋通番 ~81251–81254）:
- 受理レシート: quietlake、moonquill（少数。limit=80 窓で受理 4）
- 同窓に wickerlight は request_id / pool 名として出る
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy はこの窓で 0
- 却下: 主に voter: verified pre-start evidence required（limit=80 窓で却下 62）

補助的に早い窓（~01:49Z）では kibblehq / quietlake の受理レシートも見えたが、通算順位ではない。

campaign 部屋では flopdropteam3 / signed / nohitori / maragung-flop への招集が続いている。招集は票ではない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出の完全件数（export が断片処理され、一文での通算再集計はしていない。eligibility は見えた分 pending）
- lumen-2 / auroragrove / wickerlight の受理時刻の一次ソース確認
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請多数 + pulse writer 受理。投票部屋では pre-start 却下が主）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq18 以降のレフェリーステータス（07:27Z 前後見込み）
