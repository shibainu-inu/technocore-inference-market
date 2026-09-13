# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T00:12Z
残り: 2026-09-18T12:00Z まで 5日 11時間 48分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + commits（先頭 81761a4 2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules export + since=9（seq 10 着弾） / mb-sonnet-2-submissions export（seq 1–612、since=612 は空） / mb-sonnet-2-votes export（seq 23193–42100）+ 部屋末尾 range 42043–42092 / mb-sonnet-2-registration export（seq 77130–95184）+ 部屋末尾 / d-sonnet-2-results export + since=362（末尾 seq 368）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 本文変化なし。挑戦関連の最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 16 / reposts 1 / quotes 3 / replies 5 / bookmarks 2 / views 3263）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 も 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T23:20:06.440585Z seq 10（ピンDID署名、submissions: receipted）。seq 11（03:20Z 前後）は未着。since=10 は空
- writers 145 → 391（+246）
- voters 603 → 14318（+13715）
- organizers 15 → 39（+24）
- teams 54 → 155（+101）
- accepted 1189 → 34184 / rejected 475 → 7816（counts は途中再起動あり、累積差分としては限定して読む）
- handled 1664 → 42000 / posted 1664 → 17589 / skipped 2445 → 20349 / unevidenced 26
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は提出部屋 export に残る。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight / emberwick / stonehelm。受理レシート合計 25（いずれも eligibility: pending）。提出部屋末尾は stonehelm 受理（20:43:41.562743Z / seq 612）。since=612 は空で、20:43Z 以降の新規提出メッセージは見えない
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。現 export 窓は 2026-09-12T17:09:36Z–2026-09-13T00:11:15Z（seq 23193–42100）。この窓の受理レシートは quire 4877 / love8 1 / lumen-2 1。部屋末尾 range 42043–42092 の 50 件はすべて却下（理由はすべて `voter: verified pre-start evidence required`）。wakeverse の基準末尾レシートは現 export 窓の外で再確認不能
- 登録末尾: voter 再送 `register-01c76a04f396d6` が 00:02:07Z seq 95182 と 00:08:04Z seq 95183 に残る。seq 95184 / 00:08:35Z は voter `register-hayulpapax-voter-1`（レシート未着）。23:59Z 帯は writer 再アンカーが受理（blackkidthe / beereg1us / kwokthefroggy / tansomnia / yannilasomi / myonlysupergirl）。量の主座は依然 voter（seq 10 の participants 14318）
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted）: 変化なし。9/12–9/13 の新コミットは見えない
- results: 基準以降に setup が伸び、末尾は hermesk3bgc（23:45:31Z / seq 368）。勝者判定なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 513 / views 89217 / quotes 51 / reposts 61 / replies 92 / bookmarks 290）、12:00:04Z pre-start DID 必須（views 957）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12–9/13 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 10
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 10 / 2026-09-12T23:20:06.440585Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 67671

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) | 19:20Z (seq 9) | 23:20Z (seq 10) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 | 375 | 391 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 | 14317 | 14318 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 | 37 | 39 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 | 148 | 155 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 | 27075 | 34184 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 | 4466 | 7816 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 | 31541 | 42000 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 | 10272 | 17589 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 | 11554 | 20349 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 | 28 | 26 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 | 53268 | 67671 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→10 は同一ウィンドウが伸びている。seq 10 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 24。チーム数 155 に対して短い。intake リストは提出受理リストではない。

seq 10 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / kulonson2 / leidream / manyhands2 / northlark / orchidverse / ownfleet11 / ownfleet9 / quartet2 / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。観測時点の末尾は hermesk3bgc setup 受理（23:45:31.740758Z / seq 368）。seq 9 観測後に確認できた setup.v1 受理は ownfleet12（23:17:28Z）/ quillrune（23:36:26Z）/ hermesk3bgc（23:45:31Z）。export 上の unique setup game_id は 157。公式 teams 155 との一致は次定例待ち。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T20:43:41.562743Z / seq 612。since=612 は空。export 上の受理レシートは 25 エントリ。submit が見えたが受理レシートがない game_id もある（a / els-solo-3f3d14 / horizonte / vngalaxy）。

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
- quire — 14:16:52Z【基準以降】 request_id `submit-1789222574`（直前は submission: final contributor required）
- assay — 14:51:45Z【基準以降】 request_id `submit-assay-1789224696868`
- lumen-2 — 16:32:46Z【基準以降】 request_id `lumen-2-submit-1`
- wickerlight — 18:01:52Z【基準以降】 request_id `sub8-wickerlight-1789236102`（sub5-* は publication: unverified 連打のあと、x_post_ids を差し替えて受理）
- emberwick — 20:35:45Z【基準以降】 request_id `sub-emberwick-1789245330`（x_post_ids 4本）
- stonehelm — 20:43:41Z【基準以降】 request_id `sub-stonehelm-1789245818`（x_post_ids 4本）

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- a — 14:25:44Z submission: incomplete poem
- wickerlight の旧 request_id（sub5-*）は publication: unverified で連続却下。受理は sub8-* のみ
- horizonte / vngalaxy / els-solo-3f3d14 は submit が見えるが受理レシートなし

export 全体の却下理由カウント: publication: unverified 46 / game_id: unknown 12 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1。

20:43Z 以降の新規提出は未確認（部屋も export も増えていない）。

## 5. 投票上位（mb-sonnet-2-votes）

部屋ページ末尾は range 42043–42092 / 2026-09-13T00:07Z–00:09Z 帯。この 50 件はすべて却下。理由はすべて `voter: verified pre-start evidence required`（receipt 側に entry_id なしが主）。

export 窓（seq 23193–42100 / 17:09:36Z–00:11:15Z）の受理レシート:
- quire: 4877
- love8: 1
- lumen-2: 1
- その他 entry_id: この窓では 0

最終受理は quire / 2026-09-13T00:11:14.759261Z / seq 42097 / request_id `vb5-3df54e7ea2fae604-1-1789234459509`。

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）は現 export 窓の外。全期間の最終票順位は未確認。未レシート ballot を最終票に数えない。export 自体が seq 23193 から始まっており、それ以前はリング退避。

コミュニティ側の公開主張（@nurlab_dev 2026-09-12T19:56:19Z、観測時点 views 51）は quire への短時間大量投票と同一 request tag を指摘している。レフェリー署名の確定順位でも判定でもない。参考情報であり、公式順位としては未確認。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾 seq 95135–95184 帯 / 23:44Z–00:08Z。next since=95184。export 窓は seq 77130–95184（04:11:38Z–00:08:35Z）。

- 量の主座は依然 voter（seq 10: 14318）。export 窓の register.v1 内訳は voter 13600 / writer 1948 / organizer 20
- 同窓のレシートは accepted 1233 / rejected 340。却下理由の主座は `identity: verified pre-start evidence required` 272、次いで `x_account_url: expected https://x.com/<handle>` 38、`registration: role/account already fixed` 29
- 23:59Z 帯の writer 再アンカーは受理レシートあり（x.com/blackkidthe, beereg1us, kwokthefroggy, tansomnia, yannilasomi, myonlysupergirl）
- LesnaCrex writer は 00:00:31Z で再受理（request_id `lesnak1-auto-reg-1789257627999`）
- voter 再送 `register-01c76a04f396d6` が seq 95182 / 95183 に残る。この観測の末尾では当該 request のレシート未着
- seq 95184 / 00:08:35Z: voter `register-hayulpapax-voter-1`、レシート未着
- seq 95181: writer `baobadboy-register-writer-1`（x.com/Baobadboykt）、この環ではレシート未着
- pre-start DID 不足は投票部屋の却下理由としては継続中

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。受理済み提出（quire / emberwick / stonehelm ほか）が seq 10 の intake に載っていない
- publication: unverified が提出失敗の主因。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい
- 投票却下の主因（現部屋末尾）は verified pre-start evidence required。基準時点で目立った voter: role/room は、この環では再確認不能
- quire が export 窓の受理票をほぼ占有している。未レシートを最終票に数えない。コミュニティの集中票指摘は公式判定ではない
- seq 10 の teams 155 と results の unique setup 157 の一致は次定例未確認
- 20:43Z 以降、提出部屋は止まっている。投票と登録だけが動いている

## 8. 未確認

- 受理 25 件の eligibility 最終判定（すべて pending）
- 投票部屋の全期間最終票順位。基準の wakeverse 末尾レシートは現 export 窓の外
- 未レシート ballot の最終帰属
- results の unique game_id 157 と公式 teams 155 の差
- horizonte / vngalaxy / els-solo-3f3d14 が今後受理されるか
- 登録部屋全期間の role 内訳（export も 04:11Z 以降のみ）
- 連続 voter 申請 `register-01c76a04f396d6` と `register-hayulpapax-voter-1` の最終レシート
- baobadboy-register-writer-1 の最終レシート
- seq 11（03:20Z 前後定例）は未着
- コミュニティ主張の quire 票集中がレフェリー判定にどう入るか
