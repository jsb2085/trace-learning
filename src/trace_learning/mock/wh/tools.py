"""Warehouse floor tools — picks, SKUs, locations, lots, workers."""

from __future__ import annotations

from datetime import date
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from trace_learning.mock.data.loader import (
    get_reference_date,
    load_inbound,
    load_locations,
    load_lots,
    load_pick_orders,
    load_skus,
    load_workers,
)


class PickIdInput(BaseModel):
    pick_id: str = Field(description="Pick order ID, e.g. PK-5001")


class SkuInput(BaseModel):
    sku: str = Field(description="SKU code, e.g. SKU-HVA-4421")


class LocationInput(BaseModel):
    location_id: str = Field(description="Bin or pallet location, e.g. A-12-03")


class LotInput(BaseModel):
    lot_id: str = Field(description="Lot identifier, e.g. LOT-HV-081")


class WorkerInput(BaseModel):
    worker_id: str = Field(description="Worker ID, e.g. WK-001")


class InboundInput(BaseModel):
    inbound_id: str = Field(description="Inbound shipment ID, e.g. INB-3004")


class ReplenishmentInput(BaseModel):
    zone: str | None = Field(default=None, description="Optional zone filter")


class AsOfDateInput(BaseModel):
    as_of_date: str = Field(description="ISO date (YYYY-MM-DD)")


class AisleInput(BaseModel):
    aisle: str = Field(description="Aisle letter, e.g. B")


class QueryPicksInput(BaseModel):
    status: str | None = Field(default=None, description="Filter by pick status")
    zone: str | None = Field(default=None, description="Filter picks touching this zone")


def _get_warehouse_date() -> dict[str, str]:
    return {
        "warehouse_id": "WH-EAST",
        "reference_date": get_reference_date(),
        "timezone": "America/New_York",
    }


def _list_pick_orders(status: str | None = None, zone: str | None = None) -> list[dict[str, Any]]:
    picks = load_pick_orders()["pick_orders"]
    if status:
        picks = [p for p in picks if p["status"] == status.lower()]
    if zone:
        zone_upper = zone.upper()
        picks = [p for p in picks if zone_upper in p.get("zone_route", [])]
    return picks


def _get_pick_order(pick_id: str) -> dict[str, Any]:
    pid = pick_id.upper()
    for pick in load_pick_orders()["pick_orders"]:
        if pick["pick_id"] == pid:
            return pick
    return {"error": f"Pick order not found: {pick_id}"}


def _find_overdue_picks(as_of_date: str) -> dict[str, Any]:
    as_of = date.fromisoformat(as_of_date)
    overdue: list[dict[str, Any]] = []
    for pick in load_pick_orders()["pick_orders"]:
        if pick["status"] == "shipped":
            continue
        ship_by = date.fromisoformat(pick["ship_by"])
        if ship_by < as_of:
            overdue.append(
                {
                    "pick_id": pick["pick_id"],
                    "status": pick["status"],
                    "ship_by": pick["ship_by"],
                    "days_overdue": (as_of - ship_by).days,
                    "assigned_worker_id": pick.get("assigned_worker_id"),
                }
            )
    return {"as_of_date": as_of_date, "overdue_picks": overdue, "count": len(overdue)}


def _get_sku(sku: str) -> dict[str, Any]:
    code = sku.upper()
    for row in load_skus()["skus"]:
        if row["sku"] == code:
            return row
    return {"error": f"SKU not found: {sku}"}


def _get_sku_locations(sku: str) -> dict[str, Any]:
    info = _get_sku(sku)
    if "error" in info:
        return info
    locs = []
    for loc_id in info["locations"]:
        for loc in load_locations()["locations"]:
            if loc["location_id"] == loc_id:
                locs.append(loc)
                break
    return {"sku": info["sku"], "locations": locs}


def _get_location(location_id: str) -> dict[str, Any]:
    lid = location_id.upper()
    for loc in load_locations()["locations"]:
        if loc["location_id"] == lid:
            return loc
    return {"error": f"Location not found: {location_id}"}


def _get_bin_contents(location_id: str) -> list[dict[str, Any]]:
    lid = location_id.upper()
    return [b for b in load_locations()["bin_contents"] if b["location_id"] == lid]


def _get_lot_trace(lot_id: str) -> dict[str, Any]:
    lot_upper = lot_id.upper()
    for lot in load_lots()["lots"]:
        if lot["lot_id"] == lot_upper:
            return lot
    return {"error": f"Lot not found: {lot_id}"}


def _find_picks_by_sku(sku: str) -> list[dict[str, Any]]:
    code = sku.upper()
    matches: list[dict[str, Any]] = []
    for pick in load_pick_orders()["pick_orders"]:
        for item in pick["line_items"]:
            if item["sku"] == code:
                matches.append(
                    {
                        "pick_id": pick["pick_id"],
                        "status": pick["status"],
                        "ship_by": pick["ship_by"],
                        "quantity": item["quantity"],
                        "lot_id": item["lot_id"],
                    }
                )
                break
    return matches


def _find_picks_by_lot(lot_id: str) -> list[dict[str, Any]]:
    lot_upper = lot_id.upper()
    matches: list[dict[str, Any]] = []
    for pick in load_pick_orders()["pick_orders"]:
        for item in pick["line_items"]:
            if item["lot_id"] == lot_upper:
                matches.append(
                    {
                        "pick_id": pick["pick_id"],
                        "status": pick["status"],
                        "sku": item["sku"],
                        "quantity": item["quantity"],
                    }
                )
    return matches


def _get_inbound(inbound_id: str) -> dict[str, Any]:
    iid = inbound_id.upper()
    for row in load_inbound()["inbound"]:
        if row["inbound_id"] == iid:
            return row
    return {"error": f"Inbound not found: {inbound_id}"}


def _get_worker(worker_id: str) -> dict[str, Any]:
    wid = worker_id.upper()
    for worker in load_workers()["workers"]:
        if worker["worker_id"] == wid:
            return worker
    return {"error": f"Worker not found: {worker_id}"}


def _get_worker_assignments(worker_id: str) -> dict[str, Any]:
    worker = _get_worker(worker_id)
    if "error" in worker:
        return worker
    picks = [_get_pick_order(pid) for pid in worker.get("assigned_picks", [])]
    return {"worker_id": worker_id.upper(), "assigned_picks": picks}


def _get_replenishment_tasks(zone: str | None = None) -> list[dict[str, Any]]:
    tasks = load_workers()["replenishment_tasks"]
    if zone:
        tasks = [t for t in tasks if t["zone"] == zone.upper()]
    return tasks


def _search_locations(aisle: str) -> list[dict[str, Any]]:
    aisle_upper = aisle.upper()
    return [loc for loc in load_locations()["locations"] if loc["aisle"] == aisle_upper]


WH_TOOLS = [
    StructuredTool.from_function(
        func=_get_warehouse_date,
        name="wh_get_warehouse_date",
        description="Return the warehouse ID and current reference date for WMS operations.",
    ),
    StructuredTool.from_function(
        func=_list_pick_orders,
        name="wh_list_pick_orders",
        description="List outbound pick orders with optional status and zone filters.",
        args_schema=QueryPicksInput,
    ),
    StructuredTool.from_function(
        func=_get_pick_order,
        name="wh_get_pick_order",
        description="Get pick order details including line items, zones, and assigned worker.",
        args_schema=PickIdInput,
    ),
    StructuredTool.from_function(
        func=_find_overdue_picks,
        name="wh_find_overdue_picks",
        description="Find picks whose ship_by date is before as_of_date and not yet shipped.",
        args_schema=AsOfDateInput,
    ),
    StructuredTool.from_function(
        func=_get_sku,
        name="wh_get_sku",
        description="Get SKU master data: zones, hazmat/cold flags, inventory levels.",
        args_schema=SkuInput,
    ),
    StructuredTool.from_function(
        func=_get_sku_locations,
        name="wh_get_sku_locations",
        description="Get all storage locations and zone metadata for a SKU.",
        args_schema=SkuInput,
    ),
    StructuredTool.from_function(
        func=_get_location,
        name="wh_get_location",
        description="Get location metadata: zone, aisle, type, temperature control, status.",
        args_schema=LocationInput,
    ),
    StructuredTool.from_function(
        func=_get_bin_contents,
        name="wh_get_bin_contents",
        description="List SKUs, lots, quantities, and status at a bin/pallet location.",
        args_schema=LocationInput,
    ),
    StructuredTool.from_function(
        func=_get_lot_trace,
        name="wh_get_lot_trace",
        description="Get full event timeline for a lot (receive, QC, putaway, damage).",
        args_schema=LotInput,
    ),
    StructuredTool.from_function(
        func=_find_picks_by_sku,
        name="wh_find_picks_by_sku",
        description="Find all pick orders containing a SKU.",
        args_schema=SkuInput,
    ),
    StructuredTool.from_function(
        func=_find_picks_by_lot,
        name="wh_find_picks_by_lot",
        description="Find all pick orders that include a specific lot.",
        args_schema=LotInput,
    ),
    StructuredTool.from_function(
        func=_get_inbound,
        name="wh_get_inbound",
        description="Get inbound ASN/receipt status and planned putaway zone.",
        args_schema=InboundInput,
    ),
    StructuredTool.from_function(
        func=_get_worker,
        name="wh_get_worker",
        description="Get worker profile, role, shift, and certifications.",
        args_schema=WorkerInput,
    ),
    StructuredTool.from_function(
        func=_get_worker_assignments,
        name="wh_get_worker_assignments",
        description="Get full pick order details assigned to a worker.",
        args_schema=WorkerInput,
    ),
    StructuredTool.from_function(
        func=_get_replenishment_tasks,
        name="wh_get_replenishment_tasks",
        description="List replenishment tasks, optionally filtered by zone.",
        args_schema=ReplenishmentInput,
    ),
    StructuredTool.from_function(
        func=_search_locations,
        name="wh_search_locations",
        description="List all locations in an aisle.",
        args_schema=AisleInput,
    ),
]


def get_wh_tools() -> list[StructuredTool]:
    return list(WH_TOOLS)
