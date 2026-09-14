"""Monte Carlo runner over :class:`Scenario` objects with an injected simulator.

``run(scenario, trials, seed, simulate_fn)`` calls ``simulate_fn(scenario, seed_i) -> SimResult`` once per
trial with a distinct, deterministic seed.  ``simple_simulate`` is the pure-Python analytical fallback
(per-word latency + failure probabilities + fault injection); the Controller-based simulator plugs into
the same slot.
"""
from __future__ import annotations

import math
import random
import statistics
from collections import Counter
from dataclasses import dataclass, field, replace
from typing import Callable, Optional

from .scenarios import DEFAULT_SIM, Scenario, ScenarioWriter


@dataclass
class SimResult:
    completed: bool
    minutes: float
    reason: str = ""
    stale: int = 0
    covers: int = 0
    replans: int = 0
    reposts: int = 0


@dataclass
class MonteCarloReport:
    scenario: str
    trials: int
    completion_rate: float
    median_minutes: Optional[float]
    p90_minutes: Optional[float]
    failure_reasons: Counter = field(default_factory=Counter)
    single_failure_survivability: Optional[float] = None
    survivability_by_writer: dict[str, float] = field(default_factory=dict)
    mean_stale: float = 0.0
    mean_covers: float = 0.0
    mean_replans: float = 0.0
    seed: int = 0

    def as_dict(self) -> dict:
        return {
            "scenario": self.scenario, "trials": self.trials, "completion_rate": round(self.completion_rate, 4),
            "median_minutes": self.median_minutes, "p90_minutes": self.p90_minutes,
            "failure_reasons": dict(self.failure_reasons),
            "single_failure_survivability": self.single_failure_survivability,
            "survivability_by_writer": dict(self.survivability_by_writer),
            "mean_stale": round(self.mean_stale, 3), "mean_covers": round(self.mean_covers, 3),
            "mean_replans": round(self.mean_replans, 3), "seed": self.seed,
        }


SimulateFn = Callable[[Scenario, int], SimResult]


def _percentile(values: list[float], q: float) -> Optional[float]:
    if not values:
        return None
    s = sorted(values)
    k = (len(s) - 1) * q
    lo, hi = math.floor(k), math.ceil(k)
    if lo == hi:
        return s[lo]
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def _trial_seeds(seed: int, trials: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.getrandbits(32) for _ in range(trials)]


def run(scenario: Scenario, trials: int, seed: int, simulate_fn: SimulateFn, *,
        survivability: bool = True, survivability_trials: Optional[int] = None) -> MonteCarloReport:
    results = [simulate_fn(scenario, s) for s in _trial_seeds(seed, trials)]
    done = [r for r in results if r.completed]
    minutes = [r.minutes for r in done]
    reasons = Counter(r.reason for r in results if not r.completed)
    rep = MonteCarloReport(
        scenario=scenario.name, trials=trials,
        completion_rate=len(done) / trials if trials else 0.0,
        median_minutes=round(statistics.median(minutes), 2) if minutes else None,
        p90_minutes=round(_percentile(minutes, 0.9), 2) if minutes else None,
        failure_reasons=reasons,
        mean_stale=sum(r.stale for r in results) / trials if trials else 0.0,
        mean_covers=sum(r.covers for r in results) / trials if trials else 0.0,
        mean_replans=sum(r.replans for r in results) / trials if trials else 0.0,
        seed=seed,
    )
    if survivability:
        n = survivability_trials or max(20, trials // 5)
        threshold = float({**DEFAULT_SIM, **scenario.sim}.get("survivability_threshold", DEFAULT_SIM["survivability_threshold"]))
        by: dict[str, float] = {}
        for w in scenario.writers:
            if w.is_lead:
                continue
            variant = remove_writer(scenario, w.did)
            sub = [simulate_fn(variant, s) for s in _trial_seeds(seed ^ 0x5F3759DF, n)]
            by[w.did] = sum(1 for r in sub if r.completed) / n
        rep.survivability_by_writer = by
        rep.single_failure_survivability = (sum(1 for v in by.values() if v >= threshold) / len(by)) if by else None
    return rep


def check_expectations(report: MonteCarloReport, expectations: dict) -> list[str]:
    """Compare a report with a scenario's ``expectations``; returns the list of violated expectations."""
    bad: list[str] = []
    e = expectations or {}
    if "completion_rate_min" in e and report.completion_rate < e["completion_rate_min"]:
        bad.append(f"completion_rate {report.completion_rate:.3f} < {e['completion_rate_min']}")
    if "completion_rate_max" in e and report.completion_rate > e["completion_rate_max"]:
        bad.append(f"completion_rate {report.completion_rate:.3f} > {e['completion_rate_max']}")
    if "median_minutes_min" in e and (report.median_minutes is None or report.median_minutes < e["median_minutes_min"]):
        bad.append(f"median_minutes {report.median_minutes} < {e['median_minutes_min']}")
    if "median_minutes_max" in e and (report.median_minutes is None or report.median_minutes > e["median_minutes_max"]):
        bad.append(f"median_minutes {report.median_minutes} > {e['median_minutes_max']}")
    if "p90_minutes_max" in e and (report.p90_minutes is None or report.p90_minutes > e["p90_minutes_max"]):
        bad.append(f"p90_minutes {report.p90_minutes} > {e['p90_minutes_max']}")
    for sub in e.get("failure_reasons_include", []):
        if not any(sub in r for r in report.failure_reasons):
            bad.append(f"failure reason {sub!r} missing")
    for sub in e.get("failure_reasons_exclude", []):
        if any(sub in r for r in report.failure_reasons):
            bad.append(f"failure reason {sub!r} present")
    if "single_failure_survivability_min" in e:
        v = report.single_failure_survivability
        if v is None or v < e["single_failure_survivability_min"]:
            bad.append(f"single_failure_survivability {v} < {e['single_failure_survivability_min']}")
    if "mean_stale_min" in e and report.mean_stale < e["mean_stale_min"]:
        bad.append(f"mean_stale {report.mean_stale:.2f} < {e['mean_stale_min']}")
    if "mean_covers_min" in e and report.mean_covers < e["mean_covers_min"]:
        bad.append(f"mean_covers {report.mean_covers:.2f} < {e['mean_covers_min']}")
    return bad


def remove_writer(scenario: Scenario, did: str) -> Scenario:
    """Copy of ``scenario`` where ``did`` is DOWN from word 0 (single-failure variant)."""
    writers = [replace(w, profile="down_after", down_after=0) if w.did == did else replace(w) for w in scenario.writers]
    return replace(scenario, writers=writers, name=f"{scenario.name}~{did[-8:]}")


# ---------------------------------------------------------------- analytical fallback simulator
class _W:
    __slots__ = ("did", "letters", "profile", "latency_s", "active", "down_after", "until", "is_lead", "publisher", "miss")

    def __init__(self, w: ScenarioWriter, sim: dict):
        self.did = w.did
        self.letters = w.letter_set()
        self.profile = w.profile
        self.latency_s = w.latency_ms / 1000.0
        self.is_lead = w.is_lead
        self.publisher = bool(w.x_account)
        self.down_after = w.down_after if w.profile == "down_after" else None
        self.until: Optional[int] = None
        self.active = w.profile not in ("silent",)
        self.miss = float(sim["miss_prob"].get(w.profile, sim["miss_prob"]["healthy"]))

    def can(self, word: str) -> bool:
        return all(c in self.letters for c in word.lower() if "a" <= c <= "z")

    def alive(self, i: int) -> bool:
        if not self.active:
            return self.until is not None and i >= self.until
        if self.down_after is not None and i >= self.down_after:
            return self.until is not None and i >= self.until
        return True


def simple_simulate(scenario: Scenario, seed: int, *, settings=None) -> SimResult:
    """Fast analytical model: per-word latency + miss/stale probabilities + fault injection.

    Policy knobs (cover timer, signature timeout, post char limit) are read from ``settings`` when given,
    otherwise from the scenario's ``sim`` block / DEFAULT_SIM.
    """
    rng = random.Random(seed)
    sim = {**DEFAULT_SIM, **scenario.sim}
    if settings is not None:
        sim["signature_timeout_s"] = float(settings.consent.signature_timeout_s)
        sim["post_char_limit"] = int(settings.room.post_char_limit)
    writers = [_W(w, sim) for w in scenario.writers]
    lead = next(w for w in writers if w.is_lead)
    words = list(scenario.words)
    t = 0.0
    stale = covers = replans = reposts = 0
    by_index: dict[int, list] = {}
    for f in scenario.faults:
        if f.at_index is not None:
            by_index.setdefault(f.at_index, []).append(f)

    # ---- phase 0: roster / consent / room faults (before word 0)
    for w in writers:
        if w.profile == "never_signs":
            t += sim["signature_timeout_s"]
            if not sim["replace_non_signer"]:
                return SimResult(False, t / 60, "roster: incomplete consent", stale, covers, replans, reposts)
            w.active = False
        elif w.profile == "mass_applicant":
            if rng.random() < sim["mass_applicant_sign_prob"]:
                if rng.random() < sim["mass_applicant_silent_prob"]:
                    w.active = False
            else:
                t += sim["signature_timeout_s"]
                if not sim["replace_non_signer"]:
                    return SimResult(False, t / 60, "roster: incomplete consent", stale, covers, replans, reposts)
                w.active = False
    for f in scenario.faults:
        p = f.params
        if f.kind == "consent_lag":
            t += float(p.get("seconds", 0))
        elif f.kind == "frame_churn":
            t += int(p.get("reissues", 0)) * float(p.get("resign_s", 300))
        elif f.kind == "pre_roster_403":
            if p.get("fallback_to_discovery", True):
                t += sim["discovery_fallback_s"]
            elif rng.random() < sim["no_plan_fail_prob"]:
                return SimResult(False, t / 60, "pre_roster_403: plan never reached members", stale, covers, replans, reposts)
        elif f.kind == "long_table":
            if int(p.get("chars", 0)) > sim["post_char_limit"] and not p.get("chunked", False):
                if rng.random() < sim["no_plan_fail_prob"]:
                    return SimResult(False, t / 60, "table refused: post over char limit", stale, covers, replans, reposts)
                t += sim["table_repost_s"]
        elif f.kind in ("self_offer", "stale_offer") and not p.get("filtered", True):
            t += float(p.get("penalty_s", 0))
        elif f.kind == "down" and f.at_index is not None and p.get("until_index") is not None:
            pass  # handled per index below
    dual_until = -1
    for f in scenario.faults:
        if f.kind == "dual_table":
            dual_until = int(f.params.get("resolve_at_index", 0))

    # ---- phase 1: words
    last: Optional[_W] = None
    n = len(words)
    replanned_for: Optional[frozenset] = None   # alive set the suffix was last re-solved for
    lookahead = int(sim.get("lookahead", 0))
    excl_slow = bool(sim.get("lookahead_excludes_slow", True))

    def spell(w: _W, wd: str, alive_set: frozenset) -> bool:
        # after a replan the suffix is solved for the alive keys: every word has >= 2 keys among them
        return w.can(wd) or (replanned_for is not None and replanned_for == alive_set)

    parity_cache: dict[frozenset, list] = {}

    def parity_preference(i: int, alive: list) -> Optional[_W]:
        """Two-person alternation: the next single-key word ahead fixes who must take which parity."""
        key = frozenset(w.did for w in alive)
        nxt = parity_cache.get(key)
        if nxt is None:
            # nxt[k] = index >= k of the next word only one of the two can spell, or -1
            nxt = [-1] * (n + 1)
            for k in range(n - 1, -1, -1):
                nxt[k] = k if sum(1 for v in alive if v.can(words[k])) == 1 else nxt[k + 1]
            parity_cache[key] = nxt
        j = nxt[i]
        if j < 0:
            return None
        owner = next(v for v in alive if v.can(words[j]))
        return owner if (j - i) % 2 == 0 else next(v for v in alive if v is not owner)

    for i, word in enumerate(words):
        for f in by_index.get(i, []):
            p = f.params
            if f.kind == "down":
                for w in writers:
                    if w.did == p.get("did"):
                        w.down_after = i
                        w.profile = "down_after"
                        if p.get("until_index") is not None:
                            w.until = int(p["until_index"])
            elif f.kind == "delayed_receipt":
                t += float(p.get("delay_s", 0))
            elif f.kind == "stale_storm":
                k = int(p.get("count", 1))
                stale += k
                t += k * sim["stale_retry_s"] / max(1, len(writers))
        if i < dual_until:
            t += sim["dual_table_penalty_s"]
        alive = [w for w in writers if w.alive(i)]
        alive_set = frozenset(w.did for w in alive)
        cands = [w for w in alive if w is not last and spell(w, word, alive_set)]
        if lookahead >= 1 and len(alive) == 2 and cands and replanned_for != alive_set and sim.get("parity_plan", True):
            pref = parity_preference(i, alive)
            if pref is not None and pref in cands:
                cands = [pref]
        if lookahead >= 1 and i + 1 < n and cands:
            nxt = words[i + 1]
            keep = [w for w in cands
                    if any(v is not w and spell(v, nxt, alive_set) and not (excl_slow and v.profile == "slow") for v in alive)]
            if keep:
                cands = keep
        final_index = i == n - 1
        if sim["require_publisher_final"]:
            if final_index:
                cands = [w for w in cands if w.publisher]
                if not cands:
                    return SimResult(False, t / 60, "landing: publisher blocked by alternation", stale, covers, replans, reposts)
            elif i == n - 2 and sim["landing_plan"]:
                non_pub = [w for w in cands if not w.publisher]
                if non_pub:
                    cands = non_pub
        if not cands:
            if not sim["replan"]:
                return SimResult(False, t / 60, f"dead_end@{i}", stale, covers, replans, reposts)
            replans += 1
            t += sim["replan_s"]
            if rng.random() < sim["replan_fail_prob"]:
                return SimResult(False, t / 60, f"dead_end@{i}", stale, covers, replans, reposts)
            replanned_for = alive_set
            cands = [w for w in alive if w is not last]
            if not cands:
                return SimResult(False, t / 60, f"dead_end@{i}: no active writer", stale, covers, replans, reposts)
        rounds = 0
        while True:
            responders = []
            for w in cands:
                if rng.random() < w.miss:
                    continue
                lat = w.latency_s * math.exp(rng.gauss(0.0, sim["latency_sigma"])) + sim["word_overhead_s"]
                responders.append((lat, w))
            forced_race = any(f.kind == "race" for f in by_index.get(i, []))
            if forced_race and len(cands) >= 2 and len(responders) < 2:
                responders = [(w.latency_s + sim["word_overhead_s"], w) for w in cands[:2]]
            if responders:
                responders.sort(key=lambda x: x[0])
                lat, who = responders[0]
                if forced_race and len(responders) >= 2:
                    responders[1] = (lat + sim["race_window_s"] / 2, responders[1][1])
                stale += sum(1 for l, _w in responders[1:] if l - lat < sim["race_window_s"])
                t += lat + sim["receipt_s"]
                last = who
                break
            rounds += 1
            t += sim["cover_timeout_s"]
            # cover with the same lookahead: never take word i when word i+1 is spellable only by us
            cover_ok = lead.alive(i) and lead is not last and spell(lead, word, alive_set)
            if cover_ok and lookahead >= 1 and i + 1 < n:
                cover_ok = any(v is not lead and spell(v, words[i + 1], alive_set) and not (excl_slow and v.profile == "slow")
                               for v in alive)
            if cover_ok:
                t += lead.latency_s + sim["receipt_s"]
                covers += 1
                last = lead
                break
            if rounds >= sim["max_rounds"]:
                reposts += 1
                t += sim["table_repost_s"]
                rounds = 0
                if reposts > sim["max_reposts"]:
                    return SimResult(False, t / 60, f"stall@{i}", stale, covers, replans, reposts)
        if sim["stall_prob"] and rng.random() < sim["stall_prob"]:
            t += sim["stall_s"]
    return SimResult(True, t / 60, "", stale, covers, replans, reposts)


def run_scenario(name: str, settings, *, trials: int = 1000, seed: int = 0, engine: str = "simple") -> MonteCarloReport:
    """CLI entry: Monte Carlo over a named scenario with the analytical model (default) or the Controller world."""
    from .simulator import resolve_scenario, controller_simulate_fn
    scenario = resolve_scenario(name)
    if engine == "controller":
        fn = controller_simulate_fn(settings)
    else:
        def fn(sc, sd):
            return simple_simulate(sc, sd, settings=settings)
    return run(scenario, trials, seed, fn)
