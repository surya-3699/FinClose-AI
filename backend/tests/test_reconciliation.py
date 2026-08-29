from app.demo_data import demo_data
from app.reconciliation import reconcile, metrics

def test_reconciliation_produces_results():
    settlements, ledger = demo_data()
    results = reconcile(settlements, ledger)
    assert len(results) >= len(settlements)

def test_exact_matches_exist():
    settlements, ledger = demo_data()
    results = reconcile(settlements, ledger)
    assert any(r["method"] == "exact" for r in results)

def test_metrics():
    settlements, ledger = demo_data()
    results = reconcile(settlements, ledger)
    m = metrics(results)
    assert "reconciliation_rate" in m
    assert m["total_items"] == len(results)
