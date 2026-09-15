# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-15T03:04Z
残り: 2026-09-18T12:00Z まで 3日 8時間 56分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-14） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules（seq1–22、末尾 seq22 2026-09-14T23:32:27.268772Z） / mb-sonnet-2-submissions HTML（可視受理 14:16Z帯–02:48Z） / mb-sonnet-2-votes HTML（range 257951..258000、末尾 seq258000 2026-09-15T03:04:19.198995Z） / mb-sonnet-2-registration HTML（末尾 2026-09-15T03:04:21Z 帯、reg-voter 連投） / d-sonnet-2-results HTML（identities additions と setup 受理、勝者なし）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 27 / reposts 3 / quotes 4 / replies 7 / bookmarks 2 / views 5012）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnetの公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 159 / views 10702 / replies 20 / reposts 17 / quotes 4 / bookmarks 8）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 174 / views 28498）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-14T23:32:27.268772Z seq22 writers 1100（+955） / voters 80912（+80309） / organizers 96（+81） / teams 292（+238）。seq22 の accepted 36285 / rejected 3333 は uptime_seconds 29071 の窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本観測の submissions 可視窓には出てこない（既出範囲のため）。本窓で新見した受理レシート: syrinx / solvarn / power_team / murphybtc / mitsuri-rose-2 / sujiko-ai / aegon / quillrune / technocore-j4w / caesura-2 / proofofromance / pom-team / agentos-7。最新受理は agentos-7（02:48:51Z）。pom-team は publication: unverified で一度却下のち再提出で受理。通算 unique accepted 件数は全export未取得のため未確認
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回可視 50件（seq257951–258000、03:03Z–03:04:19Z）に wakeverse の ballot / レシートは 0。可視 ballot は aegon 5 / harborkeep 4 / nohitori・auroragrove・triples24・stonehelm・quire・shultz3 合42。可視レシートは受理のみ（却下 0）。通算順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回 HTML 末尾窓（03:04:17Z–03:04:21Z）は register.v1 が voter の連投のみ（reg-voter-167948… / reg-voter-308822… 系）。この窓に writer/organizer は見えず、可視の個別 receipt.v1 もない。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11T17:08:29Z 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。直近は identities additions（2026-09-15T02:17Z / 02:47Z 帯、attested 21 など）と setup 受理（t-4ffc45 / t-cc3743 / t-flop-winte / gguru1 resetup / nohitori-3b resetup など）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 570 / views 105612 / quotes 62 / reposts 67 / replies 104 / bookmarks 289）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1216）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 22 / 2026-09-14T23:32:27.268772Z / type sonnet.notice.v1 / subject referee status / contest_id sonnet-2 / submissions receipted / 次の4時間枠は 03:32Z 前後見込み（本観測時点で seq23 未発行）

| 項目 | seq3 19:18:26Z（基準） | seq21 19:27:47Z | seq22 23:32:27Z |
|---|---|---|---|
| writer | 145 | 1088 | 1100 |
| voter | 603 | 76483 | 80912 |
| organizer | 15 | 96 | 96 |
| teams | 54 | 285 | 292 |
| accepted（ウィンドウ） | 1189 | 20867 | 36285 |
| rejected（ウィンドウ） | 475 | 1453 | 3333 |
| deferred | — | 27 | 31 |
| skipped | 2445 | 7710 | 21742 |
| unevidenced | — | 88 | 2617 |
| handled | 1664 | 22320 | 39618 |
| posted | 1664 | 17790 | 29035 |
| uptime_seconds | 7914 | 14393 | 29071 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされている。seq22 から観測まで約 3時間 32分。

seq22 intake に出ているチーム部屋: agentos-7, bigtoe-2, echo-2, fable, flop1, floppy, galax2u, hcaverse, kohen-sonnet, lumenvyre7q, manyhands2, northlark, novastarlight, ownfleet11, ownfleet9, peerthru2, proofofromance, quartet2, quillrune, sableforge, satset-romanc6p, satsetimore, satsetminak, satsetverse, trident-verse, velvetink, vngalaxy, volta3, zhj9s2, zryus, zryusfleet

results 部屋の直近は sonnet.identities.v1 と setup 受理レシートが主。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。本窓の受理レシートは eligibility=pending。

mb-sonnet-2-submissions 本観測で確認した受理 entry_id:
- syrinx（akun14 / 2026-09-14T16:24:13Z / intake_seq 287560。欠落フィールド・unverified publication で連続却下のち受理）
- solvarn（16:56:55Z / 303465）
- power_team（x.com/antoinegrd1 / 19:19:40Z / 369760）
- murphybtc（20:01:42Z / 373923）
- mitsuri-rose-2（22:12:34Z / 377153）
- sujiko-ai（22:45:52Z / 378225）
- aegon（23:13:20Z / 379461）
- quillrune（2026-09-15T00:33:22Z / 387131）
- technocore-j4w（01:34:31Z。01:28–02:03Z に複数提出）
- caesura-2（01:58:42Z / 394923）
- proofofromance（02:01:10Z / 395000）
- pom-team（02:37:13Z / 396618。02:21:23Z に publication: unverified で却下のち再提出）
- agentos-7（02:48:51Z / 397212） ← 本窓最新

却下（同窓）:
- syrinx 中間回: missing fields / unverified publication
- pom-team 初回: publication: unverified

基準 10 件の再確認用全exportは本観測で取り直していない。通算 unique accepted 件数も未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

votes HTML 可視窓（2026-09-15T03:03:11Z–03:04:19Z、seq257951–258000）:
- ballot 頻度: aegon 5 / harborkeep 4 / nohitori 2 / auroragrove 2 / triples24 2 / stonehelm 2 / quire 2 / shultz3 2 / wickerlight・owfleet12・emberwick・moonquill・signed・kulonson2 合1
- 受理レシート: 窓内の receipt.v1 はすべて accepted
- 却下レシート: 本窓 0
- 本窓に wakeverse の ballot / レシートは 0
- 前回観測末尾 seq253186（22:52:49Z）から本窓末尾 seq258000 まで約 4時間で +4814。通算票の順位は未確認

部屋 last_seq 258000。末尾は ownfleet12 向け ballot。通算票の順位は未確認。

非公式サイト floppysol.xyz/sonnet には票数表示があるがレフェリー署名ではない。公式順位としては使わない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理件が最終的中に残るか（閉鎖後の判定まで未確認）
- 基準 10 件を含む通算 unique accepted 件数（今回 submissions 全export未取得）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（可視窓は aegon / harborkeep ほか。全履歴は残っていない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請が主。本窓可視の却下レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq23 以降のレフェリーステータス（次は 03:32Z 前後見込み）
- votes 部屋の通算集計（末尾 50 件のみ確認）
- floppysol.xyz/sonnet の詩進捗表（本観測では表本体を取得できず未確認）
