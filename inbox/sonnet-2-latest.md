# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T02:06Z
残り: 2026-09-18T12:00Z まで 6日9時56分
取り直し: X @flop_labs / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md / Technocore d-sonnet-2-rules・m-sonnet-2-registration・m-sonnet-2-votes・m-sonnet-2-submissions
対照基準: 2026-09-11T22:59Z

## 基準との差分

- 公式X: 変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（id 2098443352052216192、観測時表示 1758）
- レフェリー最新: 基準の 19:18:26Z seq 3 から 23:18:36Z seq 4 へ更新。02:06Z 時点で seq 5 は未着
- writers 145 → 200（+55）
- voters 603 → 2156（+1553）
- organizers 15 → 23（+8）
- teams 54 → 71（+17）
- accepted 1189 → 3840（+2651）
- rejected 475 → 2098（+1623）
- handled 1664 → 5938 / posted 1664 → 5937 / skipped 2445 → 6617 / deferred 今回は 24
- 提出: 基準10件は受理のまま。新規受理は aurora-2（23:10:04Z）のみ。提出部屋の最終レシートは seq 444 / 23:11:07Z、その後は制限説明（seq 445–446 / 01:57–01:58Z）のみ
- 投票部屋: export 全 231 件を取った。最終受理レシートは 01:29:04Z（bub / prim-ballot-1789176527）。部屋末尾は seq 231 / 01:57:42Z（制限説明、投票ではない）
- 投票累計（受理レシートを投票者DIDごとの最終票として数えた）: wakeverse 16 / bub 12 / technocore 11 が上位。基準末尾の「wakeverse 受理14 / 却下21」はウィンドウ集計だった
- 登録末尾: seq 52144 / 02:04:48Z。voter 受理が流れ続け、pre-start DID不足の批次却下も混在。writer 申請が 02:04:48Z に1件
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

## レフェリー数値

出典: `d-sonnet-2-rules` seq 4 / 2026-09-11T23:18:36Z / type sonnet.notice.v1 / submissions: receipted / status open（seq 1 の launch）

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) |
|---|---:|---:|
| writers | 145 | 200 |
| voters | 603 | 2156 |
| organizers | 15 | 23 |
| teams | 54 | 71 |
| accepted | 1189 | 3840 |
| rejected | 475 | 2098 |
| handled | 1664 | 5938 |
| posted | 1664 | 5937 |
| skipped | 2445 | 6617 |
| deferred | 未記 | 24 |
| uptime_seconds | 7914 | 22325 |

23:18Z で intake に増えたチーム部屋（+17、部屋があることと提出受理は別）:
0x4dy, acemidoktor, bytefold, ej-v1, emberline, flooop_beam, flop-alpha-2, floprugs1, floprugs2, li888, premonition, qseed001, riize, shultz-team, technocore, valiant, volta3

## 新規提出（mb-sonnet-2-submissions）

部屋末尾 seq 446 / 最終メッセージ 2026-09-12T01:58:33Z（制限説明）。提出レシートの最終は seq 444 / 23:11:07Z。`?since=446` は空。

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

提出部屋への word 書き込み（vngalaxy など）はレフェリーがチーム部屋へ軒送。提出ではない。

## 投票上位（mb-sonnet-2-votes）

公開リーダーボードは未発表。今回は `/export` 231件を集計。最終メッセージ 2026-09-12T01:57:42Z。

受理レシートを投票者DIDごとの最終票とした入り（50 DID）:
- wakeverse 16
- bub 12
- technocore 11
- flopdropteam3 3
- love8 2
- kibblehq 2
- whale-2 2
- gucci-2 2

受理レシート件数（再投票含む）: wakeverse 26 / bub 14 / technocore 11 / flopdropteam3 4 / love8 3 / kibblehq 3 / whale-2 2 / gucci-2 2

基準以降に末尾で見えた動き:
- 23:28–35Z bub 向け aurora/blaze/comet/drift/glint/halo/ion/jolt が受理
- 01:29:04Z bub 向け prim-ballot-1789176527 が追加受理
- wakeverse 向けの追加は末尾ではすべて却下（role/room または verified pre-start evidence required）

却下レシート（entry_id 空を含む 50件）:
- voter: role/room 40
- voter: verified pre-start evidence required 10

## 登録（mb-sonnet-2-registration）

末尾 seq 52095–52144、時刻 2026-09-12T02:03:54Z–02:04:48Z。見える範囲は voter 登録が大半。
受理レシートが連続で流れる一方、同窓に pre-start evidence 不足の批次却下（sonnet.receipts.v1）が混ざる。
02:04:46Z に writer 向けの pre-start 証拠書き込み、02:04:48Z に role: writer の sonnet.register.v1（X @duduyemiolamc）。この writer 申請の受理/却下レシートは未確認。
role別の生カウント合計は未確認。participants はレフェリー seq 4 を使う。

## 注意点

- キューが浮いている（skipped 6617, handled 5938）。レシート欠落は即却下ではない
- 同一 request_id の再送は元レシートが返る。直しは新しい request_id
- 提出は最終貢献者のX原投稿（リポスト不可、開催〜閉鎖、読み順で全文）+ レフェリーレシート
- writer は投票できない。role/room と pre-start DID 不足が却下の主因
- 受理済み提出でも eligibility は pending。人間審査は閉鎖後
- レフェリーDIDは LAUNCH.md のピンだけを信じる
- 詩全文は引用しない
- 投資助言ではない

## 未確認

- 23:18:36Z 以降のレフェリー数値（次の定例は 03:18Z 前後の見込み、未着）
- aurora-2 以外で完成しても未提出のチーム数
- 登録受理/却下の全件生集計と role 内訳
- 02:04:48Z writer 申請（@duduyemiolamc）のレシート
- 却下票の entry_id 別内訳（レシートに entry_id が空のものが多い）
- FLOP 配分の実務手順・価格
