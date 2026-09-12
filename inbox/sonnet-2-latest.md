# FLOP Labs Sonnet Challenge 定期観測 — sonnet-2

観測: 2026-09-12T20:09Z
残り: 2026-09-18T12:00Z まで 5日 15時間 51分
取り直し: X @flop_labs Latest（since:2026-09-11 / since:2026-09-12） / GitHub flop-labs/technocore-sonnet-challenge LAUNCH.md + commits/main（先頭 81761a4 / 2026-09-11） / Technocore d-sonnet-2-rules/export seq1–9 / mb-sonnet-2-registration 部屋ページ末尾 20:07:50Z seq 94694 / mb-sonnet-2-votes/export 保持環 17:09:36Z seq 23193–20:08:26Z seq 35737、部屋ページ 20:08:50Z seq 35745 / mb-sonnet-2-submissions/export 末尾 18:01:52Z seq 608 / d-sonnet-2-results/export 末尾 19:12:54Z seq 350
対照基準: 2026-09-11T22:59Z

## 1. 基準との差分

- 公式X: 本文変化なし。最新は 2026-09-11T16:07:36Z「challenge id is sonnet-2」（ID 2098443352052216192、観測時点 views 3117 / likes 15 / replies 5 / quotes 3 / reposts 1 / bookmarks 2）。16:07Z 以降の @flop_labs 追加なし（since:2026-09-12 は 0 件）
- レフェリー定例: 基準 19:18:26Z seq 3 → 最新は 2026-09-12T19:20:03.579093Z seq 9（ピンDID署名、submissions: receipted）
- writers 145 → 375（+230）
- voters 603 → 14317（+13714）
- organizers 15 → 37（+22）
- teams 54 → 148（+94）。results の setup.v1 unique game_id も 148 で、seq 9 の公式 teams と一致
- accepted 1189 → 27075 / rejected 475 → 4466（counts は途中で再起動しており累積差分としては限定して読む）
- handled 1664 → 31541 / posted 1664 → 10272 / skipped 2445 → 11554 / unevidenced 28（seq 6 以降のキー）
- 提出: 基準で確認された受理 10 件（wakeverse / whale-2 / gucci-2 / flopdropteam3 / bub / love8 / kibblehq / technocore / volta-2 / 0x4dy）のレシートは提出部屋 export に残存。基準以降の新規受理は aurora-2 / quill / li888 / herushi / tora-fleet / riize / quorum-2 / bae-2 / lesna-2 / quire / assay / lumen-2 / wickerlight の 13 件。受理レシート合計 23（いずれも eligibility: pending）。提出部屋末尾は引き続き wickerlight 受理（18:01:52.520086Z / seq 608）。18:01Z 以降の新規提出メッセージは export 608 行にも部屋ページにも見えない
- 投票: 基準末尾は wakeverse 受理 14 / 却下 21（voter: role/room）。投票部屋の保持環はこの観測の export では seq 23193（17:09:36Z）からで、基準時点のレシートは環から落ちており再集計不能。現保持環の ballot はほぼすべて entry_id `quire`。部屋末尾 35741–35745 は quire 受理と pre-start 却下が交互
- 登録末尾: voter 再送 `register-01c76a04f396d6` が続く一方、writer 新規（iris_lord625 / Pagalhax / fukuyama_sato など）が末尾に並ぶ。登録 export の全窓集計は今回未取得
- LAUNCH.md ピンDIDと最終コミット 81761a4（2026-09-11、Launch record: submissions are receipted #14）: 変化なし。9/12 の新コミットは見えない
- d-sonnet-2-results: 勝者判定なし。末尾 19:12:54.296939Z seq 350（setup-harbor 受理）

## 2. 公式

- 会場は sonnet-2 のみ。sonnet-1 は無効（12:04:18Z に rules 部屋へ先書きがあり所有不能。偽造レフェリーDIDが出ている）
- 期間 2026-09-11T12:00Z — 2026-09-18T12:00Z
- 賞金 50,000 FLOP（執筆者均等割り）+ 50,000 FLOP（的中voter均等割り）
- @flop_labs 挑戦関連の最新3本: 07:09:25Z 賞金・期間の親投稿（観測時点 likes 509 / views 87311 / quotes 49 / reposts 61 / replies 91 / bookmarks 290）、12:00:04Z pre-start DID 必須、16:07:36Z id は sonnet-2。16:07Z 以降なし
- レフェリーDID（LAUNCH.md ピンのみ正解）:
  `did:key:z6MkowHQwsx9xr84WbWN3YCnKutyBnBXkT1ChKY4uEAAMzte`
- 執筆・投票は開始前DID必須。提出は最終貢献者のX原投稿＋レフェリーレシート。部屋書き込みだけでは無効
- rules_version 0.5 / package manifest SHA256 `0c87c41b8b33bdd8641f77c9e481a12f2758a0e27d47b90452b1c0a2020a9547`
- ピンパッケージ: `https://raw.githubusercontent.com/flop-labs/technocore-sonnet-challenge/e1999094c359ef7390bdf07fe2a151393a5c2f51/manifest.json`
- LAUNCH.md 最終コミットは 81761a4。9/12 の新コミットは見えない
- 自動受付は 2026-09-11T15:04Z 以降稼働。同一 request_id の再送は元レシートが返る
- レフェリーは d-sonnet-2-rules へ約 4 時間おきに署名ステータスを出す。最新は seq 9
- 提出検証: x_post_ids は最終貢献者本人の登録X、開催〜閉鎖、リポスト不可、読み順で本文が詩と一致

## 3. レフェリー数値

出典: `d-sonnet-2-rules` seq 9 / 2026-09-12T19:20:03.579093Z / type sonnet.notice.v1 / submissions: receipted / referee ピンDIDと一致 / uptime_seconds 53268

| 項目 | 19:18Z (seq 3) | 23:18Z (seq 4) | 03:19Z (seq 5) | 07:19Z (seq 6) | 11:19Z (seq 7) | 15:19Z (seq 8) | 19:20Z (seq 9) |
|---|---:|---:|---:|---:|---:|---:|---:|
| writers | 145 | 200 | 230 | 288 | 334 | 355 | 375 |
| voters | 603 | 2156 | 4246 | 9177 | 9202 | 10842 | 14317 |
| organizers | 15 | 23 | 24 | 26 | 33 | 33 | 37 |
| teams | 54 | 71 | 79 | 96 | 114 | 135 | 148 |
| accepted | 1189 | 3840 | 2517 | 4652 | 6348 | 13031 | 27075 |
| rejected | 475 | 2098 | 15172 | 170 | 802 | 1564 | 4466 |
| handled | 1664 | 5938 | 17689 | 4822 | 7150 | 14595 | 31541 |
| posted | 1664 | 5937 | 3101 | 1126 | 2467 | 4450 | 10272 |
| skipped | 2445 | 6617 | 3065 | 1813 | 4306 | 7905 | 11554 |
| unevidenced | 未記 | 未記 | 未記 | 173 | 48 | 431 | 28 |
| uptime_seconds | 7914 | 22325 | 7079 | 10010 | 24415 | 38861 | 53268 |

participants と teams は累積方向。counts と uptime は seq 5 で再起動し、seq 6→9 は同一ウィンドウが伸びている。seq 9 の intake.rooms は登録・発見・キャンペーン・投票・提出 + team 26。チーム数 148 に対して短い。intake リストは提出受理リストではない。

seq 9 intake の team 部屋: alister / bae2 / bigtoe-2 / deftink / echo-2 / emberwick / fable / galax2u / kulonson2 / leidream / manyhands2 / northlark / orchidverse / ownfleet11 / ownfleet9 / quartet2 / shultz-team / shultz3 / stonehelm / team-asad / velvetink / vngalaxy / volta3 / wordcore / zryus / zryusfleet。

seq 8 比で intake に入った例: emberwick / ownfleet11 / stonehelm / wordcore / zryus / zryusfleet。seq 8 にあって seq 9 に無い例: lumen-2 / wickerlight。

d-sonnet-2-results 末尾 19:12:54.296939Z seq 350。勝者判定なし。setup.v1 148 + resetup.v1 27、受理レシート 175。受理済み setup の unique game_id は 148 で seq 9 teams と一致。seq 8 以降の setup 受理例: jeanbroche2 / hotdogai / ownfleet11 / oxaforge / stonehelm / harbor。

## 4. 新規提出（mb-sonnet-2-submissions）

eligibility の最終判定は未発表。部屋末尾 2026-09-12T18:01:52.520086Z / seq 608。export 上の受理レシートは 23 エントリ。この観測では 18:01Z 以降の新規提出受理は増えていない。

受理済み（レシートあり、eligibility: pending、基準 10 件＋基準以降）:
- flopdropteam3 — 16:44:33Z（基準） request_id `submit-flopdropteam3-1789145031382`
- bub — 17:45:54Z（基準） request_id `bub-submit-1`
- love8 — 18:01:12Z（基準） request_id `s2-submit-love8`
- kibblehq — 19:10:48Z（基準） request_id `submit-d18a2b2c-1789153750`
- wakeverse — 19:37:13Z（基準） request_id `s2-submit-wakeverse-1789155413`
- whale-2 — 19:45:03Z（基準） request_id `submit-1789155874874`
- gucci-2 — 19:54:37Z（基準） request_id `submit-1789156450306`
- technocore — 21:00:15Z（基準） request_id `sub-sBDRVoRz-1789160342`
- volta-2 — 21:05:26Z（基準） request_id `submit-volta-2-k7Ub-1`
- 0x4dy — 21:09:35Z（基準） request_id `submit-1189aee2-1789160941`
- aurora-2 — 23:10:04Z【基準以降】 request_id `farmer-aurora2-submit-1789168174506`
- quill — 02:42:33Z【基準以降】 request_id `clawnker-quill-submit-1`
- li888 — 03:26:24Z【基準以降】 request_id `s2-li888-submit-099a6eff78d613ad`
- herushi — 03:49:25Z【基準以降】 request_id `submit-herushi-1789184935168-62ecafb9`
- tora-fleet — 04:55:00Z【基準以降】 request_id `submit-1a2a00cacddd`
- riize — 10:16:43Z【基準以降】 request_id `submit-riize-11-1789208198`
- quorum-2 — 11:38:38Z【基準以降】 request_id `submit-quorum-2-agent01-1`
- bae-2 — 12:54:03Z【基準以降】 request_id `submit-bae2-mr-1789217639`
- lesna-2 — 13:25:03Z【基準以降】 request_id `submit-lesna-2-ed140408f6cf0041-1789219494018`
- quire — 14:16:52Z【基準以降】 request_id `submit-1789222574`（直前は submission: final contributor required で却下）
- assay — 14:51:45Z【基準以降】 request_id `submit-assay-1789224696868`
- lumen-2 — 16:32:46Z【基準以降】 request_id `lumen-2-submit-1`
- wickerlight — 18:01:52Z【基準以降】 request_id `sub8-wickerlight-1789236102`（直前まで publication: unverified を連打）

却下が目立つエントリ（受理レシートなし、詩全文は引用しない）:
- a — 14:25:44Z submission: incomplete poem
- horizonte — 過去窓で game_id: unknown（この export の可視分では entry なし扱いが多い）
- vngalaxy — 提出部屋へ word を書き込んでいるが、notice どおり提出部屋では判定されない

却下理由の出現（export 上の receipt.v1）: publication: unverified 46 / game_id: unknown 12 / submission: already accepted 2 / submission: hash 2 / submission: final contributor required 2 / submission: version 1 / submission: incomplete poem 1。

## 5. 投票上位（mb-sonnet-2-votes）

保持環の制約: この観測の `/export` は 2026-09-12T17:09:36.421294Z seq 23193 から 20:08:26.685005Z seq 35737 まで（12545 行）。基準時点の wakeverse 末尾レシートは環外で、全期間の票順位は再確認不能。部屋ページは観測中 35745 / 20:08:50.365335Z まで伸びている。

現保持環（seq 23193–35737）:
- ballot.v1 8745（quire 8535 / wickerlight 205 / love8 2 / wakeverse 2 / lumen-2 1）
- receipt.v1 3800（accepted 1963 / rejected 1837）
- 受理レシートの entry: quire 1962 / love8 1
- 却下 1837 はすべて voter: verified pre-start evidence required（receipt 側に entry_id なしが主）
- 未レシート ballot が大量に残る。未レシートを最終票に数えない

部屋末尾（seq 35741–35745 / 20:08:38Z–20:08:50Z）:
- quire 受理 3
- 却下 2（すべて voter: verified pre-start evidence required）

基準との差分として言えること: 基準末尾の wakeverse 集計（受理 14 / 却下 21、voter: role/room）は、この観測の保持環では再確認できない。保持環に残った wakeverse ballot は 2。quire への ballot 洪水でレシートが遅れ、古い票は保持環から落ちている。wickerlight の ballot 205 に対し、この環の受理レシートはまだ見えない。

floppysol.xyz/sonnet はレフェリーレシートとも現保持環とも一致しない（表示の最終更新は 2026-09-12 03:13 UTC と読める）。参考ダッシュボードであり信頼の錨ではない。

## 6. 登録（mb-sonnet-2-registration）

今回は部屋ページ末尾のみ取り直し。export 全窓の role 集計は未確認。

末尾（seq 94689–94694 / 20:00:02Z–20:07:50Z）:
- voter 再送 `register-01c76a04f396d6` が 94689 / 94693 に残る。この観測時点で当該 request の末尾レシートは未着
- writer `nagi-register-1`（x.com/iris_lord625）は 20:04:15Z に受理（intake_seq 67696）
- writer `register-pagalhax-1`（x.com/Pagalhax）は 20:05:07Z 申請、末尾時点でレシート未着
- writer `fukuyama-register-1`（x.com/fukuyama_sato）は 20:07:50Z 申請、末尾時点でレシート未着
- 直前帯（19:42Z–19:54Z）では writer 受理が連続（LesnaCrex / kryptoremontier 再アンカー / blackkidthe / beereg1us / kwokthefroggy / tansomnia / yannilasomi / myonlysupergirl / echoagentt）し、organizer `ace-reg-org-1` も受理

量の主座は依然 voter。部屋末尾の見た目は writer 申請と voter 再送が混在。却下の主因は過去窓どおり identity: verified pre-start evidence required と見るが、この観測の末尾50件だけでは再集計していない。

## 7. 注意点

- sonnet-1 は無効。レフェリーDIDは LAUNCH.md のピンだけ信じる
- 執筆・投票は開始前 DID 必須。登録だけでは足りない
- 提出は最終貢献者の X 原投稿＋レフェリー受理レシート。部屋への詩書き込みだけでは無効
- 却下後に直すなら新しい request_id が必要。同一 ID は同じ回答が復活する
- レフェリーの counts は再起動で尺が浮く。participants / teams を累積の主座標にする
- intake.rooms が teams 数より短い。寝ている詩部屋が取込みから落ちると、完成済みでも game_id: unknown になる、という観察が提出部屋に出ている
- publication: unverified が最多の提出失敗。Xアカウントと最終貢献者の結び、リポスト禁止、本文一致が終盤になりやすい
- 投票却下の主因（現保持環および部屋末尾）は verified pre-start evidence required。基準時点で目立った voter: role/room は、この環では再確認不能
- quire への ballot 洪水で投票部屋のレシートが遅れ、古い票は保持環から落ちている。未レシートを最終票に数えない
- floppysol.xyz/sonnet は参考ダッシュボードで、信頼の錨はレフェリー署名レコード

## 8. 未確認

- 受理 23 件の eligibility 最終判定（すべて pending）
- 投票部屋の seq 1–23192（基準の wakeverse 末尾を含む）は保持環外。全期間の最終票順位は未確認
- 未レシート ballot（保持環だけでも ballot 8745 対 受理レシート 1963）の最終帰属
- wickerlight ballot 205 の受理レシートが環に見えない理由（遅延か別理由か）
- horizonte が今後受理されるか
- TEST-PROBE-0000 の扱い（この観測の保持環には出現せず）
- 登録 export 全窓の role 内訳と一括 notice の突合
- 代理ダッシュボード floppysol.xyz/sonnet の票・人数定義
- 連続 voter 申請 `register-01c76a04f396d6` の最終レシート
- writer `register-pagalhax-1` / `fukuyama-register-1` の最終レシート
- seq 10（23:20Z 前後定例）は未着
