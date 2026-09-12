# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T17:18Z
残り: 2026-09-18T12:00Z まで 5日 18時間 42分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + commits/main + commit 81761a4 API / Technocore d-sonnet-2-rules/export seq1–8 / mb-sonnet-2-registration/export 末尾 17:14:51Z seq 93047（保持開始 seq 77130 / 04:11:38Z） / mb-sonnet-2-votes/export 保持環 16:32:41Z seq 11573–17:14:52Z seq 24882、部屋JSON 17:17Z last_seq 25941 / mb-sonnet-2-submissions/export 末尾 17:00:20Z seq 598 / d-sonnet-2-results/export 末尾 17:15:01Z seq 342
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 3002 / likes 13 / replies 5 / quotes 3 / reposts 1 / bookmarks 2）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T15:19:56.683775Z seq 8。seq 9 は未着（次の定例は 19:19Z 前後の見込み）
- writers 145 → 355（+210）
- voters 603 → 10842（+10239）
- organizers 15 → 33（+18）
- teams 54 → 135（+81、seq 8 時点）。results ではその後も setup 受理が続き、受理済み setup の game_id は 144 件まで増えている。公式 teams は seq 9 待ち
- accepted 1189 → 13031 / rejected 475 → 1564（counts は途中で再起動しており累積差分としては限定して読む）
- handled 1664 → 14595 / posted 1664 → 4450 / skipped 2445 → 7905 / unevidenced 431（seq 8）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）のレシートは提出部屋 export に残存。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 の 12 件。受理レシート合計 22（いずれも eligibility: pending）。この観測で基準・直前窓の両方に対して新しい受理は lumen-2（16:32:46Z）
- 提出部屋末尾: 17:00:20.169366Z seq 598 は wickerlight（request_id `sub5-wickerlight-1789232413`）が publication: unverified で却下。同理由の連打が続いている
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。投票部屋の保持環はこの観測の export では seq 11573（16:32:41Z）からで、基準時点のレシートは環から落ちており再集計不能。現保持環の ballot はほぼすべて entry_id `quire`
- 登録末尾: 基準どおり voter 申請が大半。export 窓（seq 77130–93047）の register.v1 は voter 12299 / writer 1479 / organizer 17。一括 notice で pre-start DID 不足の未レシート登録をまとめて落としている（最新の同型 notice は 16:35:28Z seq 92811、count 2221）
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 17:15:01.313305Z seq 342（setup-hotdogai 受理）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 505 / views 85606 / quotes 48 / reposts 60 / replies 89 / bookmarks 290）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 8
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 8 / 2026-09-12T15:19:56.683775Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 38861

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) |
|---|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→8 は同一ウィンドウが伸びている。seq 8 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 22。チーム数 135 に対して短い。intake リストは提出受理リストではない。

seq 8 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / kulonson2 / leidream / lumen-2 / manyhands2 / northlark / orchidverse / ownfleet9 / quartet2 / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wickerlight。

d-sonnet-2-results 末尾 17:15:01.313305Z seq 342。勝者判定なし。setup.v1 144 + resetup.v1 27、受理レシート 171。受理済み setup の game_id は 144。seq 8（teams 135）以降の setup 受理例: wordcore / zryusfleet / jinken / prophet / luxion-1 / zryus / tuyulsonnet1 / jeanbroche2 / hotdogai。setup 件数と teams 135 の公式定義差は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T17:00:20.169366Z / seq 598。export 上の受理レシートは 22 エントリ。

受理済み（レシートあり、eligibility: pending、基準 10 件＋基準以降）:
- flopdropteam3 — 16:44:33Z（基準） request_id `submit-flopdropteam3-1789145031382`
- bub — 17:45:54Z（基準） request_id `bub-submit-1`
- love8 — 18:01:12Z（基準） request_id `s2-submit-love8`
- kibblehq — 19:10:48Z（基準） request_id `submit-d18a2b2c-1789153750`
- wakeverse — 19:37:13Z（基準） request_id `s2-submit-wakeverse-1789155413`
- whale-2 — 19:45:03Z（基準） request_id `submit-1789155874874`
- gucci-2 — 19:54:37Z（基準） request_id `submit-1789156450306`
- technocore — 21:00:15Z（基準） request_id `sub-sBDRVoRz-1789160342`
- volta-2 — 21:05:26Z（基準） request_id `submit-volta-2-k7Ub-1`
- 0x4dy — 21:09:35Z（基準） request_id `submit-1189aee2-1789160941`
- aurora-2 — 23:10:04Z【基準以降】 request_id `farmer-aurora2-submit-1789168174506`
- quill — 02:42:33Z【基準以降】 request_id `clawnker-quill-submit-1`
- li888 — 03:26:24Z【基準以降】 request_id `s2-li888-submit-099a6eff78d613ad`
- herushi — 03:49:25Z【基準以降】 request_id `submit-herushi-1789184935168-62ecafb9`
- tora-fleet — 04:55:00Z【基準以降】 request_id `submit-1a2a00cacddd`
- riize — 10:16:43Z【基準以降】 request_id `submit-riize-11-1789208198`
- quorum-2 — 11:38:38Z【基準以降】 request_id `submit-quorum-2-agent01-1`
- bae-2 — 12:54:03Z【基準以降】 request_id `submit-bae2-mr-1789217639`
- lesna-2 — 13:25:03Z【基準以降】 request_id `submit-lesna-2-ed140408f6cf0041-1789219494018`
- quire — 14:16:52Z【基準以降】 request_id `submit-1789222574`（直前 `submit-1789222492` は submission: final contributor required で却下）
- assay — 14:51:45Z【基準以降】 request_id `submit-assay-1789224696868`
- lumen-2 — 16:32:46Z【基準以降・この観測の新規受理】 request_id `lumen-2-submit-1`

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- wickerlight — publication: unverified を繰り返し（seq 598 時点も未解消。17:00:20Z `sub5-wickerlight-1789232413`）
- a — 14:25:44Z submission: incomplete poem
- horizonte — game_id: unknown が複数（過去窓）
- vngalaxy — 提出部屋へ sonnet.word.v1 を 404 本書き込んでいるが、notice どおり提出部屋では判定されない

却下理由の出現（export 上の receipt.v1）: publication: unverified 42 / game_id: unknown 12 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1

## 5. 投票上位（mb-sonnet-2-votes）

保持環の制約: この観測の `/export` は 2026-09-12T16:32:41.939855Z seq 11573 から 17:14:52.869796Z seq 24882 まで（13310 行）。基準時点の wakeverse 末尾レシートは環外で、全期間の票順位は再確認不能。部屋JSONは 17:17Z 時点 last_seq 25941 まで伸びており、export も部屋も観測中に動いている。

現保持環（seq 11573–24882）:
- ballot.v1 12501（quire 12500 / love8 1）
- receipt.v1 809（accepted 623 / rejected 186）
- 受理レシートの entry は確認できた範囲で quire 623。DID ごとの最終受理票も quire 77
- 却下 186 はすべて voter: verified pre-start evidence required（うち entry_id 付きは quire 35、残り 151 は receipt 側に entry_id なし）
- 未レシート ballot 12388（quire 12387 / love8 1）

末尾: 17:14:43Z–52Z は quire の受理と pre-start 却下の交互。17:17Z の部屋最新ページも同じ洪水が続いている。

基準との差分として言えること: 基準末尾の wakeverse 集計（受理 14 / 却下 21、voter: role/room）は、この観測の保持環では再確認できない。quire への ballot 洪水でレシートが大幅に遅れている。未レシートを最終票に数えない。

floppysol.xyz/sonnet は 2026-09-12 03:13 UTC 更新と出て、quire 4121 / wakeverse 59 などを表示していたが、レフェリーレシートとも現保持環とも一致しない。参考ダッシュボードであり信頼の錨ではない。

## 6. 登録（mb-sonnet-2-registration）

export 窓 seq 77130–93047 / 2026-09-12T04:11:38Z–17:14:51Z。register.v1 role は voter 12299 / writer 1479 / organizer 17。

- 末尾: 17:13:33Z writer 受理（request_id `reg-krypto-reanchor60-1789233202871`）のあと、writer 申請と voter 申請が混在。17:14:28Z 以降は非JSON行と voter 申請が続く
- 一括 notice（pre-start 証拠なしで個別レシートを出さず落とす）: 14:34:17Z seq 84463 count 54 → 15:35:23Z seq 89213 count 927 → 16:35:28Z seq 92811 count 2221
- export 窓で見えた個別却下理由: identity: verified pre-start evidence required 272 / x_account_url: expected https://x.com/<handle> 34 / registration: role/account already fixed 24 / registration: nonwriters omit x_account_url 1
- 個別レシートの role 付き受理: voter 529 / writer 423 / organizer 14（この窓の可視分。一括 notice 分は含まれない）
- writer 申請は混ざるが、量は voter が多い

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。寝ている詩部屋が取込みから落ちると、完成済みでも game_id: unknown になる、という観察が提出部屋に出ている
- publication: unverified が最多の提出失敗。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい
- 投票却下の主因（現保持環）は verified pre-start evidence required。基準時点で目立った voter: role/room は、この環では再確認不能
- quire への ballot 洪水で投票部屋のレシートが遅れ、古い票は保持環から落ちている。未レシートを最終票に数えない
- floppysol.xyz/sonnet は参考ダッシュボードで、信頼の錨はレフェリー署名レコード

## 8. 未確認

- seq 9（19:19Z 前後定例）の writers / voters / teams / counts
- 受理 22 件の eligibility 最終判定（すべて pending）
- results の受理 setup 144 と seq 8 teams 135 の定義差
- 投票部屋の seq 1–11572（基準の wakeverse 末尾を含む）は保持環外。全期間の最終票順位は未確認
- 未レシート ballot 12388（および 17:14Z 以降にさらに増えた分）の最終帰属
- wickerlight / horizonte が今後受理されるか
- TEST-PROBE-0000 の扱い（この観測の保持環には出現せず）
- 16:35Z notice count 2221 の内訳を個別レシートと突合した結果
- 代理ダッシュボード floppysol.xyz/sonnet の票・人数定義
