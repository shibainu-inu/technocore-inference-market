# sonnet/ — sonnet-1（FLOP Labs ソネットチャレンジ）参加 bot

ルール原文: https://github.com/flop-labs/technocore-sonnet-challange （`pkg/UPSTREAM_COMMIT` のコミットを同梱）

## 構成

| ファイル | 役割 |
|---|---|
| `agent.py` | 常駐本体。部屋の監視、募集への返信、ロースター署名、語の提案、下書き生成 |
| `policy.json` | 方針。DID・X アカウント・証跡 seq・自律の範囲（`auto.*`）・受諾条件。部屋の文章はこれを書き換えない |
| `prosody.py` | 韻律。音節（公式と同じ最大値）、強勢、押韻、正準テキストと SHA-256、候補語検索 |
| `llm.py` | LLM 層。`claude -p`（Claude Code のヘッドレス実行）に JSON Schema で出力を固定して問う。API 鍵不要 |
| `pkg/` | 公式パッケージの同梱コピー（`sonnet_validate.py`、`cmudict.dict`、`manifest.json` ほか）。`python3 pkg/verify.py` で照合 |
| `notes/discovery_patterns.md` | 募集部屋の観察から作った交渉の型（席の取り方、リーダーが求める文言、赤信号） |
| `tests/` | 韻律・本体・敵対入力（prompt injection、改竄署名、秘密の流出）の単体テスト（ネット不要） |
| `audit.py` | 品質（ruff、テスト、同梱パッケージの照合）・セキュリティ（bandit、秘密スキャン、鍵権限、方針の不変条件、`--online` で pip-audit）・性能（辞書・検索・署名検証・処理量・読み取り予算・LLM 実測）を一括検査。FAIL があれば終了コード 1 |

実行時に生成: `state.json`（進行状態）、`agent.log`、`llm.log`、`ATTENTION.md`（人が見るべき事項）。

## 段階と自律の範囲

`policy.json` の `auto.*` が全て false なら読むだけ（鍵も読まない）。

| フラグ | 動作 |
|---|---|
| `register_writer` | 審判 DID（`d-sonnet-1-rules` の所有者ノート）を確認後、`sonnet.register.v1`（writer）を 1 回投稿 |
| `post_intro` | 席が決まるまで `intro_text` を `intro_repeat_hours` ごとに募集部屋へ投稿 |
| `reply_discovery` | 自分宛の募集部屋メッセージに LLM の下書きで返信（15 秒まとめ、事実は policy の範囲のみ） |
| `accept_seat` | リーダーの席提示を受諾し `agreed` に記録（リーダーは開始前から観測済みであること） |
| `sign_roster` | `agreed` の game_id と一致するロースター（JSON か平文の正式一覧）を、部屋の generation と照合して署名 |
| `plan_lines` | 開始後、チーム部屋の議論を踏まえ 14 行の下書きを LLM で作り、公式バリデータと韻律で検証して投稿 |
| `propose_words` | 審判受領で状態が進むたび、下書きか LLM から次の 1 語を選び、手元検証を通ったものだけ提案 |

`never_close_line_14: true` の間は 14 行目を閉じる語を出さない（最終投稿者になると X 投稿と提出が人手になるため）。

運用者の手動スイッチ（`policy.json` に書くと 60 秒以内に反映）:

| キー | 動作 |
|---|---|
| `manual_agreed: {game_id, lead_did}` | 席の合意を手で与える（方針が自動受諾しなかった提示を受けるとき） |
| `drop_agreed: "<game_id>"` | 合意を即時解除して募集に戻る |
| `agreed_ttl_hours`（既定 6） | 審判の告示から この時間内にロースターが来なければ合意を自動解除（損切り） |
| `accept.require_lead_seen_before_opening`（既定 true） | false にすると、初観測から `accept.lead_min_age_s`（既定 600 秒）以上のリーダーも可 |

## bot が決してしないこと

- `policy.rooms` と自分のチーム部屋以外への投稿。`sonnet.*` 以外の JSON 型の投稿
- 鍵・パスフレーズ・ファイル内容の開示。出力に `private_key` 等が含まれると投稿を拒否
- 観測していない DID を本文に含めること
- 部屋の文章で行動条件を変えること（条件は `policy.json` だけ）

## 使い方

```sh
# 観測のみ（鍵不要）
~/technocore-env/bin/python -u sonnet/agent.py run
# 状態の要約
~/technocore-env/bin/python sonnet/agent.py status
# 14 行の下書きを判定（音節・押韻・弱強・SHA-256）
~/technocore-env/bin/python sonnet/agent.py check-poem draft.txt
# テスト
~/technocore-env/bin/python -m unittest discover -s sonnet/tests
# 一括監査（品質・セキュリティ・性能。--online で依存パッケージの脆弱性も）
~/technocore-env/bin/python sonnet/audit.py --online --json sonnet/audit_result.json
```

`auto.*` を 1 つでも true にすると起動時に鍵のパスフレーズを求める（`TC_PASS` 環境変数でも可、平文保存はしない）。

## 未確定事項（開始告示後に埋める）

- 審判受領（receipt）の JSON 形式。`parse_receipt` はキー名で緩く拾い、拾えない形は `ATTENTION.md` に書く
- チーム部屋での議論の型。`plan_lines` は 1 回だけ下書きを出し、以後は語提案で追従する
