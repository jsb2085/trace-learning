"""Operational domain tools — orders, parts, shipments, inventory.

These tools model a real fulfillment stack. Most eval questions require
combining 2+ of these with RAG policy lookup or MCP ticket/user access.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from trace_learning.mock.data.loader import (
    get_reference_date,
    load_inventory,
    load_orders,
    load_parts,
    load_shipments,
)


class QueryOrdersInput(BaseModel):
    status: str | None = Field(default=None, description="Filter by order status")
    customer_id: str | None = Field(default=None, description="Filter by customer ID")


class OrderIdInput(BaseModel):
    order_id: str = Field(description="Order identifier, e.g. ORD-2001")


class PartNumberInput(BaseModel):
    part_number: str = Field(description="Part number, e.g. PN-4421")


class AsOfDateInput(BaseModel):
    as_of_date: str = Field(description="ISO date (YYYY-MM-DD) to evaluate against")


def _get_business_date() -> dict[str, str]:
    return {"reference_date": get_reference_date(), "timezone": "America/Los_Angeles"}


def _query_orders(status: str | None = None, customer_id: str | None = None) -> list[dict[str, Any]]:
    orders = load_orders()["orders"]
    results = orders
    if status:
        results = [o for o in results if o["status"] == status.lower()]
    if customer_id:
        results = [o for o in results if o["customer_id"] == customer_id.upper()]
    return results


def _get_order(order_id: str) -> dict[str, Any]:
    for order in load_orders()["orders"]:
        if order["order_id"] == order_id.upper():
            return order
    return {"error": f"Order not found: {order_id}"}


def _get_part_history(part_number: str) -> dict[str, Any]:
    pn = part_number.upper()
    for part in load_parts()["parts"]:
        if part["part_number"] == pn:
            return part
    return {"error": f"Part not found: {part_number}"}


def _get_shipment_for_order(order_id: str) -> dict[str, Any]:
    order = _get_order(order_id)
    if "error" in order:
        return order
    shipment_id = order.get("shipment_id")
    if not shipment_id:
        return {"order_id": order_id.upper(), "shipment": None, "note": "No shipment created yet"}
    for shipment in load_shipments()["shipments"]:
        if shipment["shipment_id"] == shipment_id:
            return {"order_id": order_id.upper(), **shipment}
    return {"error": f"Shipment not found for order {order_id}"}


def _get_inventory(part_number: str) -> dict[str, Any]:
    pn = part_number.upper()
    for row in load_inventory()["inventory"]:
        if row["part_number"] == pn:
            return row
    return {"error": f"No inventory record for: {part_number}"}


def _find_orders_by_part(part_number: str) -> list[dict[str, Any]]:
    pn = part_number.upper()
    matches: list[dict[str, Any]] = []
    for order in load_orders()["orders"]:
        for item in order["line_items"]:
            if item["part_number"] == pn:
                matches.append(
                    {
                        "order_id": order["order_id"],
                        "status": order["status"],
                        "quantity": item["quantity"],
                        "promised_delivery": order["promised_delivery"],
                    }
                )
                break
    return matches


def _find_late_orders(as_of_date: str) -> dict[str, Any]:
    """Apply late-order rules: promised_delivery < as_of_date and status != delivered."""
    as_of = date.fromisoformat(as_of_date)
    late: list[dict[str, Any]] = []
    for order in load_orders()["orders"]:
        if order["status"] == "delivered":
            continue
        promised = date.fromisoformat(order["promised_delivery"])
        if promised < as_of:
            late.append(
                {
                    "order_id": order["order_id"],
                    "status": order["status"],
                    "promised_delivery": order["promised_delivery"],
                    "days_late": (as_of - promised).days,
                }
            )
    return {"as_of_date": as_of_date, "late_orders": late, "count": len(late)}


OPS_TOOLS = [
    StructuredTool.from_function(
        func=_get_business_date,
        name="ops_get_business_date",
        description="Return the current business date used by all operational systems.",
    ),
    StructuredTool.from_function(
        func=_query_orders,
        name="ops_query_orders",
        description="List orders with optional filters for status and customer_id.",
        args_schema=QueryOrdersInput,
    ),
    StructuredTool.from_function(
        func=_get_order,
        name="ops_get_order",
        description="Get full details for a single order including line items.",
        args_schema=OrderIdInput,
    ),
    StructuredTool.from_function(
        func=_get_part_history,
        name="ops_get_part_history",
        description="Get the full event timeline for a part number.",
        args_schema=PartNumberInput,
    ),
    StructuredTool.from_function(
        func=_get_shipment_for_order,
        name="ops_get_shipment",
        description="Get shipment tracking details for an order.",
        args_schema=OrderIdInput,
    ),
    StructuredTool.from_function(
        func=_get_inventory,
        name="ops_get_inventory",
        description="Get stock levels and restock schedule for a part.",
        args_schema=PartNumberInput,
    ),
    StructuredTool.from_function(
        func=_find_orders_by_part,
        name="ops_find_orders_by_part",
        description="Find all orders that include a given part number.",
        args_schema=PartNumberInput,
    ),
    StructuredTool.from_function(
        func=_find_late_orders,
        name="ops_find_late_orders",
        description=(
            "Return orders whose promised_delivery is before as_of_date and are not delivered. "
            "Use after looking up the late-order policy."
        ),
        args_schema=AsOfDateInput,
    ),
]


def get_ops_tools() -> list[StructuredTool]:
    return list(OPS_TOOLS)
