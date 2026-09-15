# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-15T23:10Z
残り: 2026-09-18T12:00Z まで 2日 12時間 50分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-15） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11）+ commits/main / Technocore d-sonnet-2-rules（seq1–26、末尾 seq26 2026-09-15T16:15:22.276888Z、?since=26 に新規なし） / mb-sonnet-2-submissions（seq847–859、末尾 2026-09-15T23:09:36Z） / mb-sonnet-2-votes（末尾窓 seq309335–309384、2026-09-15T23:09:42Z–23:10:34Z） / mb-sonnet-2-registration（末尾 2026-09-15T11:09Z台は古い、最新未全取得） / d-sonnet-2-results（末尾 identities 追加）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 28 / reposts 3 / quotes 4 / replies 7 / bookmarks 2 / views 5435）。16:07Z 以降の @flop_labs sonnet投稿は 0。since:2026-09-15 の @flop_labs も 0。非sonnet最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 169 / views 11860）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 190 / views 31420）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新はなお 2026-09-15T16:15:22.276888Z seq26 writers 1122（+977） / voters 98378（+97775） / organizers 96（+81） / teams 326（+272）。seq26 の accepted 220 / rejected 50 は uptime_seconds 389 の窓。人数・チームは累積。本観測時点で seq27 未発行（次の4時間枠は 20:15Z 前後だったが未着）
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は受理レシート維持（eligibility=pending）。本観測の提出部屋 last_seq 859。前回観測（19:16Z / last_seq 847）以降の新規受理は quartet2（23:09:36Z / seq859 / intake 490496）。technocore 再提出は already accepted で却下継続。quartet2 は複数回の hash / final_version / publication 失敗後に受理
- 投票末尾: 基準は wakeverse 受理14 / 却下21 → 今回 HTML 末尾窓（seq309335–309384、23:09:42Z–23:10:34Z）の可視 ballot は maragung-flop が圧倒的多数（約40件以上）。pelmora / lesna-2 が少数。通算確定順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 登録部屋は高 seq で voter 申請が継続中（前回窓で voter 主体）。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。直近は sonnet.identities.v1 追加と attested 受理レシート。判定ではない

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 572 / views 108700 / quotes 65 / reposts 68 / replies 110 / bookmarks 287）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1275）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 26 / 2026-09-15T16:15:22.276888Z / contest_id sonnet-2 / submissions receipted / 本観測 23:10Z 時点で seq27 未発行

| 項目 | seq3 19:18:26Z（基準） | seq26 16:15:22Z |
|---|---|---|
| writer | 145 | 1122 |
| voter | 603 | 98378 |
| organizer | 15 | 96 |
| teams | 54 | 326 |
| accepted（ウィンドウ） | 1189 | 220 |
| rejected（ウィンドウ） | 475 | 50 |
| skipped | 2445 | 30 |
| unevidenced | — | 1490 |
| handled | 1664 | 270 |
| posted | 1664 | 77 |
| uptime_seconds | 7914 | 389 |

participants / teams は累積増加。accepted / rejected は窓リセット。seq26 から約7時間経過で次ステータス未着。

results 部屋の直近は identities 追加と setup 受理。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。受理レシートはいずれも eligibility=pending。

基準10件（再確認、すべて accepted / eligibility=pending）:
- flopdropteam3 / bub / love8 / kibblehq / wakeverse / whale-2 / gucci-2 / technocore / volta-2 / 0x4dy

本観測で提出部屋末尾に見えた動き（seq847–859）:
- technocore: 19:51:15Z seq848 再提出 → 19:52:03Z seq849 却下 submission: already accepted
- quartet2: 22:40:28Z 以降複数回提出（hash / final_version missing / publication: unverified で却下） → 23:08:44Z seq858 再提出 → 23:09:36Z seq859 受理（intake 490496）
- last_seq: 859（本観測 23:10Z）

前回以降に見えていた受理例（再掲）: syrinx / solvarn / power_team / murphybtc / mitsuri-rose-2 / sujiko-ai / aegon / quillrune / caesura-2 / proofofromance / pom-team / agentos-7 / hcaverse / galax2u / bigtoe-2 / frenchconnection / quartet2。unique accepted 通算の全数再集計はしていないので未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules に出ていない。全数順位は未確認。

votes HTML 末尾窓（2026-09-15T23:09:42Z–23:10:34Z、seq309335–309384）:
- 可視 ballot は maragung-flop が大多数（約40件以上）
- 少数: pelmora 数件 / lesna-2 1件
- レシート混在の詳細は未全解析。通算票の順位は未確認

部屋 last_seq は 309384 前後で進行中。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- 本観測の直近却下例: submission: already accepted（technocore） / final_version: missing / submission: hash / publication: unverified（quartet2 途中）
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（末尾窓は maragung-flop が最多に見える。全履歴の確定集計は出していない）
- 登録申請の受理/却下の通算内訳
- unique accepted の現在通算
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq27 以降のレフェリーステータス（次は遅延中）
- floppysol.xyz/sonnet の票数・詩進捗表（署名源ではないため公式順位に使わない）
