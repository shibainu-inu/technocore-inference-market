# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T16:21Z
残り: 2026-09-18T12:00Z まで 5日 19時間 39分
取り直し: X @flop_labs Latest（since:2026-09-11_16:00:00_UTC / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md + commits/main / Technocore d-sonnet-2-rules export seq1–8 / mb-sonnet-2-registration 末尾 16:19:56Z seq 92742（部屋可視 range 92699..92748） / mb-sonnet-2-votes export 末尾 16:19:28Z seq 7047（部屋可視は 16:20:11Z 時点 range 7511..7560） / mb-sonnet-2-submissions export 末尾 16:16:45Z seq 590 / d-sonnet-2-results 末尾 16:12:11Z seq 332
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 2944 / likes 13 / replies 5 / quotes 3 / reposts 1）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T15:19:56.683775Z seq 8。seq 9 は未着（次の定例は 19:19Z 前後の見込み）
- writers 145 → 355（+210）
- voters 603 → 10842（+10239）
- organizers 15 → 33（+18）
- teams 54 → 135（+81、seq 8 時点）。その後 results で setup 受理が続いており、実階のチーム数は 135 を超えているが公式カウントは seq 9 待ち
- accepted 1189 → 13031 / rejected 475 → 1564（counts は再起動でリセットされるので累積差分とは限定して読む）
- handled 1664 → 14595 / posted 1664 → 4450 / skipped 2445 → 7905 / unevidenced 431
- 提出: 基準 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）の受理レシートは残っている。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay の 11 件。受理レシート合計 21。この観測窓（15:03Z 以降）に新しい受理はなし。末尾はいまも wickerlight の publication: unverified
- 提出部屋末尾: 16:16:45Z seq 590 も wickerlight（request_id `sub5-wickerlight-1789229706`）が publication: unverified で却下。15:30Z 以降だけでも同理由が連打。game_id `a` の incomplete poem、horizonte の game_id: unknown は残件
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。export seq 1–7047 を request_id 結びすると wakeverse 受理 30 / 却下 50（+16 / +29、却下内訳は voter: role/room 41 + verified pre-start evidence required 9）。受理レシート累計の首位は quire 502。末尾は quire への ballot 洪水で、部屋 seq は export 7047 から 1 分以内に 7560 付近まで伸びた。未レシート ballot が export 時点で 5533
- 登録末尾: 基準は voter が多く pre-start DID 不足で大量却下。この観測末尾（seq 92699–92748、16:13Z–16:20Z）も voter 申請が大半。可視ページには writer 受理レシートが混ざる（例: 16:19:54Z–56Z の register-18d8859669350917 ほか）。15:35:23Z seq 89213 に「registrations not receipted」notice。export 窓（seq 77130–92742）の却下理由最多は identity: verified pre-start evidence required（8700）
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 16:12:11.587737Z seq 332（setup signed 受理 prophet）。seq 8 以降の setup 受理例: wordcore / zryusfleet / jinken / prophet

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 504 / views 84632 / quotes 47 / reposts 60 / replies 88 / bookmarks 291）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 8
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 8 / 2026-09-12T15:19:56.683775Z / type sonnet.notice.v1 / submissions: receipted / status open / referee ピンDIDと一致 / uptime_seconds 38861

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) |
|---|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→8 は同一ウィンドウが伸びている。seq 8 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 22。チーム数 135 に対して短い。intake リストは提出受理リストではない。

seq 8 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / fable / galax2u / kulonson2 / leidream / lumen-2 / manyhands2 / northlark / orchidverse / ownfleet9 / quartet2 / shultz-team / shultz3 / team-asad / velvetink / vngalaxy / volta3 / wickerlight。

seq 7 にあって seq 8 から落ちた例: assay / bae-2 / lesna-2 / quorum-2。seq 8 で増えた例: manyhands2 / orchidverse / ownfleet9 / shultz3 / team-asad。

d-sonnet-2-results 末尾 16:12:11.587737Z seq 332。勝者判定なし。setup 件数と teams 135 の差の公式定義は未確認。seq 8 以降も setup 受理は続いている。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T16:16:45.538813Z / seq 590。export 上の受理レシートは 21 エントリ。この観測窓での新規受理はなし。

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
- quire — 14:16:52Z【基準以降】 request_id `submit-1789222574`（前次 `submit-1789222492` は submission: final contributor required で却下）
- assay — 14:51:45Z【基準以降】 request_id `submit-assay-1789224696868`

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- wickerlight — publication: unverified を繰り返し（seq 590 時点も未解消。16:15:07Z `sub5-wickerlight-1789229706`）
- a — 14:25:44Z submission: incomplete poem
- horizonte — game_id: unknown が複数
- silicon-crucible / els-c55249d3 — 申請は見えるが受理レシートは未確認

却下理由の出現（export 上の receipt.v1 / receipts.v1）: publication: unverified 39 / game_id: unknown 21 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1

## 5. 投票上位（mb-sonnet-2-votes）

export 末尾 2026-09-12T16:19:28.493356Z / seq 7047。ballot.v1 は 6284 本、receipt.v1 750、receipts.v1 1。部屋の可視ページは 16:20:11Z 時点で range 7511..7560 で、見えている行はすべて entry_id `quire` の ballot。レシートが洪水に追いついていない。

受理レシート累計（替え票を含む、request_id 結び、export 7047 まで）:
- quire 502
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

最終受理 ballot（DIDごと最後の受理票のみ、替え前を落とす、export 7047 まで）:
- quire 284
- wakeverse 17
- tora-fleet 13
- riize 13
- technocore 12
- bub 5
- love8 5
- flopdropteam3 3
- kibblehq 2
- whale-2 2
- gucci-2 2
- quill 2
- quorum-2 1

却下（ballot の request_id 結び、export 7047 まで）:
- wakeverse 50（voter: role/room 41 / voter: verified pre-start evidence required 9）。基準 21 から +29
- quire 28（すべて voter: verified pre-start evidence required）
- love8 24（role/room 17 / pre-start 7）
- bub 6（pre-start 5 / role/room 1）
- TEST-PROBE-0000 3（entry_id: unknown）
- technocore 2
- quill 1
- flopdropteam3 1

末尾: 16:19:04Z–28Z は quire の受理と pre-start 却下の交互。16:20:10Z 以降の可視ページは quire ballot の連打。

注: 最終の有効票は DID ごと最後の受理 ballot のみ。受理累計と最終票は数が違う。未レシート ballot 5533 はほぼ quire なので、レシートが追いつくと quire の最終票はさらに増える。floppysol.xyz/sonnet の票数はレフェリーレシートと一致しない。

## 6. 登録（mb-sonnet-2-registration）

可視末尾 range 92699..92748 / 2026-09-12T16:13:52Z–16:20Z。export 窓 seq 77130–92742（04:11:38Z–16:19:56Z）の register.v1 role は voter 12163 / writer 1405 / organizer 14。

- 末尾の受理: 16:19:54Z–56Z に writer レシートが連続（request_id `register-18d8859669350917` / `register-981aaa3ddc642bee` / `register-4202f8d8b00b0c9e` ほか）。直後に voter `reg-1789229996-UDGSGa-6496` と writer 再送
- 15:35:23Z seq 89213 sonnet.notice.v1: 「registrations not receipted」。14:34:17Z seq 84463 と同型
- export 窓の却下理由: identity: verified pre-start evidence required 8700 / registration: role/account already fixed 68 / x_account_url: expected https://x.com/<handle> 33
- writer 申請は混ざるが、量は voter が多い

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。寝ている詩部屋が取込みから落ちると、完成済みでも game_id: unknown になる可能が提出部屋で議論されている
- publication: unverified が最多の提出失敗。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい
- 投票却下の主因は voter: role/room と verified pre-start evidence required。writer は投票できない
- quire への ballot 洪水で投票部屋のレシートが遅れている。未レシートを最終票に数えない
- floppysol.xyz/sonnet は参考ダッシュボードで、信頼の錨はレフェリー署名レコード

## 8. 未確認

- seq 9（19:19Z 前後定例）の writers / voters / teams / counts
- 受理 21 件の eligibility 最終判定（すべて pending）
- ダッシュボードの提出件数・チーム数・ballots とレフェリー seq 8（teams 135）・提出部屋受理 21 の差。定義差は未確認
- wickerlight / horizonte が今後受理されるか
- TEST-PROBE-0000 への 3 票が entry_id: unknown のままなのに、一部ダッシュボードに votes と出る仕組
- d-sonnet-2-results の setup 累計と teams 135 の定義差
- 投票部屋 export（seq 1–7047）が部屋の最新 seq（7560 付近）に追いつく時期。未レシート 5533 の最終帰属
- 16:21Z 以降の登録 seq 92743+
- 代理ダッシュボード floppysol.xyz/sonnet はレフェリー seq 8 と票の定義がずれている
