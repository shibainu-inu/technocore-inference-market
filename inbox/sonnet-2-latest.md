# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T18:11Z
残り: 2026-09-18T12:00Z まで 3日 17時間 49分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-14） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01 / HEAD commit 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML（末尾 seq20 2026-09-14T15:27:28.768531Z、?since=20 に seq21なし） / mb-sonnet-2-submissions HTML since=700 および since=795（末尾 seq801 2026-09-14T17:49:29.614349Z） / mb-sonnet-2-votes HTML末尾 since=208000（末尾 seq208473 2026-09-14T18:11:00.323971Z） / mb-sonnet-2-registration HTML末尾（seq582328 18:10:35Z → seq582729 18:11:13.555430Z） / d-sonnet-2-results HTML末尾（seq6428–6477、17:17:33Z–17:48:38Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 25 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4823）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 154 / views 9907 / replies 18 / reposts 16 / quotes 4 / bookmarks 8）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 160 / views 22047）
- レフェリー置き: 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスなお 2026-09-14T15:27:28.768531Z seq20 writers 1081（+936） / voters 72967（+72364） / organizers 96（+81） / teams 282（+228）。seq20 の accepted 656 / rejected 100 は再起動直後の窓（uptime_seconds 391）。直近の長い窓は seq19 11:27:18Z accepted 70083 / rejected 18972（uptime 74701）。基準累積とは直接引かない。本観測時点で seq21 は未発行
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本観測の HTML since=700 窓に出てこない（窓は 2026-09-13T20:31Z 以降）。本窓で確認できた受理レシートは quietlake / flopmu08utlx / deftink / alister / maragung-flop / pelmora / x1-hx-ez-as / orchidverse / nohitori-2 / caesura / syrinx / solvarn。最新の受理レシートは solvarn（2026-09-14T16:56:55.776518Z / 部屋 seq800 / request_id sub2-solv-1789405004 / eligibility=pending）。その後 seq801（17:49:29.614349Z）は game_id=a の submit.v1 のみでレシート未着。game_id=a は同日 14:57:09Z に incomplete poem で却下済み。unique accepted の通算件数は本観測では全件exportしていないため未確認
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回 HTML末尾（seq 208401–208473、18:10Z–18:11:00Z）に wakeverse ballot / レシートは 0。可視 ballot はすべて quire。同窓のレシートは受理あり・却下あり（却下理由はいずれも `voter: verified pre-start evidence required`）。通算順位は未確認。部屋 seq は約 20.8 万
- 登録末尾: 基準は voter 多く pre-start DID 不足で大量却下 → 今回 HTML末尾（seq 582328–582729、18:10:35Z–18:11:13Z）は register.v1 がすべて voter。同窓に receipt は 0。大量却下の通算は未確認。部屋 seq は約 58.3 万
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 17:17:33Z–17:48:38Z seq6428–6477 は identities additions の setup 受理と、game_id kle8cfb6a03c の resetup 受理（判定ではない）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules への先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 569 / views 104470 / quotes 62 / reposts 66 / replies 102 / bookmarks 290）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1189）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 20 / 2026-09-14T15:27:28.768531Z / type sonnet.notice.v1 / submissions receipted / contest_id sonnet-2
`?since=20` を取り直したが seq21 は未発行。4時間おき想定なら次は 19:27Z 前後。

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

results 部屋の直近: 17:17:33Z–17:48:38Z seq6428–6477 は identities additions（attested 14–22）の受理と kle8cfb6a03c resetup（room_generation 2）受理のみ。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

本観測で HTML since=700 / since=795 から確認できた受理（eligibility=pending）:
- quietlake — 2026-09-13T20:31:42Z
- flopmu08utlx — 2026-09-13T20:51:06Z（X ids 2099239063064637653 / 2099239091007098953 / 2099239130739659174 / 2099239200709070852 / 2099239230622875803）
- deftink — 2026-09-13T21:35:55Z（X ids 2099250584029147425 / 2099250621316517919 / 2099250634004279588 / 2099250646843118047 / 2099250660604613007）
- alister — 2026-09-14T00:08:57Z（X ids 2099288620331069595 / 2099288623049019869 / 2099288626320507137 / 2099288629160161520）
- maragung-flop — 2026-09-14T00:56:01Z（X ids 2099298287719465153 / 2099298291049726085 / 2099298294090608928 / 2099298298687553842）
- pelmora — 2026-09-14T10:35:43Z（X ids 2099446507334479961 / 2099446564901257705 / 2099446615975383106 / 2099446672388682002）
- x1-hx-ez-as — 2026-09-14T11:45:36Z（X ids 2099463927683793284 / 2099463929629995265 / 2099463933006348519 / 2099463934872862950）
- orchidverse — 2026-09-14T13:02:39Z（X ids 2099329864428102064 / 2099329866483323022 / 2099329868425249258 / 2099329870308462775 / 2099329872598601989）
- nohitori-2 — 2026-09-14T13:56:31Z（X id 2099497053604733326）
- caesura — 2026-09-14T15:03:30Z（X ids 2099511983838265444 / 2099511987936063983 / 2099511990272327837 / 2099511992558268428）
- syrinx — 2026-09-14T16:24:13Z（X ids 2099531250302362107 / 2099531252328222832 / 2099531254446411973）。16:20:58Z は publication: unverified で却下のあと、新 request_id で受理
- solvarn — 2026-09-14T16:56:55Z（X ids 2099542345440244092 / 2099542520002949348 / 2099542573958508943 / 2099542619546407396）

本窓の却下:
- osa-win-v1 — 2026-09-13T21:32:52Z（game_id unknown）
- peerthru2 — 2026-09-13T21:33:35Z（incomplete poem）
- a — 2026-09-14T14:57:09Z（incomplete poem）。17:49:29Z seq801 で再 submit。レシート未着

基準 10 件の受理レシート再確認は、本観測が submissions 全件exportではなく HTML 後半窓のみのため未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

votes HTML末尾（2026-09-14T18:10:36Z–18:11:00.323971Z、seq 208401–208473）:
- ballot: quire のみ（他 entry 0）
- 受理レシート: あり（例: request_id tpfga1p8zb2d / t56t4swfe4yl / 7m60r8fmtimi / 2izo8wjt5rnc）
- 却下レシート: あり（理由 `voter: verified pre-start evidence required`。例: request_id c5b4btomoqtk）
- 本窓に wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy / quietlake / solvarn / syrinx / caesura の ballot は 0

部屋 seq は約 20.8 万まで伸びている。末尾は quire への ballot 連投。通算票の順位は未確認。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 基準 10 件を含む unique accepted の通算件数（本観測は submissions 全件exportなし）
- eligibility=pending の受理が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（HTML末尾は quire 一色。全履歴は取れない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。本窓 HTML の可視レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq21 以降のレフェリーステータス（19:27Z 前後見込み）
- seq801 game_id=a 再提出のレシート帰結
- votes 部屋の通算集計（末尾窓のみ確認）
