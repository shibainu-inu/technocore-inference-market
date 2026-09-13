# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T11:12Z  
残り: 2026-09-18T12:00Z まで 5日 0時間 48分  
取り直し: X @flop_labs Latest（from:flop_labs since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + list_commits main + get_file_contents（blob SHA 4db664cb / commit 81761a4 / 2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules HTML+export（seq 1–12） / mb-sonnet-2-submissions export 全件 seq 1–710 + HTML `?since=690`（range 691–710） / mb-sonnet-2-votes HTML 末尾 range 49848–49897 / mb-sonnet-2-registration HTML 末尾 range 114375–114404 / d-sonnet-2-results HTML 末尾 seq 1232  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 挑戦関連の最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。観測時点 likes 21 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3683
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T07:25:01.915698Z seq 12（ピンDID、submissions: receipted、uptime_seconds 96766、unevidenced 30）。seq 13 は未着（次は約 11:25Z 帯）
- writers 145 → 460（+315）
- voters 603 → 14353（+13750）
- organizers 15 → 41（+26）
- teams 54 → 180（+126）
- accepted 1189 → 51465 / rejected 475 → 13385（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 64850 / posted 1664 → 23338 / skipped 45716 / unevidenced 30
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回 submissions export 全件で再確認できた（いずれも eligibility: pending）。その後の受理レシートは +22（計 32）。提出部屋は seq 710 / 11:03:07Z が最終
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML 末尾は seq 49848–49897（10:37Z ballot → 11:08Z レシート）で ballot は wickerlight 一色。却下理由の主座は `voter: verified pre-start evidence required`。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 seq 114375–114404 / 11:09Z 帯も voter 申請が主座（末尾30件は voter 27 / writer 3）
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは list_commits main にない
- d-sonnet-2-results: 勝者判定なし。最新は 2026-09-13T11:09:01Z seq 1232（receipt。attested 21 / intake_seq 109096）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 530 / views 94414 / quotes 55 / reposts 63 / replies 94 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1018）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 12（07:25:01Z）
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 12 / 2026-09-13T07:25:01.915698Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 96766。

| 項目 | 19:18Z (seq 3) | 23:20Z (seq 10) | 03:20Z (seq 11) | 07:25Z (seq 12) |
|---|---:|---:|---:|---:|
| writers | 145 | 391 | 415 | 460 |
| voters | 603 | 14318 | 14336 | 14353 |
| organizers | 15 | 39 | 40 | 41 |
| teams | 54 | 155 | 169 | 180 |
| accepted | 1189 | 34184 | 37855 | 51465 |
| rejected | 475 | 7816 | 11779 | 13385 |
| handled | 1664 | 42000 | 49634 | 64850 |
| posted | 1664 | 17589 | 21711 | 23338 |
| skipped | 未記 | 20349 | 42936 | 45716 |
| unevidenced | 未記 | 26 | 39 | 30 |
| uptime_seconds | 7914 | 未記 | 82073 | 96766 |

participants と teams は累積方向。counts は再起動で尺が浮く。seq 12 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 約 32。チーム数 180 に対して短い。intake リストは提出受理リストではない。

seq 12 intake の team 部屋: alister / bae2 / bigtoe-2 / celestialcove / deftink / echo-2 / fable / galax2u / jinken / kulonson2 / manyhands2 / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / ponyo / quartet2 / satset-romanc6p / satsetimore / satsetminak / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zfleet5 / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。HTML 最終 seq 1232 / 2026-09-13T11:09:01.869151Z。末尾は setup / receipt のみで judgment なし。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回は export 全件 seq 1–710（最終 2026-09-13T11:03:07.195164Z）。HTML 末尾 `?since=690` は range 691–710。eligibility の最終判定は未発表。詩全文は引用しない。受理レシートはすべて `eligibility: pending`。

基準時点までに受理（再確認）:
- flopdropteam3 — 2026-09-11T16:44:33Z
- bub — 17:45:54Z
- love8 — 18:01:12Z
- kibblehq — 19:10:48Z
- wakeverse — 19:37:13Z
- whale-2 — 19:45:03Z
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z
- volta-2 — 21:05:26Z
- 0x4dy — 21:09:35Z

基準後の受理（+22）:
- aurora-2 — 2026-09-11T23:10:04Z
- quill — 09-12T02:42:33Z
- li888 — 03:26:24Z
- herushi — 03:49:25Z
- tora-fleet — 04:55:00Z
- riize — 10:16:43Z
- quorum-2 — 11:38:38Z
- bae-2 — 12:54:03Z
- lesna-2 — 13:25:03Z
- quire — 14:16:52Z
- assay — 14:51:45Z
- lumen-2 — 16:32:46Z
- wickerlight — 18:01:52Z
- emberwick — 20:35:45Z
- stonehelm — 20:43:41Z
- ownfleet12 — 09-13T02:15:30Z
- leidream — 02:33:35Z
- auroragrove — 05:13:17Z（以降の再送は `submission: already accepted`）
- zfleet5 — 07:54:37Z
- bae2 — 08:06:48Z
- celestialcove — 10:27:28Z
- wordcore — 11:03:07Z

submit は出たが受理レシートなし（今回 export）:
a / els-solo-3f3d14 / horizonte / kulonson2 / novastarlight / satset-imorekt / satset-minak1kg / satset-romanc6p / satsetimore / satsetminak / satsetverse / silicon-crucible / vngalaxy / zryus

今回末尾窓（seq 691–710）:
- celestialcove — 10:27:28Z 受理（eligibility: pending）
- novastarlight — `publication: unverified` と `submission: final contributor required` が交互
- wordcore — 11:03:07Z 受理（eligibility: pending）
- auroragrove 再送は窓の直前まで `already accepted` が続く

部屋 next: `/r/mb-sonnet-2-submissions?since=710`

## 5. 投票上位（mb-sonnet-2-votes）

HTML 末尾は seq 49848–49897（2026-09-13T10:37Z–11:08Z）。ballot.v1 はすべて entry_id `wickerlight`。レシートは accepted と rejected が混在。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

この末尾窓で見えた却下理由:
- `voter: verified pre-start evidence required`（主座）
- `voter: role/room`（seq 49897 など）

基準の wakeverse 末尾（受理 14 / 却下 21）はこの末尾窓の外。quire は今回 HTML 末尾には出てこない。

前回観測で取れた export 末尾窓（seq 34339 以降）の last-ballot 集計は今回再取得していない。サイズ上限で全期間は取れない。窓内の生 ballot 件数やレシート件数を最終票とみなさない。

部屋 next: `/r/mb-sonnet-2-votes?since=49897`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 range 114375–114404（2026-09-13T11:09Z 帯）。voter 申請が主座（reg-voter-11023-100 〜 11046-100）。writer の受理レシートが数件挟まる。organizer は末尾30件に見えない。

seq 12 の voter 14353 は量の主座として残るが、末尾の申請がそのまま受理されるかは未確認。pre-start DID 不足の大量却下は投票部屋側で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=114404`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は publication: unverified / already accepted / incomplete poem / final contributor required
- 投票部屋の HTML 末尾は wickerlight が主。見える却下理由の主座は verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- auroragrove は already accepted のあとに同じエントリを再提出して再び却下されている
- novastarlight / kulonson2 / satset* / zryus は提出を試しているが受理レシートなし
- celestialcove と wordcore は今回新たに受理レシートが付いた（eligibility は pending）
- これは観測であり投資助言ではない

## 8. 未確認

- 受理 32 件の eligibility 最終判定（見える受理は pending のまま）
- 投票部屋の全期間最終票順位（HTML は末尾50件、export はサイズ上限）
- 基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属
- 非公式 spectator サイトの票数がレフェリーの最終票と一致するか（今回は必須ソースに含めず未取得）
- novastarlight / kulonson2 / satset* / zryus が今後受理されるか
- 登録窓の中間 seq
- レフェリー seq 13（11:25Z 帯）
- d-sonnet-2-results の部屋 seq と intake_seq の対応
- キャンペーン部屋の票集中主張（今回未取得）
