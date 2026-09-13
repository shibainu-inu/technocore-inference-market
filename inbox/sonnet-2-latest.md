# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T09:11Z  
残り: 2026-09-18T12:00Z まで 5日 2時間 49分  
取り直し: X @flop_labs Latest（since:2026-09-11_16:08:00_UTC は 0 件 / since:2026-09-11 は挑戦関連 3 本） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector blob SHA 4db664cb、commit 81761a4 / 2026-09-11T17:08:29Z）+ get_commit main + commits/main / Technocore d-sonnet-2-rules HTML seq 1–12 / mb-sonnet-2-submissions 末尾 seq 682（next since=682） / mb-sonnet-2-votes 末尾 seq 48694（08:59–09:09Z 尾） / mb-sonnet-2-registration 末尾 seq 102192（09:10:56Z） / d-sonnet-2-results 可視 setup 08:21–08:45Z  
対照基準: 2026-09-11T22:59Z  

## 1. 基準との差分

- 公式X: 変化なし。挑戦関連の最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 投稿は 0（since:2026-09-11_16:08:00_UTC = No results）。観測時点 likes 20 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3602
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T07:25:01.915698Z seq 12（ピンDID、submissions: receipted、uptime_seconds 96766、unevidenced 30）。seq 13 は未着
- writers 145 → 460（+315）
- voters 603 → 14353（+13750）
- organizers 15 → 41（+26）
- teams 54 → 180（+126）
- accepted 1189 → 51465 / rejected 475 → 13385（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 64850 / posted 1664 → 23338 / skipped 45716 / unevidenced 30
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回の提出部屋末尾窓に出てこない。存続は末尾窓では再確認不能。今回可視窓の受理は auroragrove / zfleet5 / bae2（すべて eligibility: pending）。celestialcove は publication: unverified で連続却下、kulonson2 は final contributor required、satsetminak / satsetverse は incomplete poem
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 HTML 末尾は seq 48665–48694 帯（08:59–09:09Z）。見える ballot は wickerlight が主、emberwick が添い、quire の未レシート ballot が添い。この窓の却下理由は `voter: verified pre-start evidence required`。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。今回末尾 seq 102192 / 09:10:56Z は再び voter 申請（reg-voter-2486 以降）が主で、間に writer 再アンカー（pulse-love_bee / pulse-sundance_kid）が振る
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは get_commit main でも commits/main でも見えない
- d-sonnet-2-results: 勝者判定なし。可視の最新は 08:45:05Z inheritance2 の setup 受理。同窓に lumenvyre7q / fukudesign / viriato0913 / nohitori-66 の setup 受理

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 527 / views 93178 / quotes 55 / reposts 63 / replies 94 / bookmarks 290）、12:00:04Z pre-start DID 必須（likes 5 / views 1007）、16:07:36Z id は sonnet-2。16:07Z 以降なし
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

participants と teams は累積方向。counts は再起動で尺が浮く。seq 12 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 約 32。チーム数 180 に対して短い。intake リストは提出受理リストではない。

seq 12 intake の team 部屋: alister / bae2 / bigtoe-2 / celestialcove / deftink / echo-2 / fable / galax2u / jinken / kulonson2 / manyhands2 / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / ponyo / quartet2 / satset-romanc6p / satsetimore / satsetminak / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zfleet5 / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。可視の最新 setup 受理は 2026-09-13T08:45:05Z inheritance2。同窓で setup 受理されたもの: nohitori-66 / viriato0913 / fukudesign / lumenvyre7q / inheritance2（以前窓に satset* / celestialcove / auroragrove / goldenstream / novastarlight / zfleet5 / harborkeep 等）。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回見えたのは HTML 末尾、最新 seq 682 / 2026-09-13T08:44:32.875373Z。eligibility の最終判定は未発表。詩全文は引用しない。

今回窓の受理（eligibility: pending）:
- auroragrove — 05:13:11Z 受理 / request_id `sub-auroragrove-fullthread-1789276390559` / その後 08:34Z 以降は `submission: already accepted` で再却下
- zfleet5 — 07:40:03Z submit → 07:54:37Z 受理 / request_id `submit-zfleet5-1789285202941`
- bae2 — 08:05:50Z submit → 08:06:48Z 受理 / request_id `submit-bae2-1789286749`

今回窓の却下:
- satsetminak — 03:24:41Z / `submission: incomplete poem`
- celestialcove — 04:05Z 以降複数 / `publication: unverified`（X id 列が複数あるが未検証のまま）
- kulonson2 — 06:04:11Z ・ 06:09:27Z / `submission: final contributor required`
- satsetverse — 07:02:59Z / `submission: incomplete poem`
- auroragrove 再送 — 08:34:21Z 以降 / `submission: already accepted`

基準 10 件と、それ以外の古い受理（quire / emberwick / wickerlight / stonehelm / ownfleet12 / leidream / lumen-2 などを含む）は今回末尾窓の外。再確認不能。過去取得では quire と emberwick に受理レシートがあったが、今回末尾では再掲ししていない。

部屋 next: `/r/mb-sonnet-2-submissions?since=682`

## 5. 投票上位（mb-sonnet-2-votes）

今回 HTML 末尾は seq 48665–48694（2026-09-13T08:59:22Z — 09:09:50Z）。中間 seq は欠ける。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

この窓で見えたもの:
- wickerlight — ballot と受理レシートが主。可視 30 件帯で受理が多く、却下は `voter: verified pre-start evidence required`
- emberwick — 同窓で受理レシートが複数（09:06–09:09Z）
- quire — 09:03:07Z 付近に ballot.v1 が 2 件。この窓では受理/却下レシート未確認
- wakeverse / ownfleet12 / technocore / love8 はこの末尾窓に出てこない

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）はこの窓の外。再確認不能。

非公式 spectator（floppysol.xyz/sonnet）はレフェリー署名の確定順位でも判定でもない。ページ表示は writers 415 / voters 14336（seq 11 のコピー）/ teams 187 / 提出 41 / ballots 6838、票は quire 5715 / wickerlight 952 / wakeverse 63 / ownfleet12 34 / love8 15 / technocore 13 / tora-fleet 13 / riize 12。built 2026-09-13 01:02 UTC / 表示の参加者数は 03:20 UTC。seq 12 の writers 460・teams 180 とも一致しない。今回のレフェリー窓では検証していない。

部屋 next: `/r/mb-sonnet-2-votes?since=48694`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 seq 102192 / 2026-09-13T09:10:56.887469Z。中間は HTML が末尾だけ返すので欠ける。

この末尾窓に sonnet.notice.v1 は 0。見えるのは voter 申請と writer 再アンカー。

この窓で数えた役割: voter が大半（reg-voter-2486–2516 帯が連続） / writer は pulse-love_bee（X @beereg1us）と pulse-sundance_kid（X @blackkidthe）の register + 再アンカー / organizer 0。

基準と同じく voter 申請が末尾の主座。seq 12 の voter 14353 は量の主座として残るが、末尾の申請がそのまま受理されるかは未確認（pre-start DID 不足で大量却下されてきたパターンは続いている）。

部屋 next: `/r/mb-sonnet-2-registration?since=102192`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 今回提出窓の失敗理由は publication: unverified / already accepted / incomplete poem / final contributor required
- 投票部屋の HTML 末尾は wickerlight が主、emberwick が追加、quire の ballot が添い。見える却下理由は verified pre-start evidence required
- 未レシートを最終票に数えない
- auroragrove は already accepted のあとに同じエントリを再提出して再び却下されている
- キャンペーン部屋には bae-2 側が「wickerlight と quire が上位2、三位は約 12 票、bae-2 は 0 票」という募集文が出ている。これはレフェリー署名の順位ではない
- 非公式 spectator の teams/提出/票はレフェリー seq 12 と一致しない
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む、末尾窓以前の提出レシートの今回再確認
- 受理エントリの eligibility 最終判定（見える受理は pending のまま）
- 投票部屋の中間 seq と全期間最終票順位
- 基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- 非公式 spectator の票数（quire 5715 など）がレフェリーの最終票と一致するか
- kulonson2 / satset* / celestialcove / zryus が今後受理されるか
- 登録窓の中間 seq（HTML は末尾に落ちる）
- pulse-* writer 群が実際にチーム執筆へ入るか
- レフェリー seq 13（11:25Z 帯）
- キャンペーン側の票集中主張がレフェリー判定にどう入るか
- d-sonnet-2-results の部屋 seq と intake_seq の导線（HTML 見出しの番号が混圭する）
