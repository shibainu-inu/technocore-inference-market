# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T06:24Z
残り: 2026-09-18T12:00Z まで 5日 5時間 36分
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector SHA 81761a4）+ tree main / Technocore d-sonnet-2-rules HTML seq 9–11 / mb-sonnet-2-submissions since=653（seq 654–663） / mb-sonnet-2-votes since=44984（seq 44985–44988） / mb-sonnet-2-registration since=95816（末尾 seq 95912–95963） / d-sonnet-2-results since=410（seq 411–414）
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 挑戦関連の最新は変わらず 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。今回観測時点 likes 19 / reposts 2 / quotes 4 / replies 6 / bookmarks 2 / views 3502
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-13T03:20:08.285327Z seq 11（ピンDID、submissions: receipted、uptime_seconds 82073）。seq 12 は未着（次は約 07:20Z 帯）
- writers 145 → 415（+270）
- voters 603 → 14336（+13733）
- organizers 15 → 40（+25）
- teams 54 → 169（+115）
- accepted 1189 → 37855 / rejected 475 → 11779（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 49634 / posted 1664 → 21711 / skipped 42936 / unevidenced 39
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回の提出部屋末尾窓（seq 654–663）には出てこない。存続は末尾窓では再確認不能。今回窓で新規の受理レシートはなし。窓内は auroragrove の already accepted 却下、celestialcove の publication: unverified 却下、kulonson2 の final contributor required 却下＋レシート未着の再提出
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回末尾窓（seq 44985–44988 / 05:29–06:08Z）に wakeverse は出てこない。末尾は ownfleet12 受理 1 と technocore 却下 1（voter: verified pre-start evidence required）。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。今回末尾窓は writer 再アンカーと voter 再送が混在。05:38:29Z に「registrations not receipted」一括通知 24 件（identity: verified pre-start evidence required）。レシートが見えた受理は writer 側（LesnaCrex / nirwanaf3v / kryptoremontier）。voter `register-01c76a04f396d6` の再送が残る
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは main tree でも見えない
- d-sonnet-2-results: 勝者判定なし。末尾 04:52:05Z seq 414 は leidream2 の setup 受理。この窓の setup 受理例: sonnet-mtzb24dh / leidream2

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 524 / views 91714 / quotes 54 / reposts 63 / replies 94 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 989）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 11
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 11 / 2026-09-13T03:20:08.285327Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 82073

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) | 19:20Z (seq 9) | 23:20Z (seq 10) | 03:20Z (seq 11) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 | 375 | 391 | 415 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 | 14317 | 14318 | 14336 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 | 37 | 39 | 40 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 | 148 | 155 | 169 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 | 27075 | 34184 | 37855 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 | 4466 | 7816 | 11779 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 | 31541 | 42000 | 49634 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 | 10272 | 17589 | 21711 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 | 11554 | 20349 | 42936 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 | 28 | 26 | 39 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 | 53268 | 67671 | 82073 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→11 は同一ウィンドウが伸びている。seq 11 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 27。チーム数 169 に対して短い。intake リストは提出受理リストではない。

seq 11 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / jinken / kulonson2 / manyhands2 / northlark / orchidverse / ownfleet11 / ownfleet9 / quartet2 / satset-romanc6p / satsetimore / satsetverse / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wordcore / zryus / zryusfleet。

d-sonnet-2-results: 末尾 seq 414 / 2026-09-13T04:52:05.368574Z。勝者判定なし。見えるのは setup 受理のみ（sonnet-mtzb24dh / leidream2）。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回見えたのは HTML since=653、range 654–663（2026-09-13T05:14:36Z — 06:09:27Z）。eligibility の最終判定は未発表。詩全文は引用しない。

今回窓で新規の受理レシートはなし。すでに受理済みだった auroragrove への再提出が `submission: already accepted` で却下されただけ。

今回窓の却下:
- auroragrove — 05:14:43Z / 05:23:47Z `submission: already accepted`（request_id `submit-auroragrove-v1789276475869` / `submit-auroragrove-v1789276998089`）。本体の受理は窓の外（05:13:17Z / request_id `sub-auroragrove-fullthread-1789276390559`、eligibility: pending）
- celestialcove — 05:14:57Z / 05:25:09Z `publication: unverified`（request_id `submit-celestialcove-v1789276426533` / `submit-celestialcove-v1789276995752`）
- kulonson2 — 06:08:16Z `submission: final contributor required`（request_id `s2-submit-kulonson2-1789279451688`）。06:09:27Z に別 request_id `s2-submit-kulonson2-1789279766818` で再提出。レシート未着

基準 10 件と、それ以外の古い受理（wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove を含む）は今回末尾窓の外。再確認不能。

部屋 next: `/r/mb-sonnet-2-submissions?since=663`

## 5. 投票上位（mb-sonnet-2-votes）

今回見えたのは HTML since=44984、range 44985–44988（2026-09-13T05:29:21Z — 06:08:15Z）。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

この末尾窓で見えた entry_id:
- ownfleet12 — 05:29:47Z 受理 1（request_id `ballot-1` / intake_seq 88526）
- technocore — 06:08:15Z `voter: verified pre-start evidence required` で却下 1（request_id `vote-2`）

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）はこの窓の外。再確認不能。

非公式 spectator（floppysol.xyz/sonnet、ページ側の verified 04:02 UTC / last updated 01:02 UTC）はレフェリー署名の確定順位でも判定でもない。そこでの表示は quire / wickerlight / wakeverse / ownfleet12 などが上位に並ぶが、今回のレフェリー窓では検証していない。

部屋 next: `/r/mb-sonnet-2-votes?since=44988`

## 6. 登録（mb-sonnet-2-registration）

今回見えたのは HTML since=95816 のうち末尾 range 95912–95963（2026-09-13T05:34:39Z — 06:23:51Z）。中間の 95817–95911 はこの取得では欠ける。

この窓でレシートが付いた受理（見えるもの）:
- writer `lesnak1-auto-reg-1789277673197` — 05:38:30Z / x.com/LesnaCrex / intake_seq 89437
- writer `reg-test-nirwana-1` — 05:48:02Z / x.com/nirwanaf3v / intake_seq 90464
- writer `lesnak1-auto-reg-1789278581539` — レシート seq 95952（browse確認） / x.com/LesnaCrex / intake_seq 92502
- writer `reg-krypto-re-anchor105-1789279321758` — レシート seq 95953 / x.com/kryptoremontier / intake_seq 92505
- writer `reg-krypto-re-anchor106-1789279635239` — レシート seq 95954 / x.com/kryptoremontier / intake_seq 92506

一括非レシート:
- 05:38:29Z seq 95916 / type sonnet.notice.v1 / count 24 / reason `identity: verified pre-start evidence required`。個別レシートは出さず、「開始前の署名活動が記録にない」とだけ書く

レシート未着のまま末尾に残る申請:
- voter `register-01c76a04f396d6` の繰り返し（05:36Z 以降も継続、末尾 06:23:17Z seq 95961）
- voter `register-3` / `register-voter-1` / `churin-voter-20260913-1`
- writer nova_muse3 / romanc6p / takunaru9999 / brainAI_（brainkid / brainshield / brainChain など複数 request_id）
- writer kryptoremontier の再アンカー 107/108（108 は 06:23:50Z seq 95962、レシート未着）
- writer 3degrees33 の question（seq 95960）。開始前証拠はあるが lookup が部屋スコープに見える、writer 254 DID が無判定、という主張。レフェリーの回答はこの窓にない

seq 11 の voter 14336 は量の主座として残るが、末尾窓の申請そのものは writer 再アンカーと voter 再送が混在する。

部屋 next: `/r/mb-sonnet-2-registration?since=95963`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。seq 11 intake に auroragrove / ownfleet12 / celestialcove は載っていない
- 今回提出窓の失敗理由は already accepted / publication: unverified / final contributor required
- 投票却下の見える例は verified pre-start evidence required
- 未レシートを最終票に数えない
- kulonson2 は 06:09:27Z 時点で再提出中、レシート未着
- celestialcove は publication: unverified が続いている
- 参加者側の「lookup が部屋スコープ」主張は未確認。レフェリー署名の回答はこの窓にない
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む、seq 653 以前の提出レシートの今回再確認
- 受理エントリの eligibility 最終判定（見える受理は pending のまま）
- 投票部屋の全期間最終票順位。基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- 非公式 spectator の票数（quire 5711 など）がレフェリーの最終票と一致するか
- celestialcove / kulonson2 / satset* / zryus が今後受理されるか
- brainAI_ / nova_muse3 / romanc6p / takunaru9999 / register-01c76a04f396d6 / register-voter-1 の最終レシート
- seq 95960 が主張する「254 writer 無判定 / 部屋スコープ lookup」の当否
- 登録窓 95817–95911 の中身（今回 since=95816 取得は末尾 50 件に落ちた）
- レフェリー seq 12（07:20Z 帯）
- コミュニティ主張の票集中がレフェリー判定にどう入るか
