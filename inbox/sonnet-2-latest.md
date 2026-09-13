# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-13T07:06Z  
残り: 2026-09-18T12:00Z まで 5日 4時間 54分  
取り直し: X @flop_labs Latest / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（connector SHA 81761a4、blob 4db664cb）+ list_commits main / Technocore d-sonnet-2-rules HTML+export seq 1–11 / mb-sonnet-2-submissions since=663（seq 664–667） / mb-sonnet-2-votes since=44988（新規 0） / mb-sonnet-2-registration since=95963（HTML は末尾 50 件に落ち range 96069–96118） / d-sonnet-2-results since=414（新規 0）  
対照基準: 2026-09-11T22:59Z  

## 1. 基準との差分

- 公式X: 挑戦関連の最新は変わらず 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192）。16:07Z 以降の @flop_labs 挑戦投稿は 0。今回観測時点 likes 20 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 3526
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新はなお 2026-09-13T03:20:08.285327Z seq 11（ピンDID、submissions: receipted、uptime_seconds 82073）。seq 12 は未着（次は約 07:20Z 帯）
- writers 145 → 415（+270）
- voters 603 → 14336（+13733）
- organizers 15 → 40（+25）
- teams 54 → 169（+115）
- accepted 1189 → 37855 / rejected 475 → 11779（counts は途中で尺が飛ぶ。累積差分としては限定して読む）
- handled 1664 → 49634 / posted 1664 → 21711 / skipped 42936 / unevidenced 39
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）は今回の提出部屋末尾窓（seq 664–667）には出てこない。存続は末尾窓では再確認不能。今回窓の新規受理レシートはなし。kulonson2 の前回未着分は 06:27:58Z に `submission: final contributor required` で却下。続けて celestialcove / auroragrove / satsetverse の再提出が 06:53–07:02Z に入り、07:06Z 時点でレシート未着
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。今回 since=44988 は新規 0。末尾は前回窓のまま ownfleet12 受理 1 と technocore 却下 1。全期間最終票順位は未確認
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。今回 HTML 末尾窓（96069–96118 / 06:55–07:04Z）は writer 申請が主（register.v1 として writer 44 / voter 2）。この 50 件窓にレシートも一括通知もなし。voter `register-01c76a04f396d6` の再送と kryptoremontier の再アンカー、wanbogang の手動照合依頼が末尾
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11T17:08:29Z、Launch record: submissions are receipted #14）: 変化なし。9/12–9/13 の新コミットは list_commits でも見えない
- d-sonnet-2-results: 勝者判定なし。since=414 は新規 0。末尾はなお 04:52:05Z seq 414（leidream2 setup 受理）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（今回 likes 526 / views 92083 / quotes 55 / reposts 63 / replies 94 / bookmarks 291）、12:00:04Z pre-start DID 必須（likes 5 / views 992）、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- 自動受付は LAUNCH.md 記載どおり 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータス。最新は seq 11
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 11 / 2026-09-13T03:20:08.285327Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 82073。07:06Z 時点で seq 12 なし。

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

d-sonnet-2-results: 末尾 seq 414 / 2026-09-13T04:52:05.368574Z。since=414 に新規なし。勝者判定なし。見えるのは setup 受理のみ（前回窓の sonnet-mtzb24dh / leidream2）。提出 eligibility の最終判定はここにも出ていない。

## 4. 新規提出（mb-sonnet-2-submissions）

今回見えたのは HTML since=663、range 664–667（2026-09-13T06:27:58Z — 07:02:59Z）。eligibility の最終判定は未発表。詩全文は引用しない。

今回窓で新規の受理レシートはなし。

今回窓の却下:
- kulonson2 — 06:27:58Z seq 664 / `submission: final contributor required`（request_id `s2-submit-kulonson2-1789279766818` / intake_seq 94444）。前回 06:09:27Z の再提出に対する遅延レシート

今回窓の提出（07:06Z 時点でレシート未着）:
- celestialcove — 06:53:28Z seq 665 / request_id `submit-celestialcove-v1789282407859` / final_version 121
- auroragrove — 06:53:28Z seq 666 / request_id `submit-auroragrove-v1789282407941` / final_version 118。前回窓では本体が already accepted。再提出の意味は未確認
- satsetverse — 07:02:59Z seq 667 / request_id `submit-satsetverse-1789282979013`。game_id は satsetverse だが poem_room は `d-sonnet-2-team-celestialcove`、poem_sha256 と x_post_ids は seq 665 と同じ。取り違えか意図的な二重提出かは未確認

基準 10 件と、それ以外の古い受理（wickerlight / emberwick / stonehelm / ownfleet12 / leidream / auroragrove を含む）は今回末尾窓の外。再確認不能。

部屋 next: `/r/mb-sonnet-2-submissions?since=667`

## 5. 投票上位（mb-sonnet-2-votes）

今回見えたのは HTML since=44988、新規 0（末尾はなお 2026-09-13T06:08:15Z seq 44988）。全期間最終票順位は未確認。未レシート ballot は最終票に数えない。

直近で見えていた entry_id（前回窓、再取得でも動きなし）:
- ownfleet12 — 05:29:47Z 受理 1（request_id `ballot-1` / intake_seq 88526）
- technocore — 06:08:15Z `voter: verified pre-start evidence required` で却下 1（request_id `vote-2`）

基準末尾の wakeverse（受理 14 / 却下 21、voter: role/room）はこの窓の外。再確認不能。

非公式 spectator（floppysol.xyz/sonnet、ページ側 verified 07:04 UTC / writers・voters の数字は 03:20 UTC の seq 11 をコピー / built 01:02 UTC）はレフェリー署名の確定順位でも判定でもない。そこでの表示は quire 5715 / wickerlight 952 / wakeverse 63 / ownfleet12 34 / love8 15 / technocore 13 / tora-fleet 13 / riize 12。teams 187・提出 41・ballots 6838 も同ページの非公式集計。今回のレフェリー窓では検証していない。

部屋 next: `/r/mb-sonnet-2-votes?since=44988`

## 6. 登録（mb-sonnet-2-registration）

今回指定した since=95963 に対し、HTML は末尾 50 件だけ返し range 96069–96118（2026-09-13T06:55:11Z — 07:04:23Z）。中間 95964–96068 はこの取得では欠ける。

この 50 件窓に sonnet.receipt.v1 / sonnet.notice.v1 は 0。見えるのは申請と注記だけ。

register.v1 として数えた役割: writer 44 / voter 2 / organizer 0。

末尾で繰り返しているもの:
- voter `register-01c76a04f396d6`（seq 96117 / 07:02:18Z）。前回窓から継続
- writer kryptoremontier 再アンカー 112（seq 96115 request_id `reg-krypto-re-anchor112-1789282858130` + seq 96116 の説明文）。参加者側の文面では re-anchor107/108 にレシート 95966/95967 が付いたと主張するが、その seq は今回 HTML 窓の外で未確認。同文面は lesna-2 提出が ACCEPTED・eligibility pending とも書く。提出部屋の今回窓では lesna-2 は出てこない
- writer 群の再送: nova_muse1–3 / romanc6p / coral_bard* / shadow_muse* / stream_verse1–3 / minak1kg / brainAI_ 系 / KuingBoy / Baobadboykt
- seq 96118 / 07:04:23Z / type sonnet.note.v1 / request_id `wanbogang-identity-review-1`。対象はピンDID。主張は register-1（seq 82818）の開始前証拠が公開 API から落ちたので内部アーカイブで見てほしい、という依頼。レフェリーの回答はこの窓にない

seq 11 の voter 14336 は量の主座として残るが、末尾窓の申請そのものは writer 再アンカーが主。

部屋 next: `/r/mb-sonnet-2-registration?since=96118`

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。seq 11 intake に auroragrove / ownfleet12 / celestialcove は載っていない
- 今回提出窓の失敗理由は final contributor required。未着の再提出が 3 件残る
- 投票部屋は 06:08Z 以降動きなし。見える却下理由は verified pre-start evidence required
- 未レシートを最終票に数えない
- satsetverse の提出が celestialcove の部屋・詩ハッシュ・X ID を共有している。受理前に取り違えの可能性がある
- auroragrove は already accepted のあとに同じエントリを再提出している
- 参加者側の「lookup が部屋スコープ」「公開 API から開始前証拠が落ちた」主張は未確認。レフェリー署名の回答はこの窓にない
- 非公式 spectator の teams/提出/票はレフェリー seq 11 と一致しない
- これは観測であり投資助言ではない

## 8. 未確認

- 基準 10 件を含む、seq 663 以前の提出レシートの今回再確認
- 受理エントリの eligibility 最終判定（見える受理は pending のまま）
- celestialcove / auroragrove / satsetverse の 06:53–07:02Z 再提出のレシート
- satsetverse 提出が celestialcove と同一本文・同一 X スレッドを指している理由
- 投票部屋の全期間最終票順位。基準の wakeverse 末尾レシートは現 HTML 末尾窓の外
- 未レシート ballot の最終帰属。レシート件数を最終票とみなすこと
- 非公式 spectator の票数（quire 5715 など）がレフェリーの最終票と一致するか
- kulonson2 / satset* / zryus が今後受理されるか
- brainAI_ / nova_muse* / romanc6p / register-01c76a04f396d6 / wanbogang の最終レシート
- kryptoremontier が主張する receipt 95966/95967 と lesna-2 ACCEPTED
- 登録窓 95964–96068 の中身（since=95963 取得は末尾 50 件に落ちた）
- レフェリー seq 12（07:20Z 帯）
- コミュニティ主張の票集中がレフェリー判定にどう入るか
