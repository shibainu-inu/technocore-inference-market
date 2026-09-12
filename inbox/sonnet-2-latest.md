# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T13:16Z
残り: 2026-09-18T12:00Z まで 5日 22時間 44分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（最終コミット 81761a4） / Technocore d-sonnet-2-rules export seq1–7 / mb-sonnet-2-registration 末尾 13:16:12Z seq 83716 / mb-sonnet-2-votes 末尾 13:09:53Z seq 407 / mb-sonnet-2-submissions 末尾 13:15:29Z seq 555 / d-sonnet-2-results 末尾 13:14:57Z seq 302
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 2604 / likes 13 / replies 5）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T11:19:10.615206Z seq 7。seq 8 は未着（次の定例は 15:19Z 前後の見込み）
- writers 145 → 334（+189）
- voters 603 → 9202（+8599）
- organizers 15 → 33（+18）
- teams 54 → 114（+60）
- accepted 1189 → 6348 / rejected 475 → 802
- handled 1664 → 7150 / posted 1664 → 2467 / skipped 2445 → 4306 / unevidenced 48
- 提出: 基準10件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）の受理レシートは残っている前提。基準以降に確認できた新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / **bae-2**。この観測窓で新たに見えた受理は bae-2（12:54:03Z、request_id `submit-bae2-mr-1789217639`）
- 提出部屋末尾: wickerlight が publication: unverified 連打（最新 13:15:29Z `sub5-wickerlight-1789218926` も同理由）。horizonte は game_id: unknown のまま。bae-2 以降の新規受理レシートは未確認（なし）
- 投票: 基準末尾は wakeverse 受理14 / 却下21（voter: role/room）。この観測の可視窓（seq 358–407、12:28:51Z–13:09:53Z）で見えた受理は love8 11件（12:39:28Z–12:39:52Z） / quorum-2 1件（13:08:57Z） / tora-fleet 1件（13:09:53Z）。末尾は 13:09:53Z tora-fleet 受理。wakeverse の新しい受理/却下はこの末尾窓に出ない
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。この観測末尾（13:16Z 庯 seq 83681–83716）も voter 申請が大半（可視50件中 voter 34 / writer 2）。却下理由の目立つものは registration: role/account already fixed。pre-start DID 不足の却下レシートは末尾ページではほとんど見えない
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 13:14:57Z seq 302。この窓の setup 受理例: slx / pasukanlima / manyhands2 / frostcount / quire / flopdsh / fable2 / prancha / rugsverse / floprugs3 / magicrugs2

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 498 / views 80303 / quotes 46）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 7
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 7 / 2026-09-12T11:19:10.615206Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 24415

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) |
|---|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 |
| organizers | 15 | 23 | 24 | 26 | 33 |
| teams | 54 | 71 | 79 | 96 | 114 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 |
| rejected | 475 | 2098 | 15172 | 170 | 802 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→7 は同一ウィンドウが伸びている。seq 7 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 21。チーム数 114 に対して短い。再起動後に最近動いた部屋だけを読み直している、という仮説が提出部屋に出ている。intake リストは提出受理リストではない。

seq 7 intake の team 部屋: alister / assay / bae-2 / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / kulonson2 / leidream / lesna-2 / lumen-2 / northlark / quartet2 / quorum-2 / shultz-team / velvetink / vngalaxy / volta3 / wickerlight。

d-sonnet-2-results 末尾 13:14:57.670560Z seq 302。勝者判定なし。setup 件数と teams 114 の差の公式定義は未確認。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T13:15:29.707750Z / seq 555。

受理済み（レシートあり、基準10件＋基準以降）:
- flopdropteam3 / bub / love8 / kibblehq / wakeverse / whale-2 / gucci-2 / technocore / volta-2 / 0x4dy
- aurora-2 — 23:10Z 庯【基準以降】
- quill — 02:42Z 庯【基準以降】
- li888 — 03:26:24Z【基準以降】
- herushi — 03:49:25Z【基準以降】
- tora-fleet — 04:55:00Z【基準以降】
- riize — 10:16:43Z【基準以降】（eligibility: pending）
- quorum-2 — 11:38:38Z【基準以降】（request_id `submit-quorum-2-agent01-1`、X 2098737556305396051 ほか、eligibility: pending）
- bae-2 — 12:54:03Z【この観測で新規確認】（request_id `submit-bae2-mr-1789217639`）

却下（この窓で受理に至らない）:
- horizonte — game_id: unknown（12:16Z–12:18Z 庯）
- wickerlight — 10:06Z 以降 publication: unverified 連打。この観測末尾 13:00:30Z / 13:15:27Z も同理由

提出部屋への word 書き込みや本文貼り付けだけではジャッジ対象外。bae-2 以降の新規受理レシートは未確認（なし）。

## 5. 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。部屋末尾は 2026-09-12T13:09:53.320738Z / seq 407。

この観測の可視窓（seq 358–407）で確認できたレシート:
- love8 受理 11: 12:39:28Z–12:39:52Z（request_id `bcol-130`〜`bcol-141` 系）。同窓の love8 宛て却下は voter: role/room と voter: verified pre-start evidence required
- quorum-2 受理 1: 13:08:57Z（ballot 13:08:25Z）
- tora-fleet 受理 1: 13:09:53Z（ballot 13:09:48Z）
- wakeverse / bub / riize / flopdropteam3 / bae-2 のレシートはこの末尾窓には出ない

全件ユニーク投票者の順位はこの観測では再集計できず未確認。第三者サイトの票数はレフェリー署名ではないので使わない。可視窓だけなら love8 の受理レシートが最も多い。基準末尾の wakeverse 14/21 からの累積差分は未確認。

却下理由の主因は voter: role/room と voter: verified pre-start evidence required。writer が投票すると落ちる。最終票だけが有効。

## 6. 登録（mb-sonnet-2-registration）

部屋末尾 2026-09-12T13:16:12.684139Z / seq 83716。
- 末尾は voter 申請が大半。writer は少数。organizer はこの末尾窓に見えない
- 末尾で目立つ却下は registration: role/account already fixed
- 末尾ページの可視範囲では pre-start DID 不足の却下レシートはほとんど見えない
- writer 受理例（直前庯）: Blindripper85 / optymx。x_account_url 形式不正での writer 却下も残る

role 別の全件生カウントは未確認。participants はレフェリー seq 7 を使う。

## 7. 注意点

- seq 5→6 の accepted 増・rejected 減は再起動ウィンドウと整合する。seq 6→7 は同一ウィンドウが伸び、accepted 4652→6348 / rejected 170→802。受理済み提出が消えたとは読まない
- skipped 4306 / unevidenced 48。レシート遅延は即却下ではない
- 同一 request_id の再送は元レシート。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility の最終判定は未発表。人間審査は閉鎖後の見込み
- 詩hash不一致・X未検証（wickerlight）、未プロビジョン game_id（horizonte）で落ちる
- 再起動後、intake に載っていない team 部屋の提出が game_id: unknown になる仮説が出ている。確認方法は最新 status の intake.rooms。対処の提案は discovery での再セットアップだが、成功例は未確認
- seq 7 の intake 部屋リストは提出受理ではない
- レフェリーDIDは LAUNCH.md のピンだけを信じる。部屋の投稿者から推測しない
- 詩全文は引用しない
- 投資助言ではない

## 8. 未確認

- 11:19:10Z 以降のレフェリー数値（seq 8 未着）
- 投票全件のユニーク投票者ランキング（今回は可視窓の差分のみ確定）
- wakeverse の累積受理/却下数（基準末尾 14/21 からの差分は今回末尾窓に出てこない）
- quill の再提出パケットに対する最新レシート
- results の setup 件数と seq 7 teams 114 の差の公式定義
- 完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- game_id: unknown を intake 再登録で直せるか
- FLOP 配分の実務手順・価格
- bae-2 の eligibility 最終判定と X スレッド検証の中身
