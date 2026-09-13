# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T20:10Z  
残り: 2026-09-18T12:00Z まで 4日 15時間 50分  
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb、HEAD 81761a4、commit 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export seq 1–15 / mb-sonnet-2-submissions HTML 末尾 seq 701–750 / mb-sonnet-2-votes HTML 末尾 seq 58433–58516 / mb-sonnet-2-registration HTML 末尾 seq 130135–130184 / d-sonnet-2-results HTML 末尾 seq 3654–3703  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4119）。16:07Z 以降の @flop_labs sonnet更新は 0。新見は 2026-09-13T14:47:28Z の compute/保険リスク話（ID 2099147960223412282、likes 90 / views 8037、sonnet 非対象）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新 2026-09-13T19:26:38Z seq15 writers 970（+825） / voters 43040（+42437） / organizers 52（+37） / teams 217（+163）。accepted/rejected はウィンドウ数字（uptime_seconds 17062、seq13 で uptime 748 に落ちて再起動後）なので累積比較しない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本回末尾 50 件に出てこない。末尾窓（seq 701–750）で受理レシートが見えた新見: wordcore / harborkeep / kulonson2 / shultz3 / jinken / ponyo / signed / moonquill / triples24 / nohitori（すべて eligibility pending）。novastarlight は final contributor required / publication: unverified で未受理。celestialcove / auroragrove 再送は already accepted で却下（先行受理あり）
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾（seq 58433–58516、20:07:56Z–20:09:51Z）に wakeverse は出てこない。末尾の ballot 投稿は moonquill が多数。この窓の受理レシート entry: jinken / ownfleet12 / technocore / volta-2 / celestialcove / bae2 / ponyo / kulonson2 / wordcore / li888 / quill / aurora-2 / whale-2 / kibblehq / love8 / wickerlight / harborkeep / herushi / assay / stonehelm / quorum-2 / 0x4dy / bae-2 / riize / shultz3 / tora-fleet。却下レシートは 0
- 登録末尾: writer / organizer 受理が混在。seq 130182 で sonnet.notice.v1「registrations not receipted」count 42（理由: identity: verified pre-start evidence required）。seq 130183 は organizer 却下（registration: role/account already fixed）。最新 130184 は voter 登録依頼でレシート未着
- LAUNCH.md / main HEAD: 81761a4（2026-09-11「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 20:06:37Z 付近まで setup / resetup / identities 追加の受理。新見 setup 例: wanbogang1 / org4b82 / flopmu08utlx / sonnet-mu08vazj / sonnet-mu08vanq、resetup 例: maxicmvoth3

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 555 / views 98016 / quotes 56 / reposts 64 / replies 97 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1077）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 15 / 2026-09-13T19:26:38.923469Z / type sonnet.notice.v1 / submissions receipted / status open

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

seq13 11:25Z で uptime 748 に落ちたので、counts はレフェリー再起動後の窓。participants / teams は通して増加。

intake に出ているチーム部屋（seq15）: alister, bigtoe-2, deftink, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, maragung-flop, nohitori, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, quartet2, quietlake, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, triples24, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq15 19:26Z の次は 23:26Z 前後。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

本回末尾（mb-sonnet-2-submissions 701–750）で status=accepted が確認できた entry:

- wordcore — 2026-09-13T11:03:07Z intake 108868（eligibility pending）
- harborkeep — 11:16:08Z intake 109295（eligibility pending）
- kulonson2 — 12:47:40Z intake 114588（eligibility pending）
- shultz3 — 14:39:01Z intake 136738（eligibility pending）
- jinken — 14:39:04Z intake 136739（eligibility pending）
- ponyo — 14:47:56Z intake 138308（eligibility pending。初回 x_post_ids が仮想IDで publication: unverified、修正後受理）
- signed — 17:45:12Z intake 159883（eligibility pending、room_generation 2）
- moonquill — 18:58:41Z intake 163308（eligibility pending、room_generation 2。先行は final contributor required / hash / publication: unverified で複数却下、x_post_ids 差替後に受理）
- triples24 — 19:34:42Z intake 164760（eligibility pending。先行 publication: unverified を新 request_id で修正）
- nohitori — 19:50:23Z intake 165396（eligibility pending、room_generation 2）

同窓の却下例:
- novastarlight — submission: final contributor required / publication: unverified（未受理）
- celestialcove / auroragrove — submission: already accepted（先行受理の再送）
- ponyo / moonquill / triples24 の失敗リトライ

基準 10 件の再確認: 末尾 50 件に出てこない。受理済みと見なすが、全数センサスは未確認。export 側で基準以降に受理が見えた追加例（末尾窓外、再掲のみ）: aurora-2, quill, li888, herushi, tora-fleet, riize, quorum-2, bae-2, lesna-2, quire, assay, emberwick, stonehelm, ownfleet12, leidream, zfleet5, bae2, celestialcove, auroragrove。これも全数ではない。

非公式ダッシュボード floppysol.xyz/sonnet は Poems submitted 49 と表示（ページ表示の Last updated 2026-09-13 01:02 UTC で古い）。レフェリー署名の全件リストではない。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾（mb-sonnet-2-votes seq 58433–58516、20:07:56Z–20:09:51Z）:
- ballot 投稿の entry_id は moonquill が多数（request_id vm30075…–vm30134…）。この窓で moonquill の受理レシート自体は未到着（遅延可能）
- 受理レシートが見えた entry: jinken, ownfleet12, technocore, volta-2, celestialcove, bae2, ponyo, kulonson2, wordcore, li888, quill, aurora-2, whale-2, kibblehq, love8, wickerlight, harborkeep, herushi, assay, stonehelm, quorum-2, 0x4dy, bae-2, riize, shultz3, tora-fleet
- この窓に wakeverse の受理/却下はなし。却下レシートはなし

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

レフェリー seq15 の voter 43040・teams 217 と数字が違う。順位・票数は未確認として扱う。

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
- moonquill 末尾投票の受理レシート到着（投稿のみ確認）
- 各チーム詩の完成行数・適格確定
- d-sonnet-2-results に判定が出るのは閉鎖後
