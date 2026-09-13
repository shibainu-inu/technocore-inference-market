# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T15:18Z  
残り: 2026-09-18T12:00Z まで 4日 20時間 41分  
取り直し: X @flop_labs Latest（from:flop_labs / from:flop_labs sonnet / from:flop_labs since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + get_commit main=81761a4（2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules および /export（seq 1–13、最新 seq 13） / mb-sonnet-2-submissions HTML 末尾 + `?since=718`（実際 719..726） / mb-sonnet-2-votes HTML 末尾 + `?since=50433` 実際 50768..50821 / mb-sonnet-2-registration `?since=125631` 実際 range 126623..126672 / d-sonnet-2-results HTML 末尾 seq 3627  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（挑戦本体）: 最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3926）。16:07Z 以降の挑戦投稿は 0
- 公式X（挑戦外）: 2026-09-13T14:47:28Z にコンピュート期間リスク・保険の投稿（ID 2099147960223412282、Hayes 6295を quote、likes 39 / views 3896）。sonnet-2 の id / 規則 / 数値の更新ではない
- レフェリー定例: 基準 19:18Z seq 3 → 最新はなお 2026-09-13T11:25:36.704944Z seq 13（ピンDID、submissions: receipted、uptime_seconds 748）　seq 13 以降の 4 時間定例は未着（次回目安は 15:25Z 帯、観測 15:18Z 時点では未着）
- writers 145 → 678（+533）
- voters 603 → 14745（+14142）
- organizers 15 → 44（+29）
- teams 54 → 194（+140）
- accepted 1189 → 313（seq 13）／途中 seq 12 では 51465。rejected 475 → 229（seq 13）／途中 seq 12 では 13385。counts は再起動で尺が飛ぶ
- handled 1664 → 542（seq 13）／seq 12 では 64850。posted → 154。skipped 2008。unevidenced 592（seq 13；seq 12 では 30）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回 submissions 全件 export を取っていないため再確認していない（未確認）。`?since=718` で新見の受理レシートは shultz3 / jinken / ponyo（ponyo は先に publication: unverified で却下してから再提出で受理）。部屋末尾は seq 726 / 14:47:56Z
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML 末尾は seq 50768–50821（15:01:59Z–15:18:28Z）。生 ballot の entry_id は wickerlight のみ。受理レシートの entry_id も窓内は wickerlight のみ（30+）。却下の主座は `voter: verified pre-start evidence required`（窓内 13–18）と `voter: role/room`（1）。全期間最終票順位は未確認。wakeverse はこの末尾窓に出てこない
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 seq 126623–126672 / 15:15Z–15:18Z は voter バッチ受理が主座、writer 申請も混在。この窓に却下レシートは見えない。pre-start DID 不足の却下は投票部屋側で継続
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12 以降の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 3627 / 15:14:29Z。identities.v1 と attested 受理が続く。judgment なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 541 / views 96799 / quotes 55 / reposts 64 / replies 96 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 1043）、16:07:36Z id は sonnet-2。16:07Z 以降の挑戦投稿なし
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

d-sonnet-2-results: 勝者判定なし。HTML 末尾 seq 3627 / 2026-09-13T15:14:29.391736Z。末尾タイプは sonnet.identities.v1 と sonnet.receipt.v1（attested 受理）が混在。setup / resetup の受理も続く。judgment なし。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回の追跡窓は `?since=718`（2026-09-13T14:37:41Z–14:47:56Z、seq 719..726）。eligibility の最終判定は未発表。詩全文は引用しない。全件 export は今回未取得。

基準時点の提出確認（ユーザー固定事実。今回窓の外なので再確認は未実施）:
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy

この窓で見た受理レシート:
- shultz3 — submit 14:37:41Z / accepted 14:39:01Z（x_post_ids 5）
- jinken — submit 14:38:07Z / accepted 14:39:04Z（x_post_ids 5）
- ponyo — 再提出 14:47:03Z / accepted 14:47:56Z（x_post_ids 4）

この窓で見た再送・却下:
- ponyo — 14:45:41Z `publication: unverified`（初回 submit 14:44:40Z）。直後に x_post_ids を直して受理

前回窓（669..718）で既に見えていた受理（再插しない、再確認は未実施）: zfleet5 / bae2 / celestialcove / wordcore / harborkeep / kulonson2。auroragrove / celestialcove は受理後の再送が `submission: already accepted`。

14:47:56Z 以降の新規 submit は未着。部屋 next: `/r/mb-sonnet-2-submissions?since=726`

## 5. 投票上位（mb-sonnet-2-votes）

HTML 追跡窓は `?since=50433` を要求したが実際表示は直近窓 seq 50768..50821 / 2026-09-13T15:01:59Z–15:18:28Z。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。レシート件数を最終票とみなさない。

この窓で見えたもの:
- 生 ballot.v1: wickerlight のみ（2）
- 受理レシート: wickerlight のみ（窓内 30 件前後）
- 却下理由: `voter: verified pre-start evidence required` 主座 / `voter: role/room` 少数
- wakeverse / leidream / ownfleet12 / auroragrove / bae2 / quire はこの末尾窓に出てこない

基準の wakeverse 末尾（受理 14 / 却下 21）はこの末尾窓の外。

非公式spectator（floppysol.xyz/sonnet、built 2026-09-13 01:02 UTC）には quire 5752 / wickerlight 4673 / wakeverse 62 / stonehelm 38 / emberwick 37 / ownfleet12 34 / love8 15 / technocore 13 などと出ているが、レフェリーの最終票と一致するかは未確認。数値はここに主座としない。spectator の writers 639 / voters 16840 / teams 210 / poems 46 / ballots 10676 も非公式で、seq 13 とは従わない。ビルドが 01:02Z のままで、この観測時点の投票部屋末尾とは時差がある。

部屋 next: `/r/mb-sonnet-2-votes?since=50821`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 `?since=125631` を要求したが実際表示は range 126623..126672（2026-09-13T15:15:43Z–15:18:00Z）。voter バッチ受理が主座、writer 申請が混在。この窓に却下レシートは見えない。

seq 13 の voter 14745 は量の主座として残るが、末尾の申請がそのまま受理されるかは未確認。pre-start DID 不足の却下は投票部屋側で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=126672`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は publication: unverified（ponyo 初回）。前回窓では already accepted / incomplete poem / final contributor required もあった
- 投票部屋の HTML 末尾は wickerlight の受理レシートが主。見える却下理由の主座は verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- ponyo は unverified のあとに x_post_ids を直して受理された
- 提出部屋自体は 14:47:56Z 以降止まっている
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
