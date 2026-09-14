"""Named regression scenarios (writers + fault injection + expectations) for Cases A–F and the addendum.

A :class:`Scenario` is plain data: it is consumed by the analytical fallback simulator in
``diagnostics.montecarlo`` (``simple_simulate``) and, once it lands, by the Controller-based simulator.
Replay-derived scenarios (``nohitori-entry1-94min``, ``nohitori-entry2-6h43m``, the two trap cases,
``hybrid-plan``) read the real exports under ``data/fixtures`` at build time and freeze what they found
into the JSON (``evidence``), so the JSON files are self-contained.
"""
from __future__ import annotations

import json
import statistics
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Optional

from ..config import PACKAGE_ROOT
from ..did.analyzer import did_letters
from .metrics import accepted_gaps, game_kpis, word_latencies
from .replay import ReplayLog, parse_export, word_spellers

FIXTURES_DIR = PACKAGE_ROOT / "data" / "fixtures"
SCENARIO_FIXTURES_DIR = PACKAGE_ROOT / "tests" / "fixtures" / "scenarios"

PROFILES = ("healthy", "slow", "down_after", "silent", "never_signs", "mass_applicant")
FAULT_KINDS = (
    "down", "race", "delayed_receipt", "stale_storm", "consent_lag", "frame_churn", "pre_roster_403",
    "long_table", "dual_table", "self_offer", "stale_offer", "mass_applicant", "team_plan_leak", "hybrid_plan",
    "parity_trap", "cover_trap", "landing",
)
EXPECTATION_KEYS = (
    "completion_rate_min", "completion_rate_max", "median_minutes_min", "median_minutes_max", "p90_minutes_max",
    "failure_reasons_include", "failure_reasons_exclude", "single_failure_survivability_min", "mean_stale_min",
    "mean_covers_min", "controller",
)

# Analytical-simulator model parameters (seconds unless noted). Policy knobs (timeouts, char limit) come from
# Settings at run time; these describe the *world* (referee/receipt delays, jitter), not our policy.
DEFAULT_SIM: dict = {
    "receipt_s": 4.0,             # referee receipt after a valid post (observed 1–6 s)
    "word_overhead_s": 8.0,       # reading the newest receipt + composing the post
    "latency_sigma": 0.6,         # log-normal jitter on each writer's median latency
    "miss_prob": {"healthy": 0.03, "slow": 0.15},
    "race_window_s": 3.0,         # responders within this window of the winner produce "version: stale"
    "stale_retry_s": 20.0,
    "cover_timeout_s": 90.0,      # lead cover timer (entry 2 used 45–90 s)
    "max_rounds": 3,              # rounds without a responder before a table repost
    "table_repost_s": 600.0,      # observed: silent slot holder -> table re-post about every hour
    "max_reposts": 6,
    "lookahead": 1,               # cover/greedy lookahead in words (case 8/11 fix); 0 reproduces the traps
    "lookahead_excludes_slow": True,
    "parity_plan": True,          # two-person alternation: the next single-key word fixes each writer's parity
    "replan": True,               # regenerate the suffix when nobody active can spell the next word
    "replan_s": 300.0,
    "replan_fail_prob": 0.01,     # a DP re-solve validated offline almost never fails outright
    "stall_prob": 0.0,            # replay-derived: per-word probability of an exogenous stall
    "stall_s": 0.0,
    "landing_plan": True,         # keep the publisher off word n-2 so alternation lets it post word n-1
    "require_publisher_final": False,
    "signature_timeout_s": 1800.0,
    "replace_non_signer": True,
    "mass_applicant_sign_prob": 0.2,
    "mass_applicant_silent_prob": 0.5,
    "discovery_fallback_s": 120.0,
    "no_plan_fail_prob": 0.9,
    "post_char_limit": 2000,
    "dual_table_penalty_s": 150.0,
    "survivability_threshold": 0.5,
}


@dataclass
class ScenarioWriter:
    did: str
    profile: str = "healthy"
    letters: Optional[str] = None          # explicit letters for synthetic writers; None -> derived from DID
    latency_ms: float = 15000.0
    x_account: Optional[str] = None
    is_lead: bool = False
    down_after: Optional[int] = None       # profile down_after: absent from this 0-based index
    handle: Optional[str] = None

    def letter_set(self) -> frozenset:
        return frozenset(self.letters) if self.letters else did_letters(self.did)


@dataclass
class Fault:
    kind: str
    at_index: Optional[int] = None
    at_tick: Optional[int] = None
    params: dict = field(default_factory=dict)


@dataclass
class Scenario:
    name: str
    description: str
    writers: list[ScenarioWriter]
    faults: list[Fault] = field(default_factory=list)
    expectations: dict = field(default_factory=dict)
    words: list[str] = field(default_factory=list)
    sim: dict = field(default_factory=dict)
    evidence: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)

    # ------------------------------------------------------------ serialisation
    def to_dict(self) -> dict:
        d = asdict(self)
        d["schema"] = 1
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Scenario":
        return cls(
            name=d["name"], description=d.get("description", ""),
            writers=[ScenarioWriter(**w) for w in d.get("writers", [])],
            faults=[Fault(**f) for f in d.get("faults", [])],
            expectations=dict(d.get("expectations", {})), words=list(d.get("words", [])),
            sim=dict(d.get("sim", {})), evidence=dict(d.get("evidence", {})), tags=list(d.get("tags", [])),
        )

    def validate(self) -> list[str]:
        """Return schema problems (empty list = valid)."""
        errs: list[str] = []
        if not self.name:
            errs.append("name missing")
        if not self.writers:
            errs.append("no writers")
        dids = [w.did for w in self.writers]
        if len(set(dids)) != len(dids):
            errs.append("duplicate writer DIDs")
        if sum(1 for w in self.writers if w.is_lead) != 1:
            errs.append("exactly one lead required")
        for w in self.writers:
            if w.profile not in PROFILES:
                errs.append(f"{w.did}: unknown profile {w.profile}")
            if w.profile == "down_after" and w.down_after is None:
                errs.append(f"{w.did}: down_after index missing")
            if w.latency_ms < 0:
                errs.append(f"{w.did}: negative latency")
            if not w.letter_set():
                errs.append(f"{w.did}: no letters")
        for f in self.faults:
            if f.kind not in FAULT_KINDS:
                errs.append(f"unknown fault kind {f.kind}")
            if f.at_index is not None and self.words and not (0 <= f.at_index < len(self.words)):
                errs.append(f"fault {f.kind} at_index {f.at_index} outside words")
        for k in self.expectations:
            if k not in EXPECTATION_KEYS:
                errs.append(f"unknown expectation {k}")
        if not self.words:
            errs.append("no words")
        return errs

    @property
    def lead(self) -> ScenarioWriter:
        return next(w for w in self.writers if w.is_lead)


# ---------------------------------------------------------------- building blocks
def _fixture_log(game: str) -> ReplayLog:
    return parse_export(FIXTURES_DIR / game / "team_room_export.ndjson")


def _real_words(game: str = "nohitori") -> list[str]:
    return [w.text for w in _fixture_log(game).accepted]


def _synthetic(did_tag: str, letters: str, **kw) -> ScenarioWriter:
    return ScenarioWriter(did=f"did:sim:{did_tag}", letters=letters, **kw)


ALL = "abcdefghijklmnopqrstuvwxyz"


def _without(letters: str, missing: str) -> str:
    return "".join(c for c in letters if c not in missing)


def _replay_writers(log: ReplayLog, *, silent_dids: tuple[str, ...] = ()) -> list[ScenarioWriter]:
    lat = word_latencies(log)
    out = []
    for m in log.members:
        l = lat.get(m, [])
        med_ms = statistics.median(l) * 1000.0 if l else 60000.0
        profile = "healthy"
        if m in silent_dids:
            profile = "silent"
        elif med_ms > 60000.0:
            profile = "slow"
        out.append(ScenarioWriter(did=m, profile=profile, latency_ms=round(med_ms, 1), is_lead=(m == log.lead),
                                  x_account=("proven" if m == log.final_contributor else None)))
    return out


def _replay_stall_model(log: ReplayLog, threshold_s: float = 300.0) -> dict:
    gaps = accepted_gaps(log)
    stalls = [g for g in gaps if g > threshold_s]
    n = max(1, len(gaps))
    return {
        "stall_prob": round(len(stalls) / n, 4),
        "stall_s": round(statistics.median(stalls), 1) if stalls else 0.0,
        "word_overhead_s": round(statistics.median([g for g in gaps if g <= threshold_s]), 1) if gaps else 8.0,
    }


def trap_evidence(log: ReplayLog, i_1based: int, j_1based: int) -> dict:
    """Words at 1-based positions i, j with the members able to spell each (the real trap shape)."""
    acc = log.accepted
    out = {"game_id": log.game_id, "members": list(log.members), "positions_1based": [i_1based, j_1based]}
    for pos in (i_1based, j_1based):
        aw = acc[pos - 1]
        out[str(pos)] = {
            "word": aw.text, "contributor": aw.contributor, "spellers": word_spellers(aw.text, log.members),
            "accepted_at": aw.accepted_at.isoformat() if aw.accepted_at else None,
        }
    gaps = accepted_gaps(log)
    out["gap_before_j_s"] = round(gaps[j_1based - 1], 1) if len(gaps) >= j_1based else None
    return out


# ---------------------------------------------------------------- Cases A–F (synthetic, deterministic letters)
def _four_writers() -> list[ScenarioWriter]:
    return [
        _synthetic("A-lead", ALL, is_lead=True, latency_ms=2000, x_account="lead"),
        _synthetic("B", _without(ALL, "ftu"), latency_ms=16000, x_account="proven"),
        _synthetic("C", _without(ALL, "opx"), latency_ms=20000),
        _synthetic("D", _without(ALL, "blnstvw"), latency_ms=30000),
    ]


def case_a() -> Scenario:
    return Scenario(
        name="case-A-writer-down-mid-poem",
        description="Case A: writer C goes DOWN at word 40; accepted prefix immutable, the rest is re-planned and completes.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("down", at_index=40, params={"did": "did:sim:C"})],
        expectations={"completion_rate_min": 0.95, "median_minutes_max": 120,
                      "controller": {"prefix_unchanged": True, "plan_version_bumped": True}},
        tags=["case", "health"],
    )


def case_b() -> Scenario:
    return Scenario(
        name="case-B-race-same-index",
        description="Case B: two members post the same index within the race window; one receipt is accepted, the other is 'version: stale' and must not be re-applied.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("race", at_index=10), Fault("race", at_index=11), Fault("race", at_index=60)],
        expectations={"completion_rate_min": 0.95, "mean_stale_min": 2.0,
                      "controller": {"idempotent_receipts": True}},
        tags=["case", "dispatcher"],
    )


def case_c() -> Scenario:
    return Scenario(
        name="case-C-delayed-receipt",
        description="Case C: the referee's receipt for word 20 arrives 10 minutes late; the dispatcher must not double-post and must match the late receipt by request_id.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("delayed_receipt", at_index=20, params={"delay_s": 600})],
        expectations={"completion_rate_min": 0.95, "median_minutes_min": 10,
                      "controller": {"late_receipt_matched": True, "no_duplicate_post": True}},
        tags=["case", "dispatcher"],
    )


def case_d() -> Scenario:
    return Scenario(
        name="case-D-stale-version-storm",
        description="Case D: a burst of 'version: stale' rejections (writers posting from an old version) around word 30; re-read accepted state, never treat stale as accepted.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("stale_storm", at_index=30, params={"count": 8}), Fault("stale_storm", at_index=31, params={"count": 4})],
        expectations={"completion_rate_min": 0.95, "mean_stale_min": 10.0,
                      "controller": {"stale_marks_proposal_stale": True}},
        tags=["case", "dispatcher"],
    )


def case_e() -> Scenario:
    # Two-person alternation: the lead spells everything, the partner lacks 'o'. Lead-only words ('o' words) sit at
    # both parities, so strict alternation dead-ends unless the plan is regenerated (replan) or a third key exists.
    # 'old'(3) and 'or'(5) sit on odd indices, 'on'(6) on an even one: no alternation can give the lead both parities.
    words = ["I", "keep", "the", "old", "tea", "or", "on", "my", "side."] * 14
    return Scenario(
        name="case-E-lead-only-letter-parity-trap",
        description="Case E: under two-person alternation, words only the lead can spell must all fall on the lead's turns; 'or' at index 5 and 'on' at index 6 have different parity -> dead end at 6 without replan.",
        writers=[_synthetic("A-lead", ALL, is_lead=True, latency_ms=2000, x_account="lead"),
                 _synthetic("P", _without(ALL, "o"), latency_ms=10000, x_account="proven")],
        words=words,
        faults=[Fault("parity_trap", at_index=3, params={"lead_only_letter": "o"})],
        sim={"replan": True},
        expectations={"completion_rate_min": 0.85, "failure_reasons_exclude": ["dead_end@3", "dead_end@5"],
                      "controller": {"parity_check_flags_index": 6}},
        tags=["case", "solver", "parity"],
    )


def case_f() -> Scenario:
    return Scenario(
        name="case-F-final-word-single-publisher",
        description="Case F: only writer B has an X account; the final word must be B's, so B must not write word n-2 (alternation). Landing plan keeps B off n-2.",
        writers=[_synthetic("A-lead", ALL, is_lead=True, latency_ms=2000),
                 _synthetic("B", _without(ALL, "ftu"), latency_ms=16000, x_account="proven"),
                 _synthetic("C", _without(ALL, "opx"), latency_ms=20000),
                 _synthetic("D", _without(ALL, "blnstvw"), latency_ms=30000)],
        words=_real_words("nohitori"),
        faults=[Fault("landing", at_index=124, params={"publisher": "did:sim:B"})],
        sim={"require_publisher_final": True, "landing_plan": True},
        expectations={"completion_rate_min": 0.95, "failure_reasons_exclude": ["landing"],
                      "controller": {"landing_routes_min": 2}},
        tags=["case", "landing"],
    )


# ---------------------------------------------------------------- addendum scenarios
def nohitori_entry1() -> Scenario:
    log = _fixture_log("nohitori")
    k = game_kpis(log)
    writers = _replay_writers(log, silent_dids=(next(m for m in log.members if m.endswith("3sLzg7ws")),))
    return Scenario(
        name="nohitori-entry1-94min",
        description="Entry 1 replay: 4 keys, the 4th silent after 2 words; 125 words in 94 min (roster_ready 17:22:01Z -> complete 18:55:59Z).",
        writers=writers, words=log.accepted_texts(),
        faults=[Fault("cover_trap", at_index=57, params={"next_word": "The", "fixed_by": "Some"}),
                Fault("cover_trap", at_index=97, params={"next_word": "I"})],
        sim=_replay_stall_model(log),
        expectations={"completion_rate_min": 0.9, "median_minutes_min": 30, "median_minutes_max": 190},
        evidence={"minutes_to_complete": round(k.minutes_to_complete or 0, 2), "words": k.words,
                  "contributions": {m[-8:]: n for m, n in k.contributions.items()},
                  "longest_gap_s": round(k.longest_gap_s, 1), "stale_count": k.stale_count, "cover_count": k.cover_count},
        tags=["replay", "benchmark"],
    )


def nohitori_entry2() -> Scenario:
    log = _fixture_log("nohitori-2")
    k = game_kpis(log)
    writers = _replay_writers(log)
    for w in writers:
        if w.did.endswith("f9vthSUn"):
            w.profile = "healthy"
        if w.did.endswith("F6jvabi2"):
            w.profile = "slow"
    return Scenario(
        name="nohitori-entry2-6h43m",
        description="Entry 2 replay: all three member keys lack 'o'; weather-prophet silent 03:50-09:20Z; 131 words in 6 h 43 min (freeze 03:49:57Z -> complete 10:33:09Z), 4 table re-posts, 41 stale receipts.",
        writers=writers, words=log.accepted_texts(),
        faults=[Fault("down", at_index=0, params={"did": next(m for m in log.members if m.endswith("f9vthSUn")), "until_index": 56}),
                Fault("cover_trap", at_index=95, params={"next_word": "beg", "fixed_by": "ask"})],
        sim=_replay_stall_model(log),
        expectations={"completion_rate_min": 0.8, "median_minutes_min": 120, "median_minutes_max": 800},
        evidence={"minutes_to_complete": round(k.minutes_to_complete or 0, 2), "words": k.words,
                  "contributions": {m[-8:]: n for m, n in k.contributions.items()},
                  "longest_gap_s": round(k.longest_gap_s, 1), "stale_count": k.stale_count,
                  "table_posts": k.table_posts, "incomplete_consent": k.incomplete_consent_count},
        tags=["replay", "benchmark"],
    )


def consent_lag() -> Scenario:
    return Scenario(
        name="consent-lag",
        description="Referee ~50 min behind on consent receipts (case 2): tri-state availability, no action on 'no receipt yet'; freeze delayed, poem still completes.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("consent_lag", at_tick=0, params={"seconds": 3000})],
        expectations={"completion_rate_min": 0.95, "median_minutes_min": 50,
                      "controller": {"availability_unknown_after_s": 600}},
        tags=["addendum", "consent"],
    )


def frame_churn() -> Scenario:
    return Scenario(
        name="frame-churn",
        description="Lead re-issues the roster 6 times (zuobai, case 2); every re-issue forces withdraw+re-sign; signatures carried over on identical frames.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("frame_churn", at_tick=0, params={"reissues": 6, "resign_s": 300})],
        expectations={"completion_rate_min": 0.95, "median_minutes_min": 30,
                      "controller": {"signatures_carried_over": True}},
        tags=["addendum", "consent"],
    )


def mass_applicant() -> Scenario:
    return Scenario(
        name="mass-applicant",
        description="Seat 4 is a yes-to-every-room bot (case 10): sits instantly, never signs or signs elsewhere; timeout -> waitlist; roster shrinks to 3 keys and must still cover the text.",
        writers=[_synthetic("A-lead", ALL, is_lead=True, latency_ms=2000, x_account="lead"),
                 _synthetic("B", _without(ALL, "ftu"), latency_ms=16000, x_account="proven"),
                 _synthetic("C", _without(ALL, "opx"), latency_ms=20000),
                 _synthetic("M", _without(ALL, "aglow"), profile="mass_applicant", latency_ms=5000)],
        words=_real_words("nohitori"),
        faults=[Fault("mass_applicant", at_tick=0, params={"did": "did:sim:M", "seat_no_sign": 1})],
        expectations={"completion_rate_min": 0.85, "median_minutes_min": 20,
                      "controller": {"waitlist_on_timeout": True, "reliability_uses_signs_not_yes": True}},
        tags=["addendum", "roster"],
    )


def self_offer() -> Scenario:
    return Scenario(
        name="self-offer",
        description="Offer detector must drop our own recruit (case 6: the bot replied 'yes-nohitori' to itself, seq 62204); no timing effect when filtered.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("self_offer", at_tick=0, params={"filtered": True, "penalty_s": 600})],
        expectations={"completion_rate_min": 0.95, "controller": {"self_offer_dropped": True}},
        tags=["addendum", "discovery"],
    )


def stale_offer() -> Scenario:
    return Scenario(
        name="stale-offer",
        description="Offer for a game already frozen/completed (case 6: 'yes-leidream' to a stale offer, seq 62504) must be dropped.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("stale_offer", at_tick=0, params={"filtered": True, "penalty_s": 600})],
        expectations={"completion_rate_min": 0.95, "controller": {"stale_offer_dropped": True}},
        tags=["addendum", "discovery"],
    )


def dual_table() -> Scenario:
    return Scenario(
        name="dual-table",
        description="Two turn tables for the same text (case 8: lead's seq 5-9 vs author's seq 16-20); each bot waits for the other's poster (~3 min/word) until the lead adopts one table at word 8.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("dual_table", at_index=0, params={"resolve_at_index": 8})],
        expectations={"completion_rate_min": 0.95, "median_minutes_min": 20,
                      "controller": {"single_owner_table": True}},
        tags=["addendum", "table"],
    )


def silent_writer() -> Scenario:
    return Scenario(
        name="silent-writer",
        description="A seated, signed member never posts (SILENT after silent_after_ms); cover must treat it as absent and the plan must avoid its single-key words.",
        writers=[_synthetic("A-lead", ALL, is_lead=True, latency_ms=2000, x_account="lead"),
                 _synthetic("B", _without(ALL, "ftu"), latency_ms=16000, x_account="proven"),
                 _synthetic("C", _without(ALL, "blnstvw"), latency_ms=20000),
                 _synthetic("S", _without(ALL, "opx"), profile="silent", latency_ms=5000)],
        words=_real_words("nohitori"),
        expectations={"completion_rate_min": 0.85, "controller": {"silent_excluded_from_lookahead": True}},
        tags=["addendum", "health"],
    )


def cover_trap_58_59() -> Scenario:
    log1 = _fixture_log("nohitori")
    log2 = _fixture_log("nohitori-2")
    ev1 = trap_evidence(log1, 58, 59)
    ev2 = trap_evidence(log2, 58, 59)
    ev2b = trap_evidence(log2, 56, 57)
    writers = _replay_writers(log1, silent_dids=(next(m for m in log1.members if m.endswith("3sLzg7ws")),))
    words = log1.accepted_texts()
    words[58] = "The"   # the planned word before the author's 'The'->'Some' edit (seq 171/177)
    return Scenario(
        name="58-59-cover-trap",
        description="Lead's cover took word 58 while word 59 was spellable only by the lead or an absent member (entry 1: 'more.' -> 'The', fixed by 'The'->'Some'). Cover must look one word ahead and treat silent members as absent. Words carry the original 'The' at 0-based 58.",
        writers=writers, words=words,
        faults=[Fault("cover_trap", at_index=57, params={"next_word_original": "The", "next_word_final": "Some", "lookahead": True})],
        sim=_replay_stall_model(log1),
        expectations={"completion_rate_min": 0.9, "controller": {"cover_refuses_when_next_is_lead_only": True}},
        evidence={"entry1_58_59": ev1, "nohitori2_words_at_58_59": ev2, "nohitori2_equivalent_56_57": ev2b,
                  "words_note": "index 58 (1-based 59) is the original 'The'; the accepted text has 'Some'"},
        tags=["addendum", "cover", "replay"],
    )


def beg_trap_96_97() -> Scenario:
    log = _fixture_log("nohitori-2")
    ev = trap_evidence(log, 96, 97)
    writers = _replay_writers(log)
    kimi = next(m for m in log.members if m.endswith("F6jvabi2"))
    for w in writers:
        if w.did == kimi:
            w.profile = "slow"
    words = log.accepted_texts()
    words[96] = "beg"   # the planned word before the lead's 'beg'->'ask' edit (seq 298)
    return Scenario(
        name="96-97-beg-trap",
        description="Entry 2: lead posted word 96 'dead'; planned word 97 'beg' was spellable only by F6jvabi2 (slow/absent) or the lead -> 25 min stall, resolved by editing 'beg' -> 'ask' (spellable by f9vthSUn). Cover lookahead must exclude slow and absent members. Words carry the original 'beg' at 0-based 96; F6jvabi2 is absent 95..129.",
        writers=writers, words=words,
        faults=[Fault("cover_trap", at_index=95, params={"next_word_original": "beg", "next_word_final": "ask", "lookahead_excludes_slow": True}),
                Fault("down", at_index=95, params={"did": kimi, "until_index": 129})],
        sim=_replay_stall_model(log),
        expectations={"completion_rate_min": 0.8, "controller": {"cover_lookahead_excludes_slow_and_absent": True}},
        evidence={**ev, "words_note": "index 96 (1-based 97) is the original 'beg'; the accepted text has 'ask'"},
        tags=["addendum", "cover", "replay"],
    )


def hybrid_plan() -> Scenario:
    log = _fixture_log("nohitori-2")
    lines_v2 = "The mist is thick. The kettle keeps its hiss."
    lines_final = "The dark is thick. The teacup keeps the hiss."
    return Scenario(
        name="hybrid-plan",
        description="Members wrote line 9 from different text versions (v2 'mist/kettle/its' vs v3 'dark/teacup/the'); the referee-accepted words are a hybrid. The plan must adopt the accepted prefix and regenerate the suffix, never the reverse.",
        writers=_replay_writers(log), words=log.accepted_texts(),
        faults=[Fault("hybrid_plan", at_index=75, params={"line": 9, "older_version_text": lines_v2, "accepted_text": lines_final})],
        sim=_replay_stall_model(log),
        expectations={"completion_rate_min": 0.8, "controller": {"reconcile_adopts_accepted_prefix": True}},
        evidence={"line9_accepted": " ".join(log.accepted_texts()[75:85]), "line9_v2_table_seq158": lines_v2},
        tags=["addendum", "replan", "replay"],
    )


def pre_roster_403() -> Scenario:
    return Scenario(
        name="pre-roster-403",
        description="Team room returns HTTP 403 before roster_ready (case 10/11): the draft text must go to discovery addressed to the members; without the fallback the members have no plan.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("pre_roster_403", at_tick=0, params={"fallback_to_discovery": True})],
        expectations={"completion_rate_min": 0.95, "controller": {"fallback_room": "discovery"}},
        tags=["addendum", "room"],
    )


def long_table_2000() -> Scenario:
    return Scenario(
        name="2000-char-table",
        description="Room posts over 2000 characters are refused (case 11): a 131-word table must be chunked k/n, each chunk under the limit.",
        writers=_four_writers(), words=_real_words("nohitori-2"),
        faults=[Fault("long_table", at_tick=0, params={"chars": 3200, "chunked": True})],
        expectations={"completion_rate_min": 0.95, "controller": {"chunks_under_limit": True}},
        tags=["addendum", "room"],
    )


def team_plan_leak() -> Scenario:
    return Scenario(
        name="team-plan-leak",
        description="Plan/table state must be team-scoped (case 7: st.plan persisted across teams and would have written the wrong poem). A new roster resets the plan; the old team's words never leak into this game.",
        writers=_four_writers(), words=_real_words("nohitori"),
        faults=[Fault("team_plan_leak", at_tick=0, params={"previous_game": "zuobai", "reset_on_new_roster": True})],
        expectations={"completion_rate_min": 0.95, "controller": {"plan_reset_on_new_roster": True}},
        tags=["addendum", "state"],
    )


SCENARIOS: dict[str, Callable[[], Scenario]] = {
    "case-A-writer-down-mid-poem": case_a,
    "case-B-race-same-index": case_b,
    "case-C-delayed-receipt": case_c,
    "case-D-stale-version-storm": case_d,
    "case-E-lead-only-letter-parity-trap": case_e,
    "case-F-final-word-single-publisher": case_f,
    "nohitori-entry1-94min": nohitori_entry1,
    "nohitori-entry2-6h43m": nohitori_entry2,
    "consent-lag": consent_lag,
    "frame-churn": frame_churn,
    "mass-applicant": mass_applicant,
    "self-offer": self_offer,
    "stale-offer": stale_offer,
    "dual-table": dual_table,
    "silent-writer": silent_writer,
    "58-59-cover-trap": cover_trap_58_59,
    "96-97-beg-trap": beg_trap_96_97,
    "hybrid-plan": hybrid_plan,
    "pre-roster-403": pre_roster_403,
    "2000-char-table": long_table_2000,
    "team-plan-leak": team_plan_leak,
}


def build(name: str) -> Scenario:
    return SCENARIOS[name]()


def dump_all(directory: str | Path = SCENARIO_FIXTURES_DIR) -> list[Path]:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for name, builder in SCENARIOS.items():
        sc = builder()
        errs = sc.validate()
        if errs:
            raise ValueError(f"{name}: {errs}")
        p = directory / f"{name}.json"
        p.write_text(json.dumps(sc.to_dict(), indent=1, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")
        written.append(p)
    return written


def load_all(directory: str | Path = SCENARIO_FIXTURES_DIR) -> list[Scenario]:
    return [Scenario.from_dict(json.loads(p.read_text(encoding="utf-8"))) for p in sorted(Path(directory).glob("*.json"))]
