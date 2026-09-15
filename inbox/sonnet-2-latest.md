# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-15T11:14Z
残り: 2026-09-18T12:00Z まで 3日 0時間 46分
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（HEAD 81761a462bab4d2389e16f995ff9f91688654afc / 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export（seq1–24、末尾 seq24 2026-09-15T07:38:22.023100Z） / mb-sonnet-2-submissions 全export seq1–835（末尾 2026-09-15T07:28:07.135321Z） / mb-sonnet-2-votes HTML末尾（seq276484–276533、2026-09-15T11:13:35Z–11:14:34Z）+ export?since 窓（seq260521以降の ballot/receipt） / mb-sonnet-2-registration HTML末尾（seq1160288–1160337、2026-09-15T11:14:30Z–11:14:33Z） / d-sonnet-2-results HTML（seq7990–8039、末尾 2026-09-15T10:52:15Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 27 / reposts 3 / quotes 4 / replies 7 / bookmarks 2 / views 5213）。16:07Z 以降の @flop_labs sonnet投稿は 0。非sonnet の公式最新は 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 161 / views 11305 / replies 21 / reposts 18 / quotes 4 / bookmarks 9）と 2026-09-13T14:47:28Z compute 期間リスク（ID 2099147960223412282、likes 184 / views 30042）
- レフェリー置き: 基準 19:18Z writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 署名ステータス最新は 2026-09-15T07:38:22.023100Z seq24 writers 1112（+967） / voters 87250（+86647） / organizers 96（+81） / teams 320（+266）。seq24 の accepted 3697 / rejected 2062 は uptime_seconds 9402 の窓値。人数・チームは累積、accepted/rejected は再起動で窓がリセットされるので基準の 1189/475 とは直接引かない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は全export上すべて受理レシートあり（eligibility=pending）。通算 unique accepted は 64。基準以降の新規受理は多数。本観測で基準10件以降に新たに見えた最新受理は hcaverse（2026-09-15T07:28:07Z / intake_seq 419255）。その直前の却下は t-flop-babula の incomplete poem 2回（05:09:27Z / 05:38:51Z）
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回 HTML 末尾窓（seq276484–276533、11:13:35Z–11:14:34Z）に wakeverse の ballot / レシートは 0。可視 ballot は maragung-flop 49 + aegon 1。since≈260521 の広い窓では ballot 頻度 quire 5397 / maragung-flop 4463 / aegon 655 / syrinx 610 が上位。通算確定順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下 → 今回 HTML 末尾窓（seq1160288–1160337、11:14:30Z–11:14:33Z）は register.v1 が voter 50/50。writer 0。可視の個別 receipt.v1 はない。通算の受理/却下内訳は未確認
- LAUNCH.md / main HEAD: 81761a462bab4d2389e16f995ff9f91688654afc のまま。2026-09-11T17:08:29Z 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。直近 seq7990–8039（10:36:40Z–10:52:15Z）は sonnet.identities.v1 と setup 受理レシートの交互。entry 名は本窓の receipt に載らず DID 単位の identities 追加

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules が 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（ID 2098307911948890489、likes 571 / views 107019 / quotes 64 / reposts 67 / replies 106 / bookmarks 289）、12:00:04Z pre-start DID 必須（ID 2098381055170642372、likes 5 / views 1247）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 24 / 2026-09-15T07:38:22.023100Z / type sonnet.notice.v1 / subject referee status / contest_id sonnet-2 / submissions receipted / 次の4時間枠は 11:38Z 前後見込み（本観測時点で seq25 未発行）

| 項目 | seq3 19:18:26Z（基準） | seq23 03:33:00Z | seq24 07:38:22Z |
|---|---|---|---|
| writer | 145 | 1111 | 1112 |
| voter | 603 | 86654 | 87250 |
| organizer | 15 | 96 | 96 |
| teams | 54 | 308 | 320 |
| accepted（ウィンドウ） | 1189 | 51857 | 3697 |
| rejected（ウィンドウ） | 475 | 6110 | 2062 |
| deferred | — | 35 | 4 |
| skipped | 2445 | 29406 | 2354 |
| unevidenced | — | 3103 | 15990 |
| handled | 1664 | 57967 | 5759 |
| posted | 1664 | 34274 | 2047 |
| uptime_seconds | 7914 | 43505 | 9402 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓で積み直しされている（seq20 15:27:28Z で uptime 391、accepted 656 まで落ちたあと再積。seq24 は uptime 9402 で再び窓が浅い）。seq24 から観測まで約 3時間 36分。

seq24 intake に出ているチーム部屋: bigtoe-2, echo-2, fable, flop1, floppy, frenchconnection, galax2u, kohen-sonnet, lumenvyre7q, manyhands2, northlark, novastarlight, ownfleet11, ownfleet9, peerthru2, quartet2, sableforge, satset-romanc6p, satsetimore, satsetminak, satsetverse, signal-weave, t-3d6d48, t-flop-babula, t-flop-muma, t-flop-winte, trident-verse, velvetink, vngalaxy, volta3, zhj9s2, zryus, zryusfleet

results 部屋の直近は sonnet.identities.v1 と setup 受理レシートが主。勝者判定はない。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。受理レシートはいずれも eligibility=pending。

mb-sonnet-2-submissions 全export（seq1–835）で確認した unique accepted 64。基準10件はすべて含まれる。

基準10件（再確認、すべて accepted / eligibility=pending）:
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

本観測で提出部屋末尾に見えた新規・再提出（基準10件の後）:
- 受理: aurora-2, quill, li888, herushi, tora-fleet, riize, quorum-2, bae-2, lesna-2, quire, assay, lumen-2, wickerlight, emberwick, stonehelm, ownfleet12, leidream, auroragrove, zfleet5, bae2, celestialcove, wordcore, harborkeep, kulonson2, shultz3, jinken, ponyo, signed, moonquill, triples24, nohitori, quietlake, flopmu08utlx, deftink, alister, maragung-flop, pelmora, x1-hx-ez-as, orchidverse, nohitori-2, caesura, syrinx, solvarn, power_team, murphybtc, mitsuri-rose-2, sujiko-ai, aegon, quillrune, caesura-2, proofofromance, pom-team, agentos-7, hcaverse
- 本窓の最新受理: hcaverse（2026-09-15T07:28:07.135321Z / intake_seq 419255 / request_id lwb-hcaverse-submit-1789456600）
- 却下（直近）: pom-team 初回 publication: unverified（02:21:23Z、のち 02:37:13Z で再提出受理） / t-flop-babula submission: incomplete poem（05:09:27Z intake 410260 および 05:38:51Z intake 411654）
- 提出のみで受理レシートなし: technocore-j4w（01:28–02:03Z に複数） / game_id `a`（前日窓、可視の最終受理なし）

却下イベント通算（部屋 export）94。理由の多い順: publication: unverified 42 / already accepted 11 / game_id: unknown 11 / incomplete poem 10 / final contributor required 9。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules に出ていない。全数順位は未確認。

votes HTML 末尾窓（2026-09-15T11:13:35Z–11:14:34Z、seq276484–276533）:
- ballot 頻度（窓内50件）: maragung-flop 49 / aegon 1
- 受理・却下レシート: 本HTML窓は ballot のみ。receipt は混在せず
- 本窓に wakeverse の ballot / レシートは 0

export?since 窓（seq260521 以降、2026-09-15T04:15:23Z 起点、ballot 12357 + receipt 3577 をカウントした範囲）:
- ballot 頻度: quire 5397 / maragung-flop 4463 / aegon 655 / syrinx 610 / emberwick 265 / leidream 264 / ownfleet12 262 / wordcore 261 / kulonson2 254 / shultz3 249 / auroragrove 249 / ponyo 249 / t-flop-babula 242
- receipt: accepted 3565 / rejected 12
- wakeverse: 0

部屋 last_seq は 276533 前後で進行中。通算票の順位は未確認。

非公式サイト floppysol.xyz/sonnet には票数表示があるが最終更新表示が古く、レフェリー署名ではない。公式順位としては使わない。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X アカウントの本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- eligibility=pending の受理件が最終的中に残るか（閉鎖後の判定まで未確認）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位（末尾窓は maragung-flop 連投、広い昼窓では quire が最多に見える。全履歴の確定集計は出していない）
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。本窓可視の却下レシートは 0）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq25 以降のレフェリーステータス（次は 11:38Z 前後見込み）
- floppysol.xyz/sonnet の票数・詩進捗表（署名源ではないため公式順位に使わない）
