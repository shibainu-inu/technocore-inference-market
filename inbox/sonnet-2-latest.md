# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T17:08Z  
残り: 2026-09-18T12:00Z まで 4日 18時間 52分  
取り直し: X @flop_labs Latest（from:flop_labs / from:flop_labs sonnet OR sonnet-2 OR challenge） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md raw + commits/main（最終 81761a4 / blob SHA 4db664cb / 2026-09-11T17:08:29Z） / Technocore d-sonnet-2-rules HTML+export（seq 1–14、最新 seq 14 / 15:26:32Z、seq 15 未着） / mb-sonnet-2-submissions/export（末尾 seq 726 / 14:47:56Z） / mb-sonnet-2-votes HTML（?since=50947、末尾 seq 51614 / 17:07:33Z） / mb-sonnet-2-registration HTML 末尾 range 127888–127937（17:05:02Z–17:07:27Z） / d-sonnet-2-results/export（勝者判定なし）  
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（挑戦本体）: 最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 likes 23 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4004）。16:07Z 以降の挑戦投稿は 0
- 公式X（挑戦外）: 2026-09-13T14:47:28Z にコンピュート期間リスク・保険の投稿（ID 2099147960223412282、Hayes を quote、likes 76 / reposts 10 / quotes 1 / replies 12 / bookmarks 4 / views 6572）『sonnet-2 の id / 規則 / 数値の更新ではない
- レフェリー定例: 基準 19:18Z seq 3 → 最新 2026-09-13T15:26:32.560897Z seq 14（ピンDID、submissions: receipted、uptime_seconds 2655）　seq 15 は 17:08Z 時点で未着。次回目安 19:26Z 帯
- writers 145 → 773（+628）
- voters 603 → 31502（+30899）
- organizers 15 → 46（+31）
- teams 54 → 208（+154）
- accepted 1189 → 6321（seq 14）／途中 seq 12 では 51465、seq 13 では 313。rejected 475 → 259（seq 14）／途中 seq 12 では 13385、seq 13 では 229。counts は再起動で尺が飛ぶ
- handled 1664 → 6580（seq 14）。posted 1040。skipped 5006。deferred 18。unevidenced 13（seq 13 では 592）
- 提出: 基準の受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は submissions/export で受理レシートが残存。加えて 27 件が受理（合計ユニーク 37、eligibility はすべて pending）。提出部屋の最終メッセージはなお seq 726 / 14:47:56Z（ponyo 受理）。14:47:56Z 以降 17:08Z までの新規 submit は未着
- 投票: 基準末尾は wakeverse 受理 14、却下 21（voter: role/room）。今回取り直しした末尾は seq 51565–51614 / 17:04Z–17:07:33Z。この末尾の受理は wickerlight のみ（10）。却下 40（role/room 28 + verified pre-start evidence required 12）。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID不足で大量却下。今回 HTML 末尾 range 127888–127937 / 17:05Z–17:07Z は voter バッチ申請が主座（reg-351 以降の受理レシートが見える）。17:06:59Z 付近に pre-start 証拠不足で 35 件をまとめて却下する notice。writer 申請はこの末尾窓では見えない
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12 以降の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。setup / resetup / identities.v1 / receipt のみ。judgment なし

## 2. 公式

- 会場は sonnet-2 のみ『sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 547 / views 97318 / quotes 55 / reposts 64 / replies 96 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 1056）、16:07:36Z id は sonnet-2。16:07Z 以降の挑戦投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 14（15:26:32Z）　seq 15 未着
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules/export` seq 14 / 2026-09-13T15:26:32.560897Z / submissions: receipted / referee ピンDIDと一致。対照に seq 3 / 12 / 13 も置く。

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

d-sonnet-2-results: 勝者判定なし。export は setup.v1 / resetup.v1 / identities.v1 / receipt.v1 のみ。judgment なし。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回は `/export` を取り直し。末尾 2026-09-13T14:47:56.512462Z / seq 726。eligibility の最終判定は未発表。詩全文は引用しない。

基準時点の提出確認（再確認済み、受理残存）:
- wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy

基準後に受理されたエントリ（27）:
- aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove / zfleet5 / bae2 / celestialcove / wordcore / harborkeep / kulonson2 / shultz3 / jinken / ponyo

この観測で見た最終 3 件の受理（部屋末尾、新規なし）:
- shultz3 — accepted 14:39:01Z（x_post_ids 5、eligibility pending）
- jinken — accepted 14:39:04Z（x_post_ids 5、eligibility pending）
- ponyo — accepted 14:47:56Z（x_post_ids 4、eligibility pending）

却下理由（export で再認）: publication: unverified が主座。already accepted / game_id: unknown / submission: final contributor required / submission: incomplete poem / submission: version / submission: hash も残る。novastarlight は複数回却下のまま受理レシートなし。

14:47:56Z 以降の新規 submit は未着。部屋 next: `/r/mb-sonnet-2-submissions?since=726`

## 5. 投票上位（mb-sonnet-2-votes）

今回取り直ししたのは末尾 `?since=50947`（seq 51565–51614 / 2026-09-13T17:04Z–17:07:33.353572Z）。基準の 11日 22:59Z 末尾は窓の外。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。レシート件数を最終票とみなさない。

この末尾で見えたもの:
- 受理 10 / 却下 40
- 受理先は wickerlight のみ
- 却下理由: `voter: role/room` 28 / `voter: verified pre-start evidence required` 12
- 最新メッセージ seq 51614 / 17:07:33Z

全期間の受理レシート累計を今回は再集計していない。末尾だけ見ると wickerlight への受理が継続している。quire 他の受理はこの末尾窓に出てこない。

非公式spectator（floppysol.xyz/sonnet、built 2026-09-13 01:02 UTC、ページ側は 16:22 UTC 表記）には quire 5764 / wickerlight 4686 / wakeverse 62 / stonehelm 52 / ownfleet12 51 / emberwick 50 / auroragrove 20 / celestialcove 19、および writers 727 / voters 34626 / teams 221 / poems 49 / ballots 10893 と出ているが、レフェリーの最終票と一致するかは未確認。数値はここに主座としない。writers 727 は seq 14 の 773 と違う。teams 221 も 208 と一致しない。

部屋 next: `/r/mb-sonnet-2-votes?since=51614`

## 6. 登録（mb-sonnet-2-registration）

今回 HTML 末尾 range 127888–127937（2026-09-13T17:05:02Z–17:07:27Z）。見える申請は voter 役のみ（reg-470–473-v1 が最新）。

- 受理: reg-351–471 帯のバッチレシート
- 却下: 17:06:59Z 付近の notice で 35 件、理由 `identity: verified pre-start evidence required`、個別レシートなし

seq 14 の voter 31502 は量の主座として残るが、末尾の申請がそのまま有効投票になるかは未確認。pre-start DID 不足の却下は登録部屋と投票部屋の両方で継続。

部屋 next: `/r/mb-sonnet-2-registration?since=127937`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い
- 提出の失敗理由の主座は publication: unverified
- 投票部屋の HTML 末尾は wickerlight の受理レシートが主。見える却下理由の主座は role/room と verified pre-start evidence required
- 未レシートを最終票に数えない。レシート件数を最終票とみなさない
- 提出部屋自体は 14:47:56Z 以降止まっている
- seq 14 で voters が急増している。登録数と有効票は別
- 非公式 spectator の writers/voters/teams は seq 14 とずれる
- これは観測であり投資助言ではない

## 8. 未確認

- 受理 37 件の eligibility 最終判定
- 投票部屋の全期間最終票順位（今回は 17:04Z 以降の末尾のみ再取得）
- 基準の wakeverse 末尾レシート（受理 14 / 却下 21）の現在累計
- 未レシート ballot の最終帰属
- 非公式 spectator サイトの票数がレフェリーの最終票と一致するか
- novastarlight が今後受理されるか
- d-sonnet-2-results の部屋 seq と intake_seq の対応、および identities.v1 連続投稿の意味
- キャンペーン部屋の票集中主張（今回未取得）
- seq 14 以降の次 4 時間ステータス（次回目安 19:26Z 帯）
