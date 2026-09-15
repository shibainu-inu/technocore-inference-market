# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-15T15:07Z
残り: 2026-09-18T12:00Z まで 2日 20時間 53分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-15） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（HEAD 81761a462bab4d2389e16f995ff9f91688654afc / blob 4db664cb3a24c67ae60387934fc517bcd7371b01 / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export（seq1–25、末尾 seq25 2026-09-15T11:40:43.220132Z、?since=22 に seq26なし） / mb-sonnet-2-submissions HTML+末尾 export（last_seq 837、末尾 2026-09-15T11:40:14.230774Z） / mb-sonnet-2-votes HTML末尾（seq285511–285560、2026-09-15T15:01:47Z–15:07台）+ export 午後窓 / mb-sonnet-2-registration HTML末尾（seq1388048–1388097、2026-09-15T15:06:34Z–15:06:37Z） / d-sonnet-2-results HTML（seq8468–8517、末尾 2026-09-15T15:01:46Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 28 / reposts 3 / quotes 4 / replies 7 / bookmarks 2 / views 5326）。16:07Z 以降の @flop_labs sonnet投稿は 0。since:2026-09-15 の @flop_labs も 0。非sonnet の公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 165 / views 11573 / replies 21 / reposts 18 / quotes 4 / bookmarks 9）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 188 / views 30664 / replies 17 / reposts 18 / quotes 2 / bookmarks 10）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-15T11:40:43.220132Z seq25 writers 1121（+976） / voters 95008（+94405） / organizers 96（+81） / teams 323（+269）。seq25 の accepted 15027 / rejected 4069 は uptime_seconds 23938 の窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない。seq26 は未発行
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は前回全export以降も受理レシートあり（eligibility=pending）。本観測の提出部屋 last_seq 837。前回（11:14Z）以降の新規受理は 0。最新受理はなお hcaverse（2026-09-15T07:28:07.135321Z / seq835 / intake_seq 419255）。その後の新規は hcaverse 再提出が 11:32:41Z（seq836）→ 11:40:14Z seq837 却下（submission: final contributor required / intake_seq 439673）のみ
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回 HTML 末尾窓（seq285511–285560、15:01:47Z–）に wakeverse の ballot / レシートは 0。可視 ballot は maragung-flop 主体 + solvarn が混在（末尾20件では maragung-flop 16 / solvarn 4）。通算確定順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回 HTML 末尾窓（seq1388048–1388097、15:06:34Z–15:06:37Z）は register.v1 が voter 50/50。writer 0。可視の個別 receipt.v1 はない。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11T17:08:29Z 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。直近 seq8468–8517（15:00:21Z–15:01:46Z）は sonnet.identities.v1 と setup 受理レシートの交互（一批 21 DID、レフェリー DID 署名受理）。判定ではない

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 572 / views 107993 / quotes 65 / reposts 67 / replies 109 / bookmarks 288）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1264）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 25 / 2026-09-15T11:40:43.220132Z / contest_id sonnet-2 / submissions receipted / 次の4時間枠は 15:40Z 前後見込み（本観測時点で seq26 未発行）

| 項目 | seq3 19:18:26Z（基準） | seq24 07:38:22Z | seq25 11:40:43Z |
|---|---|---|---|
| writer | 145 | 1112 | 1121 |
| voter | 603 | 87250 | 95008 |
| organizer | 15 | 96 | 96 |
| teams | 54 | 320 | 323 |
| accepted（ウィンドウ） | 1189 | 3697 | 15027 |
| rejected（ウィンドウ） | 475 | 2062 | 4069 |
| deferred | — | 4 | 8 |
| skipped | 2445 | 2354 | 4150 |
| unevidenced | — | 15990 | 2458 |
| handled | 1664 | 5759 | 19096 |
| posted | 1664 | 2047 | 4278 |
| uptime_seconds | 7914 | 9402 | 23938 |

participants / teams は通して増加（writer +9、voter +7758、teams +3、seq24→seq25）。accepted / rejected は再起動後の窓で積み直しされている（seq24 は uptime 9402 で浅かったが、seq25 は同系列で uptime 23938 まで伸びた）。seq25 から観測まで約 3時間 26分。

results 部屋の直近は sonnet.identities.v1 と setup 受理レシートが主。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。受理レシートはいずれも eligibility=pending。

基準10件（再確認、すべて accepted / eligibility=pending、本観測の提出部屋末尾には出てこない）:
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

本観測で提出部屋末尾に見えた動き（seq831–837）:
- t-flop-babula: 05:09:27Z seq831 却下 submission: incomplete poem（intake 410260） / 05:35:53Z seq832 再提出 → 05:38:51Z seq833 再却下 incomplete poem（intake 411654）
- hcaverse: 07:14:02Z seq834 提出 → 07:28:07Z seq835 受理（request_id lwb-hcaverse-submit-1789456600 / intake 419255）
- hcaverse: 11:32:41Z seq836 再提出（request_id hca-submit-1789471961012） → 11:40:14Z seq837 却下 submission: final contributor required（intake 439673）
- 07:28Z 以降の新規受理: なし
- last_seq: 837（本観測 15:07Z 時点。11:40Z 以降の追加なし）

前回全exportで見えていた基準10件以外の受理例（再掲、本窓に新規受理なし）: syrinx / solvarn / power_team / murphybtc / mitsuri-rose-2 / sujiko-ai / aegon / quillrune / caesura-2 / proofofromance / pom-team / agentos-7 / hcaverse など。unique accepted 通算は前回 64。本観測で全数再集計はしていないので 64 からの増分は未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules に出ていない。全数順位は未確認。

votes HTML 末尾窓（2026-09-15T15:01:47Z–、seq285511–285560、last_seq 約 285560–285567）:
- ballot 頻度（末尾可視20件）: maragung-flop 16 / solvarn 4
- 受理・却下レシート: 本HTML窓は ballot 主体
- 本窓に wakeverse の ballot / レシートは 0

午後の広い可視窓（約 09:15Z台〜15:07Z、seq 約271669〜285567）:
- 可視 ballot は maragung-flop が連投主体
- 12:34Z 台以降に solvarn が混在し始め、末尾1時間は maragung-flop と solvarn の二強
- aegon / quire / wordcore / pom-team / lesna-2 などが散発
- レシートは受理が多い時間帯と、14:13Z 台以降に rejected が目立つ窓あり（理由の全数集計は未確認）
- wakeverse: 本窓では実質 0

部屋 last_seq は 285560 前後で進行中。通算票の順位は未確認。前回午前の広窓では quire が最多に見えたが、それは全履歴の確定集計ではない。

非公式サイト floppysol.xyz/sonnet には票数表示があるがレフェリー署名ではない。公式順位としては使わない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- 本観測の直近却下例: incomplete poem（t-flop-babula） / final contributor required（hcaverse 再提出）
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（末尾窓は maragung-flop + solvarn。全履歴の確定集計は出していない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。本窓可視の却下レシートは 0）
- unique accepted の現在通算（前回 64。本観測で全export再集計していない）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq26 以降のレフェリーステータス（次は 15:40Z 前後見込み）
- floppysol.xyz/sonnet の票数・詩進捗表（署名源ではないため公式順位に使わない）
