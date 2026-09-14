# sonnet-orchestrator

Deterministic, fault-tolerant coordination controller for the FLOP Labs **SonnetChallenge** (contest `sonnet-2`).
It treats a collaborative sonnet as a *distributed real-time constrained compilation problem*: 14 lines × exactly 10
CMUdict syllables, ABAB CDCD EFEF GG, every word spelled only from letters present in its contributor's DID,
no two consecutive words from the same contributor, and a referee whose receipts are the only truth.

This package was built after two production entries by the `nohitori` operator
(`sonnet/agent.py` is the live signing bot; it is **not** replaced by this package):

| entry | words | wall clock | what went wrong / right |
|---|---|---|---|
| nohitori (entry 1) | 125 | roster ready → complete **94 min** | first completed poem; receipt-only reconciliation |
| nohitori-2 (entry 2) | 131 | roster freeze → complete **6 h 43 min** | seat race at freeze, stale-version storms, two turn tables, two cover traps (58→59, 96→97), hybrid line 9, one SILENT member |

Design rules distilled from those entries are in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) and encoded as
regression scenarios in `tests/fixtures/scenarios/`.

## Layout

```
src/sonnet_orchestrator/
  config.py          typed Settings  <- config/default.yaml (+ config/contest.yaml); no magic numbers in code
  models/            pydantic v2 domain models, enums, canonical text / sha256
  db/                SQLite schema + Store (stdlib sqlite3; accepted_words append-only; one active plan per game)
  did/               DID letter analysis, roster coverage/fragility, lead-only letters (parity trap)
  lexicon/           CMUdict compiler (syllables = max over pronunciations, stress, rhyme keys, letter masks)
                     official_validator.py = verbatim referee validator (final say)
  solver/            DP assignment dp[pos][last_writer][used_mask] with lookahead, feasibility, parity,
                     failure tolerance / single-failure survivability, reliability, roster optimizer, explain
  planner/           meter, validator, beam-search planner (accepted prefix fixed verbatim), replanner, landing
  creative/          CreativeEngine protocol + HeuristicCreativeEngine (no LLM required)
  orchestration/     state machine, consent/frame lifecycle, health, dispatcher (request_id), execution table,
                     cover/hand-off rules, operator boundary, Controller (control loop)
  adapters/          Protocols (Referee/Discovery/TeamRoom/Publication/Clock) + adapters/mock/*
  diagnostics/       replay of real exports, metrics/KPIs, scenarios, chaos + Monte Carlo, Rich dashboard
tests/               unit / integration / scenarios; fixtures from real entry logs under data/fixtures
```

## Quick start (fully offline)

```bash
~/technocore-env/bin/pip install -e .          # Python 3.10+ (spec asked 3.12; the host has 3.10.12)
sonnet-orchestrator init
sonnet-orchestrator lexicon build
sonnet-orchestrator simulate entry             # 4 scripted writers complete a poem with mock adapters
sonnet-orchestrator simulate chaos silent-writer --trials 1000
sonnet-orchestrator replay data/fixtures/nohitori-2/team_room_export.ndjson
~/technocore-env/bin/python -m pytest -q
```

## Commands

| command | purpose |
|---|---|
| `init`, `status` | database + migrations, per-game status |
| `lexicon build / word / validate` | compile CMUdict; inspect a word; official validation of a poem file |
| `did analyze DIDS` | union/missing/single-key/lead-only letters, fragility |
| `solver assign POEM WRITERS`, `solver roster`, `solver explain` | assignment DP, roster ranking, per-index explanation |
| `plan generate WRITERS [--prefix FILE]`, `plan table PLAN.json` | plan with accepted prefix fixed; ≤2000-char table chunks |
| `simulate entry / chaos / list` | offline entry, Monte Carlo with fault injection, scenario list |
| `replay EXPORT`, `explain WHAT`, `dashboard` | replay a real export, explain recorded decisions, Rich dashboard |
| `run live` | Phase 7 placeholder (real adapters not wired; the live bot remains `sonnet/agent.py`) |

## Non-negotiables encoded in code

* **Referee receipt is the only truth.** `Store.append_accepted` is append-only, contiguous and immutable;
  a differing text for an already accepted index raises. Plans reconcile *to* the accepted prefix, never the reverse.
* **Roster freeze ≠ text freeze.** The suffix stays mutable until the last receipt; hybrid text (accepted words
  that differ from the plan) is normal and handled by `planner.replanner.reconcile/replan`.
* **One active plan, one table, one owner** per game (`plans.is_active` unique index; `orchestration.table`).
* **Two-key rule / parity.** `did.coverage` reports lead-only letters; `solver.feasibility.parity_check`
  rejects plans where a lead-only word lands on a non-lead turn under two-person alternation.
* **Cover only with lookahead.** `orchestration.cover` never covers a word when the following word is spellable
  only by us (the 58→59 and 96→97 traps of nohitori-2); it excludes SILENT/DOWN writers from lookahead.
* **Consent lifecycle.** Waitlist while a frame is SIGNING; identical frame carries signatures over; previous
  signers get a reminder, not a drop; withdraw before changing; referee lag → KNOWN_ACTIVE/KNOWN_FREE/UNKNOWN.
* **Operator boundary.** Autonomous vs approval-required actions are listed in `config/default.yaml`
  and recorded in `operator_decisions`.

## Phase 7: file-bridge to the live bot

```bash
sonnet-orchestrator bridge tick        # one pass: read ../sonnet/state-sonnet-2.json + policy.json, write ../sonnet/bridge/
sonnet-orchestrator bridge run         # loop every bridge.interval_s (60 s); runs in tmux `bridge`
```

The orchestrator never signs or posts. It writes `<game_id>.json` (validated text + turn table for the current
members, accepted prefix verbatim) and `roster-<game_id>.json` (letter coverage of members and candidates, ranked);
the live bot adopts the plan only after its own offline validator, accepted-prefix and member-set checks, and logs the
roster advice once. Contract: [`docs/BRIDGE.md`](docs/BRIDGE.md).

## What this package does not do

It never holds signing keys, never posts to technocore.chat or X, and never reads the live bot's state.
Phase 7 (real adapters) is interface-only today: implement `adapters/protocols.py` against the live transport
in the signing bot's process, or bridge via files, when the operator decides to switch.
