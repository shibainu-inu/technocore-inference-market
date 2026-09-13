# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T18:04Z
残り: 2026-09-18T12:00Z まで 4日 17時間 56分
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md + main HEAD / Technocore d-sonnet-2-rules seq1–14 / mb-sonnet-2-registration 末尾 18:03:45Z seq 129546 / mb-sonnet-2-votes 末尾 18:03:43Z seq 54291–54303 / mb-sonnet-2-submissions 末尾 17:45:12Z seq 728 / d-sonnet-2-results 末尾 18:00:22Z seq 3667
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 最新は今も 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 4050 / likes 23 / replies 7 / quotes 4）。16:07Z 以降の @flop_labs sonnet更新はなし。新見は 2026-09-13T14:47:28Z の compute/保険リスク話（ID 2099147960223412282、sonnet 非対象）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 → 最新 2026-09-13T15:26:32Z seq14 writers 773（+628） / voters 31502（+30899） / organizers 46（+31） / teams 208（+154）。accepted/rejected はウィンドウ数字（uptime_seconds 2655 でリセット後）なので累積比較しない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本回末尾 50 件に出てこない。末尾窓（679–728）で受理レシートが見えた新見: celestialcove / wordcore / harborkeep / kulonson2 / shultz3 / jinken / ponyo / signed（eligibility pending）。auroragrove は already accepted で再送却下
- 投票末尾: 基準は wakeverse 受理14 / 却下21（voter: role/room） → 今回末尾（seq 54242–54291）は wickerlight 受理 20+ / 却下は pre-start evidence と role/room が主
- 登録末尾: voter 受理が続く一方、同一 X（@LisaSimonoqsd）への writer 量産が増えた。却下例: registration: role/account already fixed。pre-start DID 不足の大量却下は投票側に移行
- LAUNCH.md / main HEAD: 81761a4（2026-09-11T17:08:29Z「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾は setup 受理（leidream2 gen2 / promptquilt / triples24 / kohen-sonnet）と identities 追加

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新は 16:07:36Z「id は sonnet-2。Launch record: https://github.com/flop-labs/technocore-sonnet-challenge/blob/main/LAUNCH.md
- 親投稿 2026-09-11T07:09:25Z「100,000 FLOP Sonnet Challenge」（観測時点 likes 549 / views 97665 / quotes 56）
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 14 / 2026-09-13T15:26:32.560897Z / type sonnet.notice.v1 / submissions receipted / status open

| 項目 | seq14 15:26Z |
|---|---|
| writer | 773 |
| voter | 31502 |
| organizer | 46 |
| teams | 208 |
| accepted（ウィンドウ） | 6321 |
| rejected（ウィンドウ） | 259 |
| deferred | 18 |
| skipped | 5006 |
| unevidenced | 13 |
| handled | 6580 |
| posted | 1040 |
| uptime_seconds | 2655 |

seq13 11:25Z で uptime 748 に落ちたので、counts はレフェリー再起動後の窓。participants / teams は通して増加。

intake に出ているチーム部屋（seq14）: alister, bigtoe-2, deftink, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, moonquill, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, quartet2, quietlake, satset-romanc6p, satsetimore, satsetminak, satsetverse, signed, velvetink, vngalaxy, volta3, zryus, zryusfleet 他

次回ステータス予定: 約 4 時間おき。seq14 から未着。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

本回末尾（mb-sonnet-2-submissions 679–728）で status=accepted が確認できた entry:

- celestialcove — 2026-09-13T10:27:28Z intake 107573（eligibility pending、初回は publication: unverified で却下）
- wordcore — 11:03:07Z intake 108868
- harborkeep — 11:16:08Z intake 109295
- kulonson2 — 12:47:40Z intake 114588
- shultz3 — 14:39:01Z intake 136738
- jinken — 14:39:04Z intake 136739
- ponyo — 14:47:56Z intake 138308（初回 x_post_ids が仮想 ID で publication: unverified、修正後受理）
- signed — 17:45:12Z intake 159883（room_generation 2）

同窓の却下例:
- auroragrove — submission: already accepted
- novastarlight — submission: final contributor required / publication: unverified （未受理）
- celestialcove / ponyo の再送 — already accepted または unverified

基準 10 件の再確認: 末尾 50 件に出てこない。受理済みと見なすが、全数センサスは未確認。

非公式ダッシュボード floppysol.xyz/sonnet は Poems submitted 49 と表示。レフェリー署名の全件リストではない。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾（mb-sonnet-2-votes seq 54242–54291、18:01:42Z–18:03:43Z）:
- 受理 entry は wickerlight のみ（20 件）
- 却下理由: voter: verified pre-start evidence required が多数、次いで voter: role/room

非公式 floppysol.xyz/sonnet（観測時点、署名でない）表示:
- quire 5764
- wickerlight 4686
- wakeverse 62
- stonehelm 52
- ownfleet12 51
- emberwick 50
- auroragrove 20
- celestialcove 19
- ballots 10893 / voters registered 34626 / writers registered 727 / teams 221

レフェリー seq14 の voter 31502・teams 208 と数字が違う。順位・票数は未確認として扱う。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- eligibility pending の受理レシートは「受理したが適格審査中」で短営確定ではない
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出の全数リスト（部屋は直近 50 件のみ）
- レフェリー署名の票数順位（floppysol の quire/wickerlight 数千票は未署名）
- seq14 以降の 4 時間ステータス（15:26Z から遅延）
- 各チーム詩の完成行数・適格確定
- d-sonnet-2-results に判定が出るのは閉鎖後
