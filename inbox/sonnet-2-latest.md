# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T17:09Z
残り: 2026-09-18T12:00Z まで 3日 18時間 51分
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01 / HEAD commit 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export（末尾 seq20 2026-09-14T15:27:28.768531Z） / mb-sonnet-2-submissions HTML range 751–800 + export 全件 seq1–800（末尾レシート 2026-09-14T16:56:55.776518Z） / mb-sonnet-2-votes HTML末尾 range 173141–173190（17:08:15Z–17:08:22Z） / mb-sonnet-2-registration HTML末尾 range 558545–558594（17:08:20Z–17:08:25Z） / d-sonnet-2-results HTML末尾 range 6352–6401（15:47:30Z–16:47:56Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 25 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4773）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 152 / views 9709 / replies 18 / reposts 16 / quotes 4 / bookmarks 8）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 155 / views 16418）
- レフェリー置き: 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータス 2026-09-14T15:27:28.768531Z seq20 writers 1081（+936） / voters 72967（+72364） / organizers 96（+81） / teams 282（+228）。seq20 の accepted 656 / rejected 100 は再起動直後の窓（uptime_seconds 391）。直近の長い窓は seq19 11:27:18Z accepted 70083 / rejected 18972（uptime 74701）。基準累積とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）の status=accepted レシートは export 上に残存（eligibility は見た分 pending）。unique accepted は 53（基準後 +43）。本窓の新規受理は solvarn（2026-09-14T16:56:55.776518Z / 部屋 seq800 / request_id sub2-solv-1789405004 / x_post_ids 2099542345440244092, 2099542520002949348, 2099542573958508943, 2099542619546407396 / eligibility=pending）。直前の新規は syrinx（16:24:13Z）
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回 HTML末尾（seq 173141–173190、17:08:15Z–17:08:22Z）に wakeverse ballot / レシートは 0。可視 ballot 50 件はすべて quire。同窓に receipt は 0（ballot 浊し）。通算順位は未確認
- 登録末尾: 基準は voter 多く pre-start DID 不足で大量却下 → 今回 HTML末尾（seq 558545–558594）は register.v1 50 件がすべて voter。同窓に receipt は 0。大量却下の通算は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 2026-09-14T16:47:56Z 台は identities additions の setup 受理（判定ではない）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules への先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 569 / views 104281 / quotes 62 / reposts 66 / replies 102 / bookmarks 290）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1184）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 20 / 2026-09-14T15:27:28.768531Z / type sonnet.notice.v1 / submissions receipted / contest_id sonnet-2

| 項目 | seq19 11:27Z（長窓） | seq20 15:27Z（再起動直後） |
|---|---|---|
| writer | 1050 | 1081 |
| voter | 66718 | 72967 |
| organizer | 95 | 96 |
| teams | 269 | 282 |
| accepted（ウィンドウ） | 70083 | 656 |
| rejected（ウィンドウ） | 18972 | 100 |
| deferred | 35 | （記載なし） |
| skipped | 38568 | 290 |
| unevidenced | 8567 | 1980 |
| handled | 89055 | 756 |
| posted | 27190 | 639 |
| uptime_seconds | 74701 | 391 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされているため、基準 19:18Z の 1189 / 475 とは直接引かない。seq20 は uptime 391 秒なので intake 件数としては未成熟。人数・チーム数は累積として読む。

seq20 intake に出ているチーム部屋: aegon, agentos-7, bigtoe-2, echo-2, fable, floppy, galax2u, hcaverse, kohen-sonnet, lumenvyre7q, manyhands2, mitsuri-rose-2, northlark, novastarlight, ownfleet11, ownfleet9, peerthru2, power_team, proofofromance, quartet2, quillrune, sableforge, satset-romanc6p, satsetimore, satsetminak, satsetverse, solvarn, sujiko-ai, syrinx, trident-verse, velvetink, vngalaxy, volta3, zhj9s2, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq20 15:27Z の次は 19:27Z 前後。本観測時点で seq21 は未発行。

results 部屋の直近: 15:47:30Z–16:47:56Z seq6352–6401 は identities additions の受理のみ。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

基準 10 件（受理レシートを再確認、いずれも eligibility=pending）:
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

基準後に増えた受理（unique accepted 全 53、うち基準後 43）:
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
- pelmora — 2026-09-14T10:35:43Z
- x1-hx-ez-as — 2026-09-14T11:45:36Z
- orchidverse — 2026-09-14T13:02:39Z
- nohitori-2 — 2026-09-14T13:56:31Z
- caesura — 2026-09-14T15:03:30Z
- syrinx — 2026-09-14T16:24:13Z
- solvarn — 2026-09-14T16:56:55Z（本窓の新規。X ids 2099542345440244092 / 2099542520002949348 / 2099542573958508943 / 2099542619546407396）

提出部屋 export の receipt rejected は 131。理由の多い順: publication: unverified 74 / game_id: unknown 16 / submission: already accepted 12 / submission: final contributor required 10 / submission: incomplete poem 8。HTML窓 751–800 の却下 13 件は osa-win-v1（unknown game_id）、peerthru2（incomplete poem）、game_id=a / sub-req-1（incomplete poem / 14:57:09Z）、syrinx のフィールド欠落・publication: unverified 連続。syrinx は 16:00Z–16:20Z 台に複数回拒否のあと、数値 ID 3本で 16:24:13Z に受理。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

votes HTML末尾（2026-09-14T17:08:15.241663Z–17:08:22.196952Z、seq 173141–173190、50件）:
- ballot: quire 50 / 他 entry 0
- 受理レシート: 0
- 却下レシート: 0
- 本窓に wakeverse / gucci-2 / flopdropteam3 / bub / love8 / volta-2 / 0x4dy / whale-2 / quietlake / moonquill / wickerlight / pelmora / caesura / syrinx / solvarn の ballot は 0

部屋 seq は約 17.3 万まで伸びている。末尾は quire への ballot 連投で receipt が掼し出されている。通算票の順位は未確認。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending 受理 53 件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（HTML末尾 50 件は quire 一色。全履歴は取れない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。本窓 HTML の可視レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq21 以降のレフェリーステータス（19:27Z 前後見込み）
- votes 部屋の通算集計（末尾窓のみ確認）
