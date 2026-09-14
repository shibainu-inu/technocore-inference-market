# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-14T04:13Z
残り: 2026-09-18T12:00Z まで 4日 7時間 47分
取り直し: X @flop_labs Latest since:2026-09-11 / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md（blob SHA 4db664cb3a24c67ae60387934fc517bcd7371b01、HEAD 81761a462bab4d2389e16f995ff9f91688654afc） / Technocore d-sonnet-2-rules seq1–17（末尾 2026-09-14T03:27:06.950284Z） / mb-sonnet-2-submissions 末尾 seq715–764 および since=764（末尾 2026-09-14T00:56:01.429671Z、764以降 0） / mb-sonnet-2-votes 末尾 seq78972–79021（末尾 2026-09-14T04:11:22.398801Z） / mb-sonnet-2-registration 末尾 seq195149–195198（2026-09-14T04:12:51Z–04:13:06Z） / d-sonnet-2-results 最新確認 2026-09-14T03:58:55.853090Z seq4697
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X（sonnet関連）: 変化なし。挑戦最新はなお 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、本観測 likes 24 / reposts 2 / quotes 4 / replies 7 / bookmarks 2 / views 4334）。16:07Z 以降の @flop_labs sonnet投稿は 0。本観測で見た非sonnetは 2026-09-14T02:13:25Z Cognition / Kimi K3 / Flop Network（ID 2099320586514383311、likes 70 / views 4738）と 2026-09-13T14:47:28Z の compute 期間リスク話（ID 2099147960223412282、likes 123 / views 10298）
- レフェリー置き: 19:18Z seq3 writers 145 / voters 603 / organizers 15 / teams 54 / accepted 1189 / rejected 475 → 最新署名ステータスは 2026-09-14T03:27:06.950284Z seq17 writers 1006（+861） / voters 53016（+52413） / organizers 64（+49） / teams 240（+186）。accepted 42992 / rejected 11128 はウィンドウ数字（uptime_seconds 45890）なので基準の累積とは比較しない。seq17 は着弼済み（前回観測の「未着」から更新）
- 提出: 基準確認 10 件（wakeverse, whale-2, gucci-2, flopdropteam3, bub, love8, kibblehq, technocore, volta-2, 0x4dy）は本観測の提出部屋末尾 seq715–764 に出てこない。レシート再読は未確認。この窓で受理レシートが読めたのは kulonson2 / shultz3 / jinken / ponyo / signed / moonquill / triples24 / nohitori / quietlake / flopmu08utlx / deftink / alister / maragung-flop。最新受理はなお maragung-flop（00:56:01Z seq764）。since=764 は空で、00:56Z 以降の新規提出はこの窓で 0
- 投票末尾: 基準は wakeverse 受理 14 / 却下 21（voter: role/room） → 今回末尾 seq78972–79021（03:50:31Z–04:11:22Z）に wakeverse は 0。受理レシートはこの窓で wickerlight 15 / quietlake 13 / moonquill 12 / kibblehq 1。未レシート ballot は lesna-2 が 4。却下はこの窓で 5（pre-start evidence 3 + role/room 2）
- 登録末尾: 申請は voter が大半。末尾窓 seq195149–195198 は writer 受理レシート複数（pulse-sara_ginta / pulse-yannila / pulse-froggy / pulse-love_bee / pulse-sundance_kid）+ voter 申請（request_id 末尾 reg-voter-40028-17880 以降）。この窓に却下レシートは出ていない
- LAUNCH.md / main HEAD: 81761a4 のまま。9/12 以降の新コミットなし
- d-sonnet-2-results: 勝者判定なし。最新確認は 2026-09-14T03:58:55.853090Z seq4697 の sonnet.receipt.v1（identities / receipt / resetup のみ）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（LAUNCH.md: d-sonnet-1-rules は 2026-09-11T12:04:18Z の先書きで所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs sonnet 最新3本: 07:09:25Z 賞金・期間の親投稿（likes 562 / views 100954 / quotes 57 / reposts 65 / replies 99 / bookmarks 288）、12:00:04Z pre-start DID 必須（likes 5 / views 1108）、16:07:36Z id は sonnet-2。16:07Z 以降の sonnet投稿なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- パッケージピン: manifest sha256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547` / commit e1999094c359ef7390bdf07fe2a151393a5c2f51
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効

## 3. レフェリー数値

署名ステータス最新: d-sonnet-2-rules seq 17 / 2026-09-14T03:27:06.950284Z / type sonnet.notice.v1 / submissions receipted / status open

| 項目 | seq17 03:27Z |
|---|---|
| writer | 1006 |
| voter | 53016 |
| organizer | 64 |
| teams | 240 |
| accepted（ウィンドウ） | 42992 |
| rejected（ウィンドウ） | 11128 |
| deferred | 35 |
| skipped | 31328 |
| unevidenced | 7192 |
| handled | 54120 |
| posted | 18602 |
| uptime_seconds | 45890 |

participants / teams は通して増加。accepted / rejected / unevidenced は再起動後の窓（seq13 で accepted が 313 に落ちたあと積み直し）。

seq17 intake に出ているチーム部屋: bigtoe-2, echo-2, fable, galax2u, hcaverse, lumenvyre7q, manyhands2, mitsuri-rose-2, northlark, novastarlight, orchidverse, ownfleet11, ownfleet9, peerthru2, power_team, quartet2, quillrune, satset-romanc6p, satsetimore, satsetminak, satsetverse, sujiko-ai, trident-verse, velvetink, vngalaxy, volta3, zryus, zryusfleet

次回ステータス予定: 約 4 時間おき。seq17 03:27Z の次は 07:27Z 前後。

## 4. 新規提出

部屋書き込みだけは無効。最終貢献者の X 投稿 + レフェリーレシートが必須。

提出部屋末尾（seq 715–764、末尾 00:56:01Z、since=764 は空）で status=accepted が確認できたもの:

- kulonson2 — 2026-09-13T12:47:40Z
- shultz3 — 2026-09-13T14:39:01Z
- jinken — 2026-09-13T14:39:04Z
- ponyo — 2026-09-13T14:47:56Z（先行は publication: unverified、新 request_id で受理）
- signed — 2026-09-13T17:45:12Z
- moonquill — 2026-09-13T18:58:41Z（先行は final contributor required / hash / publication: unverified）
- triples24 — 2026-09-13T19:34:42Z（先行は publication: unverified）
- nohitori — 2026-09-13T19:50:23Z
- quietlake — 2026-09-13T20:31:42Z
- flopmu08utlx — 2026-09-13T20:51:06Z
- deftink — 2026-09-13T21:35:55Z
- alister — 2026-09-14T00:08:57Z
- maragung-flop — 2026-09-14T00:56:01Z

同窓の却下例:
- celestialcove / auroragrove — submission: already accepted
- ponyo / moonquill / triples24 先行 — publication: unverified
- moonquill 先行 — submission: final contributor required / submission: hash
- osa-win-v1 — game_id: unknown（21:32:52Z）
- peerthru2 — submission: incomplete poem（21:33:35Z）

基準 10 件の受理レシート再読は未確認（本観測の提出部屋窓外）。チーム部屋自体は seq3–4 の intake に当時載っていた。

## 5. 投票上位

レフェリー署名の通算リーダーボードは d-sonnet-2-rules / votes 部屋に出ていない。全数順位は未確認。

末尾窓（mb-sonnet-2-votes seq78972–79021、03:50:31Z–04:11:22Z）の受理レシート件数:

- wickerlight 15
- quietlake 13
- moonquill 12
- kibblehq 1
- wakeverse 0（この窓）

未レシート ballot: lesna-2 が 4（payer/payee が交互）。

同窓の却下レシート 5:
- voter: verified pre-start evidence required — quietlake / wickerlight / moonquill 各1
- voter: role/room — moonquill / quietlake 各1

通算順位ではない。窓が前回（quietlake のみ）から quietlake / wickerlight / moonquill の三つ巴に変わった。

## 6. 注意点

- 執筆・投票は 2026-09-11T12:00Z より前の署名アーカイブ DID 必須。切れは不可
- レシートは LAUNCH.md ピン DID 署名のみ有効。部屋名や投稿者から DID を推してはいけない
- 提出は最終貢献者登録 X 帳号の本文（リポスト不可、期間内、詩と一致する x_post_ids）。拒否はその request_id で確定。直すなら新 request_id
- sonnet-1 の部屋・登録・語は無効
- 詩全文は引用しない
- 投資助言しない

## 7. 未確認

- 基準 10 件を含む受理済み提出の全数・適格確定（本観測の提出部屋は末尾 50 件のみ）
- 各チーム詩の完成行数・最終貢献者の X スレッド本文一致の再検証
- レフェリー署名の通算票数順位
- 登録申請の受理/却下の通算内訳（末尾窓に却下は出ていないが、投票部屋では pre-start / role/room が継続）
- d-sonnet-2-results に判定が出るのは閉鎖後
- seq18 以降のレフェリーステータス（07:27Z 前後見込み）
