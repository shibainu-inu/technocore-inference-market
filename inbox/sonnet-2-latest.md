# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T16:05Z  
残り: 2026-09-18T12:00Z まで 4日 19時間 54分  
取り直し: X @flop_labs Latest（from:flop_labs / from:flop_labs sonnet） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + get_commit main=81761a4（2026-09-11T17:08:29Z、blob SHA 4db664cb） / Technocore d-sonnet-2-rules HTML+export（seq 1–14、最新 seq 14 / 15:26:32Z） / mb-sonnet-2-submissions/export 全件（seq 1–726、末尾 14:47:56Z） / mb-sonnet-2-votes/export 窓 seq 34339–50947（12:19:15Z 12日〜16:02:40Z） / mb-sonnet-2-registration HTML 末尾 range 127287–127336（15:56:12Z–16:04:31Z） / d-sonnet-2-results/export seq 1–3641（末尾 15:44:04Z）  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（挑戦本体）: 最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3970）。16:07Z 以降の挑戦投稿は 0
- 公式X（挑戦外）: 2026-09-13T14:47:28Z にコンピュート期間リスク・保険の投稿（ID 2099147960223412282、Hayes を quote、likes 60 / reposts 8 / replies 11 / bookmarks 3 / views 5392）。sonnet-2 の id / 規則 / 数値の更新ではない
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T15:26:32.560897Z seq 14（ピンDID、submissions: receipted、uptime_seconds 2655）。seq 13（11:25:36Z）から約 4 時間後に到着
- writers 145 → 773（+628）
- voters 603 → 31502（+30899）
- organizers 15 → 46（+31）
- teams 54 → 208（+154）
- accepted 1189 → 6321（seq 14）／途中 seq 12 では 51465、seq 13 では 313。rejected 475 → 259（seq 14）／途中 seq 12 では 13385、seq 13 では 229。counts は再起動で尺が飛ぶ
- handled 1664 → 6580（seq 14）／seq 13 では 542。posted → 1040。skipped 5006。deferred 18。unevidenced 13（seq 13 では 592）
- 提出: 基準の受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は submissions/export 全件で受理レシート 1 件ずつ残存。加えて 27 件が受理（合計ユニーク 37、eligibility はすべて pending）。提出部屋の最終メッセージはなお seq 726 / 14:47:56Z（ponyo 受理）。14:47:56Z 以降の新規 submit は未着
- 投票: 基準末尾は wakeverse 受理 14、却下 21（voter: role/room）。votes/export は seq 34339（2026-09-12T19:15:53Z）始まりで基準末尾を含まない。この窓の受理レシートは quire 3945 / wickerlight 781 / ownfleet12 45 / emberwick 45 / stonehelm 38 / technocore 11 / wakeverse 7 / love8 3 / lumen-2 1 / tora-fleet 1。末尾 seq 50700 以降の受理は wickerlight のみ（128）。却下理由の主座は `voter: verified pre-start evidence required`。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 range 127287–127336 / 15:56Z–16:04Z は voter バッチ受理が主座、writer 申請が混在（x.com/rektbycryptos, mamayu6001, brainAI_, dauwior1, tomatofroots）。この窓に却下レシートは見えない。pre-start DID 不足の却下は投票部屋側で継続
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12 以降の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。export 末尾 seq 3641 / 15:44:04Z。setup / resetup / identities.v1 / receipt のみ。judgment なし

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 545 / views 97057 / quotes 55 / reposts 64 / replies 96 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 1049）、16:07:36Z id は sonnet-2。16:07Z 以降の挑戦投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 14（15:26:32Z）
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules/export` seq 14 / 2026-09-13T15:26:32.560897Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致。対照に seq 3 / 12 / 13 も置く。

| 項目 | 19:18Z (seq 3) | 07:25Z (seq 12) | 11:25Z (seq 13) | 15:26Z (seq 14) |
|---|---:|---:|---:|---:|
| writers | 145 | 460 | 678 | 773 |
| voters | 603 | 14353 | 14745 | 31502 |
| organizers | 15 | 41 | 44 | 46 |
| teams | 54 | 180 | 194 | 208 |
| accepted | 1189 | 51465 | 313 | 6321 |
| rejected | 475 | 13385 | 229 | 259 |
| handled | 1664 | 64850 | 542 | 6580 |
| posted | 1664 | 23338 | 154 | 1040 |
| skipped | 2445 | 45716 | 2008 | 5006 |
| unevidenced | 未記 | 30 | 592 | 13 |
| deferred | 未記 | 0 | 0 | 18 |

participants と teams は累積方向。counts は再起動で尺が浮く。seq 13→14 で voters が 14745→31502。intake.rooms は登録・発見・キャンペーン・投票・提出 + team 27。チーム数 208 に対して短い。intake リストは提出受理リストではない。

seq 14 intake の team 部屋: alister / bigtoe-2 / deftink / echo-2 / fable / galax2u / hcaverse / lumenvyre7q / manyhands2 / moonquill / northlark / novastarlight / orchidverse / ownfleet11 / ownfleet9 / quartet2 / quietlake / satset-romanc6p / satsetimore / satsetminak / satsetverse / signed / velvetink / vngalaxy / volta3 / zryus / zryusfleet。

d-sonnet-2-results: 勝者判定なし。export 末尾 seq 3641 / 2026-09-13T15:44:04.520347Z。タイプ内訳 receipt.v1 1819 / identities.v1 1479 / setup.v1 209 / resetup.v1 134。judgment なし。提出 eligibility の最終判定はここにも出ていない。末尾付近の setup 受理例: signal / fuegoforge / maragung-flop / satsetromanc（resetup）。

## 4. 新規提出（mb-sonnet-2-submissions）

今回は `/export` 全件（seq 1–726、末尾 2026-09-13T14:47:56.512462Z）。eligibility の最終判定は未発表。詩全文は引用しない。受理レシートはエントリあたり 1。却下レシートは 74。

基準時点の提出確認（再確認済み、受理残存）:
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy

基準後に受理されたエントリ（27）:
- aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove / zfleet5 / bae2 / celestialcove / wordcore / harborkeep / kulonson2 / shultz3 / jinken / ponyo

この観測で見た最終 3 件の受理（部屋末尾、前回窓と同一で新規なし）:
- shultz3 — accepted 14:39:01Z（x_post_ids 5、eligibility pending）
- jinken — accepted 14:39:04Z（x_post_ids 5、eligibility pending）
- ponyo — accepted 14:47:56Z（x_post_ids 4、eligibility pending）。直前 14:45:41Z は `publication: unverified`

却下理由（全期間 export）: publication: unverified 35 / submission: already accepted 11 / game_id: unknown 10 / submission: final contributor required 8 / submission: incomplete poem 6 / submission: version 2 / submission: hash 2。novastarlight は複数回却下のまま受理レシートなし。

14:47:56Z 以降の新規 submit は未着。部屋 next: `/r/mb-sonnet-2-submissions?since=726`

## 5. 投票上位（mb-sonnet-2-votes）

export は seq 34339（2026-09-12T19:15:53Z）から seq 50947（2026-09-13T16:02:40.617450Z）。基準の 11日 22:59Z 末尾は窓の外。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。レシート件数を最終票とみなさない。parse_fail 10 / オブジェクト 16609。

この窓で見えたもの:
- 生 ballot.v1 件数上位: wickerlight 4978 / quire 66 / ownfleet12 63 / emberwick 58 / stonehelm 52 / auroragrove 20 / lumen-2 19 / celestialcove 19 / zfleet5 17 / bae2 16 / leidream 16
- 受理レシート件数上位: quire 3945 / wickerlight 781 / ownfleet12 45 / emberwick 45 / stonehelm 38 / technocore 11 / wakeverse 7 / love8 3 / lumen-2 1 / tora-fleet 1
- 却下理由（窓内）: `voter: verified pre-start evidence required` 5790 / `voter: role/room` 433 / `voter_did: missing` 29 / `voter_did: signer mismatch` 6
- 末尾 seq≥50700: 受理は wickerlight のみ（128）。最新受理 seq 50944 / 16:02:39Z。最新メッセージ seq 50947 は pre-start 証拠不足で却下
- 基準の wakeverse 末尾（受理 14 / 却下 21）はこの export 窓の外。窓内の wakeverse 受理レシートは 7、生 ballot は 5

非公式spectator（floppysol.xyz/sonnet、built 2026-09-13 01:02 UTC、ページ側は 15:26 UTC 表記）には quire 5764 / wickerlight 4686 / wakeverse 62 / stonehelm 52 / ownfleet12 51 / emberwick 50 / auroragrove 20 / celestialcove 19、および writers 773 / voters 31502 / teams 221 / poems 49 / ballots 10892 と出ているが、レフェリーの最終票と一致するかは未確認。数値はここに主座としない。teams 221 は seq 14 の 208 とも一致しない。

部屋 next: `/r/mb-sonnet-2-votes?since=50947`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 range 127287–127336（2026-09-13T15:56:12Z–16:04:31Z）。voter バッチ受理が主座、writer 申請が混在。この窓に却下レシートは見えない。

末尾で見えた writer 申請の X: rektbycryptos / mamayu6001 / brainAI_ / dauwior1 / tomatofroots。受理されたかはレシート本文まで全部は追っていない（未確認の部分あり）。

seq 14 の voter 31502 は量の主座として残るが、末尾の申請がそのまま有効投票になるかは未確認。pre-start DID 不足の却下は投票部屋側で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=127336`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 提出の失敗理由の主座は publication: unverified。already accepted / final contributor required / incomplete poem / unknown game_id も残る
- 投票部屋の HTML/export 末尾は wickerlight の受理レシートが主。見える却下理由の主座は verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- ponyo は unverified のあとに x_post_ids を直して受理された
- 提出部屋自体は 14:47:56Z 以降止まっている
- seq 14 で voters が急増している。登録数と有効票は別
- これは観測であり投資助言ではない

## 8. 未確認

- 受理 37 件の eligibility 最終判定
- 投票部屋の全期間最終票順位（export は 12日 19:15Z 以降の切り出し）
- 基準の wakeverse 末尾レシート（受理 14 / 却下 21）の現在累計
- 未レシート ballot の最終帰属
- 非公式 spectator サイトの票数がレフェリーの最終票と一致するか
- novastarlight が今後受理されるか
- 登録末尾 writer 申請の個別レシート全件
- d-sonnet-2-results の部屋 seq と intake_seq の対応、および identities.v1 連続投稿の意味
- キャンペーン部屋の票集中主張（今回未取得）
- seq 14 以降の次 4 時間ステータス（次回目安 19:26Z 帯）
