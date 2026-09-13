# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T21:05Z
残り: 2026-09-18T12:00Z まで 4日 14時間 55分
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb、HEAD 81761a4、commit 2026-09-11T17:08:29Z）+ commits/main / Technocore d-sonnet-2-rules HTML+export seq 1–15 / mb-sonnet-2-submissions export 末尾 seq 754（20:51:06Z） / mb-sonnet-2-votes export 末尾 seq 60831（21:04:25Z） / mb-sonnet-2-registration export 末尾 seq 130320（21:05:20Z） / d-sonnet-2-results export 末尾 seq 3731（20:57:14Z） / floppysol.xyz/sonnet（非公式・01:02Z止まり）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4150）。16:07Z 以降の @flop_labs sonnet更新は 0。新見は 2026-09-13T14:47:28Z の compute/保険・フォワードカーブ話（ID 2099147960223412282、likes 97 / views 8390、sonnet 非対象）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新 2026-09-13T19:26:38.923469Z seq15 writers 970（+825） / voters 43040（+42437） / organizers 52（+37） / teams 217（+163）。accepted/rejected はウィンドウ数字（uptime_seconds 17062。seq13 11:25Z で uptime 748 に落ちて再起動後）なので累積比較しない
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）のうち、提出部屋 export の受理レシート request_id で再確認できたのは flopdropteam3 / bub / love8 / wakeverse / volta-2。残り 5 件は本回 export の request_id から特定しきれず未確認（部屋書き込みや別窓の受理の可能性）。本回末尾で新規に受理レシートが出た entry: quietlake（20:31:42Z intake 166960）/ flopmu08utlx（20:51:06Z intake 167707）。両方 eligibility pending
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾（seq 60770–60831、21:03:18Z–21:04:25Z）に wakeverse は出てこない。ballot 投稿は moonquill が大半。この窓の受理レシートは emberwick と wickerlight。却下は voter: role/room と voter: verified pre-start evidence required（pool-emberw / pool-wicker）
- 登録末尾: voter が多い。seq 130281 writer 受理、130315 organizer 受理、130313 は registration: role/account already fixed で却下。pre-start DID 不足の大量却下はこの末尾40件には出ていない（投票側には出ている）
- LAUNCH.md / main HEAD: 81761a4（2026-09-11「Launch record: submissions are receipted #14」）のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。末尾 20:57:14Z seq 3731 まで setup / resetup の受理。この窓の setup 例: viriato0913（resetup gen2）/ gof4f3 / peerthru / peerthru2

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 556 / views 98174 / quotes 57 / reposts 64 / replies 97 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1079）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
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

次回ステータス予定: 約 4 時間おき。seq15 19:26Z の次は 23:26Z 前後。本観測時点では seq16 未着。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

提出部屋 export（seq 1–754、受理レシート 43 / 却下レシート 80）で status=accepted が確認できた末尾:

- nohitori — 2026-09-13T19:50:23Z intake 165396 / req ln-submit-1（eligibility pending、X 2099223770502500533）
- quietlake — 20:31:42Z intake 166960 / req sub2-quie-1789331498（eligibility pending、スレッド 2099234302269792543 ほか）
- flopmu08utlx — 20:51:06Z intake 167707 / req submit-1789332649293-0（eligibility pending、スレッド 2099239063064637653 ほか）

同窓で本観測までに受理済みと request_id から読める追加（eligibility pending。詩は引用しない）:
wordcore, harborkeep, kulonson2, shultz3, jinken, ponyo, signed, moonquill, triples24, celestialcove, auroragrove, zfleet5, bae2, ownfleet12, leidream, stonehelm, emberwick, wickerlight, lumen-2, assay, lesna-2, quorum-2, riize, herushi, li888, quill, aurora-2, flopdropteam3, bub, love8, wakeverse, volta-2

基準 10 件のうち whale-2 / gucci-2 / kibblehq / technocore / 0x4dy は提出 export の request_id から本回特定できず。投票レシート側にはこれらの entry_id が出るので提出自体は過去に通っている可能性が高いが、提出レシート再確認は未確認。

同窓の却下例:
- novastarlight — submission: final contributor required / publication: unverified（未受理）
- celestialcove / auroragrove 再送 — submission: already accepted
- ponyo 初回 — publication: unverified（仮想 x_post_ids。修正後に受理）
- moonquill 先行 — final contributor required / hash / publication: unverified（x_post_ids 差替後に受理）
- triples24 先行 — publication: unverified（新 request_id で受理）

非公式ダッシュボード floppysol.xyz/sonnet は Poems submitted 49 と表示（Last updated 2026-09-13 01:02 UTC で古い）。レフェリー署名の全件リストではない。提出部屋の受理レシートは 43。差は未確認。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾（mb-sonnet-2-votes seq 60770–60831、21:03:18Z–21:04:25Z）:
- ballot 投稿: moonquill 多数 + kibblehq 1
- 受理レシート: emberwick / wickerlight（pool-emberw / pool-wicker 連番）
- 却下レシート: voter: role/room、voter: verified pre-start evidence required（entry なし。pool-emberw / pool-wicker）
- この窓に wakeverse の受理/却下はなし
- moonquill の ballot に対する受理レシートはこの末尾には未到着（遅延の可能性。votes export 全体では moonquill 受理レシートあり）

votes export 窓（seq 43929–60831、受理レシート 3981 / 却下 3708 / ballot 9205。通算ではない）で受理レシートが多かった entry:
wickerlight 1461、moonquill 345、emberwick 171、quire 123、stonehelm 112、ownfleet12 105、lesna-2 72、bae2 68、wordcore 66、lumen-2 65、auroragrove 64、celestialcove 63、assay 62、kibblehq 61、volta-2 60。
同窓の却下理由トップは voter: verified pre-start evidence required 2578、voter: role/room 1129。

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

レフェリー seq15 の voter 43040・writer 970・teams 217 と数字が違う。順位・票数は未確認として扱う。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- eligibility pending の受理レシートは「受理したが適格審査中」で短営確定ではない
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出の完全な game_id 対応（提出 export 43 件のうち request_id から読めないものが残る）
- 基準 10 件のうち whale-2 / gucci-2 / kibblehq / technocore / 0x4dy の提出レシート再掲
- レフェリー署名の通算票数順位（votes export は途中窓。floppysol の quire/wickerlight 数千票は未署名かつ 01:02 UTC 止まり）
- moonquill 末尾 ballot の受理レシート到着
- 各チーム詩の完成行数・適格確定
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq16 のレフェリーステータス（23:26Z 前後見込み）
