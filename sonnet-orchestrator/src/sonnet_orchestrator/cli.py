"""Typer CLI. Heavy modules are imported lazily so `--help` stays fast and partial builds still work."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import load_settings

app = typer.Typer(help="sonnet-orchestrator: deterministic coordination controller for the SonnetChallenge", no_args_is_help=True)
lexicon_app = typer.Typer(help="Dictionary compilation and lookups")
did_app = typer.Typer(help="DID letter analysis")
solver_app = typer.Typer(help="Assignment / feasibility / roster solver")
plan_app = typer.Typer(help="Poem planning with the accepted prefix fixed")
simulate_app = typer.Typer(help="Offline simulation (mock adapters)")
run_app = typer.Typer(help="Control loop (Phase 7: real adapters; today mock only)")
bridge_app = typer.Typer(help="Phase 7 file-bridge: read the live bot's state/policy, write plan + roster advice files")
app.add_typer(bridge_app, name="bridge")
app.add_typer(lexicon_app, name="lexicon")
app.add_typer(did_app, name="did")
app.add_typer(solver_app, name="solver")
app.add_typer(plan_app, name="plan")
app.add_typer(simulate_app, name="simulate")
app.add_typer(run_app, name="run")
console = Console()

CONFIG_OPT = typer.Option(None, "--config", "-c", help="config yaml (default config/default.yaml)")


def _settings(config: Optional[Path]):
    return load_settings(config)


def _lexicon(settings):
    from .lexicon import load_lexicon
    return load_lexicon(str(settings.cmudict_path))


def _writers_from(spec: str, settings):
    """spec = comma-separated DIDs or a JSON file path with [{did, x_account, ...}]."""
    from .models import WriterProfile
    p = Path(spec)
    if p.exists():
        return [WriterProfile(**w) for w in json.loads(p.read_text())]
    return [WriterProfile(did=d.strip()) for d in spec.split(",") if d.strip()]


# --------------------------------------------------------------------- init / db
@app.command()
def init(config: Optional[Path] = CONFIG_OPT):
    """Create the SQLite database and run migrations."""
    from .db import Store
    s = _settings(config)
    st = Store(s.db_path)
    console.print(f"database ready at {s.db_path} (schema v{st.migrate()})")


@app.command()
def status(config: Optional[Path] = CONFIG_OPT, game_id: Optional[str] = None):
    """Show games, active plan and accepted prefix from the database."""
    from .db import Store
    s = _settings(config)
    st = Store(s.db_path)
    rows = st.con.execute("SELECT game_id,state,version FROM games").fetchall()
    for r in rows:
        if game_id and r[0] != game_id:
            continue
        plan = st.active_plan(r[0])
        console.print(f"[bold]{r[0]}[/] state={r[1]} version={r[2]} accepted={len(st.accepted(r[0]))} plan={(plan.plan_id + ' v' + str(plan.version)) if plan else '-'}")
    if not rows:
        console.print("no games")


# --------------------------------------------------------------------- lexicon
@lexicon_app.command("build")
def lexicon_build(config: Optional[Path] = CONFIG_OPT):
    """Compile CMUdict into SQLite (syllables, stress, rhyme keys, letter masks)."""
    from .db import Store
    s = _settings(config)
    lex = _lexicon(s)
    st = Store(s.db_path)
    st.bulk_lexicon(lex.rows(), lex.pron_rows())
    console.print(f"compiled {st.lexicon_count()} words into {s.db_path}")


@lexicon_app.command("word")
def lexicon_word(word: str, config: Optional[Path] = CONFIG_OPT):
    lex = _lexicon(_settings(config))
    i = lex.info(word)
    console.print_json(data={"word": i.word, "syllables": i.syllables, "letters": "".join(sorted(i.letters)),
                             "stresses": ["".join(map(str, s)) for s in i.stresses], "rhyme_keys": sorted(i.rhyme_keys)})


@lexicon_app.command("validate")
def lexicon_validate(poem: Path, config: Optional[Path] = CONFIG_OPT):
    """Run the official validator (exact ten) on a poem file; print per-line syllables."""
    lex = _lexicon(_settings(config))
    from .planner.validator import validate_poem_lines
    lines = [l for l in poem.read_text().splitlines() if l.strip()]
    rep = validate_poem_lines(lines, lex)
    console.print_json(data=rep.model_dump() if hasattr(rep, "model_dump") else rep.__dict__)
    raise typer.Exit(0 if rep.ok else 1)


# --------------------------------------------------------------------- did
@did_app.command("analyze")
def did_analyze(dids: str, lead: Optional[str] = None):
    """Letter coverage of a roster (comma-separated DIDs)."""
    from .did import coverage
    members = [d.strip() for d in dids.split(",") if d.strip()]
    rep = coverage(members, lead=lead or members[0])
    console.print_json(data={"missing_from_union": rep.missing_from_union, "single_key": rep.single_key_letters,
                             "lead_only": rep.lead_only_letters, "weighted_coverage": round(rep.weighted_coverage, 3),
                             "fragility": round(rep.fragility, 3), "explanation": rep.explanation})


# --------------------------------------------------------------------- solver
@solver_app.command("assign")
def solver_assign(poem: Path, writers: str, lead: Optional[str] = None, config: Optional[Path] = CONFIG_OPT, explain: bool = False):
    """Assign every word of a poem file to writers (DP with lookahead)."""
    from .solver.assignment import assign
    from .solver.explain import explain_assignment
    from .planner.validator import words_of_poem
    s = _settings(config)
    lex = _lexicon(s)
    ws = _writers_from(writers, s)
    lines = [l for l in poem.read_text().splitlines() if l.strip()]
    words = words_of_poem(lines, lex)
    res = assign(words, ws, settings=s, lead_did=lead or ws[0].did)
    console.print(f"feasible={res.feasible} cost={res.cost:.2f} dead_ends={res.dead_ends}")
    for a in res.assignments:
        console.print(f"{a.index:3d} {words[a.index].text:14s} {a.primary[-8:]}  backup={a.backup[-8:] if a.backup else '-':8s} keys={a.keys}{' LEAD-ONLY' if a.lead_only else ''}")
    if explain:
        console.print(explain_assignment(res, words, ws))


@solver_app.command("roster")
def solver_roster(candidates: str, lead: str, size: Optional[int] = None, config: Optional[Path] = CONFIG_OPT):
    """Rank roster options from candidate writers (JSON file or DIDs)."""
    from .solver.roster import optimize
    from .models import WriterProfile
    s = _settings(config)
    cands = _writers_from(candidates, s)
    lead_w = next((w for w in cands if w.did == lead), None) or WriterProfile(did=lead, is_self=True)
    for opt in optimize([c for c in cands if c.did != lead], lead_w, s, size=size)[:5]:
        console.print(f"score={opt.score:.3f} members={[m[-8:] for m in opt.members]}")
        for line in opt.explanation:
            console.print(f"   {line}")


@solver_app.command("explain")
def solver_explain(poem: Path, writers: str, index: int, lead: Optional[str] = None, config: Optional[Path] = CONFIG_OPT):
    """Explain why word #index is assigned the way it is."""
    from .solver.assignment import assign
    from .solver.explain import explain_index
    from .planner.validator import words_of_poem
    s = _settings(config)
    lex = _lexicon(s)
    ws = _writers_from(writers, s)
    lines = [l for l in poem.read_text().splitlines() if l.strip()]
    words = words_of_poem(lines, lex)
    res = assign(words, ws, settings=s, lead_did=lead or ws[0].did)
    console.print(explain_index(res, words, ws, index))


# --------------------------------------------------------------------- plan
@plan_app.command("generate")
def plan_generate(writers: str, prefix: Optional[Path] = None, theme: str = "", seed: int = 0, out: Optional[Path] = None,
                  config: Optional[Path] = CONFIG_OPT):
    """Generate a full plan with the heuristic creative engine; optional accepted-prefix file (one word per line or text)."""
    from .creative.heuristic import HeuristicCreativeEngine
    from .planner.beam import plan_poem
    s = _settings(config)
    lex = _lexicon(s)
    ws = _writers_from(writers, s)
    pre = prefix.read_text().split() if prefix else []
    plan = plan_poem(HeuristicCreativeEngine(lex, seed=seed), lex, ws, s, accepted_prefix=pre, theme=theme, seed=seed)
    console.print(plan.text)
    console.print(f"\nsha256={plan.sha256} words={len(plan.words)} version={plan.version}")
    if out:
        out.write_text(plan.model_dump_json(indent=1))


@plan_app.command("table")
def plan_table(plan_file: Path, next_index: int = 0, config: Optional[Path] = CONFIG_OPT):
    """Render the execution table chunks (≤2000 chars each) from a saved plan JSON."""
    from .models import Plan, PoemState
    from .orchestration.table import render_table
    s = _settings(config)
    plan = Plan.model_validate_json(plan_file.read_text())
    poem = PoemState(game_id=plan.game_id)
    for chunk in render_table(plan, poem, [], s, next_index=next_index):
        console.print(chunk)
        console.print(f"--- {len(chunk)} chars ---")


# --------------------------------------------------------------------- simulate
@simulate_app.command("entry")
def simulate_entry(scenario: str = "demo-4-writers", seed: int = 0, ticks: int = 5000, show: bool = True, config: Optional[Path] = CONFIG_OPT):
    """Run one full entry offline with mock adapters and scripted writers; prints the completed poem."""
    from .diagnostics.simulator import simulate_scenario
    s = _settings(config)
    res = simulate_scenario(scenario, s, seed=seed, max_ticks=ticks)
    if show:
        from .diagnostics.dashboard import render
        console.print(render(res.snapshot))
    console.print(f"completed={res.completed} minutes={res.minutes:.1f} words={res.words} reason={res.reason}")
    if res.poem_text:
        console.print("\n" + res.poem_text + f"\n\nsha256={res.sha256}")
    raise typer.Exit(0 if res.completed else 1)


@simulate_app.command("chaos")
def simulate_chaos(scenario: str, trials: int = 0, seed: int = 0, config: Optional[Path] = CONFIG_OPT):
    """Monte Carlo over a scenario with fault injection (default trials from config)."""
    from .diagnostics.montecarlo import run_scenario
    s = _settings(config)
    rep = run_scenario(scenario, s, trials=trials or s.simulation.default_trials, seed=seed or s.simulation.seed)
    console.print_json(data=rep.as_dict())


@simulate_app.command("list")
def simulate_list():
    from .diagnostics.scenarios import SCENARIOS, build
    from .diagnostics.simulator import DEMO, demo_scenario
    console.print(f"[bold]{DEMO}[/]: {demo_scenario().description}")
    for name in SCENARIOS:
        console.print(f"[bold]{name}[/]: {build(name).description}")


# --------------------------------------------------------------------- replay / metrics
@app.command()
def replay(export: Path, config: Optional[Path] = CONFIG_OPT):
    """Replay a team-room export: accepted words, contributors, KPIs."""
    from .diagnostics.replay import parse_export, canonical_from_export
    from .diagnostics.metrics import game_kpis
    s = _settings(config)
    lex = _lexicon(s)
    log = parse_export(export)
    data = game_kpis(log).as_dict()
    text, sha = canonical_from_export(export, lex)
    data["canonical_sha256"] = sha
    console.print_json(data=data)


@app.command()
def explain(what: str = typer.Argument(..., help="assignment|roster|cover|plan"), game_id: Optional[str] = None, config: Optional[Path] = CONFIG_OPT):
    """Explain the last decision of a kind from the database (why this writer / why cover / why replan)."""
    from .db import Store
    s = _settings(config)
    st = Store(s.db_path)
    rows = st.con.execute("SELECT at,action,decision,detail FROM operator_decisions WHERE action LIKE ? ORDER BY id DESC LIMIT 10", (f"%{what}%",)).fetchall()
    for r in rows:
        console.print(f"{r[0]} {r[1]} [{r[2]}] {r[3]}")
    if not rows:
        console.print(f"no recorded decisions matching {what!r}")


@app.command()
def dashboard(snapshot: Optional[Path] = None, config: Optional[Path] = CONFIG_OPT):
    """Render the Rich dashboard from a snapshot JSON (or a demo snapshot)."""
    from .diagnostics.dashboard import render, demo_snapshot
    data = json.loads(snapshot.read_text()) if snapshot else demo_snapshot()
    console.print(render(data))


# --------------------------------------------------------------------- bridge (Phase 7)
def _bridge_paths(s, state, policy, out, scores):
    b = s.bridge
    return (state or s.resolve(b.state_path), policy or s.resolve(b.policy_path), out or s.resolve(b.out_dir),
            scores or s.resolve(b.scores_path))


def _bridge_tick_once(s, state, policy, out, scores, seed):
    from .bridge import tick
    return tick(state, policy, out, s, scores_path=scores, seed=seed)


@bridge_app.command("tick")
def bridge_tick(state: Optional[Path] = typer.Option(None, "--state", help="live bot state JSON (read-only)"),
                policy: Optional[Path] = typer.Option(None, "--policy", help="live bot policy JSON (read-only)"),
                out: Optional[Path] = typer.Option(None, "--out", help="bridge output directory"),
                scores: Optional[Path] = typer.Option(None, "--scores", help="writer_scores_*.json"),
                seed: int = typer.Option(0, "--seed"), config: Optional[Path] = CONFIG_OPT):
    """One bridge tick: write <out>/<game_id>.json and <out>/roster-<game_id>.json when they changed."""
    s = _settings(config)
    st, po, od, sc = _bridge_paths(s, state, policy, out, scores)
    r = _bridge_tick_once(s, st, po, od, sc, seed)
    print(f"{_ts()} game={r.game_id} plan={r.plan_id} wrote_plan={r.wrote_plan} wrote_roster={r.wrote_roster}"
          f" {r.elapsed_s:.1f}s :: {r.reason}", flush=True)


@bridge_app.command("run")
def bridge_run(state: Optional[Path] = typer.Option(None, "--state"), policy: Optional[Path] = typer.Option(None, "--policy"),
               out: Optional[Path] = typer.Option(None, "--out"), scores: Optional[Path] = typer.Option(None, "--scores"),
               seed: int = typer.Option(0, "--seed"), interval: Optional[float] = typer.Option(None, "--interval", help="seconds"),
               config: Optional[Path] = CONFIG_OPT):
    """Loop forever: one tick every --interval seconds (default bridge.interval_s); exceptions are logged, not fatal."""
    import time
    s = _settings(config)
    st, po, od, sc = _bridge_paths(s, state, policy, out, scores)
    every = float(interval if interval is not None else s.bridge.interval_s)
    print(f"{_ts()} bridge run: state={st} policy={po} out={od} interval={every:g}s", flush=True)
    while True:
        try:
            r = _bridge_tick_once(s, st, po, od, sc, seed)
            print(f"{_ts()} game={r.game_id} plan={r.plan_id} wrote_plan={r.wrote_plan} wrote_roster={r.wrote_roster}"
                  f" {r.elapsed_s:.1f}s :: {r.reason}", flush=True)
        except Exception as e:  # noqa: BLE001 - keep the loop alive
            print(f"{_ts()} tick error: {e!r}", flush=True)
        time.sleep(every)


def _ts() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@run_app.command("live")
def run_live(config: Optional[Path] = CONFIG_OPT):
    """Phase 7 placeholder: real adapters are not wired yet. The live signing bot stays sonnet/agent.py."""
    console.print("[yellow]Real Technocore/X adapters are not implemented (Phase 7). Use `simulate entry` for the offline loop.[/]")
    raise typer.Exit(2)


if __name__ == "__main__":
    app()
