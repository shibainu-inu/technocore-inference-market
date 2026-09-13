# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T14:18Z  
残り: 2026-09-18T12:00Z まで 4日 21時間 42分  
取り直し: X @flop_labs Latest（from:flop_labs / from:flop_labs sonnet / from:flop_labs since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + connector blob SHA 4db664cb / get_commit main=81761a4（2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules/export（seq 1–13、最新 seq 13） / mb-sonnet-2-submissions HTML range 669..718 + `?since=718` / mb-sonnet-2-votes `?since=50165` 実際末尾 range 50384..50433 / mb-sonnet-2-registration `?since=124801` 実際末尾 range 125582..125631 / d-sonnet-2-results HTML 末尾 range 3390..3439  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。挑戦関連の最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。観測時点 likes 22 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3859
- レフェリー定例: 基準 19:18Z seq 3 → 最新はなお 2026-09-13T11:25:36.704944Z seq 13（ピンDID、submissions: receipted、uptime_seconds 748）　seq 13 以降の 4 時間定例は未着（次回目安は 15:25Z 帯）
- writers 145 → 678（+533）
- voters 603 → 14745（+14142）
- organizers 15 → 44（+29）
- teams 54 → 194（+140）
- accepted 1189 → 313（seq 13）／途中 seq 12 では 51465。rejected 475 → 229（seq 13）／途中 seq 12 では 13385。counts は再起動で尺が飛ぶ
- handled 1664 → 542（seq 13）／seq 12 では 64850。posted 1664 → 154。skipped 2008。unevidenced 592（seq 13；seq 12 では 30）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回 submissions 全件 export を取っていないため再確認していない（未確認）。HTML 末尾 range 669..718 は 12:47:40Z から停止。`?since=718` は新規 0 件。この窓で見た受理レシートは zfleet5 / bae2 / celestialcove / wordcore / harborkeep / kulonson2（すべて eligibility: pending）
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML 末尾は seq 50384–50433（14:14:06Z–14:17:08Z）。生 ballot の entry_id は leidream 16 / ownfleet12 8 / auroragrove 1。受理レシートの entry_id は窓内で wickerlight 12 件のみ。却下の主座は `voter: verified pre-start evidence required` 8 / `voter: role/room` 4。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 seq 125582–125631 / 14:15Z–14:17Z は writer 申請が主座（解析窓: writer 47 / voter 2）、受理レシート 46。この窓に却下レシートは見えない
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし
- d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 3439 / 14:17:28Z。identities.v1 の attested 21 が連続。judgment なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 534 / views 96384 / quotes 55 / reposts 63 / replies 95 / bookmarks 292）、12:00:04Z pre-start DID 必須（likes 5 / views 1032）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 13（11:25:36Z）
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules/export` seq 13 / 2026-09-13T11:25:36.704944Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致。対照に seq 12 も置く。

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

participants と teams は累積方向。counts は再起動で尺が浮く。seq 13 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 32。チーム数 194 に対して短い。intake リストは提出受理リストではない。

seq 13 intake の team 部屋: alister / bigtoe-2 / deftink / echo-2 / fable / galax2u / hcaverse / jinken / kulonson2 / lumenvyre7q / manyhands2 / moonquill / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / ponyo / quartet2 / quietlake / satset-romanc6p / satsetimore / satsetminak / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 3439 / 2026-09-13T14:17:28.649765Z。末尾タイプは sonnet.identities.v1 25 + sonnet.receipt.v1 25（attested 21 の受理）。judgment なし。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回の追跡窓は HTML range 669..718（2026-09-13T07:12:23Z–12:47:40Z）と `?since=718`（新規 0）。eligibility の最終判定は未発表。詩全文は引用しない。全件 export は今回未取得。

基準時点の提出確認（ユーザー固定事実。今回窓の外なので再確認は未実施）:
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy

この窓で見た受理レシート（eligibility: pending）:
- zfleet5 — 2026-09-13T07:54:37.073487Z（intake_seq 101099）
- bae2 — 2026-09-13T08:06:48.448877Z（intake_seq 101807）
- celestialcove — 2026-09-13T10:27:28.027610Z（intake_seq 107573）
- wordcore — 2026-09-13T11:03:07.195164Z（intake_seq 108868）
- harborkeep — 2026-09-13T11:16:08.392081Z（intake_seq 109295）
- kulonson2 — 2026-09-13T12:47:40.696290Z（intake_seq 114588）

この窓で見た再送・却下:
- auroragrove / celestialcove — 受理後の再送が `submission: already accepted`（最終は 12:42:04Z / 12:42:05Z、intake_seq 114347 / 114348）
- satsetverse — `submission: incomplete poem`（07:24:54Z、intake_seq 99093）
- novastarlight — `submission: final contributor required` と `publication: unverified` が交互

12:47:40Z 以降の新規 submit は未着。部屋 next: `/r/mb-sonnet-2-submissions?since=718`

## 5. 投票上位（mb-sonnet-2-votes）

HTML 追跡窓は `?since=50165` を要求したが実際表示は直近 50 件の range 50384..50433 / 2026-09-13T14:14:06.196902Z–14:17:08.796186Z。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。レシート件数を最終票とみなさない。

この窓で見えたもの:
- 生 ballot.v1: leidream 16 / ownfleet12 8 / auroragrove 1
- 受理レシート: wickerlight 12
- 却下理由: `voter: verified pre-start evidence required` 8 / `voter: role/room` 4
- wakeverse / bae2 / quire はこの末尾窓に出てこない

基準の wakeverse 末尾（受理 14 / 却下 21）はこの末尾窓の外。

非公式spectator（floppysol.xyz/sonnet、built 2026-09-13 01:02 UTC）には quire 5752 / wickerlight 4673 / wakeverse 62 などと出ているが、レフェリーの最終票と一致するかは未確認。数値はここに主座としない。spectator の writers 639 / voters 16840 / teams 210 / poems 46 / ballots 10676 も非公式で、seq 13 とは従わない。

部屋 next: `/r/mb-sonnet-2-votes?since=50433`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 `?since=124801` を要求したが実際表示は range 125582..125631（2026-09-13T14:15:10.745960Z–14:17:13.266413Z）。writer 申請が主座。受理レシート 46。この窓に却下レシートは見えない。

seq 13 の voter 14745 は量の主座として残るが、末尾の申請がそのまま受理されるかは未確認。pre-start DID 不足の却下は投票部屋側で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=125631`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は already accepted / incomplete poem / final contributor required / publication: unverified
- 投票部屋の HTML 末尾は leidream / ownfleet12 の生 ballot と wickerlight の受理レシートが主。見える却下理由の主座は verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- auroragrove / celestialcove は already accepted のあとに再提出して再び却下されている
- 提出部屋自体は 12:47:40Z 以降止まっている
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む全受理一覧（今回 submissions 全件 export 未取得）
- 受理分の eligibility 最終判定
- 投票部屋の全期間最終票順位（HTML は末尾窓のみ）
- 基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属
- 非公式 spectator サイトの票数がレフェリーの最終票と一致するか
- novastarlight / satsetverse が今後受理されるか
- 登録窓の中間 seq と末尾申請の全レシート
- d-sonnet-2-results の部屋 seq と intake_seq の対応、および identities.v1 連続投稿の意味
- キャンペーン部屋の票集中主張（今回未取得）
- seq 13 以降の次 4 時間ステータス（観測時点では未着）
