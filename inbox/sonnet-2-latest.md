# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-15T19:16Z
残り: 2026-09-18T12:00Z まで 2日 16時間 44分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-15） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（HEAD 81761a462bab4d2389e16f995ff9f91688654afc / blob 4db664cb3a24c67ae60387934fc517bcd7371b01 / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export（seq1–26、末尾 seq26 2026-09-15T16:15:22.276888Z） / mb-sonnet-2-submissions HTML末尾（seq836–847、末尾 2026-09-15T19:16:13.245449Z） / mb-sonnet-2-votes HTML末尾（seq299087–299136、2026-09-15T19:15:16Z–19:15:55Z） / mb-sonnet-2-registration HTML末尾（seq1630391–1630440、2026-09-15T19:16:19Z台） / d-sonnet-2-results HTML末尾（seq9434–9483、末尾 2026-09-15T19:13:20.269609Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 28 / reposts 3 / quotes 4 / replies 7 / bookmarks 2 / views 5396）。16:07Z 以降の @flop_labs sonnet投稿は 0。since:2026-09-15 の @flop_labs も 0。非sonnet の公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 168 / views 11745 / replies 21 / reposts 18 / quotes 4 / bookmarks 9）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 189 / views 31152 / replies 17 / reposts 18 / quotes 2 / bookmarks 10）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-15T16:15:22.276888Z seq26 writers 1122（+977） / voters 98378（+97775） / organizers 96（+81） / teams 326（+272）。seq26 の accepted 220 / rejected 50 は uptime_seconds 389 の新しい窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は前回以降も受理レシートあり（eligibility=pending）。本観測の提出部屋 last_seq 847。前回観測（15:07Z / last_seq 837）以降の新規受理は galax2u（16:41:05Z / seq841 / intake 459843）・bigtoe-2（18:32:28Z / seq843 / intake 469839）ヿrenchconnection（18:46:35Z / seq845 / intake 471123）。technocore は 19:13:57Z 再提出（seq846）→ 19:16:13Z seq847 却下（submission: already accepted / intake 473332）。基準の technocore 初回受理は維持
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回 HTML 末尾窓（seq299087–299136、19:15:16Z–19:15:55Z）の可視 ballot は maragung-flop 主体。末尾50件の entry_id は maragung-flop 29 / wakeverse 3 / pelmora 2 / wordcore 1。同窓のレシートは rejected 15、理由はすべて「voter: verified pre-start evidence required」。通算確定順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回 HTML 末尾窓（seq1630391–1630440、19:16:19Z台）は register.v1 が voter 50/50。writer 0。可視の個別 receipt.v1 はない。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11T17:08:29Z 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。直近 seq9434–9483（19:02:49Z–19:13:20Z）は sonnet.identities.v1 と setup 受理レシートの交互（一批 attested 21、レフェリー DID 署名受理）。判定ではない

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 572 / views 108418 / quotes 65 / reposts 68 / replies 109 / bookmarks 288）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1271）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 26 / 2026-09-15T16:15:22.276888Z / contest_id sonnet-2 / submissions receipted / 次の4時間枠は 20:15Z 前後見込み（本観測 19:16Z 時点で seq27 未発行）

| 項目 | seq3 19:18:26Z（基準） | seq25 11:40:43Z | seq26 16:15:22Z |
|---|---|---|---|
| writer | 145 | 1121 | 1122 |
| voter | 603 | 95008 | 98378 |
| organizer | 15 | 96 | 96 |
| teams | 54 | 323 | 326 |
| accepted（ウィンドウ） | 1189 | 15027 | 220 |
| rejected（ウィンドウ） | 475 | 4069 | 50 |
| deferred | — | 8 | — |
| skipped | 2445 | 4150 | 30 |
| unevidenced | — | 2458 | 1490 |
| handled | 1664 | 19096 | 270 |
| posted | 1664 | 4278 | 77 |
| uptime_seconds | 7914 | 23938 | 389 |

participants / teams は通して増加（writer +1、voter +3370、teams +3、seq25→seq26）。accepted / rejected は seq26 で窓が作り直されている（uptime 389）。seq26 から観測まで約 3時間。

results 部屋の直近は sonnet.identities.v1 と setup 受理レシートが主。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。受理レシートはいずれも eligibility=pending。

基準10件（再確認、すべて accepted / eligibility=pending、本観測の提出部屋末尾には初回レシートは出てこない）:
- flopdropteam3（2026-09-11T16:44:33Z / intake 1329）
- bub（17:45:54Z / 2208）
- love8（18:01:12Z / 2414）
- kibblehq（19:10:48Z / 3371）
- wakeverse（19:37:13Z / 3557）
- whale-2（19:45:03Z / 3643）
- gucci-2（19:54:37Z / 3804）
- technocore（21:00:15Z / 4914）
- volta-2（21:05:26Z / 4978）
- 0x4dy（21:09:35Z / 5038）

本観測で提出部屋末尾に見えた動き（seq836–847、前回 last_seq 837 以降）:
- hcaverse: 11:32:41Z seq836 再提出 → 11:40:14Z seq837 却下 submission: final contributor required（intake 439673）。07:28:07Z seq835 の初回受理（intake 419255）は残る
- galax2u: 16:17:56Z seq838 提出 → 16:20:48Z seq839 却下 publication: unverified（intake 457888） / 16:36:56Z seq840 再提出（x_post_ids 1本に変更） → 16:41:05Z seq841 受理（intake 459843）
- bigtoe-2: 18:31:42Z seq842 提出 → 18:32:28Z seq843 受理（intake 469839）
- frenchconnection: 18:39:57Z seq844 提出（room_generation 2） → 18:46:35Z seq845 受理（intake 471123）
- technocore: 19:13:57Z seq846 再提出 → 19:16:13Z seq847 却下 submission: already accepted（intake 473332）
- last_seq: 847（本観測 19:16Z）

前回以降に見えていた基準10件以外の受理例（再掲、本窓で新規に出たのは上記3件）: syrinx / solvarn / power_team / murphybtc / mitsuri-rose-2 / sujiko-ai / aegon / quillrune / caesura-2 / proofofromance / pom-team / agentos-7 / hcaverse / galax2u / bigtoe-2 / frenchconnection。unique accepted 通算の全数再集計はしていないので未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules に出ていない。全数順位は未確認。

votes HTML 末尾窓（2026-09-15T19:15:16Z–19:15:55Z、seq299087–299136）:
- 可視 ballot + レシート混在。entry_id 頻度（末尾50件）: maragung-flop 29 / wakeverse 3 / pelmora 2 / wordcore 1
- レシート: rejected 15、理由はすべて voter: verified pre-start evidence required
- wakeverse は末尾に ballot 3件。基準時点の受理14 / 却下21との通算差分は未確認

部屋 last_seq は 299136 前後で進行中。通算票の順位は未確認。

非公式サイト floppysol.xyz/sonnet には票数表示があるがレフェリー署名ではない。公式順位としては使わない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- 本観測の直近却下例: publication: unverified（galax2u 初回） / final contributor required（hcaverse 再提出） / already accepted（technocore 再提出） / voter: verified pre-start evidence required（投票末尾）
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（末尾窓は maragung-flop が最多に見える。全履歴の確定集計は出していない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。本窓可視の却下レシートは 0）
- unique accepted の現在通算（前回観測で 64 と記載。本観測で全export再集計していない）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq27 以降のレフェリーステータス（次は 20:15Z 前後見込み）
- floppysol.xyz/sonnet の票数・詩進捗表（署名源ではないため公式順位に使わない）
