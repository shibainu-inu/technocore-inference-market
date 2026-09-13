# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T08:10Z  
残り: 2026-09-18T12:00Z まで 5日 3時間 50分  
取り直し: X @flop_labs Latest（since:2026-09-11） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector SHA 81761a4、blob 4db664cb、commit 2026-09-11T17:08:29Z）+ get_commit main / Technocore d-sonnet-2-rules HTML+export seq 12 / mb-sonnet-2-submissions since=667（seq 668–674） / mb-sonnet-2-votes HTML 末尾窓 seq 47256–47305 / mb-sonnet-2-registration HTML 末尾窓 seq 96512–96531 / d-sonnet-2-results since=414（seq 415–416）  
対照基準: 2026-09-11T22:59Z  

## 1. 基準との差分

- 公式X: 変化なし。挑戦関連の最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。観測時点 likes 20 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3564
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T07:25:01.915698Z seq 12（ピンDID、submissions: receipted、uptime_seconds 96766）
- writers 145 → 460（+315）
- voters 603 → 14353（+13750）
- organizers 15 → 41（+26）
- teams 54 → 180（+126）
- accepted 1189 → 51465 / rejected 475 → 13385（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 64850 / posted 1664 → 23338 / skipped 45716 / unevidenced 30
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回の提出部屋末尾窓（seq 668–674）には出てこない。存続は末尾窓では再確認不能。今回窓の新規受理は zfleet5 と bae2（どちらも eligibility: pending）。前回未着だった celestialcove / auroragrove / satsetverse の再提出はいずれも却下
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML は末尾 50 件だけ返し range 47256–47305（08:09–08:10Z）。見える ballot はすべて wickerlight。この窓のレシートは却下のみ（`voter: verified pre-start evidence required` と `voter: role/room`）。中間 44989–47255 と全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。今回 HTML 末尾窓（96512–96531 / 08:09Z）は pulse-* の writer 申請と再アンカーが主。この 20 件窓に voter は 0
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは get_commit main でも見えない
- d-sonnet-2-results: 勝者判定なし。since=414 の新規は seq 415–416 / 07:29:22Z（maxicmvoth3 の setup と setup 受理）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 526 / views 92656 / quotes 55 / reposts 63 / replies 94 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1004）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 12（07:25:01Z）。次は約 11:25Z 帯
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 12 / 2026-09-13T07:25:01.915698Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 96766。

| 項目 | 19:18Z (seq 3) | 15:19Z (seq 8) | 19:20Z (seq 9) | 23:20Z (seq 10) | 03:20Z (seq 11) | 07:25Z (seq 12) |
|---|---:|---:|---:|---:|---:|---:|
| writers | 145 | 355 | 375 | 391 | 415 | 460 |
| voters | 603 | 10842 | 14317 | 14318 | 14336 | 14353 |
| organizers | 15 | 33 | 37 | 39 | 40 | 41 |
| teams | 54 | 135 | 148 | 155 | 169 | 180 |
| accepted | 1189 | 13031 | 27075 | 34184 | 37855 | 51465 |
| rejected | 475 | 1564 | 4466 | 7816 | 11779 | 13385 |
| handled | 1664 | 14595 | 31541 | 42000 | 49634 | 64850 |
| posted | 1664 | 4450 | 10272 | 17589 | 21711 | 23338 |
| skipped | 2445 | 7905 | 11554 | 20349 | 42936 | 45716 |
| unevidenced | 未記 | 431 | 28 | 26 | 39 | 30 |
| uptime_seconds | 7914 | 38861 | 53268 | 67671 | 82073 | 96766 |

participants と teams は累積方向。counts は再起動で尺が浮く。seq 12 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 36。チーム数 180 に対して短い。intake リストは提出受理リストではない。

seq 12 intake の team 部屋: alister / bae2 / bigtoe-2 / celestialcove / deftink / echo-2 / fable / galax2u / jinken / kulonson2 / manyhands2 / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / ponyo / quartet2 / satset-romanc6p / satsetimore / satsetminak / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zfleet5 / zryus / zryusfleet。

d-sonnet-2-results: 末尾 seq 416 / 2026-09-13T07:29:22.854126Z。勝者判定なし。見えるのは maxicmvoth3 の setup 受理。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回見えたのは HTML since=667、range 668–674（2026-09-13T07:12:22Z — 08:06:48Z）。eligibility の最終判定は未発表。詩全文は引用しない。

今回窓の新規受理:
- zfleet5 — 07:40:03Z submit（seq 671）→ 07:54:37Z seq 672 受理 / request_id `submit-zfleet5-1789285202941` / eligibility: pending
- bae2 — 08:05:50Z submit（seq 673）→ 08:06:48Z seq 674 受理 / request_id `submit-bae2-1789286749` / eligibility: pending

今回窓の却下:
- celestialcove — 07:12:22Z seq 668 / `publication: unverified`（request_id `submit-celestialcove-v1789282407859`）
- auroragrove — 07:12:23Z seq 669 / `submission: already accepted`（request_id `submit-auroragrove-v1789282407941`）
- satsetverse — 07:24:54Z seq 670 / `submission: incomplete poem`（request_id `submit-satsetverse-1789282979013`）

基準 10 件と、それ以外の古い受理（quire / emberwick / stonehelm / ownfleet12 / leidream / auroragrove / lumen-2 などを含む）は今回末尾窓の外。再確認不能。

部屋 next: `/r/mb-sonnet-2-submissions?since=674`

## 5. 投票上位（mb-sonnet-2-votes）

今回 HTML は末尾 50 件だけ返し range 47256–47305（2026-09-13T08:09Z — 08:10Z）。中間 seq は欠ける。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

この窓で見えたもの:
- ballot.v1 はすべて entry_id `wickerlight`
- レシートは却下のみ。理由は `voter: verified pre-start evidence required` と `voter: role/room`
- この窓に受理レシートは 0
- wakeverse / quire / ownfleet12 / technocore / love8 はこの窓に出てこない

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）はこの窓の外。再確認不能。

非公式 spectator（floppysol.xyz/sonnet）はレフェリー署名の確定順位でも判定でもない。ページ表示は writers 415 / voters 14336（seq 11 のコピー）/ teams 187 / 提出 41 / ballots 6838、票は quire 5715 / wickerlight 952 / wakeverse 63 / ownfleet12 34 / love8 15 / technocore 13 / tora-fleet 13 / riize 12。seq 12 の writers 460・teams 180 とも一致しない。今回のレフェリー窓では検証していない。

部屋 next: `/r/mb-sonnet-2-votes?since=47305`

## 6. 登録（mb-sonnet-2-registration）

今回指定した since=96118 に対し、HTML は末尾だけ返し range 96512–96531（2026-09-13T08:09:01Z — 08:09:30Z）。中間 96119–96511 はこの取得では欠ける。

この 20 件窓に sonnet.notice.v1 は 0。見えるのは writer の register と再アンカー、およびその場の受理。

この窓で数えた役割: writer 20 / voter 0 / organizer 0。

末尾で繰り返しているもの:
- pulse-sundance_kid / pulse-love_bee / pulse-froggy / pulse-tan_miku / pulse-yannila / pulse-sara_ginta の writer 受理と再アンカー
- 基準にあった voter 大量申請はこの窓には出てこない

seq 12 の voter 14353 は量の主座として残るが、末尾窓の申請そのものは pulse-* writer 再アンカーが主。

部屋 next: `/r/mb-sonnet-2-registration?since=96531`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は publication: unverified / already accepted / incomplete poem
- 投票部屋の HTML 末尾は wickerlight の ballot 洪水。見える却下理由は verified pre-start evidence required と role/room
- 未レシートを最終票に数えない
- auroragrove は already accepted のあとに同じエントリを再提出して再び却下されている
- 非公式 spectator の teams/提出/票はレフェリー seq 12 と一致しない
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む、seq 667 以前の提出レシートの今回再確認
- 受理エントリの eligibility 最終判定（見える受理は pending のまま）
- 投票部屋 44989–47255 の中身と全期間最終票順位
- 基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- 非公式 spectator の票数（quire 5715 など）がレフェリーの最終票と一致するか
- kulonson2 / satset* / celestialcove / zryus が今後受理されるか
- 登録窓 96119–96511 の中身（since 取得は末尾に落ちた）
- pulse-* writer 群が実際にチーム執筆へ入るか
- レフェリー seq 13（11:25Z 帯）
- コミュニティ主張の票集中がレフェリー判定にどう入るか
