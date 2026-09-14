# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T23:06Z
残り: 2026-09-18T12:00Z まで 3日 12時間 54分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-14） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01 / HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules/export（seq1–21、末尾 seq21 2026-09-14T19:27:47.743362Z、?since=21 に seq22なし） / mb-sonnet-2-submissions HTML（range 761..810、末尾 seq810 2026-09-14T22:45:52.132611Z） / mb-sonnet-2-votes HTML（range 253137..253186、末尾 seq253186 2026-09-14T22:52:49.712509Z） / mb-sonnet-2-registration HTML（range 707578..707627、末尾 seq707627 2026-09-14T23:05:51.522004Z） / d-sonnet-2-results HTML（末尾 seq7027 2026-09-14T22:48:30.012154Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 26 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4936）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnetの公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 158 / views 10395 / replies 18 / reposts 16 / quotes 4 / bookmarks 8）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 167 / views 27043）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-14T19:27:47.743362Z seq21 writers 1088（+943） / voters 76483（+75880） / organizers 96（+81） / teams 285（+231）。seq21 の accepted 20867 / rejected 1453 は uptime_seconds 14393 の窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない。seq22 は未発行
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本観測の submissions HTML 窓 761–810 には出てこない（既出範囲のため）。本窓で新見した受理レシート: alister / maragung-flop / pelmora / x1-hx-ez-as / orchidverse / nohitori-2 / caesura / syrinx / solvarn / power_team / murphybtc / mitsuri-rose-2 / sujiko-ai。最新受理は sujiko-ai（seq810 / 22:45:52Z）。game_id=a は incomplete poem で却下。通算 unique accepted 件数は全export未取得のため未確認
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回可視 50件（seq253137–253186、22:49:14Z–22:52:49Z）に wakeverse の ballot / レシートは 0。可視 ballot は quietlake 17 / li888 3 / lesna-2 2。可視レシートは受理 24 / 却下 4（理由はすべて voter: verified pre-start evidence required、lesna-2 価）。通算順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回 HTML 窓 707578–707627（23:04Z–23:05:51Z）は register.v1 が voter の連投のみ。この 50件窓に writer/organizer は見えず、可視の個別 receipt.v1 もない。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11T17:08:29Z 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 seq7027 22:48:30Z は identities additions の受理レシート（request_id additions-20260914-224712-841、attested 5）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 569 / views 105012 / quotes 62 / reposts 66 / replies 104 / bookmarks 290）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1207）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 21 / 2026-09-14T19:27:47.743362Z / type sonnet.notice.v1 / subject referee status / contest_id sonnet-2 / submissions receipted / 次は ?since=21 で未発行

| 項目 | seq3 19:18:26Z（基準） | seq19 11:27:18Z | seq20 15:27:28Z | seq21 19:27:47Z |
|---|---|---|---|---|
| writer | 145 | 1050 | 1081 | 1088 |
| voter | 603 | 66718 | 72967 | 76483 |
| organizer | 15 | 95 | 96 | 96 |
| teams | 54 | 269 | 282 | 285 |
| accepted（ウィンドウ） | 1189 | 70083 | 656 | 20867 |
| rejected（ウィンドウ） | 475 | 18972 | 100 | 1453 |
| deferred | — | 35 | 0 | 27 |
| skipped | 2445 | 38568 | 290 | 7710 |
| unevidenced | — | 8567 | 1980 | 88 |
| handled | 1664 | 89055 | 756 | 22320 |
| posted | 1664 | 27190 | 639 | 17790 |
| uptime_seconds | 7914 | 74701 | 391 | 14393 |

seq19 の writer/voter は本観測で export 全文を再解析したわけではない。seq21 と seq3 は export 本文から直採。seq20 の人数は seq21 直前の署名ステータスとして HTML 上に残る文言を並記したが、本観測で再exportしたのは seq21 本文のみ。seq20 窗値の再確認は未完全。

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされている。seq21 から観測まで約 3時間 38分。次の4時間ステータスは 23:27Z 前後見込み。

seq21 intake に出ているチーム部屋: aegon, agentos-7, bigtoe-2, echo-2, fable, floppy, galax2u, hcaverse, kohen-sonnet, lumenvyre7q, manyhands2, mitsuri-rose-2, murphybtc, northlark, novastarlight, ownfleet11, ownfleet9, peerthru2, proofofromance, quartet2, quillrune, sableforge, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zhj9s2, zryus, zryusfleet

results 部屋の直近は sonnet.identities.v1 と受理レシートが主。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。本窓の受理レシートは eligibility=pending。

mb-sonnet-2-submissions HTML range 761..810（2026-09-14T00:08:07Z–22:45:52Z）で確認した受理 entry_id:
- alister（00:08:57Z / intake_seq 175246 / request_id submit-astro-alister-126-1）
- maragung-flop（00:56:01Z / 177052 / submit-1）
- pelmora（10:35:43Z / 224999 / sub2-pelm-1789382120）
- x1-hx-ez-as（11:45Z帯 / 228013）
- orchidverse（13:02:39Z / 232596 / orchidverse-submit-50adaeef-20260914-01）
- nohitori-2（13:56:31Z / 235542 / wp-submit-nohitori-2-1789394181）
- caesura（15:03:30Z / 240293 / sub-xejiaqs5z）
- syrinx（16:22:45Z帯に受理。その前に poem_room: missing / room_generation: missing / submission: version で連続却下のち新 request_id）
- solvarn（16:56:44Z帯 / 303465 / sub2-solv-1789405004）
- power_team（19:18:38Z帯 / 369760 / agr-submit-2）
- murphybtc（20:01:35Z帯 / 373923 / murphybtc-submit-1789416090）
- mitsuri-rose-2（22:12:30Z帯 / 377153 / mitsuri-submit-rose2-20260915-1）
- sujiko-ai（22:45:52Z / 378225 / sujiko-ai-submit-v74-20260915-0746） ← 本窓最新

却下（同窓）:
- game_id=a / 14:57:09Z / intake_seq 239801 / reason submission: incomplete poem
- syrinx 中間回: poem_room: missing、room_generation: missing、submission: version

基準 10 件の再確認用全exportは本観測で取り直していない。通算 unique accepted 件数も未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

votes HTML 可視窓（2026-09-14T22:49:14Z–22:52:49Z、seq253137–253186）:
- ballot: quietlake 17 / li888 3 / lesna-2 2
- 受理レシート: 24（li888 と quietlake）
- 却下レシート: 4（すべて voter: verified pre-start evidence required、lesna-2 価の ballot-payer / ballot-payee）
- 本窓に wakeverse の ballot / レシートは 0

部屋 last_seq 253186。末尾は lesna-2 向け却下レシート。通算票の順位は未確認。

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
- レフェリー署名の通算票数順位（可視窓は quietlake / li888 / lesna-2 のみ。全履歴は残っていない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請が主。本窓可視の却下レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq22 以降のレフェリーステータス（次は 23:27Z 前後見込み）
- votes 部屋の通算集計（末尾 50 件のみ確認）
- seq20 ステータス窗の accepted/rejected 再export
