from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.db import Store
from sonnet_orchestrator.models import Decision
from sonnet_orchestrator.orchestration.operator import OperatorBoundary


def test_classify_from_settings_and_unknown_fails_closed():
    settings = load_settings()
    ob = OperatorBoundary(settings)
    assert ob.classify("retry") == Decision.AUTONOMOUS
    assert ob.classify("table_repost") == Decision.AUTONOMOUS
    assert ob.classify("switch_team") == Decision.OPERATOR_APPROVAL
    assert ob.classify("start_next_entry") == Decision.OPERATOR_APPROVAL
    assert ob.classify("something_new") == Decision.OPERATOR_APPROVAL


def test_request_records_and_gates():
    settings = load_settings()
    store = Store(":memory:")
    ob = OperatorBoundary(settings, store)
    assert ob.request("reconcile", "prefix differs at 12") is True
    assert ob.request("abandon_current_team", "roster stalled 3 h") is False
    assert [r.action for r in ob.pending()] == ["abandon_current_team"]
    ob.approve("abandon_current_team")
    assert ob.request("abandon_current_team", "operator said go") is True
    rows = store.con.execute("SELECT action, decision, approved FROM operator_decisions ORDER BY id").fetchall()
    assert [tuple(r) for r in rows] == [("reconcile", "AUTONOMOUS", None), ("abandon_current_team", "OPERATOR_APPROVAL", 0),
                                        ("abandon_current_team", "OPERATOR_APPROVAL", 1)]


def test_overlap_prefers_approval():
    settings = load_settings()
    settings.operator.autonomous.append("switch_team")   # a misconfiguration: listed in both
    assert OperatorBoundary(settings).classify("switch_team") == Decision.OPERATOR_APPROVAL
