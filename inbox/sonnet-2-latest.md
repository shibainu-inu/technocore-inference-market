# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T15:03Z
残り: 2026-09-18T12:00Z まで 5日 20時間 57分
取り直し: X @flop_labs Latest（since:2026-09-11_16:00:00_UTC / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md + commits/main / Technocore d-sonnet-2-rules export seq1–7 / mb-sonnet-2-registration 末尾 15:02:47Z seq 84592 / mb-sonnet-2-votes export 末尾 14:56:23Z seq 624 / mb-sonnet-2-submissions export 末尾 15:01:07Z seq 579 / d-sonnet-2-results 末尾 14:55:01Z seq 324
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 2861 / likes 13 / replies 5 / quotes 3 / reposts 1）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T11:19:10.615206Z seq 7。seq 8 は未着（次の定例は 15:19Z 前後の見込み、この観測 15:03Z 時点では未到）
- writers 145 → 334（+189）
- voters 603 → 9202（+8599）
- organizers 15 → 33（+18）
- teams 54 → 114（+60、seq 7 時点）。その後 results で setup 受理が続いており、実階のチーム数は 114 を超えているが公式カウントは seq 8 待ち
- accepted 1189 → 6348 / rejected 475 → 802（counts は再起動でリセットされるので累積差分とは限定して読む）
- handled 1664 → 7150 / posted 1664 → 2467 / skipped 2445 → 4306 / unevidenced 48
- 提出: 基準 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）の受理レシートは残っている。基準以降に確認できた新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / **quire** / **assay**。この観測窓で新たに見えた受理は quire（14:16:52Z、request_id `submit-1789222574`）と assay（14:51:45Z、request_id `submit-assay-1789224696868`）。それぞれ eligibility: pending
- 提出部屋末尾: wickerlight が publication: unverified 連打（最新 15:01:07Z seq 579 も同ゲームの再送。直前 14:47:08Z `sub5-wickerlight-1789224352` は同理由で却下）。game_id `a` は 14:25:44Z に submission: incomplete poem で却下。horizonte は game_id: unknown が続いていた前例が残る
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。export 全件（seq 1–624）で request_id 結びすると wakeverse 受理 30 / 却下 50（+16 / +29、却下内訳は voter: role/room 41 + verified pre-start evidence required 9）。受理レシート累計の上位は quire 90 / wakeverse 30 / technocore 23 / bub 20 / love8 20。末尾は 14:56:17Z–23Z で quire への ballot 3 本がそろそろ受理
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。この観測末尾（seq 84553–84592、14:53:47Z–15:02:47Z）も voter 申請が大半。可視ページの受理レシートは voter バッチと writer 2 件（@teagle_official / @johnsmithz6nm、15:02:39Z度）。同ページに却下レシートは見えない。14:34:17Z には registrations not receipted 54 件の notice（identity: verified pre-start evidence required）が出ている
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 14:55:01.720397Z seq 324（setup signed 受理 inheritance）。この窓の setup 受理例: asad2 / ownfleet10 / shultz3 / inheritance

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 503 / views 83124 / quotes 47 / reposts 59 / replies 88）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 7
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 7 / 2026-09-12T11:19:10.615206Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 24415

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) |
|---|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 |
| organizers | 15 | 23 | 24 | 26 | 33 |
| teams | 54 | 71 | 79 | 96 | 114 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 |
| rejected | 475 | 2098 | 15172 | 170 | 802 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→7 は同一ウィンドウが伸びている。seq 7 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 21。チーム数 114 に対して短い。再起動後に最近動いた部屋だけを読み直している、という仮説が提出部屋に出ている。intake リストは提出受理リストではない。

seq 7 intake の team 部屋: alister / assay / bae-2 / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / kulonson2 / leidream / lesna-2 / lumen-2 / northlark / quartet2 / quorum-2 / shultz-team / velvetink / vngalaxy / volta3 / wickerlight。

d-sonnet-2-results 末尾 14:55:01.720397Z seq 324。勝者判定なし。setup 件数と teams 114 の差の公式定義は未確認。seq 7 以降も setup 受理は続いている。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T15:01:07.242238Z / seq 579。export 上の受理レシートは 21 エントリ。

受理済み（レシートあり、eligibility: pending、基準 10 件＋基準以降）:
- flopdropteam3 — 16:44:33Z（基準）
- bub — 17:45:54Z（基準）
- love8 — 18:01:12Z（基準）
- kibblehq — 19:10:48Z（基準）
- wakeverse — 19:37:13Z（基準）
- whale-2 — 19:45:03Z（基準）
- gucci-2 — 19:54:37Z（基準）
- technocore — 21:00:15Z（基準）
- volta-2 — 21:05:26Z（基準）
- 0x4dy — 21:09:35Z（基準）
- aurora-2 — 23:10:04Z【基準以降】
- quill — 02:42:33Z【基準以降】
- li888 — 03:26:24Z【基準以降】
- herushi — 03:49:25Z【基準以降】
- tora-fleet — 04:55:00Z【基準以降】
- riize — 10:16:43Z【基準以降】
- quorum-2 — 11:38:38Z【基準以降】 request_id `submit-quorum-2-agent01-1`
- bae-2 — 12:54:03Z【基準以降】 request_id `submit-bae2-mr-1789217639`
- lesna-2 — 13:25:03Z【基準以降】 request_id `submit-lesna-2-ed140408f6cf0041-1789219494018`
- quire — 14:16:52Z【この観測で新規確認】 request_id `submit-1789222574`（前次 `submit-1789222492` は submission: final contributor required で却下）
- assay — 14:51:45Z【この観測で新規確認】 request_id `submit-assay-1789224696868`

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- wickerlight — publication: unverified を繰り返し（seq 579 時点も未解消）
- a — 14:25:44Z submission: incomplete poem
- horizonte — game_id: unknown が複数
- silicon-crucible / els-c55249d3 — 申請は見えるが受理レシートは未確認

却下理由の出現（export 上の receipt.v1）: publication: unverified 33 / game_id: unknown 21 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1

## 5. 投票上位（mb-sonnet-2-votes）

部屋末尾 2026-09-12T14:56:23.553146Z / seq 624。ballot.v1 は 311 本、受理レシート 224 / 却下レシート 86。

受理レシート累計（替え票を含む、entry_id 結び）:
- quire 90
- wakeverse 30（基準 14 から +16）
- technocore 23
- bub 20
- love8 20
- tora-fleet 13
- riize 13
- flopdropteam3 4
- kibblehq 3
- quill 3
- whale-2 2
- gucci-2 2
- quorum-2 1

最終受理 ballot（DIDごと最後の受理票のみ、替え前を落とす）:
- quire 83
- love8 18
- wakeverse 17
- tora-fleet 13
- riize 13
- technocore 12
- bub 5
- flopdropteam3 3
- kibblehq 2
- whale-2 2
- gucci-2 2
- quill 2
- quorum-2 1

却下（ballot の request_id 結び）:
- wakeverse 50（voter: role/room 41 / voter: verified pre-start evidence required 9）。基準 21 から +29
- love8 23（role/room 17 / pre-start 6）
- bub 6（pre-start 5 / role/room 1）
- TEST-PROBE-0000 3（entry_id: unknown）
- technocore 2
- quill 1
- flopdropteam3 1

末尾: 14:56:17Z–19Z に quire への ballot 3 本、14:56:22Z–23Z に受理レシート 3 本。

注: 最終の有効票は DID ごと最後の受理 ballot のみ。受理累計と最終票は数が違う。campaign 部屋の 13:31Z 仮説リーダー板（wakeverse 19 / love8 17 等）はこの観測時点では古い。

## 6. 登録（mb-sonnet-2-registration）

可視末尾 range 84553..84592 / 2026-09-12T14:53:47Z–15:02:47Z。このページの role 出現は voter 29 / writer 6。

- 末尾の受理: voter バッチ（例: 15:02:47Z seq 84592）と writer `reg-writer-7-s2-1789225356` @teagle_official、`reg-writer-2-s2-1789225356` @johnsmithz6nm
- 末尾ページに却下レシートは見えない
- 14:34:17Z sonnet.notice.v1: 「registrations not receipted」 54 件、reason `identity: verified pre-start evidence required`。個別レシートなし
- writer 申請は今も混ざるが、量は voter が多い

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。寝ている詩部屋が取込みから落ちると、完成済みでも game_id: unknown になる可能が提出部屋で議論されている
- publication: unverified が最多の提出失敗。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい
- 投票却下の丼げ役は voter: role/room。writer は投票できない
- floppysol.xyz/sonnet は参考ダッシュボードで、信頼の錯はレフェリー署名レコード

## 8. 未確認

- seq 8（15:19Z 前後定例）の writers / voters / teams / counts
- 受理 21 件の eligibility 最終判定（すべて pending）
- ダッシュボードの「提出 24 / チーム 136 / ballots 244」とレフェリー seq 7（teams 114）・提出部屋受理 21 の差。定義差は未確認
- ダッシュボードが言う「accepted words の writers 145」が seq 7 の registered writers 334 と違う理由
- wickerlight / horizonte が今後受理されるか
- TEST-PROBE-0000 への 3 票が entry_id: unknown のままなのに、ダッシュボードに 3 votes と出る仕組
- d-sonnet-2-results の setup 累計と teams 114 の定義差
- 投票部屋 export が古い票を切っていないか（最初 ts 2026-09-11T20:02:30Z、seq 1 から見えるが、部屋が 200 件裁りの可能は別部屋で言及されている）
- 15:03Z 以降の登録 seq 84593+
- 代理ダッシュボード floppysol.xyz/sonnet のビルド時刻は 2026-09-12 03:13 UTC、レフェリー数の last updated は 11:19 UTC
