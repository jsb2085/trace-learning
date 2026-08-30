"""WMS integration tools exposed via MCP — work orders, incidents, equipment."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from trace_learning.mock.data.loader import load_wms, load_workers


class WorkOrderInput(BaseModel):
    work_order_id: str = Field(description="Work order ID, e.g. WO-7001")


class IncidentSearchInput(BaseModel):
    query: str = Field(description="Search incidents by keyword, pick, zone, or SKU")


class EquipmentInput(BaseModel):
    equipment_id: str = Field(description="Equipment ID, e.g. FL-02")


class ZoneInput(BaseModel):
    zone: str = Field(description="Warehouse zone")


class ShiftInput(BaseModel):
    shift_id: str = Field(description="Shift ID, e.g. SHIFT-DAY")


def _get_work_order(work_order_id: str) -> dict[str, Any]:
    woid = work_order_id.upper()
    for wo in load_wms()["work_orders"]:
        if wo["work_order_id"] == woid:
            return wo
    return {"error": f"Work order not found: {work_order_id}"}


def _search_incidents(query: str) -> list[dict[str, Any]]:
    q = query.lower()
    results: list[dict[str, Any]] = []
    for inc in load_wms()["incidents"]:
        blob = " ".join(str(inc.get(k, "")) for k in inc).lower()
        if q in blob:
            results.append(inc)
    return results


def _get_equipment(equipment_id: str) -> dict[str, Any]:
    eid = equipment_id.upper()
    for eq in load_wms()["equipment"]:
        if eq["equipment_id"] == eid:
            return eq
    return {"error": f"Equipment not found: {equipment_id}"}


def _list_equipment_by_zone(zone: str) -> list[dict[str, Any]]:
    z = zone.upper()
    return [eq for eq in load_wms()["equipment"] if eq["zone"] == z]


def _get_shift_roster(shift_id: str) -> dict[str, Any]:
    sid = shift_id.upper()
    for shift in load_wms()["shifts"]:
        if shift["shift_id"] == sid:
            roster = []
            for wid in shift["roster"]:
                for worker in load_workers()["workers"]:
                    if worker["worker_id"] == wid:
                        roster.append(worker)
                        break
            return {**shift, "workers": roster}
    return {"error": f"Shift not found: {shift_id}"}


WMS_MCP_TOOLS = [
    StructuredTool.from_function(
        func=_get_work_order,
        name="wms_get_work_order",
        description="Fetch a WMS work order (replenishment, cycle count, cold chain check).",
        args_schema=WorkOrderInput,
    ),
    StructuredTool.from_function(
        func=_search_incidents,
        name="wms_search_incidents",
        description="Search warehouse incidents by pick, zone, SKU, lot, or equipment.",
        args_schema=IncidentSearchInput,
    ),
    StructuredTool.from_function(
        func=_get_equipment,
        name="wms_get_equipment",
        description="Get equipment status (forklift, reach truck) by ID.",
        args_schema=EquipmentInput,
    ),
    StructuredTool.from_function(
        func=_list_equipment_by_zone,
        name="wms_list_equipment_by_zone",
        description="List all equipment assigned to a warehouse zone.",
        args_schema=ZoneInput,
    ),
    StructuredTool.from_function(
        func=_get_shift_roster,
        name="wms_get_shift_roster",
        description="Get workers on a shift with roles and certifications.",
        args_schema=ShiftInput,
    ),
]


def get_wms_tools() -> list[StructuredTool]:
    return list(WMS_MCP_TOOLS)
