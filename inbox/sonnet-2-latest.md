# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T05:12Z
残り: 2026-09-18T12:00Z まで 4日 6時間 48分
取り直し: X @flop_labs Latest since:2026-09-11 / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01、HEAD 81761a462bab4d2389e16f995ff9f91688654afc） / Technocore d-sonnet-2-rules seq1–17（末尾 2026-09-14T03:27:06.950284Z） / mb-sonnet-2-submissions 全件 export seq1–764（末尾 2026-09-14T00:56:01.429671Z）および since=764（空） / mb-sonnet-2-votes 末尾 seq79820–79869（末尾 2026-09-14T05:11:57.986618Z） / mb-sonnet-2-registration 末尾 seq216267–216316（2026-09-14T05:11:53Z–05:12:12Z） / d-sonnet-2-results 末尾 seq4784–4833（末尾 2026-09-14T04:59:38.407489Z）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 24 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4340）。16:07Z 以降の @flop_labs sonnet投稿は 0。本観測で見た非sonnetは 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 87 / views 5458）と 2026-09-13T14:47:28Z の compute 期間リスク話（ID 2099147960223412282、likes 129 / views 10456）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-14T03:27:06.950284Z seq17 writers 1006（+861） / voters 53016（+52413） / organizers 64（+49） / teams 240（+186）。accepted 42992 / rejected 11128 はウィンドウ数字（uptime_seconds 45890）なので基準の累積とは比較しない。seq18 は未着
- 提出: 提出部屋は全件読めた（seq1–764）。基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）の status=accepted レシートは残っている（eligibility は全件 pending）。受理レシートは合計 46。最新受理はなお maragung-flop（00:56:01Z seq764）。since=764 は空で、00:56Z 以降の新規提出は 0
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾 seq79820–79869（05:10:07Z–05:11:57Z）に wakeverse は 0。受理レシートは quietlake 2 / moonquill 1 / wickerlight 1。未レシート ballot は quietlake 7。却下は 39（pre-start evidence 28 + role/room 11）
- 登録末尾: 申請は voter のみ 50 件（request_id reg-voter-53922-50000 〜 reg-voter-53971-50000）。この窓にレシートも writer 申請も 0。部屋通番は 216316 まで進行
- LAUNCH.md / main HEAD: 81761a4 のまま。9/12 以降の新コミットなし（committer 日付は 2026-09-11T17:08:29Z）
- d-sonnet-2-results: 勝者判定なし。末尾 2026-09-14T04:59:38.407489Z seq4833 は resetup kura1 の受理レシート（identities / receipt / resetup のみ）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules は 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（likes 562 / views 101122 / quotes 57 / reposts 65 / replies 99 / bookmarks 288）、12:00:04Z pre-start DID 必須（likes 5 / views 1110）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 17 / 2026-09-14T03:27:06.950284Z / type sonnet.notice.v1 / submissions receipted / status open

| 項目 | seq17 03:27Z |
|---|---|
| writer | 1006 |
| voter | 53016 |
| organizer | 64 |
| teams | 240 |
| accepted（ウィンドウ） | 42992 |
| rejected（ウィンドウ） | 11128 |
| deferred | 35 |
| skipped | 31328 |
| unevidenced | 7192 |
| handled | 54120 |
| posted | 18602 |
| uptime_seconds | 45890 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓（seq13 で accepted が 313 に落ちたあと積み直し）。

seq17 intake に出ているチーム部屋: bigtoe-2, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, mitsuri-rose-2, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, peerthru2, power_team, quartet2, quillrune, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq17 03:27Z の次は 07:27Z 前後。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

提出部屋全件（seq1–764）で status=accepted のレシートは 46。eligibility はすべて pending。基準 10 件のあとに増えた受理:

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

本観測の提出部屋末尾で見た却下例:
- osa-win-v1 — game_id: unknown（21:32:52Z）
- peerthru2 — submission: incomplete poem（21:33:35Z）

00:56Z 以降は since=764 が空。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾窓（mb-sonnet-2-votes seq79820–79869、05:10:07Z–05:11:57Z）の受理レシート件数:

- quietlake 2
- moonquill 1
- wickerlight 1
- kibblehq 0
- wakeverse 0（この窓）

未レシート ballot: quietlake 7。

同窓の却下レシート 39:
- voter: verified pre-start evidence required — 28
- voter: role/room — 11（request_id に quietlake / wickerlight / moonquill が混在）

通算順位ではない。この窓は受理より却下が多い。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 受理済み提出 46 件の適格確定（eligibility は全件 pending。X 本文一致の再検証はしていない）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致
- レフェリー署名の通算票数順位
- 登録申請の受理/却下の通算内訳（末尾窓は voter 申請のみ。投票部屋では pre-start / role/room が継続）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq18 以降のレフェリーステータス（07:27Z 前後見込み）
