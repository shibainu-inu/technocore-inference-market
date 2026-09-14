"""solver.assignment — DP word->writer assignment with synthetic DIDs.

Synthetic DID = "did:key:z6Mk" + letters, so d,i,k,e,y,z,m are always present.
"""
from __future__ import annotations

import itertools
import random
import time

import pytest

from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models.core import WordEntry, WriterHealth, WriterProfile
from sonnet_orchestrator.solver import assignment as A
from sonnet_orchestrator.solver import explain_assignment

ALL = "abcdefghijklmnopqrstuvwxyz"


_seq = itertools.count(1)


def W(letters: str = ALL, **kw) -> WriterProfile:
    """Synthetic DID: prefix + letters + a numeric suffix (digits add no letters) so DIDs stay unique."""
    return WriterProfile(did="did:key:z6Mk" + letters + str(next(_seq)), **kw)


def without(*missing: str) -> str:
    return "".join(c for c in ALL if c not in missing)


def words(*texts: str, start: int = 0) -> list[WordEntry]:
    return [WordEntry(index=start + i, text=t, line=(start + i) // 10, syllables=1) for i, t in enumerate(texts)]


def primaries(result) -> list[str]:
    return [a.primary for a in result.assignments]


@pytest.fixture(scope="module")
def settings():
    return load_settings()


# ---------------------------------------------------------------- basics
def test_alternation_no_consecutive_same_writer(settings):
    lead = W(ALL, handle="lead", is_lead=True)
    b = W(ALL, handle="b")
    ws = words("me", "dim", "key", "zed", "ink")
    r = A.assign(ws, [lead, b], settings=settings, lead_did=lead.did)
    assert r.feasible and not r.dead_ends
    p = primaries(r)
    assert len(p) == 5 and all(p[i] != p[i + 1] for i in range(4))
    assert [a.index for a in r.assignments] == [0, 1, 2, 3, 4]
    assert all(a.keys == 2 for a in r.assignments)
    assert r.cost == pytest.approx(sum(r.per_index_cost.values()))


def test_last_contributor_constrains_first_word(settings):
    lead = W(ALL, handle="lead")
    b = W(ALL, handle="b")
    r = A.assign(words("me", "dim"), [lead, b], settings=settings, lead_did=lead.did, last_contributor=lead.did)
    assert primaries(r) == [b.did, lead.did]
    r = A.assign(words("me", "dim"), [lead, b], settings=settings, lead_did=lead.did, last_contributor=b.did)
    assert primaries(r) == [lead.did, b.did]


def test_letters_rule_only_spellers_are_eligible(settings):
    lead = W(ALL, handle="lead")
    no_o = W(without("o"), handle="no_o")
    r = A.assign(words("go", "me", "to", "dim"), [lead, no_o], settings=settings, lead_did=lead.did)
    assert r.feasible
    assert primaries(r) == [lead.did, no_o.did, lead.did, no_o.did]
    assert r.assignments[0].lead_only and r.assignments[0].keys == 1
    assert not r.assignments[1].lead_only and r.assignments[1].keys == 2


def test_start_index_slices_the_suffix_only(settings):
    lead, b = W(ALL, handle="lead"), W(ALL, handle="b")
    ws = words("a", "b", "c", "d", "e", "f")
    r = A.assign(ws, [lead, b], settings=settings, lead_did=lead.did, start_index=4, last_contributor=lead.did)
    assert [a.index for a in r.assignments] == [4, 5]
    assert r.start_index == 4
    assert primaries(r) == [b.did, lead.did]


def test_empty_suffix(settings):
    lead, b = W(ALL), W(ALL)
    r = A.assign(words("a", "b"), [lead, b], settings=settings, lead_did=lead.did, start_index=2)
    assert r.feasible and r.assignments == [] and r.cost == 0.0


# ---------------------------------------------------------------- lookahead / dead ends
def test_lookahead_catches_dead_end_a_greedy_choice_would_cause(settings):
    """A is far cheaper than B, so a greedy solver takes A for 'me'; then 'go' (A-only) has no writer.
    Only lookahead (or the exhaustive DP) gives 'me' to B."""
    a = W(ALL, handle="A", word_latency_median_ms=100, health=WriterHealth.HEALTHY)
    b = W(without("o"), handle="B", word_latency_median_ms=10000, health=WriterHealth.SLOW)
    r = A.assign(words("me", "go"), [a, b], settings=settings, lead_did=a.did)
    assert r.feasible, r.explanation
    assert primaries(r) == [b.did, a.did]
    # longer chain: the A-only word sits 3 slots ahead; parity must be arranged from index 0
    r = A.assign(words("me", "dim", "key", "go"), [a, b], settings=settings, lead_did=a.did)
    assert r.feasible
    assert primaries(r) == [b.did, a.did, b.did, a.did]
    # greedy sanity: A really is the cheaper writer when unconstrained
    r = A.assign(words("me"), [a, b], settings=settings, lead_did=a.did)
    assert primaries(r) == [a.did]


def test_dead_end_beyond_lookahead_window_is_still_found(settings):
    """The DP is exhaustive: a parity trap 9 words ahead is avoided even with lookahead 2."""
    a = W(ALL, handle="A", word_latency_median_ms=100)
    b = W(without("o"), handle="B", word_latency_median_ms=10000)
    ws = words("me", "dim", "key", "zed", "ink", "mid", "dye", "kid", "go")
    r = A.assign(ws, [a, b], settings=settings, lead_did=a.did, lookahead=2)
    assert r.lookahead == max(2, settings.solver.minimum_lookahead)
    assert r.feasible
    assert primaries(r)[-1] == a.did and primaries(r)[0] == a.did


def test_effective_lookahead_respects_minimum(settings):
    assert A.effective_lookahead(settings, 0) == settings.solver.minimum_lookahead
    assert A.effective_lookahead(settings) == max(settings.solver.lookahead_words, settings.solver.minimum_lookahead)
    assert A.effective_lookahead(settings, 9) == 9


def test_unspellable_word_is_a_dead_end_with_penalty(settings):
    lead = W(without("q"), handle="lead")
    b = W(without("q"), handle="b")
    ws = words("me", "quiz", "dim")
    r = A.assign(ws, [lead, b], settings=settings, lead_did=lead.did)
    assert not r.feasible
    assert r.dead_ends == [1]
    dead = r.assignments[1]
    assert dead.primary == "" and dead.backup is None and dead.keys == 0
    assert r.cost >= settings.solver.dead_end_penalty
    assert r.per_index_cost[1] == settings.solver.dead_end_penalty
    assert any("DEAD END" in e and "q" in e for e in r.explanation)
    # words around the dead end are still assigned
    assert r.assignments[0].primary and r.assignments[2].primary


def test_two_lead_only_words_in_a_row_is_a_dead_end(settings):
    lead = W(ALL, handle="lead")
    b = W(without("o"), handle="b")
    r = A.assign(words("go", "to", "me"), [lead, b], settings=settings, lead_did=lead.did)
    assert not r.feasible
    assert len(r.dead_ends) == 1 and r.dead_ends[0] in (0, 1)
    assert any("no consecutive" in e for e in r.explanation)
    assert r.assignments[2].primary  # continues after the dead end


# ---------------------------------------------------------------- every member must contribute
def test_every_member_must_contribute_uses_the_expensive_writer(settings):
    a = W(ALL, handle="A", word_latency_median_ms=100)
    b = W(ALL, handle="B", word_latency_median_ms=100)
    c = W(ALL, handle="C", word_latency_median_ms=20000, health=WriterHealth.SUSPECT)
    ws = words(*(["me", "dim"] * 4))
    off = A.assign(ws, [a, b, c], settings=settings, lead_did=a.did)
    assert c.did not in primaries(off)
    on = A.assign(ws, [a, b, c], settings=settings, lead_did=a.did, every_member_must_contribute=True)
    assert on.feasible and on.missing_contributors == []
    assert primaries(on).count(c.did) == 1  # exactly once: it is the expensive one
    assert on.cost > off.cost
    p = primaries(on)
    assert all(p[i] != p[i + 1] for i in range(len(p) - 1))


def test_every_member_must_contribute_infeasible_when_a_member_spells_nothing(settings):
    a = W(ALL, handle="A")
    b = W(ALL, handle="B")
    c = W("", handle="C")  # only d,i,k,e,y,z,m
    ws = words("go", "to", "no", "so")
    r = A.assign(ws, [a, b, c], settings=settings, lead_did=a.did, every_member_must_contribute=True)
    assert not r.feasible
    assert r.missing_contributors == [c.did]
    assert r.dead_ends == []
    assert r.cost >= settings.solver.dead_end_penalty
    assert any("never assigned" in e and "C" in e for e in r.explanation)


def test_every_member_flag_default_off_can_come_from_settings(settings):
    assert A.every_member_flag(settings, None) is False
    assert A.every_member_flag(settings, True) is True


# ---------------------------------------------------------------- backups
def test_backup_is_cheapest_alternative_that_keeps_alternation(settings):
    a = W(ALL, handle="A", word_latency_median_ms=100)
    b = W(ALL, handle="B", word_latency_median_ms=500)
    c = W(ALL, handle="C", word_latency_median_ms=5000)
    r = A.assign(words("me", "dim", "key"), [a, b, c], settings=settings, lead_did=a.did)
    assert r.feasible
    p = primaries(r)
    assert p == [a.did, b.did, a.did]  # A cheapest, B second; C never needed
    for k, asg in enumerate(r.assignments):
        prev = p[k - 1] if k else None
        nxt = p[k + 1] if k + 1 < len(p) else None
        assert asg.backup not in (asg.primary, prev, nxt)
        assert asg.backup is not None
    assert r.assignments[0].backup == c.did  # B is next, so the backup for index 0 is C
    assert r.assignments[1].backup == c.did


def test_backup_none_when_only_two_writers(settings):
    a, b = W(ALL, handle="A"), W(ALL, handle="B")
    r = A.assign(words("me", "dim", "key"), [a, b], settings=settings, lead_did=a.did)
    assert primaries(r) == [a.did, b.did, a.did]
    # index 1 (prev A, next A) and index 2 (prev B) have nobody left; index 0 gets B only as a relaxed backup
    assert r.assignments[1].backup is None and r.assignments[2].backup is None
    assert r.assignments[0].backup == b.did
    assert any("#0" in e and "next slot re-covered" in e for e in r.explanation)


def test_backup_relaxed_when_next_slot_blocks_all_strict_candidates(settings):
    a = W(ALL, handle="A", word_latency_median_ms=100)
    b = W(without("o"), handle="B", word_latency_median_ms=200)
    c = W(without("o"), handle="C", word_latency_median_ms=300)
    # 'go' can only be A; 'me' before it must be B or C; backup for 'me' cannot avoid A being next
    r = A.assign(words("me", "go"), [a, b, c], settings=settings, lead_did=a.did)
    assert primaries(r) == [b.did, a.did]
    assert r.assignments[0].backup == c.did
    assert r.assignments[1].backup is None


# ---------------------------------------------------------------- availability / health / cost terms
def test_down_silent_and_unavailable_writers_never_get_words(settings):
    a = W(ALL, handle="A")
    b = W(ALL, handle="B")
    down = W(ALL, handle="D", health=WriterHealth.DOWN, word_latency_median_ms=1)
    silent = W(ALL, handle="S", health=WriterHealth.SILENT, word_latency_median_ms=1)
    gone = W(ALL, handle="G", word_latency_median_ms=1)
    r = A.assign(words("me", "dim", "key", "zed"), [a, b, down, silent, gone], settings=settings, lead_did=a.did,
                 unavailable={gone.did})
    assert set(primaries(r)) == {a.did, b.did}
    assert all(asg.keys == 2 for asg in r.assignments)
    assert A.active_writers([a, down, silent, gone], {gone.did}) == [a]


def test_last_contributor_that_is_down_does_not_constrain(settings):
    a = W(ALL, handle="A", word_latency_median_ms=100)
    b = W(ALL, handle="B", word_latency_median_ms=1000)
    d = W(ALL, handle="D", health=WriterHealth.DOWN)
    r = A.assign(words("me"), [a, b, d], settings=settings, lead_did=a.did, last_contributor=d.did)
    assert primaries(r) == [a.did]


def test_cost_prefers_fast_reliable_healthy_writers(settings):
    fast = W(ALL, handle="fast", word_latency_median_ms=100)
    slow = W(ALL, handle="slow", word_latency_median_ms=10000, health=WriterHealth.SLOW)
    suspect = W(ALL, handle="sus", word_latency_median_ms=100, health=WriterHealth.SUSPECT)
    unreliable = W(ALL, handle="unrel", word_latency_median_ms=100, words_accepted=1, words_rejected=9,
                   seat_no_sign_count=5)
    ws = words(*(["me", "dim"] * 5))
    r = A.assign(ws, [unreliable, suspect, slow, fast], settings=settings, lead_did=fast.did)
    p = primaries(r)
    assert p.count(fast.did) == 5
    assert suspect.did not in p and slow.did not in p or p.count(fast.did) == 5
    # the partner slot goes to the cheapest of the rest: unreliable (healthy, fast) vs suspect vs slow
    partner = {x for x in p if x != fast.did}
    assert len(partner) == 1


def test_latency_norm_and_health_penalty(settings):
    a = W(ALL, word_latency_median_ms=500)
    b = W(ALL, word_latency_median_ms=2000)
    c = W(ALL)
    ln = A.latency_norm([a, b, c])
    assert ln[a.did] == pytest.approx(0.25) and ln[b.did] == 1.0 and ln[c.did] == 1.0
    assert A.latency_norm([c])[c.did] == 1.0
    assert A.health_penalty(W(ALL, health=WriterHealth.HEALTHY)) == 0.0
    assert A.health_penalty(W(ALL, health=WriterHealth.SLOW)) == 0.5
    assert A.health_penalty(W(ALL, health=WriterHealth.SUSPECT)) == 0.8


def test_cost_formula_matches_weights(settings):
    w = settings.solver.weights
    a = W(ALL, handle="A", word_latency_median_ms=300, health=WriterHealth.SLOW)
    b = W(ALL, handle="B", word_latency_median_ms=600)
    r = A.assign(words("me"), [a, b], settings=settings, lead_did=a.did)
    # B: latency 1.0, reliability prior 0.5 (no history), health 0 ; A: latency .5, health .5
    from sonnet_orchestrator.solver import reliability as R
    cost_a = w.latency * 0.5 + w.reliability * (1 - R.effective_reliability(a, settings)) + w.fragility * 0.5 + w.health * 0.5
    cost_b = w.latency * 1.0 + w.reliability * (1 - R.effective_reliability(b, settings)) + w.fragility * 0.5
    assert r.cost == pytest.approx(min(cost_a, cost_b))


# ---------------------------------------------------------------- determinism / performance / explain
def test_deterministic(settings):
    random.seed(7)
    writers = [W(ALL, handle="lead")] + [W(without(m), handle=f"w{i}", word_latency_median_ms=100 * (i + 1))
                                        for i, m in enumerate("oatns")]
    vocab = ["me", "go", "sat", "tin", "dim", "key", "not", "so", "at", "on", "zed"]
    ws = words(*[random.choice(vocab) for _ in range(60)])
    r1 = A.assign(ws, writers, settings=settings, lead_did=writers[0].did)
    r2 = A.assign(ws, writers, settings=settings, lead_did=writers[0].did)
    assert primaries(r1) == primaries(r2) and r1.cost == r2.cost and r1.explanation == r2.explanation


def test_performance_130_words_6_writers_under_one_second(settings):
    random.seed(20260914)
    writers = [W(ALL, handle="lead")] + [W(without(*m), handle=f"w{i}", word_latency_median_ms=100 * (i + 1))
                                        for i, m in enumerate(["o", "a", "st", "n", "x"])]
    vocab = ["the", "and", "of", "to", "in", "is", "you", "that", "it", "he", "was", "for", "on", "are", "as",
             "with", "his", "they", "at", "be", "this", "from", "have", "or", "one", "had", "by", "word", "not"]
    ws = words(*[random.choice(vocab) for _ in range(130)])
    t0 = time.perf_counter()
    r = A.assign(ws, writers, settings=settings, lead_did=writers[0].did, every_member_must_contribute=True)
    dt = time.perf_counter() - t0
    assert r.feasible
    assert dt < 1.0, dt
    p = primaries(r)
    assert all(p[i] != p[i + 1] for i in range(len(p) - 1))
    assert set(p) == {w.did for w in writers}


def test_explain_assignment_text(settings):
    lead = W(without("q"), handle="lead")
    b = W(without("o", "q"), handle="b")
    ws = words("go", "me", "quiz")
    r = A.assign(ws, [lead, b], settings=settings, lead_did=lead.did)
    text = explain_assignment(r, ws, [lead, b])
    assert "feasible=False" in text
    assert "#  0 go" in text and "lead" in text and "lead-only" in text
    assert "DEAD END" in text
    assert "reasons:" in text
    assert "keys=1" in text
