"""Tests for warehouse mock tools."""

from trace_learning.mock.mcp.tools import _get_equipment, _search_incidents
from trace_learning.mock.rag.store import MockDocumentStore
from trace_learning.mock.tools.registry import _days_between
from trace_learning.mock.wh.tools import (
    _find_overdue_picks,
    _find_picks_by_sku,
    _get_bin_contents,
    _get_lot_trace,
    _get_pick_order,
)


def test_overdue_picks_on_reference_date():
    result = _find_overdue_picks("2026-08-30")
    ids = {p["pick_id"] for p in result["overdue_picks"]}
    assert ids == {"PK-5001", "PK-5002", "PK-5005", "PK-5007"}


def test_lot_trace_qc_failure():
    lot = _get_lot_trace("LOT-GR-044")
    events = [e["event"] for e in lot["events"]]
    assert "qc_failed" in events
    assert "rework_started" in events


def test_find_picks_by_sku():
    picks = _find_picks_by_sku("SKU-GR-7782")
    pick_ids = {p["pick_id"] for p in picks}
    assert pick_ids == {"PK-5002", "PK-5005"}


def test_pick_order_line_items():
    pick = _get_pick_order("PK-5005")
    assert len(pick["line_items"]) == 2


def test_rag_overdue_policy():
    store = MockDocumentStore()
    results = store.search("overdue pick")
    assert "ship_by" in results[0]["body"]


def test_incident_search_by_pick():
    incidents = _search_incidents("PK-5002")
    assert any(i["incident_id"] == "INC-8003" for i in incidents)


def test_damaged_bin_contents():
    contents = _get_bin_contents("B-08-05")
    assert contents[0]["status"] == "damaged"


def test_equipment_down():
    eq = _get_equipment("FL-02")
    assert eq["status"] == "down"


def test_days_between():
    assert _days_between("2026-08-28", "2026-08-30")["days"] == 2
