"""Typed configuration loaded from config/default.yaml (no magic numbers in code)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PACKAGE_ROOT / "config" / "default.yaml"
CONTEST_CONFIG_PATH = PACKAGE_ROOT / "config" / "contest.yaml"


class DatabaseConfig(BaseModel):
    path: str = "./data/orchestrator.db"


class LexiconConfig(BaseModel):
    cmudict_path: str = "./data/cmudict/cmudict.dict"
    official_validator_path: str = "../sonnet/pkg/sonnet_validate.py"


class SolverWeights(BaseModel):
    latency: float = 0.2
    reliability: float = 0.3
    fragility: float = 0.3
    health: float = 0.2


class SolverConfig(BaseModel):
    lookahead_words: int = 4
    minimum_lookahead: int = 2
    weights: SolverWeights = Field(default_factory=SolverWeights)
    dead_end_penalty: float = 1000.0
    every_member_must_contribute: bool = False  # solver default; contest rule lives in contest.yaml and the Controller passes it explicitly
    health_penalty: dict[str, float] = Field(default_factory=lambda: {"HEALTHY": 0.0, "SLOW": 0.5, "SUSPECT": 0.8})


class HealthConfig(BaseModel):
    minimum_timeout_ms: int = 15000
    slow_multiplier: float = 2.0
    suspect_multiplier: float = 3.0
    down_multiplier: float = 6.0
    silent_after_ms: int = 900000
    recover_to: str = "SUSPECT"


class RosterWeights(BaseModel):
    reliability: float = 0.3
    lexical_coverage: float = 0.25
    redundant_coverage: float = 0.2
    response_speed: float = 0.15
    historical_completion: float = 0.1


class RosterConfig(BaseModel):
    minimum_size: int = 4
    maximum_size: int = 8
    preferred_size: int = 4
    require_accepted_word_history: bool = True
    coverage_excluding_lead_target: int = 2
    bottleneck_letters: str = "anost"
    weights: RosterWeights = Field(default_factory=RosterWeights)
    size_penalty_per_extra_member: float = 0.05
    candidate_pool_limit: int = 12


class ReliabilityWeights(BaseModel):
    completion_rate: float = 0.35
    accepted_rate: float = 0.25
    response_score: float = 0.2
    recent_activity: float = 0.1
    stale_conflict_score: float = 0.1


class MassApplicationConfig(BaseModel):
    seat_no_sign_weight: int = 3
    consent_conflict_weight: int = 2


class ReliabilityConfig(BaseModel):
    weights: ReliabilityWeights = Field(default_factory=ReliabilityWeights)
    mass_application: MassApplicationConfig = Field(default_factory=MassApplicationConfig)


class PlannerConfig(BaseModel):
    beam_width: int = 8
    expansion_count: int = 24
    lookahead_lines: int = 2
    landing_routes: int = 2


class ConsentConfig(BaseModel):
    signature_timeout_s: int = 1800
    reminder_interval_s: int = 900
    referee_lag_unknown_after_s: int = 600


class RoomConfig(BaseModel):
    post_char_limit: int = 2000
    table_prefix: str = "PLAN"


class SchedulerConfig(BaseModel):
    tick_seconds: int = 60


class SimulationConfig(BaseModel):
    default_trials: int = 10000
    seed: int = 20260914


class OperatorConfig(BaseModel):
    autonomous: list[str] = Field(default_factory=list)
    approval_required: list[str] = Field(default_factory=list)


class BridgeConfig(BaseModel):
    """Phase 7 file-bridge (docs/BRIDGE.md). Paths are relative to the repo root."""
    interval_s: int = 60
    text_source: str = "bot"             # "bot": the live bot's LLM writes the text, the bridge only assigns; "heuristic": bridge writes text too
    lead_word_latency_ms: float = 120000.0   # the lead is a controller + emergency cover, not a workhorse: assign it words last
    max_seeds: int = 6
    seed_budget_s: float = 18.0          # stop trying further seeds once this much time was spent (tick must stay < 30 s)
    state_path: str = "../sonnet/state-sonnet-2.json"
    policy_path: str = "../sonnet/policy.json"
    out_dir: str = "../sonnet/bridge"
    scores_path: str = "data/fixtures/writer_scores_2026-09-13.json"


class Settings(BaseModel):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    lexicon: LexiconConfig = Field(default_factory=LexiconConfig)
    solver: SolverConfig = Field(default_factory=SolverConfig)
    health: HealthConfig = Field(default_factory=HealthConfig)
    roster: RosterConfig = Field(default_factory=RosterConfig)
    reliability: ReliabilityConfig = Field(default_factory=ReliabilityConfig)
    planner: PlannerConfig = Field(default_factory=PlannerConfig)
    consent: ConsentConfig = Field(default_factory=ConsentConfig)
    room: RoomConfig = Field(default_factory=RoomConfig)
    scheduler: SchedulerConfig = Field(default_factory=SchedulerConfig)
    simulation: SimulationConfig = Field(default_factory=SimulationConfig)
    operator: OperatorConfig = Field(default_factory=OperatorConfig)
    bridge: BridgeConfig = Field(default_factory=BridgeConfig)
    contest: dict[str, Any] = Field(default_factory=dict)
    self_identity: dict[str, Any] = Field(default_factory=dict)
    base_dir: Path = PACKAGE_ROOT

    def resolve(self, rel: str) -> Path:
        p = Path(rel)
        return p if p.is_absolute() else (self.base_dir / p).resolve()

    @property
    def cmudict_path(self) -> Path:
        return self.resolve(self.lexicon.cmudict_path)

    @property
    def db_path(self) -> Path:
        return self.resolve(self.database.path)


def load_settings(path: str | os.PathLike | None = None, contest_path: str | os.PathLike | None = None) -> Settings:
    cfg_path = Path(path or os.environ.get("SONNET_ORCHESTRATOR_CONFIG") or DEFAULT_CONFIG_PATH)
    raw: dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    c_path = Path(contest_path or CONTEST_CONFIG_PATH)
    if c_path.exists():
        contest_raw = yaml.safe_load(c_path.read_text(encoding="utf-8")) or {}
        raw["contest"] = contest_raw.get("contest", {})
        raw["self_identity"] = contest_raw.get("self", {})
    raw["base_dir"] = cfg_path.resolve().parent.parent
    return Settings(**raw)
