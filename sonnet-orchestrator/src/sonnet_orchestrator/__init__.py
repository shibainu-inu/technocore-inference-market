"""sonnet-orchestrator: fault-tolerant, deterministic coordination controller for the SonnetChallenge.

Layers (see README):
  deterministic core  -> did/, lexicon/, solver/, planner/, orchestration/, db/
  creative layer      -> creative/ (pluggable CreativeEngine; heuristic engine is the default)
  world I/O           -> adapters/ (Protocols + mocks; real adapters are Phase 7)
"""
__version__ = "0.1.0"
