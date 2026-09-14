-- sonnet-orchestrator SQLite schema (v1). Referee receipts are the only truth:
-- accepted_words is append-only; plans are versioned; one active plan per game.
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS writers (
  did TEXT PRIMARY KEY,
  handle TEXT,
  x_account TEXT,
  letters TEXT NOT NULL,                 -- sorted letters the DID can spell
  health TEXT NOT NULL DEFAULT 'HEALTHY',
  consent TEXT NOT NULL DEFAULT 'NONE',
  is_self INTEGER NOT NULL DEFAULT 0,
  poems_completed INTEGER NOT NULL DEFAULT 0,
  games_joined INTEGER NOT NULL DEFAULT 0,
  words_accepted INTEGER NOT NULL DEFAULT 0,
  words_rejected INTEGER NOT NULL DEFAULT 0,
  signs INTEGER NOT NULL DEFAULT 0,
  seat_no_sign_count INTEGER NOT NULL DEFAULT 0,       -- addendum
  consent_conflict_count INTEGER NOT NULL DEFAULT 0,   -- addendum
  stale_offer_count INTEGER NOT NULL DEFAULT 0,        -- addendum
  published_entry_count INTEGER NOT NULL DEFAULT 0,    -- addendum
  sign_latency_median_ms REAL,                         -- addendum
  word_latency_median_ms REAL,                         -- addendum
  mass_application_score REAL NOT NULL DEFAULT 0,      -- addendum
  reliability REAL NOT NULL DEFAULT 0.5,
  last_activity_at TEXT,
  updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS writer_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  did TEXT NOT NULL,
  kind TEXT NOT NULL,
  at TEXT NOT NULL,
  latency_ms REAL,
  game_id TEXT,
  detail TEXT
);
CREATE INDEX IF NOT EXISTS ix_writer_events_did ON writer_events(did, at);

CREATE TABLE IF NOT EXISTS lexicon_words (
  word TEXT PRIMARY KEY,
  syllables INTEGER NOT NULL,           -- max over pronunciations (official rule)
  letters TEXT NOT NULL,
  letter_mask INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS word_pronunciations (
  word TEXT NOT NULL,
  variant INTEGER NOT NULL,
  phones TEXT NOT NULL,
  stress TEXT NOT NULL,                  -- e.g. "01"
  rhyme_key TEXT NOT NULL,
  PRIMARY KEY (word, variant)
);

CREATE TABLE IF NOT EXISTS writer_word_eligibility (
  did TEXT NOT NULL,
  word TEXT NOT NULL,
  PRIMARY KEY (did, word)
);

CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  state TEXT NOT NULL DEFAULT 'DISCOVER',
  lead_did TEXT,
  poem_room TEXT,
  room_generation INTEGER NOT NULL DEFAULT 1,
  frame_state TEXT NOT NULL DEFAULT 'DRAFT',
  version INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
  updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);

CREATE TABLE IF NOT EXISTS game_members (
  game_id TEXT NOT NULL,
  did TEXT NOT NULL,
  position INTEGER NOT NULL,
  role TEXT NOT NULL DEFAULT 'Author',
  consent TEXT NOT NULL DEFAULT 'SEATED',
  signed_at TEXT,
  frame_signature TEXT,
  PRIMARY KEY (game_id, did)
);

CREATE TABLE IF NOT EXISTS accepted_words (
  game_id TEXT NOT NULL,
  idx INTEGER NOT NULL,
  text TEXT NOT NULL,
  contributor TEXT NOT NULL,
  version INTEGER NOT NULL,
  receipt_seq INTEGER,
  request_id TEXT,
  accepted_at TEXT,
  PRIMARY KEY (game_id, idx)
);

CREATE TABLE IF NOT EXISTS proposals (
  request_id TEXT PRIMARY KEY,
  game_id TEXT NOT NULL,
  idx INTEGER NOT NULL,
  text TEXT NOT NULL,
  contributor TEXT NOT NULL,
  base_version INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'PENDING',
  sent_at TEXT NOT NULL,
  resolved_at TEXT,
  reason TEXT
);
CREATE INDEX IF NOT EXISTS ix_proposals_game ON proposals(game_id, idx);

CREATE TABLE IF NOT EXISTS plans (
  plan_id TEXT PRIMARY KEY,
  game_id TEXT NOT NULL,
  version INTEGER NOT NULL,
  owner TEXT NOT NULL,                   -- addendum: one owner per active plan
  source TEXT NOT NULL DEFAULT 'solver', -- addendum: solver | operator | hybrid
  is_active INTEGER NOT NULL DEFAULT 1,  -- addendum: exactly one active plan per game
  accepted_prefix_len INTEGER NOT NULL DEFAULT 0,
  sha256 TEXT NOT NULL,
  lines_json TEXT NOT NULL,
  words_json TEXT NOT NULL,
  assignments_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_plans_active ON plans(game_id) WHERE is_active = 1;

CREATE TABLE IF NOT EXISTS offers (
  seq INTEGER PRIMARY KEY,
  at TEXT NOT NULL,
  sender TEXT NOT NULL,
  game_id TEXT,
  kind TEXT NOT NULL,
  to_did TEXT,
  text TEXT,
  handled INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS operator_decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  at TEXT NOT NULL,
  action TEXT NOT NULL,
  decision TEXT NOT NULL,               -- AUTONOMOUS | OPERATOR_APPROVAL
  detail TEXT,
  approved INTEGER
);
