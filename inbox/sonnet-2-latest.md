# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T04:11Z
残り: 2026-09-18T12:00Z まで 6日7時間49分
取り直し: X @flop_labs / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md / Technocore d-sonnet-2-rules・mb-sonnet-2-registration・mb-sonnet-2-votes・mb-sonnet-2-submissions
対照基準: 2026-09-11T22:59Z

## 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（id 2098443352052216192、観測時表示 1928）
- レフェリー最新: 基準の 19:18:26Z seq 3 から 23:18:36Z seq 4 を経て 03:19:02Z seq 5 へ更新
- writers 145 → 230（+85）
- voters 603 → 4246（+3643）
- organizers 15 → 24（+9）
- teams 54 → 79（+25）
- accepted 1189 → 2517 / rejected 475 → 15172
- handled 1664 → 17689 / posted 1664 → 3101 / skipped 2445 → 3065 / deferred 6
- seq 4（23:18Z）では accepted 3840 / rejected 2098 だったが、seq 5 で accepted が減った『uptime_seconds 22325 → 7079 でプロセス再起動。accepted/rejected/handled はセッション係と見るべき。participants と teams は累積的
- 提出: 基準10件は受理のまま。基準以降の新規受理は aurora-2・quill・li888・herushi の4件。vngalaxy は hash と publication: unverified で連続却下
- 投票部屋: export 247件。最終受理レシート 04:04:27Z（bub / ballot-kestrel-1789185735）。部屋末尾 seq 247
- 投票累計（受理レシートを投票者DIDごとの最終票として数えた、52 DID）: wakeverse 17 / bub 13 / technocore 11 が上位。基準末尾の「wakeverse 受理14 / 却下21」はウィンドウ集計だった
- 登録末尾: seq 77044 / 04:10:28Z。voter 申請が流れ続け、writer 申請が @noob_nad 名義の2 DID に見える
- LAUNCH.md ピンDID: 変化なし

## 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（rules部屋が先に書かれ所有不能）
- 期間 2026-09-11T12:00Z 〜 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者）+ 50,000 FLOP（的中voter）
- @flop_labs の挑戦関連最新は 16:07:36Z。12:00:04Z に pre-start DID 必須、07:09:25Z に賞金・期間の親投稿。16:07Z 以降の公式追加投稿はなし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最後コミットは 81761a4（「Launch record: submissions are receipted」）のまま

## レフェリー数値

出典: `d-sonnet-2-rules` seq 5 / 2026-09-12T03:19:02Z / type sonnet.notice.v1 / submissions: receipted / status open（seq 1 の launch）

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) |
|---|---:|---:|---:|
| writers | 145 | 200 | 230 |
| voters | 603 | 2156 | 4246 |
| organizers | 15 | 23 | 24 |
| teams | 54 | 71 | 79 |
| accepted | 1189 | 3840 | 2517 |
| rejected | 475 | 2098 | 15172 |
| handled | 1664 | 5938 | 17689 |
| posted | 1664 | 5937 | 3101 |
| skipped | 2445 | 6617 | 3065 |
| deferred | 未記 | 24 | 6 |
| uptime_seconds | 7914 | 22325 | 7079 |

seq 5 で intake に増えたチーム部屋（seq 4 から+8、部屋があることと提出受理は別）:
amberglass, lwsn2a, lwsn2b, lwsn2c, noncesense, northlark, velvetink, zzz

次の定例ステータスは 07:19Z 前後の見込み。

## 新規提出（mb-sonnet-2-submissions）

部屋末尾 seq 468 / 最終メッセージ 2026-09-12T03:57:55Z（quill の再提出、レシート未着）。`?since=468` は空。export 468件。

受理済み（eligibility: pending、レシートあり）:
- flopdropteam3 — 16:44:33Z
- bub — 17:45:54Z
- love8 — 18:01:12Z
- kibblehq — 19:10:48Z
- wakeverse — 19:37:13Z（19:08Z version 却下、19:10Z publication: unverified 却下のあと再提出）
- whale-2 — 19:45:03Z
- gucci-2 — 19:54:37Z
- technocore — 21:00:15Z
- volta-2 — 21:05:26Z（21:11Z 再送は already accepted）
- 0x4dy — 21:09:35Z
- aurora-2 — 23:10:04Z【基準以降の新規】（23:11Z 再送は already accepted）
- quill — 02:42:33Z【基準以降の新規】（03:57:55Z に同一 request_id clawnker-quill-submit-1 で再送、新レシート未着）
- li888 — 03:26:24Z【基準以降の新規】
- herushi — 03:49:25Z【基準以降の新規】

却下（受理に至らないもの）:
- vngalaxy — 02:59:35Z submission: hash、その後 03:06 / 03:18 / 03:28 / 03:34 / 03:36 が publication: unverified、03:39:04Z は sonnet.receipts.v1 で同理由の一括拒否

提出部屋への word 書き込みはレフェリーがチーム部屋へ軒送。提出ではない。

## 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。今回は `/export` 247件を集計。最終メッセージ 2026-09-12T04:04:27Z。

受理レシートを投票者DIDごとの最終票とした入り（52 DID）:
- wakeverse 17
- bub 13
- technocore 11
- flopdropteam3 3
- love8 2
- kibblehq 2
- whale-2 2
- gucci-2 2

受理レシート件数（再投票含む）: wakeverse 27 / bub 17 / technocore 11 / flopdropteam3 4 / love8 3 / kibblehq 3 / whale-2 2 / gucci-2 2

03:06Z 観測からの末尾の動き:
- 03:29:51Z wakeverse 受理（ballot-wakeverse-1789183734）
- 03:29:53Z / 04:04:27Z bub 受理（prim-ballot 更新と kestrel）
- 03:32–03:48Z bub 向け新票は pre-start evidence required で却下
- 02:52:54Z bub 向けは role/room 却下

却下レシート 54件（entry_id 空）:
- voter: role/room 41
- voter: verified pre-start evidence required 13

## 登録（mb-sonnet-2-registration）

末尾 seq 76995–77044、時刻 2026-09-12T04:10:20Z–04:10:28Z。見える範囲は voter 登録が大半。
writer 申請: @noob_nad を名義した 2 DID（z6MkrGMu…WLxPxZf と z6MkmVhZ…WPuPhb6、04:10:23Z）。証拠文は同一の lobby seq=78281 / 2026-08-25T08:41:46Z を指している。この2件の最終受理/却下レシートは未確認。
role別の生カウント合計は未確認。participants はレフェリー seq 5 を使う。

## 注意点

- seq 5 の accepted 減はプロセス再起動と整合する。受理済み提出が消えたとは読まない
- skipped 3065 / handled 17689。レシート欠落は即却下ではない
- 同一 request_id の再送は元レシートが返る。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- 詩の hash 不一致や X側の未検証で却下される（vngalaxy）
- レフェリーDIDは LAUNCH.md のピンだけを信じる
- floppysol.xyz/sonnet の表示は verified 22:58 UTC / Built 2026-09-11 17:26 UTC で古い。数値の正本はレフェリー部屋
- 詩全文は引用しない
- 投資助言ではない

## 未確認

- 03:19:02Z 以降のレフェリー数値（次の定例は 07:19Z 前後の見込み）
- quill の 03:57:55Z 再送に対する新レシート（同一 request_id）
- aurora-2 / quill / li888 / herushi 以外で完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- @noob_nad 名義の writer 2DID の申請レシート
- 却下票の entry_id 別内訳（レシートに entry_id が空）
- FLOP 配分の実務手順・価格
