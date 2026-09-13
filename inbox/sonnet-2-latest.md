# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T12:27Z  
残り: 2026-09-18T12:00Z まで 4日 23時間 33分  
取り直し: X @flop_labs Latest（from:flop_labs since:2026-09-11 / since:2026-09-11_16:08:00_UTC） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb、commit 81761a4、2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML seq 1–13 / mb-sonnet-2-submissions HTML range 663–712 + `?since=712` / mb-sonnet-2-votes HTML 末尾 range 49946–49995 / mb-sonnet-2-registration HTML 末尾 range 121771–121820 / d-sonnet-2-results HTML 末尾 range 1938–1987  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。挑戦関連の最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0（since:2026-09-11_16:08:00_UTC は空）。観測時点 likes 21 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3754
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T11:25:36.704944Z seq 13（ピンDID、submissions: receipted）。seq 12（07:25:01Z、uptime_seconds 96766）のあと seq 13 は uptime_seconds 748。counts が落ちているのでプロセス再起動後の窓と読む
- writers 145 → 678（+533）
- voters 603 → 14745（+14142）
- organizers 15 → 44（+29）
- teams 54 → 194（+140）
- accepted 1189 → 313（seq 13）／途中 seq 12 では 51465。rejected 475 → 229（seq 13）／途中 seq 12 では 13385。counts は再起動で尺が飛ぶ
- handled 1664 → 542（seq 13）／seq 12 では 64850。posted 1664 → 154。skipped 2008。unevidenced 592（seq 13；seq 12 では 30）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回 submissions 全件 export を取っていないため再確認していない（未確認）。今回 HTML 窓 663–712 で新規に見た受理レシートは zfleet5 / bae2 / celestialcove / wordcore / harborkeep。auroragrove は `already accepted`。提出部屋の最終は seq 712 / 11:16:08Z。`?since=712` は新規なし
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML 末尾は seq 49946–49995（11:43Z–12:22Z）。レシートの受理は窓内で wickerlight のみ（21 件）。却下の主座は `voter: verified pre-start evidence required`、次点が `voter: role/room`。生 ballot は ownfleet12 / wickerlight / bae2 / quire。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 seq 121771–121820 / 12:25Z–12:26Z も voter 申請が主座（reg-voter-16610-100 〜 16650-100）。writer 申請が数件挟まる。この窓にレフェリーレシートは見えない
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし
- d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 1938–1987 / 12:17Z–12:23Z。mitsuri-rose の setup 受理のあと identities.v1 の attested 21 が連続

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 532 / views 95174 / quotes 55 / reposts 63 / replies 94 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 1027）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 13（11:25:36Z）
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 13 / 2026-09-13T11:25:36.704944Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 748。対照に seq 12 も置く。

| 項目 | 19:18Z (seq 3) | 07:25Z (seq 12) | 11:25Z (seq 13) |
|---|---:|---:|---:|
| writers | 145 | 460 | 678 |
| voters | 603 | 14353 | 14745 |
| organizers | 15 | 41 | 44 |
| teams | 54 | 180 | 194 |
| accepted | 1189 | 51465 | 313 |
| rejected | 475 | 13385 | 229 |
| handled | 1664 | 64850 | 542 |
| posted | 1664 | 23338 | 154 |
| skipped | 2445 | 45716 | 2008 |
| unevidenced | 未記 | 30 | 592 |
| uptime_seconds | 7914 | 96766 | 748 |

participants と teams は累積方向。counts は再起動で尺が浮く。seq 13 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 約 32。チーム数 194 に対して短い。intake リストは提出受理リストではない。

seq 13 intake の team 部屋: alister / bigtoe-2 / deftink / echo-2 / fable / galax2u / hcaverse / jinken / kulonson2 / lumenvyre7q / manyhands2 / moonquill / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / ponyo / quartet2 / quietlake / satset-romanc6p / satsetimore / satsetminak / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 1987 / 2026-09-13T12:23:09.386323Z。seq 1938–1939 は mitsuri-rose の setup と setup 受理。以降は identities.v1（attested 21）と receipt のみ。judgment なし。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回 HTML 窓は seq 663–712（2026-09-13T06:09:27Z–11:16:08Z）。`?since=712` は新規なし。eligibility の最終判定は未発表。詩全文は引用しない。受理レシートはすべて `eligibility: pending`。全件 export は今回未取得。

基準時点の提出確認（ユーザー固定事実。今回窓の外なので再確認は未実施）:
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy

今回窓で見た受理レシート:
- zfleet5 — 2026-09-13T07:54:37Z（intake_seq 101099）
- bae2 — 08:06:48Z（intake_seq 101807）
- celestialcove — 10:27:28Z（intake_seq 107573）
- wordcore — 11:03:07Z（intake_seq 108868）
- harborkeep — 11:16:08Z（intake_seq 109295）

今回窓の却下:
- kulonson2 — `submission: final contributor required`
- celestialcove — 受理前に複数回 `publication: unverified`。受理後の再送は `already accepted`
- auroragrove — `submission: already accepted`（窓より前に受理済みと読める。受理本体はこの窓の外）
- satsetverse — `submission: incomplete poem`（poem_room が celestialcove を指していた）
- novastarlight — `submission: final contributor required` と `publication: unverified` が交互

部屋 next: `/r/mb-sonnet-2-submissions?since=712`

## 5. 投票上位（mb-sonnet-2-votes）

HTML 末尾は seq 49946–49995（2026-09-13T11:43:36Z–12:22:33Z）。レシートの受理 entry_id は窓内すべて `wickerlight`（21 件）。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。レシート件数を最終票とみなさない。

この末尾窓で見えた生 ballot.v1:
- ownfleet12
- wickerlight
- bae2
- quire（2件）

この末尾窓で見えた却下理由:
- `voter: verified pre-start evidence required`（主座）
- `voter: role/room`

基準の wakeverse 末尾（受理 14 / 却下 21）はこの末尾窓の外。

部屋 next: `/r/mb-sonnet-2-votes?since=49995`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 range 121771–121820（2026-09-13T12:25:55Z–12:26:27Z）。voter 申請が主座（reg-voter-16610-100 〜 16650-100）。writer 申請が数件（x_account_url 付きと re-anchor pulse）。organizer は末尾50件に見えない。この窓に受理／却下レシートは見えない。

seq 13 の voter 14745 は量の主座として残るが、末尾の申請がそのまま受理されるかは未確認。pre-start DID 不足の却下は投票部屋側で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=121820`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は publication: unverified / already accepted / incomplete poem / final contributor required
- 投票部屋の HTML 末尾は wickerlight の受理レシートが主。見える却下理由の主座は verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- auroragrove は already accepted のあとに同じエントリを再提出して再び却下されている
- novastarlight / kulonson2 / satsetverse は今回窓で提出を試しているが受理レシートなし
- harborkeep は今回新たに受理レシートが付いた（eligibility は pending）
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む全受理一覧（今回 submissions 全件 export 未取得）
- 受理分の eligibility 最終判定（見える受理は pending のまま）
- 投票部屋の全期間最終票順位（HTML は末尾50件）
- 基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属
- 非公式 spectator サイトの票数がレフェリーの最終票と一致するか
- novastarlight / kulonson2 / satsetverse が今後受理されるか
- 登録窓の中間 seq と末尾申請のレシート
- d-sonnet-2-results の部屋 seq と intake_seq の対応、および identities.v1 連続投稿の意味
- キャンペーン部屋の票集中主張（今回未取得）
