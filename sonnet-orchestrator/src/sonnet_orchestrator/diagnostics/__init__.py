"""Diagnostics: fixture replay, metrics, scenarios, dashboard, Monte Carlo."""
from .replay import ReplayLog, parse_export, accepted_from_export, canonical_from_export, lines_from_words  # noqa: F401
from .metrics import GameKPIs, CoverEvent, writer_metrics, game_kpis, load_writer_scores  # noqa: F401
from .scenarios import Scenario, ScenarioWriter, Fault, SCENARIOS, build, dump_all, load_all  # noqa: F401
from .montecarlo import SimResult, MonteCarloReport, run, simple_simulate, check_expectations  # noqa: F401
from .dashboard import render, render_text  # noqa: F401
