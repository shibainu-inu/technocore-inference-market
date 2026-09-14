# Architecture

## Three layers (Production Lessons Addendum)

1. **Recruitment / Consent** — discovery offers → filters (dedupe, self, stale, personal-first) → seat → frame
   (DRAFT→SIGNING→READY→FROZEN, SUPERSEDED) with waitlist during SIGNING, signature carry-over on identical frames,
   reminder-not-drop for earlier signers, signature timeout + reminders, withdraw-before-changing.
   Reliability is computed from accepted words and signs, never from a "yes".
2. **Roster / Plan Control** — DID coverage (union, single-key, lead-only), roster optimizer (reliability, coverage,
   redundancy excluding lead, speed, history, size penalty), plan = poem + assignment (DP with lookahead), one active
   plan/table/owner, plan reset on team change, team-scoped state, pre-roster 403 fallback to discovery.
3. **Word Execution / Recovery** — dispatcher with request_id, receipts → immutable accepted prefix, health
   (HEALTHY/SLOW/SUSPECT/DOWN/SILENT), cover with lookahead, hand-off, replan of the suffix only, landing routes to a
   publisher-capable final contributor, official validator final say, publish + submit.

## Control loop (`orchestration/controller.py`, tick every `scheduler.tick_seconds`)

```
receipts → reconcile prefix → health → cover / hand-off → replan (suffix) → table repost on version change
        → landing → COMPLETE → PUBLISH_PENDING → SUBMITTED → ACCEPTED
```

## Determinism

The core has no randomness (seeded where search needs it) and no wall clock: `Clock` is injected. All policy
numbers live in `config/default.yaml`. The creative layer enters only through `CreativeEngine`; every candidate is
re-validated by the lexicon, the meter/rhyme validator and the solver before it can enter a plan.

## Data

SQLite (`db/schema.sql`): writers (+ addendum metrics), writer_events, lexicon_words, word_pronunciations,
writer_word_eligibility, games, game_members, accepted_words (append-only), proposals, plans (is_active/owner/source),
offers, operator_decisions.

## State machine

DISCOVER → APPLY → SEATED → ROSTER_PENDING → ROSTER_READY → WRITING ⇄ RECOVERING → LANDING → COMPLETE →
PUBLISH_PENDING → SUBMITTED → ACCEPTED; ABANDONED from any state before COMPLETE.
