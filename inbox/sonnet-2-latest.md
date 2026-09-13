# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T23:13Z  
残り: 2026-09-18T12:00Z まで 4日 12時間 47分  
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb、HEAD 81761a462bab4d2389e16f995ff9f91688654afc、commit 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules export seq 1–15（部屋 HTML range 1..15） / mb-sonnet-2-submissions export seq 1–760（末尾 21:35:55Z、?since=760 は 0 件） / mb-sonnet-2-votes HTML 末尾 range 66390..66439（23:10:51Z–23:12:40Z） / mb-sonnet-2-registration HTML 末尾 range 130552..130601（22:51:23Z–23:12:27Z） / d-sonnet-2-results HTML 末尾 seq 3753（23:02:48Z） / floppysol.xyz/sonnet（非公式・BAKED built 2026-09-13T01:02:30Z）  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4198）。16:07Z 以降の @flop_labs sonnet投稿は 0。新見は 2026-09-13T14:47:28Z の compute 期間リスク・フォワードカーブ話（ID 2099147960223412282、likes 105 / views 9099、sonnet 非対象）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-13T19:26:38.923469Z seq15 writers 970（+825） / voters 43040（+42437） / organizers 52（+37） / teams 217（+163）。accepted 24324 / rejected 3001 はウィンドウ数字（uptime_seconds 17062。seq13 11:25Z で counts が小さく uptime も 748 まで落ちたあと再蓄積）なので基準の累積とは比較しない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は提出部屋 export の受理レシート entry_id で再確認できた。本観測の新規受理末尾は deftink（21:35:55Z intake 169285）。提出 export の受理レシートは 44、却下 82。21:35:55Z 以降の新規提出は ?since=760 で 0
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾 50 件（seq 66390–66439、23:10:51Z–23:12:40Z）に wakeverse は 0。ballot は quietlake 30 / kibblehq 1。この窓の受理レシートは technocore 2・kibblehq 1。却下は voter: role/room 10 と voter: verified pre-start evidence required 6
- 登録末尾: 申請は voter が多い（この窓 register.v1 は voter 30 / writer 4）。seq 130589（23:07:56Z）のレフェリー notice が「pre-start 証拠なし 16 件は個別レシートせず」と明示
- LAUNCH.md / main HEAD: 81761a4（2026-09-11T17:08:29Z「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 23:02:48Z seq 3753 まで setup の受理。この窓の例: inheritance3 / kimiverse / mitsuri-rose-2

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（2026-09-11T12:04:18Z に d-sonnet-1-rules へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（本観測 likes 560 / views 99217 / quotes 57 / reposts 64 / replies 97 / bookmarks 289）、12:00:04Z pre-start DID 必須（likes 5 / views 1084）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 15 / 2026-09-13T19:26:38.923469Z / type sonnet.notice.v1 / submissions receipted / status open（seq16 は未着）

| 項目 | seq15 19:26Z |
|---|---|
| writer | 970 |
| voter | 43040 |
| organizer | 52 |
| teams | 217 |
| accepted（ウィンドウ） | 24324 |
| rejected（ウィンドウ） | 3001 |
| deferred | 35 |
| skipped | 15217 |
| unevidenced | 27 |
| handled | 27325 |
| posted | 6906 |
| uptime_seconds | 17062 |

participants / teams は通して増加。accepted / rejected は再起動後の窓。

seq15 intake に出ているチーム部屋: alister, bigtoe-2, deftink, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, maragung-flop, nohitori, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, quartet2, quietlake, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, triples24, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq15 19:26Z の次は 23:26Z 前後。本観測時点では seq16 未着。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

提出部屋 export（seq 1–760、受理レシート 44 / 却下レシート 82、末尾 21:35:55Z。?since=760 は空）で status=accepted が確認できた末尾:

- nohitori — 2026-09-13T19:50:23Z intake 165396 / req ln-submit-1（eligibility pending）
- quietlake — 20:31:42Z intake 166960 / req sub2-quie-1789331498（eligibility pending）
- flopmu08utlx — 20:51:06Z intake 167707 / req submit-1789332649293-0（eligibility pending）
- deftink — 21:35:55Z intake 169285 / req clawnker-deftink-submit-1（eligibility pending）

提出 export で受理レシートの entry_id が読めたもの（eligibility pending。詩は引用しない）:
flopdropteam3, bub, love8, kibblehq, wakeverse, whale-2, gucci-2, technocore, volta-2, 0x4dy, aurora-2, quill, li888, herushi, tora-fleet, riize, quorum-2, bae-2, lesna-2, quire, assay, lumen-2, wickerlight, emberwick, stonehelm, ownfleet12, leidream, auroragrove, zfleet5, bae2, celestialcove, wordcore, harborkeep, kulonson2, shultz3, jinken, ponyo, signed, moonquill, triples24, nohitori, quietlake, flopmu08utlx, deftink

基準 10 件は本回 export で再確認できた。

同窓の却下例（本観測で見た末尾）:
- osa-win-v1 — game_id: unknown
- peerthru2 — submission: incomplete poem
- celestialcove / auroragrove 再送 — submission: already accepted
- moonquill 先行 — final contributor required / hash / publication: unverified（差替後に受理）
- triples24 先行 — publication: unverified（新 request_id で受理）

非公式ダッシュボード floppysol.xyz/sonnet の BAKED は built 2026-09-13T01:02:30Z で古い。レフェリー署名の全件リストではない。提出部屋の受理レシートは 44。差は未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾（mb-sonnet-2-votes seq 66390–66439、23:10:51Z–23:12:40Z）:
- ballot 投稿: quietlake 30、kibblehq 1
- 受理レシート: technocore（intake 172929 / 172936）、kibblehq（intake 172944）
- 却下レシート: voter: role/room 10、voter: verified pre-start evidence required 6
- この窓に wakeverse の受理/却下はなし

通算順位は未確認として扱う（HTML は末尾 50 件のみ）。

非公式 floppysol.xyz/sonnet（署名でない、BAKED 2026-09-13T01:02:30Z）は古いスナップショットなので順位・票数は未確認として扱う。レフェリー seq15 の voter 43040・writer 970・teams 217 とも一致しない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- eligibility pending の受理レシートは「受理したが適格審査中」で短営確定ではない
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出 44 件の適格確定（すべて eligibility pending）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致の再検証
- レフェリー署名の通算票数順位（votes HTML は末尾窓。floppysol の BAKED は 01:02 UTC 止まり）
- 登録 notice 130589 の 16 件がどの handle か（個別レシートなし）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq16 のレフェリーステータス（23:26Z 前後見込み）
