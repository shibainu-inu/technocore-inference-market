"""solver.roster + solver.reliability."""
from __future__ import annotations

import itertools
import time
from datetime import timedelta

import pytest

from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models.core import WriterProfile, utcnow
from sonnet_orchestrator.solver import reliability as R
from sonnet_orchestrator.solver import roster as RO

ALL = "abcdefghijklmnopqrstuvwxyz"


_seq = itertools.count(1)


def W(letters: str = ALL, **kw) -> WriterProfile:
    """Synthetic DID: prefix + letters + a numeric suffix (digits add no letters) so DIDs stay unique."""
    return WriterProfile(did="did:key:z6Mk" + letters + str(next(_seq)), **kw)


def without(*missing: str) -> str:
    return "".join(c for c in ALL if c not in missing)


def veteran(letters: str = ALL, **kw) -> WriterProfile:
    base = dict(words_accepted=30, words_rejected=1, signs=2, games_joined=2, poems_completed=2,
                word_latency_median_ms=20000)
    base.update(kw)
    return W(letters, **base)


@pytest.fixture(scope="module")
def settings():
    return load_settings()


# ---------------------------------------------------------------- reliability
def test_fresh_writer_scores_neutral_with_clean_addendum_record(settings):
    w = W(ALL)
    comps = R.components(w, settings)
    assert comps["completion_rate"] == 0.5 and comps["accepted_rate"] == 0.5
    assert comps["response_score"] == 0.5 and comps["recent_activity"] == 0.5
    assert comps["stale_conflict_score"] == 1.0
    assert 0.5 < R.score(w, settings) < 0.7
    assert not R.has_history(w)
    # no history -> the stored prior is used
    assert R.effective_reliability(W(ALL, reliability=0.9), settings) == 0.9


def test_counts_from_accepted_words_and_signs_not_from_yes(settings):
    good = veteran()
    assert R.has_history(good)
    assert R.score(good, settings) > R.score(W(ALL), settings)
    assert R.effective_reliability(good, settings) == R.score(good, settings)
    assert R.completion_rate(good) == 1.0
    assert R.accepted_rate(W(ALL, words_accepted=3, words_rejected=1)) == 0.75
    assert R.accepted_rate(W(ALL, words_accepted=0, words_rejected=4)) == 0.0


def test_mass_application_penalty_normalised_against_evidence(settings):
    ma = settings.reliability.mass_application
    spammer = W(ALL, seat_no_sign_count=2, consent_conflict_count=1)
    assert R.mass_application_penalty(spammer, settings) == ma.seat_no_sign_weight * 2 + ma.consent_conflict_weight
    assert R.stale_conflict_score(spammer, settings) == 0.0            # no evidence, only bad signs
    forgiven = W(ALL, seat_no_sign_count=1, words_accepted=50, signs=3)
    assert 0.9 < R.stale_conflict_score(forgiven, settings) < 1.0
    assert R.score(spammer, settings) < R.score(W(ALL), settings)
    assert R.score(forgiven, settings) > R.score(spammer, settings)
    clamped = W(ALL, mass_application_score=1.0)
    assert R.stale_conflict_score(clamped, settings) == 0.0


def test_response_and_recent_activity(settings):
    ref = settings.health.minimum_timeout_ms
    assert R.response_score(W(ALL, word_latency_median_ms=ref), settings) == pytest.approx(0.5)
    assert R.response_score(W(ALL, word_latency_median_ms=0), settings) == 1.0
    assert R.response_score(W(ALL, sign_latency_median_ms=ref * 3), settings) == pytest.approx(0.25)
    now = utcnow()
    fresh = W(ALL, last_activity_at=now)
    stale = W(ALL, last_activity_at=now - timedelta(milliseconds=settings.health.silent_after_ms))
    assert R.recent_activity(fresh, settings, now) == 1.0
    assert R.recent_activity(stale, settings, now) == pytest.approx(0.5)


def test_score_is_bounded_and_uses_weights(settings):
    best = W(ALL, games_joined=3, poems_completed=3, words_accepted=100, word_latency_median_ms=0,
             last_activity_at=utcnow())
    assert R.score(best, settings) == pytest.approx(1.0)
    worst = W(ALL, games_joined=3, poems_completed=0, words_rejected=10, word_latency_median_ms=10 ** 9,
              seat_no_sign_count=9, last_activity_at=utcnow() - timedelta(days=365))
    assert R.score(worst, settings) < 0.05


# ---------------------------------------------------------------- roster optimiser
def test_optimize_prefers_redundant_coverage_of_bottleneck_letters(settings):
    lead = veteran(ALL, handle="lead", is_lead=True)
    full1 = veteran(ALL, handle="full1")
    full2 = veteran(ALL, handle="full2")
    no_a = veteran(without("a"), handle="no_a")
    no_n = veteran(without("n"), handle="no_n")
    no_o = veteran(without("o"), handle="no_o")
    opts = RO.optimize([no_a, no_n, full1, no_o, full2], lead, settings, size=3)
    assert opts and all(o.size == 3 for o in opts)
    assert len(opts) == 10  # C(5, 2)
    best = opts[0]
    assert best.members[0] == lead.did
    assert set(best.members[1:]) == {full1.did, full2.did}
    assert best.components["redundant_bottleneck"] == 1.0
    assert best.tolerance == 1.0
    assert best.coverage.lead_only_letters == ""
    # a roster missing 'a' on one member covers "anost" only 4/5 twice -> lower
    worse = next(o for o in opts if set(o.members[1:]) == {no_a.did, no_n.did})
    assert worse.components["redundant_bottleneck"] < 1.0
    assert worse.score < best.score
    assert any("bottleneck" in e for e in best.explanation)
    assert opts == sorted(opts, key=lambda o: -o.score)


def test_optimize_penalises_lead_only_letters_via_tolerance(settings):
    lead = veteran(ALL, handle="lead")
    p1 = veteran(without("o"), handle="p1")
    p2 = veteran(without("o"), handle="p2")
    p3 = veteran(ALL, handle="p3")
    opt_bad = RO.evaluate([lead, p1, p2], lead, settings)
    assert opt_bad.coverage.lead_only_letters == "o"
    assert opt_bad.tolerance == 0.0 and any("parity trap" in e for e in opt_bad.explanation)
    opt_ok = RO.evaluate([lead, p1, p3], lead, settings)
    assert opt_ok.coverage.lead_only_letters == ""
    assert opt_ok.tolerance == 0.5  # losing p3 leaves 'o' uncovered excluding lead; losing p1 is fine
    assert opt_ok.score > opt_bad.score
    assert opt_ok.components["redundant_bottleneck"] > opt_bad.components["redundant_bottleneck"]


def test_require_accepted_word_history_drops_no_history_when_enough_remain(settings):
    lead = veteran(ALL, handle="lead")
    vets = [veteran(ALL, handle=f"v{i}") for i in range(4)]
    newbie = W(ALL, handle="new", reliability=1.0, word_latency_median_ms=0)
    assert settings.roster.require_accepted_word_history
    opts = RO.optimize(vets + [newbie], lead, settings, size=settings.roster.minimum_size)
    assert opts
    assert all(newbie.did not in o.members for o in opts)
    assert any("without accepted-word history" in e for e in opts[0].explanation)


def test_no_history_candidates_kept_but_ranked_last_when_pool_is_short(settings):
    lead = veteran(ALL, handle="lead")
    vet = veteran(ALL, handle="vet")
    newbies = [W(ALL, handle=f"new{i}") for i in range(3)]
    opts = RO.optimize([*newbies, vet], lead, settings, size=3)
    assert opts and vet.did in opts[0].members
    assert any("no-history candidates kept" in e for e in opts[0].explanation)
    assert any("no accepted-word history" in e for e in opts[0].explanation)


def test_size_penalty_prefers_preferred_size_when_extra_members_add_nothing(settings):
    lead = veteran(ALL, handle="lead")
    vets = [veteran(ALL, handle=f"v{i}") for i in range(settings.roster.maximum_size - 1)]
    opts = RO.optimize(vets, lead, settings)  # sizes minimum..maximum
    sizes = {o.size for o in opts}
    assert sizes == set(range(settings.roster.minimum_size, settings.roster.maximum_size + 1))
    assert opts[0].size == settings.roster.preferred_size
    bigger = next(o for o in opts if o.size == settings.roster.preferred_size + 1)
    assert bigger.components["size_penalty"] == pytest.approx(settings.roster.size_penalty_per_extra_member)


def test_pool_cap_keeps_large_candidate_sets_tractable(settings):
    lead = veteran(ALL, handle="lead")
    cands = [veteran(without(c), handle=f"c{i}") for i, c in enumerate(ALL)]
    cands += [veteran(ALL, handle=f"f{i}") for i in range(10)]   # same speed/history, one more letter
    t0 = time.perf_counter()
    opts = RO.optimize(cands, lead, settings)
    dt = time.perf_counter() - t0
    assert opts and dt < 2.0, dt
    assert any("pool capped" in e for e in opts[0].explanation)
    # the pool ranks full-alphabet veterans first, so the best roster is made of them
    assert all(m in {c.did for c in cands if c.letters == frozenset(ALL)} for m in opts[0].members[1:])


def test_speed_and_completion_terms_rank_candidates(settings):
    lead = veteran(ALL, handle="lead")
    fast = veteran(ALL, handle="fast", word_latency_median_ms=5000)
    slow = veteran(ALL, handle="slow", word_latency_median_ms=200000)
    quitter = veteran(ALL, handle="quit", games_joined=4, poems_completed=1)
    opts = RO.optimize([slow, quitter, fast], lead, settings, size=2)
    assert opts[0].members == [lead.did, fast.did]
    assert opts[-1].members[1] in (slow.did, quitter.did)
    assert RO.member_value(fast, settings) > RO.member_value(slow, settings)


def test_optimize_edge_cases(settings):
    lead = veteran(ALL, handle="lead")
    assert RO.optimize([], lead, settings) == []
    assert RO.optimize([lead], lead, settings) == []          # lead is never its own candidate
    one = veteran(ALL, handle="one")
    opts = RO.optimize([one, one], lead, settings)             # dedupe + too few for minimum size
    assert len(opts) == 1 and opts[0].members == [lead.did, one.did]
    assert any("too few candidates" in e for e in opts[0].explanation)
    assert RO.optimize([one], lead, settings, size=2, max_options=0) == []


def test_evaluate_components_and_explanation(settings):
    lead = veteran(ALL, handle="lead")
    a = veteran(without("q", "x"), handle="a")
    b = veteran(without("q"), handle="b")
    o = RO.evaluate([a, b, lead], lead, settings)
    assert o.members[0] == lead.did and set(o.members[1:]) == {a.did, b.did}
    for k in ("reliability", "lexical_coverage", "redundant_coverage", "response_speed", "historical_completion", "size_penalty"):
        assert k in o.components
    assert 0.0 <= o.components["reliability"] <= 1.0
    assert o.coverage.lead_only_letters == "q"
    assert any("lead-only letters" in e for e in o.explanation)
    assert any(e.startswith("score ") for e in o.explanation)
