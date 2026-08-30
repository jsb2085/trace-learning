"""Tests for mock tool implementations."""

from trace_learning.mock.mcp.tools import _get_ticket, _get_user, _search_tickets
from trace_learning.mock.ops.tools import (
    _find_late_orders,
    _find_orders_by_part,
    _get_order,
    _get_part_history,
)
from trace_learning.mock.rag.store import MockDocumentStore
from trace_learning.mock.tools.registry import _days_between


def test_late_orders_on_reference_date():
    result = _find_late_orders("2026-08-30")
    ids = {o["order_id"] for o in result["late_orders"]}
    assert ids == {"ORD-2001", "ORD-2002", "ORD-2005", "ORD-2008"}


def test_part_history_qc_failure():
    part = _get_part_history("PN-7782")
    events = [e["event"] for e in part["events"]]
    assert "qc_failed" in events
    assert "rework_started" in events


def test_find_orders_by_part():
    orders = _find_orders_by_part("PN-7782")
    order_ids = {o["order_id"] for o in orders}
    assert order_ids == {"ORD-2002", "ORD-2005"}


def test_get_order_with_line_items():
    order = _get_order("ORD-2005")
    assert len(order["line_items"]) == 2


def test_rag_late_order_policy():
    store = MockDocumentStore()
    results = store.search("late order definition")
    assert "promised_delivery" in results[0]["body"]


def test_ticket_search_by_order():
    tickets = _search_tickets("ORD-2001")
    assert any(t["ticket_id"] == "TKT-5001" for t in tickets)


def test_ticket_owner_lookup():
    ticket = _get_ticket("TKT-5001")
    user = _get_user(ticket["owner_user_id"])
    assert user["name"] == "Carol Wu"


def test_days_between():
    result = _days_between("2026-08-28", "2026-08-30")
    assert result["days"] == 2
