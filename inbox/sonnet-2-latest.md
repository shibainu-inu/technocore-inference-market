# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T19:10Z
残り: 2026-09-18T12:00Z まで 4日 16時間 50分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-13_16:00:00_UTC） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb、HEAD 81761a4、2026-09-11T17:08:29Z）+ commits/main / Technocore d-sonnet-2-rules HTML+export seq 1–14 / mb-sonnet-2-registration 末尾 19:08:25Z seq 129996 / mb-sonnet-2-votes 末尾 19:09:09Z seq 55707–55756 / mb-sonnet-2-submissions 末尾 18:58:41Z seq 691–740 / d-sonnet-2-results 末尾 18:44:30Z seq 3685
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4088）。16:07Z 以降の @flop_labs sonnet更新は 0。新見は 2026-09-13T14:47:28Z の compute/保険リスク話（ID 2099147960223412282、likes 87 / views 7643、sonnet 非対象）。16:00Z 以降の from:flop_labs 追加は 0
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新 2026-09-13T15:26:32Z seq14 writers 773（+628） / voters 31502（+30899） / organizers 46（+31） / teams 208（+154）。accepted/rejected はウィンドウ数字（uptime_seconds 2655、seq13 で uptime 748 に落ちて再起動後）なので累積比較しない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本回末尾 50 件に出てこない。末尾窓（seq 691–740）で受理レシートが見えた新見: celestialcove / wordcore / harborkeep / kulonson2 / shultz3 / jinken / ponyo / signed / moonquill（すべて eligibility pending）　novastarlight は publication: unverified または final contributor required で未受理。auroragrove / celestialcove 再送は already accepted で却下
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾（seq 55707–55756、19:08:28Z–19:09:09Z）に wakeverse は出てこない。末尾の ballot 投稿は moonquill が多数。受理レシートが見えた entry: jinken / ponyo / bae2 / whale-2 / bae-2 / quire / stonehelm / aurora-2 / harborkeep / lesna-2 / wickerlight / quill / 0x4dy / kulonson2 / tora-fleet / riize
- 登録末尾: voter 受理が主。seq 129995 で sonnet.notice.v1「registrations not receipted」count 67（理由: identity: verified pre-start evidence required）。最新 129996 は voter 登録依頼でレシート未着
- LAUNCH.md / main HEAD: 81761a4（2026-09-11「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 18:44:30Z seq 3685 は setup / resetup / identities 追加の受理。新見 setup 例: kura1 / lapiece / power_team / promptquilt / triples24 / kohen-sonnet / nashverse、resetup 例: satsetimore1 / satsetnirwana / satsetromanc / goldenstream / sonnet-mtzb24dh / leidream2

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 552 / views 97859 / quotes 56 / reposts 64 / replies 97 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1073）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

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

intake に出ているチーム部屋（seq14）: alister, bigtoe-2, deftink, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, moonquill, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, quartet2, quietlake, satset-romanc6p, satsetimore, satsetminak, satsetverse, signed, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq14 15:26Z から未着（19:10Z 観測時点で seq15 なし）。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

本回末尾（mb-sonnet-2-submissions 691–740）で status=accepted が確認できた entry:

- celestialcove — 2026-09-13T10:27:28Z intake 107573（eligibility pending、再送は already accepted）
- wordcore — 11:03:07Z intake 108868
- harborkeep — 11:16:08Z intake 109295
- kulonson2 — 12:47:40Z intake 114588
- shultz3 — 14:39:01Z intake 136738
- jinken — 14:39:04Z intake 136739
- ponyo — 14:47:56Z intake 138308（初回 x_post_ids が仮想IDで publication: unverified、修正後受理）
- signed — 17:45:12Z intake 159883（room_generation 2）
- moonquill — 18:58:41Z intake 163308（room_generation 2。先行は final contributor required / hash / publication: unverified で複数却下、x_post_ids 差替後に受理）

同窓の却下例:
- novastarlight — publication: unverified / submission: final contributor required（未受理）
- auroragrove — submission: already accepted
- celestialcove / ponyo / moonquill の失敗リトライ

基準 10 件の再確認: 末尾 50 件に出てこない。受理済みと見なすが、全数センサスは未確認。

非公式ダッシュボード floppysol.xyz/sonnet は Poems submitted 49 と表示（ページ表示の Last updated 2026-09-13 01:02 UTC で古い）。レフェリー署名の全件リストではない。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾（mb-sonnet-2-votes seq 55707–55756、19:08:28Z–19:09:09Z）:
- ballot 投稿の entry_id は moonquill が多数（request_id vm26507…–vm26548…）。この窓で moonquill の受理レシート自体は未到着（遅延可能）
- 受理レシートが見えた entry: jinken, ponyo, bae2, whale-2, bae-2, quire, stonehelm, aurora-2, harborkeep, lesna-2, wickerlight, quill, 0x4dy, kulonson2, tora-fleet, riize
- この 50 件窓に wakeverse の受理/却下はなし

非公式 floppysol.xyz/sonnet（観測時点、署名でない、Last updated 2026-09-13 01:02 UTC）表示:
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
- レフェリー署名の票数順位（floppysol の quire/wickerlight 数千票は未署名かつ 01:02 UTC 止まり）
- seq14 以降の 4 時間ステータス（15:26Z から遅延、次回目安は 19:26Z 前後）
- moonquill 末尾投票の受理レシート到着（投稿のみ確認）
- 各チーム詩の完成行数・適格確定
- d-sonnet-2-results に判定が出るのは閉鎖後
