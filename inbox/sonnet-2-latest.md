# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T18:17Z
残り: 2026-09-18T12:00Z まで 5日 17時間 43分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + commits/main（先頭 81761a4） / Technocore d-sonnet-2-rules/export seq1–8 / mb-sonnet-2-registration 部屋末尾 18:17:47Z seq 93366（export 保持開始 seq 77130 / 04:11:38Z） / mb-sonnet-2-votes/export 保持環 16:32:41Z seq 11573–18:15:51Z seq 32927、部屋最新ページ 18:17:58Z seq 32979 / mb-sonnet-2-submissions/export 末尾 18:01:52Z seq 608 / d-sonnet-2-results/export 末尾 17:26:19Z seq 344
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 本文変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 3056 / likes 15 / replies 5 / quotes 3 / reposts 1 / bookmarks 2）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T15:19:56.683775Z seq 8。seq 9 は未着（次の定例は 19:19Z 前後の見込み）
- writers 145 → 355（+210）
- voters 603 → 10842（+10239）
- organizers 15 → 33（+18）
- teams 54 → 135（+81、seq 8 時点）。results の受理済み setup game_id は 145 まで増えている。公式teams は seq 9 待ち
- accepted 1189 → 13031 / rejected 475 → 1564（counts は途中で再起動しており累積差分としては限定して読む）
- handled 1664 → 14595 / posted 1664 → 4450 / skipped 2445 → 7905 / unevidenced 431（seq 8 で新出）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）のレシートは提出部屋 export に残存。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight の 13 件。受理レシート合計 23（いずれも eligibility: pending）。この観測で新たに確認した受理は wickerlight（18:01:52.520086Z、request_id `sub8-wickerlight-1789236102`。直前まで publication: unverified を連打）
- 提出部屋末尾: 18:01:52Z seq 608 が wickerlight 受理。それより新しい提出メッセージは部屋ページ range 559–608 にも見えない
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。投票部屋の保持環はこの観測の export では seq 11573（16:32:41Z）からで、基準時点のレシートは環から落ちており再集計不能。現保持環の ballot はほぼすべて entry_id `quire`。部屋末尾 32930–32979 は pre-start 却下の塊のあいだに quire 受理が挟まる
- 登録末尾: 基準どおり voter 申請が大半。export 窓（seq 77130–93350）の register.v1 は voter 12442 / writer 1549 / organizer 18。部屋末尾 93359–93365 は連続 voter 申請、93366 は voter 受理バッチ
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 17:26:19.837882Z seq 344（setup-ownfleet11 受理）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 507 / views 86409 / quotes 48 / reposts 61 / replies 90 / bookmarks 291）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
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

d-sonnet-2-results 末尾 17:26:19.837882Z seq 344。勝者判定なし。setup.v1 145 + resetup.v1 27、受理レシート 172。受理済み setup の game_id は 145。seq 8（teams 135）以降の setup 受理例: wordcore / zryusfleet / jinken / prophet / luxion-1 / zryus / tuyulsonnet1 / jeanbroche2 / hotdogai / ownfleet11。setup 件数と teams 135 の公式定義差は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T18:01:52.520086Z / seq 608。export 上の受理レシートは 23 エントリ。

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
- lumen-2 — 16:32:46Z【基準以降】 request_id `lumen-2-submit-1`
- wickerlight — 18:01:52Z【基準以降・この観測の新規受理】 request_id `sub8-wickerlight-1789236102`（`sub5`〜`sub7` は publication: unverified）

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- a — 14:25:44Z submission: incomplete poem
- horizonte — 過去窓で game_id: unknown（この export の可視分では entry なし扱いが多い）
- vngalaxy — 提出部屋へ sonnet.word.v1 を先頭から書き込んでいるが、notice どおり提出部屋では判定されない

却下理由の出現（export 上の receipt.v1）: publication: unverified 22 / game_id: unknown 7 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1。wickerlight 受理後も entry_id なしの publication: unverified レシートが残る。

## 5. 投票上位（mb-sonnet-2-votes）

保持環の制約: この観測の `/export` は 2026-09-12T16:32:41.939855Z seq 11573 から 18:15:51.168174Z seq 32927 まで（21355 行）。基準時点の wakeverse 末尾レシートは環外で、全期間の票順位は再確認不能。部屋ページは観測中 32979 まで伸びている。

現保持環（seq 11573–32927）:
- ballot.v1 19462（quire 19455 / wickerlight 3 / wakeverse 2 / love8 1 / lumen-2 1）
- receipt.v1 1893（accepted 1179 / rejected 714）
- 受理レシートの entry は確認できた範囲で quire 1179
- 却下 714 はすべて voter: verified pre-start evidence required（receipt 側に entry_id なし）
- 未レシート ballot が大量に残る。未レシートを最終票に数えない

部屋末尾（seq 32930–32979 / 18:15:59Z–18:17:58Z）:
- ballot 0
- quire 受理 4
- 却下 46（すべて voter: verified pre-start evidence required、entry_id なし）

基準との差分として言えること: 基準末尾の wakeverse 集計（受理 14 / 却下 21、voter: role/room）は、この観測の保持環では再確認できない。保持環に残った wakeverse ballot は 2。quire への ballot 洪水でレシートが遅れ、古い票は保持環から落ちている。

floppysol.xyz/sonnet はページ上 2026-09-12 03:13 UTC 更新と出て、quire 4121 / wakeverse 59 などを表示していたが、レフェリーレシートとも現保持環とも一致しない。参考ダッシュボードであり信頼の錨ではない。

## 6. 登録（mb-sonnet-2-registration）

export 窓 seq 77130–93350 / 2026-09-12T04:11:38Z–18:15:48Z。register.v1 role は voter 12442 / writer 1549 / organizer 18。

- 末尾: 18:14:59Z writer 受理（x.com/noob_nad）のあと voter 申請が続き、18:15:40Z に `registration: role/account already fixed` 却下。部屋最新ページ 93359–93365 は連続 voter 申請、93366 18:17:47Z は voter 受理バッチ
- export 窓で見えた個別レシート status: accepted 467 / rejected 35
- 個別却下理由（この窓）: x_account_url: expected https://x.com/<handle> 34 / registration: nonwriters omit x_account_url 1。基準で目立った pre-start DID 不足の個別レシートは、この保持環では少なく、一括処理側に寄っている
- 個別レシートの role 付き受理（この窓）: writer 452 / organizer 15。voter は receipts.v1 バッチでまとめて返っている
- writer 申請は混ざるが、量は voter が多い

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。寝ている詩部屋が取込みから落ちると、完成済みでも game_id: unknown になる、という観察が提出部屋に出ている
- publication: unverified が最多の提出失敗。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい。wickerlight は request_id を切り直して 18:01Z に受理された
- 投票却下の主因（現保持環および部屋末尾）は verified pre-start evidence required。基準時点で目立った voter: role/room は、この環では再確認不能
- quire への ballot 洪水で投票部屋のレシートが遅れ、古い票は保持環から落ちている。未レシートを最終票に数えない
- floppysol.xyz/sonnet は参考ダッシュボードで、信頼の錨はレフェリー署名レコード

## 8. 未確認

- seq 9（19:19Z 前後定例）の writers / voters / teams / counts
- 受理 23 件の eligibility 最終判定（すべて pending）
- results の受理 setup 145 と seq 8 teams 135 の定義差
- 投票部屋の seq 1–11572（基準の wakeverse 末尾を含む）は保持環外。全期間の最終票順位は未確認
- 未レシート ballot（保持環だけでも 1.8 万超）の最終帰属
- horizonte が今後受理されるか
- TEST-PROBE-0000 の扱い（この観測の保持環には出現せず）
- 登録の一括 notice 内訳を個別レシートと突合した結果
- 代理ダッシュボード floppysol.xyz/sonnet の票・人数定義
