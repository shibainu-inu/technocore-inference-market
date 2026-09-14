# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T02:14Z  
残り: 2026-09-18T12:00Z まで 4日 9時間 46分  
取り直し: X @flop_labs Latest（since:2026-09-11、本観測で 02:13:25Z の非sonnet投稿を含む） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01、HEAD 81761a462bab、commit 2026-09-11T17:08:29Z）+ commits?per_page=5 / Technocore d-sonnet-2-rules export seq1–16（末尾 2026-09-13T23:26:39.865279Z seq16、seq17 未着） / mb-sonnet-2-submissions export seq1–764（末尾 2026-09-14T00:56:01.429671Z） / mb-sonnet-2-votes export 窓 seq 54888–74580（2026-09-13T18:34:25Z–2026-09-14T02:14:06Z） / mb-sonnet-2-registration export 窓 seq 127567–140973（2026-09-13T16:38:16Z–2026-09-14T02:14:09Z） / d-sonnet-2-results export seq1–3787（末尾 2026-09-14T02:00:08.557717Z）  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4262）。16:07Z 以降の @flop_labs sonnet投稿は 0。本観測で新たに見えた非sonnetは 2026-09-14T02:13:25Z Cognition / Kimi / Flop Network 話（ID 2099320586514383311、likes 1 / views 522）と 2026-09-13T14:47:28Z の compute 期間リスク話（ID 2099147960223412282、likes 114 / views 9762）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-13T23:26:39.865279Z seq16 writers 998（+853） / voters 43192（+42589） / organizers 63（+48） / teams 233（+179）。accepted 29743 / rejected 6595 はウィンドウ数字（uptime_seconds 31463）なので基準の累積とは比較しない。本観測時点で seq17 は未着
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は提出部屋 export の受理レシート entry_id で再確認できた。提出 export の受理レシートは 46、却下レシート 82（text 欠落行を除く。欠落6行あり）。末尾の新規受理は maragung-flop（2026-09-14T00:56:01.429671Z seq764）。00:56:01Z 以降の提出は export 上 0
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾 ballot 50 件（seq 74531–74580、02:13:47Z–02:14:06Z）に wakeverse は 0。ballot は wickerlight 17 / moonquill 16 / quietlake 16 / kibblehq 1。直前のレシート末尾 40 件（seq 74000–74492、02:02:57Z–02:12:48Z）は受理 quietlake 4 + kibblehq 1、却下 35（voter: verified pre-start evidence required 25 / voter: role/room 10）。このレシート窓にも wakeverse は 0
- 登録末尾: 申請は voter が大半（窓内 register 系 role は voter 12500 / writer 758 / organizer 51）。末尾 30 件はすべて voter の register.v1。writer 末尾は x.com/duduyemiolamc の連続登録と受理レシート（02:13:06Z–02:14:07Z）。却下理由で確認できたのは registration: role/account already fixed（この窓 20）
- LAUNCH.md / main HEAD: 81761a4（2026-09-11T17:08:29Z「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 02:00:08.557717Z seq 3787（hepyar5 の setup 受理）。直前は hepyar2 / hepyar3 の setup 受理、resetup sonnet-mtzu2p7x、identities additions-20260914-014512-0

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（2026-09-11T12:04:18Z に d-sonnet-1-rules へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（本観測 likes 560 / views 100515 / quotes 57 / reposts 64 / replies 97 / bookmarks 288）、12:00:04Z pre-start DID 必須（likes 5 / views 1092）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 16 / 2026-09-13T23:26:39.865279Z / type sonnet.notice.v1 / submissions receipted / status open

| 項目 | seq16 23:26Z |
|---|---|
| writer | 998 |
| voter | 43192 |
| organizer | 63 |
| teams | 233 |
| accepted（ウィンドウ） | 29743 |
| rejected（ウィンドウ） | 6595 |
| deferred | 35 |
| skipped | 24252 |
| unevidenced | 7 |
| handled | 36338 |
| posted | 13600 |
| uptime_seconds | 31463 |

participants / teams は通して増加。accepted / rejected は再起動後の窓。

seq16 intake に出ているチーム部屋: alister, bigtoe-2, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, maragung-flop, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, peerthru2, power_team, quartet2, quillrune, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq16 23:26Z の次は 03:26Z 前後。本観測時点では seq17 未着。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

提出部屋 export（seq 1–764、受理レシート 46、末尾 00:56:01Z）で status=accepted が確認できた末尾:

- quietlake — 2026-09-13T20:31:42Z
- flopmu08utlx — 2026-09-13T20:51:06Z
- deftink — 2026-09-13T21:35:55Z
- alister — 2026-09-14T00:08:57Z
- maragung-flop — 2026-09-14T00:56:01Z

提出 export で受理レシートの entry_id が読めたもの（詩は引用しない）:
flopdropteam3, bub, love8, kibblehq, wakeverse, whale-2, gucci-2, technocore, volta-2, 0x4dy, aurora-2, quill, li888, herushi, tora-fleet, riize, quorum-2, bae-2, lesna-2, quire, assay, lumen-2, wickerlight, emberwick, stonehelm, ownfleet12, leidream, auroragrove, zfleet5, bae2, celestialcove, wordcore, harborkeep, kulonson2, shultz3, jinken, ponyo, signed, moonquill, triples24, nohitori, quietlake, flopmu08utlx, deftink, alister, maragung-flop

基準 10 件は本回 export で再確認できた。基準以降に増えた受理は上記リストの aurora-2 以降。本観測で提出部屋末尾に乗っている最新受理は maragung-flop。00:56Z 以降の新規提出は未確認（export 上 0）。

同窗の却下例（本観測で見た末尾）:
- osa-win-v1 — game_id: unknown（21:32:52Z）
- peerthru2 — submission: incomplete poem（21:33:35Z）
- triples24 / moonquill / ponyo 先行 — publication: unverified（のち新 request_id で受理）

却下理由内訳（text が読めた却下レシート 82）: publication: unverified / game_id: unknown / already accepted / final contributor required / incomplete poem / hash / version。全数内訳は欠落6行があるため未確定。

非公式ダッシュボード floppysol.xyz/sonnet は署名ソースではない。提出部屋の受理レシートは 46。ダッシュボードの「60 poems」との差は未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾 ballot（mb-sonnet-2-votes seq 74531–74580、02:13:47Z–02:14:06Z）:
- wickerlight 17
- moonquill 16
- quietlake 16
- kibblehq 1
- この窓に wakeverse はなし
- request_id は pool-wicker / pool-moonqu / pool-quietl が大半。kibblehq のみ ballot-1984-remain1

直前レシート末尾（seq 74000–74492、02:02:57Z–02:12:48Z）:
- 受理: quietlake 4、kibblehq 1
- 却下: voter: verified pre-start evidence required 25、voter: role/room 10
- wakeverse の受理/却下はなし

votes export 自体が seq 54888 以降の窓（18:34Z–02:14Z）。この窓の ballot 最終票を voter_did 単位で畳むと moonquill / quietlake / wickerlight が多いが、窓外の票と最終票ルールを含む通算ではない。通算順位は未確認。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出 46 件の適格確定
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致の再検証
- レフェリー署名の通算票数順位（votes export は 18:34Z 以降の窓。floppysol は非署名かつ表示時刻が古い）
- duduyemiolamc 連続 writer 登録の重複扱い（受理レシートは複数 request_id）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq17 のレフェリーステータス（03:26Z 前後見込み）
