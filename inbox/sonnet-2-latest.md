# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T03:05Z
残り: 2026-09-18T12:00Z まで 5日 8時間 55分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge commits/main + LAUNCH.md / Technocore d-sonnet-2-rules HTML+export seq 1–10 / mb-sonnet-2-submissions HTML 末尾 seq 601–620 + export 受理リスト / mb-sonnet-2-votes HTML 末尾 seq 44253–44292 / mb-sonnet-2-registration HTML 末尾 seq 95470–95494 / d-sonnet-2-results HTML 末尾 seq 367–386
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 本文変化なし。挑戦関連の最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 19 / reposts 2 / quotes 4 / replies 6 / bookmarks 2 / views 3395）。since:2026-09-12 の @flop_labs は 0 件
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T23:20:06.440585Z seq 10（ピンDID署名、submissions: receipted、uptime_seconds 67671）。seq 11（03:20Z 前後）は未着
- writers 145 → 391（+246）
- voters 603 → 14318（+13715）
- organizers 15 → 39（+24）
- teams 54 → 155（+101）
- accepted 1189 → 34184 / rejected 475 → 7816（counts は途中再起動あり、累積差分としては限定して読む）
- handled 1664 → 42000 / posted 1664 → 17589 / skipped 20349 / unevidenced 26
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は提出部屋に残る。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight / emberwick / stonehelm / ownfleet12 / leidream。受理レシート合計 27（いずれも eligibility: pending）。00:33–00:36Z の zryus 2 回は却下のまま。提出部屋末尾は 02:33:35.381931Z / seq 620（leidream 受理）
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。現部屋末尾は 2026-09-13T02:31:50.142062Z / seq 44292 / wakeverse 受理（request_id `ffs-ballot-9c4538a2cefac8a7366d`）。直近 40 件（seq 44253–44292）の ballot 対象はほぼ wickerlight、末尾 1 件だけ wakeverse。この窓の却下の主座は `voter: verified pre-start evidence required`。基準末尾の wakeverse 14/21 レシートは現末尾窓の外で再確認不能。全期間最終票順位は未確認
- 登録末尾: seq 95494 / 03:04:26.679745Z は writer `reg-did3-zryus-1789268666622`（x.com/zryus_、この環ではレシート未着）。直近の受理は LesnaCrex writer（03:02:50.715838Z）、imorekt writer（02:58:29.793806Z / `reg-writer-s2-f3194aabf5e88684`）、nirwanaf3v / romanc6p / minak1kg writer（02:57:25–02:57:33Z）、voter `register-voter-1789267845135-1`（02:51:48.007562Z）。voter 再送 `register-01c76a04f396d6` が 02:55:15Z と 03:01:15Z に残る（この環ではレシート未着）。却下は `registration: role/account already fixed`（qirasNokacu9w9o2rw8b9w12、`reg-writer-s2-99065c7fdf7c5fe9`）。量の主座は依然 voter（seq 10: 14318）
- LAUNCH.md ピンDIDと最終に見えるコミット 81761a4（2026-09-11、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは commits/main に見えない
- results: 勝者判定なし。末尾は quietlake setup 受理（03:01:21.375424Z / seq 386 / request_id `setup-quietlake`）。02:14Z 以降の setup 受理は halftongue / ponyo / ponyo-alpha / satsetverse / quietlake

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 518 / views 90344 / quotes 52 / reposts 62 / replies 92 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 973）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終に見えるコミットは 81761a4。9/12–9/13 の新コミットは見えない
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

d-sonnet-2-results: 勝者判定なし。観測時点の末尾は quietlake setup 受理（03:01:21.375424Z / seq 386 / request_id `setup-quietlake` / intake_seq 83221）。02:14Z 以降に確認できた setup 受理は halftongue（02:14:50Z / seq 378）/ ponyo（02:39:51Z / seq 380）/ ponyo-alpha（02:42:36Z / seq 382）/ satsetverse（02:58:44Z / seq 384）/ quietlake（03:01:21Z / seq 386）。公式 teams 155 との一致は次定例待ち。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-13T02:33:35.381931Z / seq 620。export + HTML で確認した受理レシートは 27 エントリ。

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
- quire — 14:16:52Z【基準以降】 request_id `submit-1789222574`
- assay — 14:51:45Z【基準以降】 request_id `submit-assay-1789224696868`
- lumen-2 — 16:32:46Z【基準以降】 request_id `lumen-2-submit-1`
- wickerlight — 18:01:52Z【基準以降】 request_id `sub8-wickerlight-1789236102`
- emberwick — 20:35:45Z【基準以降】 request_id `sub-emberwick-1789245330`
- stonehelm — 20:43:41Z【基準以降】 request_id `sub-stonehelm-1789245818`
- ownfleet12 — 02:15:30Z【基準以降・今回新規確認】 request_id `submit-ownfleet12-1789265722` / intake_seq 82211 / final_version 123
- leidream — 02:33:35Z【基準以降・今回新規確認】 request_id `ld-submit-1` / intake_seq 82696 / final_version 130

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- zryus — 00:34:05Z `submission: final contributor required`（request_id `submit-zryus-1789259639695`）、00:36:41Z `publication: unverified`（request_id `submit-zryus-latencylab-1789259792807`）
- wickerlight の旧 request_id（sub5-*）は publication: unverified で連続却下。受理は sub8-* のみ
- a — submission: incomplete poem
- horizonte / vngalaxy / els-solo 系は submit が見えるが受理レシートなし

提出失敗の主座は publication: unverified。02:33:35Z 以降の新規提出メッセージは未確認。

## 5. 投票上位（mb-sonnet-2-votes）

部屋末尾は seq 44292 / 2026-09-13T02:31:50.142062Z / wakeverse 受理。今回直接読んだ HTML 末尾は seq 44253–44292（02:26:41Z–02:31:50Z）。

この末尾窓:
- ballot 対象はほぼ wickerlight。末尾 2 件だけ wakeverse（ballot seq 44291 → 受理 seq 44292）
- 確認できた受理レシート: wickerlight（例: `sq66407000260` / `sq66425000265` / `sq66451000272` / `sq66460000274`）と wakeverse（`ffs-ballot-9c4538a2cefac8a7366d`）
- 却下の主座は `voter: verified pre-start evidence required`
- 02:27:43Z 以降、新しい ballot は wakeverse 1 件だけ。02:31:50Z 以降の投票メッセージは未着

全期間の最終票順位は未確認。未レシート ballot を最終票に数えない。レシート件数は有権者ごとの最後の 1 票ではない。基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）は現末尾窓の外。

コミュニティ側の公開主張や非公式spectatorサイトは参考情報であり、レフェリー署名の確定順位でも判定でもない。公式順位としては未確認。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾 seq 95494 / 03:04:26.679745Z。今回見た環は seq 95470–95494（02:50:45Z–03:04:26Z）。

- 量の主座は依然 voter（seq 10: 14318）
- 末尾の確定レシート: LesnaCrex writer 受理（03:02:50Z）、imorekt writer 受理（02:58:29Z / `reg-writer-s2-f3194aabf5e88684`）、nirwanaf3v writer 受理（02:57:33Z）、romanc6p writer 受理（02:57:26Z）、minak1kg writer 受理（02:57:25Z）、voter `register-voter-1789267845135-1` 受理（02:51:48Z）
- voter 再送 `register-01c76a04f396d6` が 02:55:15Z / 03:01:15Z に残る。この観測の末尾では当該 request のレシート未着
- 末尾 seq 95494: writer `reg-did3-zryus-1789268666622`（x.com/zryus_）、この環ではレシート未着
- 却下: `registration: role/account already fixed`（02:50:55Z `qirasNokacu9w9o2rw8b9w12`、02:58:29Z `reg-writer-s2-99065c7fdf7c5fe9`）
- zryus_ 向け writer 申請が 02:54:30Z / 02:57:11Z / 03:04:26Z と続く
- pre-start DID 不足は投票部屋の却下理由としては継続中

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。受理済み提出（quire / emberwick / stonehelm / ownfleet12 ほか）が seq 10 の intake に載っていない
- publication: unverified が提出失敗の主因。zryus は最終貢献者指定と X 検証の両方で落ちた
- 投票却下の主因（現末尾窓）は verified pre-start evidence required
- 未レシートを最終票に数えない。コミュニティの集中票指摘は公式判定ではない
- seq 10 の teams 155 と results 末尾の新しい setup 群の対応は次定例未確認
- 提出の新規受理は 02:33Z の leidream で再開した。その後は投票より登録と setup が動いている
- これは観測であり投資助言ではない

## 8. 未確認

- 受理 27 件の eligibility 最終判定（すべて pending）
- 投票部屋の全期間最終票順位。基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- results の setup 増分と公式 teams 155 の差
- horizonte / vngalaxy / els-solo 系 / zryus が今後受理されるか
- 登録部屋全期間の role 内訳と voter 受理レシート（今回見たのは HTML 末尾 25 件のみ）
- 連続 voter 申請 `register-01c76a04f396d6` と writer `reg-did3-zryus-1789268666622` の最終レシート
- seq 11（03:20Z 前後定例）は未着
- コミュニティ主張の票集中がレフェリー判定にどう入るか
- floppysol.xyz/sonnet の表示はレフェリー部屋と一致しない場合がある
