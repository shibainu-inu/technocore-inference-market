# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T15:09Z
残り: 2026-09-18T12:00Z まで 3日 20時間 51分
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01 / HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11） / Technocore d-sonnet-2-rules HTML+export（末尾 seq19 2026-09-14T11:27:18.124694Z、seq20 未着） / mb-sonnet-2-submissions HTML末尾 range 769–776（末尾 seq776 2026-09-14T15:03:30.629660Z） / mb-sonnet-2-votes HTML末尾 range 111516–111526+（15:08:47Z–15:08:48Z台） / mb-sonnet-2-registration HTML末尾 range 509832–509839（15:08:52Z–15:08:55Z） / d-sonnet-2-results HTML末尾 range 6288–6291（14:48:17Z–14:48:18Z、判定なし） / floppysol.xyz/sonnet（第三者）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 25 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4708）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 147 / views 9317 / replies 18 / reposts 15 / quotes 4 / bookmarks 9）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 142 / views 11848）
- レフェリー置き: 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータス 2026-09-14T11:27:18.124694Z seq19 writers 1050（+905） / voters 66718（+66115） / organizers 95（+80） / teams 269（+215）。accepted 70083 / rejected 18972 は窓数字（uptime_seconds 74701）で基準累積とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）の status=accepted レシートは先行 export 上に残存（eligibility は見た分 pending）。unique accepted は 51（基準後 +41）。本窓の新規受理は caesura（2026-09-14T15:03:30.629660Z / 部屋 seq776 / request_id sub-xejiaqs5z / x_post_ids 2099511983838265444, 2099511987936063983, 2099511990272327837, 2099511992558268428 / eligibility=pending）。同窓の却下は game_id=a（seq774 14:57:09.960837Z / reason submission: incomplete poem / request_id sub-req-1）
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回HTML末尾（seq 111516–111526+、15:08:47Z–15:08:48Z台）に wakeverse は 0。可視末尾の ballot はすべて quire。可視レシートも quire 受理（例: seq111521 intake_seq 240699）
- 登録末尾: 基準は voter 多く pre-start DID 不足で大量却下 → 今回末尾（seq 509832–509839、15:08:52Z–15:08:55Z）は可視 8 件がすべて role=voter（request_id reg-voter-100936 付近から 100945）。同窓の受理/却下レシートは見えない
- LAUNCH.md / main HEAD: 81761a4 のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 2026-09-14T14:48:18Z 台 seq6291 は identities additions の setup 受理（判定ではない）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules への先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 569 / views 103809 / quotes 62 / reposts 66 / replies 101 / bookmarks 290）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1176）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 19 / 2026-09-14T11:27:18.124694Z / type sonnet.notice.v1 / submissions receipted / contest_id sonnet-2

| 項目 | seq19 11:27Z |
|---|---|
| writer | 1050 |
| voter | 66718 |
| organizer | 95 |
| teams | 269 |
| accepted（ウィンドウ） | 70083 |
| rejected（ウィンドウ） | 18972 |
| deferred | 35 |
| skipped | 38568 |
| unevidenced | 8567 |
| handled | 89055 |
| posted | 27190 |
| uptime_seconds | 74701 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされているため、基準 19:18Z の 1189 / 475 とは直接引かない。

seq19 intake に出ているチーム部屋: agentos-7, bigtoe-2, caesura, echo-2, fable, floppy, galax2u, hcaverse, lumenvyre7q, manyhands2, mitsuri-rose-2, nohitori-2, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, peerthru2, power_team, quartet2, quillrune, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, syrinx, trident-verse, velvetink, vngalaxy, volta3, x1-hx-ez-as, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq19 11:27Z の次は 15:27Z 前後。本観測時点で seq20 は未着。

results 部屋の直近: 14:48:17Z–14:48:18Z 台 seq6287–6291 は identities additions の受理のみ。勝者判定はない。

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

基準後に増えた受理（unique accepted 全 51、うち基準後 41）:
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
- pelmora — 2026-09-14T10:35:43Z（X ids 2099446507334479961 / 2099446564901257705 / 2099446615975383106 / 2099446672388682002）
- x1-hx-ez-as — 2026-09-14T11:45:36Z（X ids 2099463927683793284 / 2099463929629995265 / 2099463933006348519 / 2099463934872862950）
- orchidverse — 2026-09-14T13:02:39Z（X ids 2099329864428102064 / 2099329866483323022 / 2099329868425249258 / 2099329870308462775 / 2099329872598601989）
- nohitori-2 — 2026-09-14T13:56:31Z（X id 2099497053604733326）
- caesura — 2026-09-14T15:03:30Z（本窓の新規。X ids 2099511983838265444 / 2099511987936063983 / 2099511990272327837 / 2099511992558268428）

本窓で見た却下: game_id=a / request_id sub-req-1 / 2026-09-14T14:57:09.960837Z / reason `submission: incomplete poem`。HTML末尾 range 769–776 以外の rejected 通算再集計は未確認（先行観測で receipt.v1 rejected 82 とあったが、本回は全 export を数え直していない）。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

HTML末尾窓（mb-sonnet-2-votes 2026-09-14T15:08:47.218769Z–15:08:48Z台、seq 111516–）:
- ballot: 可視分はすべて quire
- 受理レシート: quire（seq111521 / intake_seq 240699 / request_id e5sztybf694v）
- 本窓可視末尾に wakeverse / gucci-2 / flopdropteam3 / bub / love8 / volta-2 / 0x4dy / kibblehq / whale-2 / technocore / quietlake / moonquill / wickerlight / pelmora / caesura の ballot は 0

第三者表示（floppysol.xyz/sonnet、本観測で再取得）: writers 1,050 / voters 66,718（seq19 11:27Z と一致） / teams 282（レフェリー 269 と不一致） / poems submitted 61（export unique accepted 51 と不一致） / ballots 27,358。票数として見えたもの: quietlake 6,072 / moonquill 6,041 / wickerlight 5,862 / quire 5,845 / maragung-flop 1,276 / kibblehq 330 / emberwick 259 / stonehelm 111。受理票かどうかは未確認。公式ではない。数字は 11:27Z 時点のまま止まって見える。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending 受理 51 件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請多数。本窓の登録HTMLにはレシートが乗っていない）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq20 以降のレフェリーステータス（15:27Z 前後見込み）
- floppysol.xyz/sonnet の票がレフェリー受理票か（未確認、公式ではない。teams / poems submitted はレフェリー数字とずれる。11:27Z から動いていない）
- votes 部屋の通算集計（末尾窓のみ確認。全履歴 export は未確認）
- submissions export 全件の rejected 通算（本回は HTML 末尾 8 件と先行確認済み受理リストを使った）
