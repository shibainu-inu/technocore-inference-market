# Phase 7 file-bridge (orchestrator plans, the live bot executes)

The orchestrator never signs or posts. It reads the live bot's state file and writes JSON advice files; the live
bot (`sonnet/agent.py`) reads them on its 60 s tick and applies them through the same checks it applies to operator
switches (offline validator, accepted-prefix match, DID letters). Nothing here bypasses the referee.

```
sonnet/state-sonnet-2.json  --read-->  sonnet-orchestrator bridge tick  --write-->  sonnet/bridge/<game_id>.json
sonnet/policy.json          --read-->                                   --write-->  sonnet/bridge/roster-<game_id>.json
```

## Inputs (read-only)
- `state-sonnet-2.json`: `team {game_id, members[], ready, lead}`, `lead {game_id, members[], waitlist[], signed{}, declined[]}`,
  `poem {lines[], current[], last_contributor, frozen, version, contributors[]}`, `plan` (14 lines or null), `script {words[], who[]}`,
  `applications {did: {...}}`, `writers_ok {did: seq}`.
- `policy.json`: `did` (self), `lead_invites[]`, `slow_members[]`, `absent_members[]`, `lead_max_members`.
- Optional writer metrics: `data/fixtures/writer_scores_*.json` (latency medians, spam) via `diagnostics.metrics.load_writer_scores`.

## Output 1: plan file `sonnet/bridge/<game_id>.json`
```json
{
  "id": "<sha256 of lines+who, 12 hex>",
  "game_id": "nohitori-3",
  "generated_at": "2026-09-14T13:00:00Z",
  "members": ["did:key:...lead", "did:key:...", ...],          // exact set the plan was made for
  "prefix_len": 23,                                            // accepted words the plan keeps verbatim
  "lines": ["14 lines ...", ...],                              // validated with the official validator, exact ten
  "who": ["did:key:...", ...],                                 // one DID per word (len == word count); prefix positions = actual contributors
  "keys": [4, 2, 3, ...],                                      // number of members able to spell each word
  "fit_problems": [],                                          // two-key / adjacent-lead-only problems left (strings)
  "source": "orchestrator",
  "feasible": true
}
```
Rules for the writer (orchestrator):
- Regenerate only when: no file, members changed, accepted prefix diverges from `lines`, or the remaining assignment is
  infeasible for the currently available members (policy `slow_members`/`absent_members` treated as unavailable for
  lookahead; they still get words when nobody else can spell them).
- Never change `lines[:prefix]`; if the accepted words diverge, adopt them and regenerate the suffix only.
- `who` must alternate (no two consecutive equal DIDs), every member appears at least once after `prefix_len`
  when spellable, and the word after a lead-only word is never lead-only.
- If the poem is complete (`poem.frozen` and 14 lines accepted) write nothing new.

Rules for the reader (live bot, `apply_bridge`):
- Apply only when `game_id` equals the current lead/team game and `members` equals the current member set,
  `id` differs from `state.bridge_done`, `check_poem(lines)` passes, and `lines`' words start with the accepted words.
- Sets `state.plan = lines`; if the team is frozen, sets `state.script = {words, who}` and posts the turn script.
  Before freeze the plan feeds `key_fits_plan` (seating gate) and blocks the LLM planner.

### Text source (config `bridge.text_source`, default `bot`)
- `bot` (体制 b): the live bot's LLM (Opus, `make_plan`) writes the text — before the freeze as soon as
  `plan_min_members` (2) seats are filled, and after any reset. The bridge takes `state.plan` verbatim, validates it,
  assigns `who`, and writes the plan file with `source: "bot-text+orchestrator-assign"`. While the bot has no plan
  the bridge writes only the roster report. If the remaining words cannot be alternated by the available members, or the
  accepted words diverge from the text, the bridge writes `{"request": "replan", "reason": ...}` with a stable id; the
  bot clears its plan and the LLM rewrites from the accepted words (prefix enforced in the retry loop). The operator can
  always replace the text with `plan_override` before the freeze (the bot logs every adopted text to ATTENTION).
- `heuristic`: the bridge writes the text too (offline generator; valid form, plain poetry).

## Output 2: roster report `sonnet/bridge/roster-<game_id>.json`
```json
{
  "id": "...", "game_id": "...", "generated_at": "...",
  "members": [...], "missing_from_union": "", "single_key_letters": "lo", "lead_only_letters": "lo",
  "fragility": 0.12, "survivability": 0.67,
  "candidates": [ {"did": "...", "source": "waitlist|application|invite", "adds_letters": "lo", "lead_only_after": "", "fragility_after": 0.05, "rank": 1, "note": "..."} ],
  "advice": "one line for ATTENTION"
}
```
The live bot only logs `advice` to ATTENTION once per `id`; seating decisions stay with `key_fits_plan` + the operator.

## Auto GO (live bot)
Policy: `auto.next_entry_on_release: true`, `next_game_id: "nohitori-3"`, `bridge_dir: "sonnet/bridge"`.
When the referee's accepted submission receipt for the current team's game is seen in the submissions room, the bot
archives the finished game (same as the `lead_next_game` switch), withdraws, resets, and requests a team room for
`next_game_id`; recruiting then runs with the existing invite etiquette (1 message, windows, 6/h).
