"""Tests for mock tool implementations."""

from trace_learning.mock.mcp.tools import _get_user, _read_file, _search_files
from trace_learning.mock.rag.store import MockDocumentStore
from trace_learning.mock.tools.registry import _calculator, _get_weather, _lookup_order


def test_mcp_read_file():
    content = _read_file("docs/onboarding.md")
    assert "security training" in content


def test_mcp_read_file_not_found():
    assert "not found" in _read_file("missing.txt")


def test_mcp_search_files():
    results = _search_files("remote")
    paths = [r["path"] for r in results]
    assert "docs/policies/remote-work.md" in paths


def test_mcp_get_user():
    user = _get_user("u-001")
    assert user["name"] == "Alice Chen"
    assert user["team"] == "platform"


def test_rag_search():
    store = MockDocumentStore()
    results = store.search("refund policy")
    assert len(results) >= 1
    assert results[0]["title"] == "Refund Policy"


def test_calculator():
    assert _calculator("2 + 3 * 4") == 14.0


def test_lookup_order():
    order = _lookup_order("ORD-1001")
    assert order["status"] == "shipped"


def test_get_weather():
    weather = _get_weather("Austin")
    assert weather["condition"] == "sunny"
