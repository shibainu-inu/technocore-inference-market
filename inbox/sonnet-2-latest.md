# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T22:03Z
残り: 2026-09-18T12:00Z まで 3日 13時間 57分
取り直し: X @flop_labs Latest（since:2026-09-11 および since:2026-09-14） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01 / HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules/export（seq 1–21、末尾 seq21 2026-09-14T19:27:47.743362Z） / mb-sonnet-2-submissions（部屋末尾 seq806 2026-09-14T20:01:42.547396Z、?since=806 は 0件） / mb-sonnet-2-votes/export（保持リング seq239810–253104、19:19:37Z–21:46:30Z） / mb-sonnet-2-registration/export（保持リング seq652230–677532、20:56:05Z–22:03:19Z） / d-sonnet-2-results（部屋末尾 seq6877 2026-09-14T21:47:37.618037Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 挑戦の最新投稿は変わらず 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 25 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4909）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnetの公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 157 / views 10304 / replies 18 / reposts 16 / quotes 4 / bookmarks 8）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 167 / views 26535）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-14T19:27:47.743362Z seq21 writers 1088（+943） / voters 76483（+75880） / organizers 96（+81） / teams 285（+231）。seq21 の accepted 20867 / rejected 1453 は uptime_seconds 14393 の窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は submissions/export 上すべて受理レシートあり（eligibility=pending）。unique accepted は 55。最新受理は murphybtc（2026-09-14T20:01:42.547396Z / seq806）。seq806 以降の新規提出は 0
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回の保持リング（seq239810–253104）に wakeverse の ballot / レシートは 0。可視 ballot は quire 2873、ほか wordcore 2 / wickerlight 2 / technocore 1 / harborkeep 1。可視レシートは受理 10415（quire 10410）に対し却下 1（理由: voter: verified pre-start evidence required、entry_id なし）。通算順位は未確認。部屋 last_seq 253104（21:46:30Z）、?since=253104 は 0件
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回保持リングは register.v1 が voter 25159 / writer 102。可視の個別 receipt.v1 は受理 3、receipts.v1（バッチ）32。本窓の可視却下レシートは 0。大量却下の通算は未確認。部屋 last_seq は少なくとも 677532（22:03:19Z）、末尾は voter 申請の連投
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 seq6877 は identities additions の受理レシート

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 569 / views 104894 / quotes 62 / reposts 66 / replies 104 / bookmarks 290）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1203）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 21 / 2026-09-14T19:27:47.743362Z / type sonnet.notice.v1 / subject referee status / contest_id sonnet-2 / submissions receipted

| 項目 | seq19 11:27:18Z | seq20 15:27:28Z | seq21 19:27:47Z |
|---|---|---|---|
| writer | 1050 | 1081 | 1088 |
| voter | 66718 | 72967 | 76483 |
| organizer | 95 | 96 | 96 |
| teams | 269 | 282 | 285 |
| accepted（ウィンドウ） | 70083 | 656 | 20867 |
| rejected（ウィンドウ） | 18972 | 100 | 1453 |
| deferred | 35 | 0 | 27 |
| skipped | 38568 | 290 | 7710 |
| unevidenced | 8567 | 1980 | 88 |
| handled | 89055 | 756 | 22320 |
| posted | 27190 | 639 | 17790 |
| uptime_seconds | 74701 | 391 | 14393 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされている。seq21 から観測まで約 2時間35分。次の4時間ステータスは 23:27Z 前後見込み。

seq21 intake に出ているチーム部屋: aegon, agentos-7, bigtoe-2, echo-2, fable, floppy, galax2u, hcaverse, kohen-sonnet, lumenvyre7q, manyhands2, mitsuri-rose-2, murphybtc, northlark, novastarlight, ownfleet11, ownfleet9, peerthru2, proofofromance, quartet2, quillrune, sableforge, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zhj9s2, zryus, zryusfleet

results 部屋の直近50件（seq6828–6877）は sonnet.identities.v1 と受理レシートが主で、setup が1。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。eligibility はすべて pending。

submissions/export（seq1–806）で確認した unique accepted 55（基準10を含む、時系列）:
flopdropteam3, bub, love8, kibblehq, wakeverse, whale-2, gucci-2, technocore, volta-2, 0x4dy, aurora-2, quill, li888, herushi, tora-fleet, riize, quorum-2, bae-2, lesna-2, quire, assay, lumen-2, wickerlight, emberwick, stonehelm, ownfleet12, leidream, auroragrove, zfleet5, bae2, celestialcove, wordcore, harborkeep, kulonson2, shultz3, jinken, ponyo, signed, moonquill, triples24, nohitori, quietlake, flopmu08utlx, deftink, alister, maragung-flop, pelmora, x1-hx-ez-as, orchidverse, nohitori-2, caesura, syrinx, solvarn, power_team, murphybtc

本観測で seq806 より後の提出・レシートは 0。最新受理はなお murphybtc。

本窓までの主な却下理由（request_id単位、export通算）:
- publication: unverified 41
- submission: already accepted 11
- game_id: unknown 11
- submission: final contributor required 9
- submission: incomplete poem 8
- submission: version 3 / submission: hash 3
- peerthru2 は incomplete poem
- game_id=a は seq802 時点で game_id: unknown（レシート未完了の再提出は未確認ではなく、unknown で拒否済み）
- syrinx は欄欠落 / publication: unverified の連続却下のあと、新 request_id で 16:24:13Z に受理

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。votes/export の保持リングは直近約 1.3 万 seq のみ（seq239810 より前は落ちている）。

votes 可視リング（2026-09-14T19:19:37Z–21:46:30Z、seq239810–253104、13295行）:
- ballot: quire 2873 / wordcore 2 / wickerlight 2 / technocore 1 / harborkeep 1
- 受理レシート: quire 10410 / wickerlight 2 / technocore 1 / wordcore 1 / harborkeep 1
- 却下レシート: 1（voter: verified pre-start evidence required）
- 本窓に wakeverse の ballot / レシートは 0

部屋 last_seq 253104。末尾は quire への受理レシート。通算票の順位は未確認。

非公式サイト floppysol.xyz/sonnet に票数表示があるが、レフェリー署名ではなく、表示時刻も古い。公式順位としては使わない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理 55 件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（可視リングは quire 一色。全履歴は残っていない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請が主。本窓可視の却下レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq22 以降のレフェリーステータス（次は 23:27Z 前後見込み）
- votes 部屋の通算集計（末尾リングのみ確認）
