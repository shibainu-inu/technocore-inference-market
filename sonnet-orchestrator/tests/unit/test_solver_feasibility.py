"""solver.feasibility — exact reachability, two-person parity, failure tolerance."""
from __future__ import annotations

import itertools
import pytest

from sonnet_orchestrator.models.core import WordEntry, WriterHealth, WriterProfile
from sonnet_orchestrator.solver import feasibility as F

ALL = "abcdefghijklmnopqrstuvwxyz"


_seq = itertools.count(1)


def W(letters: str = ALL, **kw) -> WriterProfile:
    """Synthetic DID: prefix + letters + a numeric suffix (digits add no letters) so DIDs stay unique."""
    return WriterProfile(did="did:key:z6Mk" + letters + str(next(_seq)), **kw)


def without(*missing: str) -> str:
    return "".join(c for c in ALL if c not in missing)


def words(*texts: str, start: int = 0) -> list[WordEntry]:
    return [WordEntry(index=start + i, text=t, line=(start + i) // 10, syllables=1) for i, t in enumerate(texts)]


@pytest.fixture
def pair():
    lead = W(ALL, handle="lead", is_lead=True)
    partner = W(without("o"), handle="partner")
    return lead, partner


# ---------------------------------------------------------------- parity (two-person alternation)
def test_parity_lead_only_word_on_wrong_turn_is_infeasible(pair):
    lead, partner = pair
    ws = words("go", "me", "key", "dim")  # 'go' is lead-only
    # previous word by the lead -> index 0 is the partner's turn -> trap
    bad = F.check(ws, [lead, partner], lead_did=lead.did, last_contributor=lead.did)
    assert not bad.feasible and bad.first_dead_end == 0
    assert bad.lead_only == [0]
    assert any("no consecutive" in r for r in bad.reasons)
    pr = F.parity_check(ws, [lead, partner], lead.did, 0, lead.did)
    assert pr.applicable and not pr.ok and pr.violations == [0] and pr.lead_starts is False
    assert any("forced by last_contributor" in r for r in pr.reasons)


def test_parity_shifted_by_one_word_becomes_feasible(pair):
    lead, partner = pair
    ws = words("me", "go", "key", "dim")  # a two-key word first shifts the parity
    good = F.check(ws, [lead, partner], lead_did=lead.did, last_contributor=lead.did)
    assert good.feasible and good.first_dead_end is None and good.dead_ends == []
    pr = F.parity_check(ws, [lead, partner], lead.did, 0, lead.did)
    assert pr.applicable and pr.ok and pr.violations == [] and pr.lead_starts is False


def test_parity_free_start_picks_a_working_parity(pair):
    lead, partner = pair
    ws = words("go", "me", "to", "dim")   # lead-only at 0 and 2: works iff lead starts
    pr = F.parity_check(ws, [lead, partner], lead.did, 0, None)
    assert pr.ok and pr.lead_starts is True and pr.lead_only == [0, 2]
    ws2 = words("go", "me", "dim", "to")  # lead-only at 0 and 3: no parity works
    pr2 = F.parity_check(ws2, [lead, partner], lead.did, 0, None)
    assert not pr2.ok and len(pr2.violations) == 1
    assert not F.check(ws2, [lead, partner], lead_did=lead.did).feasible


def test_parity_partner_only_words(pair):
    lead, partner = pair
    lead2 = W(without("a"), handle="lead")   # lead lacks 'a'; partner lacks 'o'
    ws = words("cat", "go", "cab", "so")
    pr = F.parity_check(ws, [lead2, partner], lead2.did, 0, None)
    assert pr.partner_only == [0, 2] and pr.lead_only == [1, 3]
    assert pr.ok and pr.lead_starts is False


def test_parity_not_applicable_with_three_writers(pair):
    lead, partner = pair
    third = W(ALL, handle="third")
    ws = words("go", "me", "dim", "to")
    pr = F.parity_check(ws, [lead, partner, third], lead.did, 0, None)
    assert not pr.applicable and pr.ok
    # a DOWN third writer does not count: back to a two-person alternation
    third_down = W(ALL, handle="third", health=WriterHealth.DOWN)
    pr2 = F.parity_check(ws, [lead, partner, third_down], lead.did, 0, None)
    assert pr2.applicable and not pr2.ok


def test_parity_with_start_index(pair):
    lead, partner = pair
    ws = words("me", "go", "key", "dim", "to")  # suffix from 3: 'dim'(both) 'to'(lead)
    pr = F.parity_check(ws, [lead, partner], lead.did, 3, lead.did)
    assert pr.ok and pr.lead_only == [4]
    pr_bad = F.parity_check(ws, [lead, partner], lead.did, 3, partner.did)
    assert not pr_bad.ok and pr_bad.violations == [4]


# ---------------------------------------------------------------- check
def test_check_unspellable_word_reason_lists_missing_letters(pair):
    lead, partner = pair
    lead_q = W(without("q"), handle="lead")
    partner_q = W(without("q", "o"), handle="p")
    ws = words("me", "quiz", "go")
    fz = F.check(ws, [lead_q, partner_q], lead_did=lead_q.did)
    assert not fz.feasible and fz.first_dead_end == 1 and fz.dead_ends == [1]
    assert fz.keys == {0: 2, 1: 0, 2: 1}
    assert any("missing letters: q" in r for r in fz.reasons)


def test_check_reports_every_dead_end_and_keeps_going(pair):
    lead, partner = pair
    ws = words("go", "to", "me", "so", "no")
    fz = F.check(ws, [lead, partner], lead_did=lead.did)
    assert fz.dead_ends == [1, 4] and fz.first_dead_end == 1


def test_check_three_writers_is_reachability_not_parity():
    a, b, c = W(ALL, handle="a"), W(without("o"), handle="b"), W(without("o"), handle="c")
    ws = words("go", "me", "dim", "to")   # infeasible for 2, feasible with a third writer
    assert F.check(ws, [a, b, c], lead_did=a.did).feasible
    assert not F.check(ws, [a, b], lead_did=a.did).feasible


def test_check_no_active_writers():
    a = W(ALL, health=WriterHealth.DOWN)
    fz = F.check(words("me"), [a], lead_did=a.did)
    assert not fz.feasible and fz.first_dead_end == 0 and "no active writer" in fz.reasons[0]


def test_check_unavailable_treated_like_absent(pair):
    lead, partner = pair
    third = W(ALL, handle="third")
    ws = words("go", "me", "dim", "to")
    assert F.check(ws, [lead, partner, third], lead_did=lead.did).feasible
    assert not F.check(ws, [lead, partner, third], lead_did=lead.did, unavailable={third.did}).feasible


# ---------------------------------------------------------------- failure tolerance
def test_failure_tolerance_survivability_kpi():
    a = W(ALL, handle="A", is_lead=True)
    b = W(without("o"), handle="B")
    c = W(without("o"), handle="C")
    ws = words("go", "me", "to", "dim", "so", "key")   # lead-only words all on even slots
    ft = F.failure_tolerance(ws, [a, b, c], lead_did=a.did)
    assert ft.baseline.feasible
    assert isinstance(ft, F.FailureTolerance) and len(ft) == 3 and set(ft) == {a.did, b.did, c.did}
    assert not ft[a.did].feasible            # losing the only 'o' writer is fatal
    assert ft[b.did].feasible and ft[c.did].feasible
    assert ft.fatal == [a.did] and set(ft.survivors) == {b.did, c.did}
    assert ft.survivability == pytest.approx(2 / 3)
    assert dict(ft)[a.did].first_dead_end is not None


def test_failure_tolerance_excludes_inactive_and_unavailable():
    a = W(ALL, handle="A")
    b = W(ALL, handle="B")
    c = W(ALL, handle="C")
    d = W(ALL, handle="D", health=WriterHealth.SILENT)
    ws = words("me", "dim", "key")
    ft = F.failure_tolerance(ws, [a, b, c, d], lead_did=a.did, unavailable={c.did})
    assert set(ft) == {a.did, b.did}
    # with a pair only, losing either leaves one writer -> consecutive words impossible
    assert ft.survivability == 0.0 and set(ft.fatal) == {a.did, b.did}


def test_failure_tolerance_full_redundancy():
    ws = words("go", "me", "to", "so")
    writers = [W(ALL, handle=h) for h in "ABC"]
    ft = F.failure_tolerance(ws, writers, lead_did=writers[0].did)
    assert ft.survivability == 1.0 and ft.fatal == []
