#!/usr/bin/env python3
"""Generate warehouse agent eval dataset — 15 templates x 4 instances, 4 tools each."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "eval" / "questions.json"

# Each instance declares exactly 4 expected tool calls (3-4 range; all use 4 here).
INSTANCES: list[dict] = [
    # overdue-picks (4)
    {
        "id": "overdue-picks-001",
        "template_id": "overdue-picks",
        "params": {"as_of_date": "2026-08-30"},
        "category": "outbound",
        "expected_answer": "PK-5001",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "overdue pick definition"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-30"}},
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-001"}},
        ],
        "notes": "Also overdue: PK-5002, PK-5005, PK-5007",
    },
    {
        "id": "overdue-picks-002",
        "template_id": "overdue-picks",
        "params": {"as_of_date": "2026-08-29"},
        "category": "outbound",
        "expected_answer": "PK-5005",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "overdue pick"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-29"}},
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-003"}},
        ],
        "notes": "Also overdue: PK-5002",
    },
    {
        "id": "overdue-picks-003",
        "template_id": "overdue-picks",
        "params": {"as_of_date": "2026-08-28"},
        "category": "outbound",
        "expected_answer": "PK-5005",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "overdue pick SLA"}},
            {"tool": "wh_list_pick_orders", "args": {"status": "picking"}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-28"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "overdue-picks-004",
        "template_id": "overdue-picks",
        "params": {"as_of_date": "2026-08-31"},
        "category": "outbound",
        "expected_answer": "PK-5006",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "overdue pick"}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-31"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5006"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
        ],
        "notes": "PK-5006 on_hold also overdue; plus PK-5001/5002/5005/5007",
        "difficulty": "hard",
    },
    # sku-trace (4)
    {
        "id": "sku-trace-001",
        "template_id": "sku-trace",
        "params": {"sku": "SKU-GR-7782"},
        "category": "inventory",
        "expected_answer": "qc_failed",
        "expected_tool_calls": [
            {"tool": "wh_get_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-044"}},
            {"tool": "wh_find_picks_by_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "rag_search", "args": {"query": "lot traceability"}},
        ],
    },
    {
        "id": "sku-trace-002",
        "template_id": "sku-trace",
        "params": {"sku": "SKU-BKT-3309"},
        "category": "inventory",
        "expected_answer": "damage_reported",
        "expected_tool_calls": [
            {"tool": "wh_get_sku", "args": {"sku": "SKU-BKT-3309"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-BK-210"}},
            {"tool": "wh_find_picks_by_sku", "args": {"sku": "SKU-BKT-3309"}},
            {"tool": "rag_search", "args": {"query": "traceability SOP"}},
        ],
    },
    {
        "id": "sku-trace-003",
        "template_id": "sku-trace",
        "params": {"sku": "SKU-CTL-9901"},
        "category": "inventory",
        "expected_answer": "firmware",
        "expected_tool_calls": [
            {"tool": "wh_get_sku", "args": {"sku": "SKU-CTL-9901"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-IC-009"}},
            {"tool": "wh_find_picks_by_sku", "args": {"sku": "SKU-CTL-9901"}},
            {"tool": "rag_search", "args": {"query": "lot traceability"}},
        ],
    },
    {
        "id": "sku-trace-004",
        "template_id": "sku-trace",
        "params": {"sku": "SKU-COLD-110"},
        "category": "inventory",
        "expected_answer": "temp_check_passed",
        "expected_tool_calls": [
            {"tool": "wh_get_sku", "args": {"sku": "SKU-COLD-110"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-CD-019"}},
            {"tool": "wh_find_picks_by_sku", "args": {"sku": "SKU-COLD-110"}},
            {"tool": "rag_search", "args": {"query": "cold chain compliance"}},
        ],
    },
    # pick-delay (4)
    {
        "id": "pick-delay-001",
        "template_id": "pick-delay",
        "params": {"pick_id": "PK-5002"},
        "category": "outbound",
        "expected_answer": "qc_failed",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-044"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5002"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-002"}},
        ],
    },
    {
        "id": "pick-delay-002",
        "template_id": "pick-delay",
        "params": {"pick_id": "PK-5005"},
        "category": "outbound",
        "expected_answer": "Missed transfer scan",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-BK-210"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5005"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-003"}},
        ],
    },
    {
        "id": "pick-delay-003",
        "template_id": "pick-delay",
        "params": {"pick_id": "PK-5007"},
        "category": "outbound",
        "expected_answer": "hazmat",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5007"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-IC-009"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5007"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-CTL-9901"}},
        ],
    },
    {
        "id": "pick-delay-004",
        "template_id": "pick-delay",
        "params": {"pick_id": "PK-5001"},
        "category": "outbound",
        "expected_answer": "picking",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-HV-081"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5001"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-001"}},
        ],
    },
    # bin-audit (4)
    {
        "id": "bin-audit-001",
        "template_id": "bin-audit",
        "params": {"location_id": "B-08-05"},
        "category": "inventory",
        "expected_answer": "damaged",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "B-08-05"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "B-08-05"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-BKT-3309"}},
            {"tool": "rag_search", "args": {"query": "damage hold policy"}},
        ],
    },
    {
        "id": "bin-audit-002",
        "template_id": "bin-audit",
        "params": {"location_id": "Q-03-01"},
        "category": "inventory",
        "expected_answer": "qc_hold",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "Q-03-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "Q-03-01"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-043"}},
            {"tool": "rag_search", "args": {"query": "hold policy"}},
        ],
    },
    {
        "id": "bin-audit-003",
        "template_id": "bin-audit",
        "params": {"location_id": "A-04-01"},
        "category": "inventory",
        "expected_answer": "allocated",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "A-04-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "A-04-01"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "wh_find_picks_by_sku", "args": {"sku": "SKU-FST-M8"}},
        ],
    },
    {
        "id": "bin-audit-004",
        "template_id": "bin-audit",
        "params": {"location_id": "C-02-01"},
        "category": "inventory",
        "expected_answer": "available",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "C-02-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "C-02-01"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "rag_search", "args": {"query": "cold chain"}},
        ],
    },
    # replenishment-block (4)
    {
        "id": "replen-block-001",
        "template_id": "replenishment-block",
        "params": {"zone": "PICK-FACE"},
        "category": "operations",
        "expected_answer": "FL-02",
        "expected_tool_calls": [
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "PICK-FACE"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7001"}},
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "PICK-FACE"}},
            {"tool": "rag_search", "args": {"query": "replenishment SOP"}},
        ],
    },
    {
        "id": "replen-block-002",
        "template_id": "replenishment-block",
        "params": {"zone": "BULK-A"},
        "category": "operations",
        "expected_answer": "RPL-1002",
        "expected_tool_calls": [
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "BULK-A"}},
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "BULK-A"}},
            {"tool": "wh_search_locations", "args": {"aisle": "B"}},
            {"tool": "rag_search", "args": {"query": "replenishment"}},
        ],
    },
    {
        "id": "replen-block-003",
        "template_id": "replenishment-block",
        "params": {"zone": "COLD"},
        "category": "operations",
        "expected_answer": "RPL-1003",
        "expected_tool_calls": [
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "COLD"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7003"}},
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "COLD"}},
            {"tool": "rag_search", "args": {"query": "replenishment SOP"}},
        ],
    },
    {
        "id": "replen-block-004",
        "template_id": "replenishment-block",
        "params": {"zone": "PICK-FACE"},
        "category": "operations",
        "expected_answer": "equipment_unavailable",
        "expected_tool_calls": [
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "PICK-FACE"}},
            {"tool": "wms_search_incidents", "args": {"query": "FL-02"}},
            {"tool": "wms_get_equipment", "args": {"equipment_id": "FL-02"}},
            {"tool": "rag_search", "args": {"query": "equipment assignment"}},
        ],
        "difficulty": "hard",
    },
    # worker-load (4)
    {
        "id": "worker-load-001",
        "template_id": "worker-load",
        "params": {"worker_id": "WK-001"},
        "category": "operations",
        "expected_answer": "PK-5001",
        "expected_tool_calls": [
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-001"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-001"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-30"}},
        ],
    },
    {
        "id": "worker-load-002",
        "template_id": "worker-load",
        "params": {"worker_id": "WK-002"},
        "category": "operations",
        "expected_answer": "PK-5002",
        "expected_tool_calls": [
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-002"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-002"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_find_overdue_picks", "args": {"as_of_date": "2026-08-30"}},
        ],
    },
    {
        "id": "worker-load-003",
        "template_id": "worker-load",
        "params": {"worker_id": "WK-003"},
        "category": "operations",
        "expected_answer": "PK-5005",
        "expected_tool_calls": [
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-003"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-003"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "days_between", "args": {"start_date": "2026-08-27", "end_date": "2026-08-30"}},
        ],
    },
    {
        "id": "worker-load-004",
        "template_id": "worker-load",
        "params": {"worker_id": "WK-004"},
        "category": "operations",
        "expected_answer": "none",
        "expected_tool_calls": [
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-004"}},
            {"tool": "wh_get_worker_assignments", "args": {"worker_id": "WK-004"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7001"}},
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "PICK-FACE"}},
        ],
    },
    # inbound-putaway (4)
    {
        "id": "inbound-001",
        "template_id": "inbound-putaway",
        "params": {"inbound_id": "INB-3004"},
        "category": "inbound",
        "expected_answer": "receiving",
        "expected_tool_calls": [
            {"tool": "wh_get_inbound", "args": {"inbound_id": "INB-3004"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "wh_get_location", "args": {"location_id": "R-01-01"}},
            {"tool": "rag_search", "args": {"query": "putaway rules"}},
        ],
    },
    {
        "id": "inbound-002",
        "template_id": "inbound-putaway",
        "params": {"inbound_id": "INB-3003"},
        "category": "inbound",
        "expected_answer": "COLD",
        "expected_tool_calls": [
            {"tool": "wh_get_inbound", "args": {"inbound_id": "INB-3003"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-COLD-110"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-CD-019"}},
            {"tool": "rag_search", "args": {"query": "putaway cold"}},
        ],
    },
    {
        "id": "inbound-003",
        "template_id": "inbound-putaway",
        "params": {"inbound_id": "INB-3001"},
        "category": "inbound",
        "expected_answer": "putaway_complete",
        "expected_tool_calls": [
            {"tool": "wh_get_inbound", "args": {"inbound_id": "INB-3001"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "wh_get_sku_locations", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "rag_search", "args": {"query": "putaway rules"}},
        ],
    },
    {
        "id": "inbound-004",
        "template_id": "inbound-putaway",
        "params": {"inbound_id": "INB-3002"},
        "category": "inbound",
        "expected_answer": "PICK-FACE",
        "expected_tool_calls": [
            {"tool": "wh_get_inbound", "args": {"inbound_id": "INB-3002"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-HVA-4421"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-HV-081"}},
            {"tool": "rag_search", "args": {"query": "putaway"}},
        ],
    },
    # pick-route-cold (4)
    {
        "id": "pick-cold-001",
        "template_id": "pick-route-cold",
        "params": {"pick_id": "PK-5002"},
        "category": "outbound",
        "expected_answer": "yes",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-COLD-110"}},
            {"tool": "wh_get_sku_locations", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "rag_search", "args": {"query": "zone routing cold"}},
        ],
    },
    {
        "id": "pick-cold-002",
        "template_id": "pick-route-cold",
        "params": {"pick_id": "PK-5001"},
        "category": "outbound",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-HVA-4421"}},
            {"tool": "wh_get_sku_locations", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "rag_search", "args": {"query": "zone routing"}},
        ],
    },
    {
        "id": "pick-cold-003",
        "template_id": "pick-route-cold",
        "params": {"pick_id": "PK-5005"},
        "category": "outbound",
        "expected_answer": "yes",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "wh_get_sku_locations", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "rag_search", "args": {"query": "cold zone"}},
        ],
    },
    {
        "id": "pick-cold-004",
        "template_id": "pick-route-cold",
        "params": {"pick_id": "PK-5007"},
        "category": "outbound",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5007"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-CTL-9901"}},
            {"tool": "wh_get_sku_locations", "args": {"sku": "SKU-CTL-9901"}},
            {"tool": "rag_search", "args": {"query": "zone routing"}},
        ],
    },
    # damage-impact (4)
    {
        "id": "damage-001",
        "template_id": "damage-impact",
        "params": {"pick_id": "PK-5005"},
        "category": "inventory",
        "expected_answer": "damage",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wms_search_incidents", "args": {"query": "B-08-05"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "B-08-05"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-BK-210"}},
        ],
    },
    {
        "id": "damage-002",
        "template_id": "damage-impact",
        "params": {"pick_id": "PK-5006"},
        "category": "inventory",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5006"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5006"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "B-08-04"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-BKT-3309"}},
        ],
    },
    {
        "id": "damage-003",
        "template_id": "damage-impact",
        "params": {"pick_id": "PK-5002"},
        "category": "inventory",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5002"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-044"}},
            {"tool": "wh_get_location", "args": {"location_id": "C-02-01"}},
        ],
    },
    {
        "id": "damage-004",
        "template_id": "damage-impact",
        "params": {"pick_id": "PK-5001"},
        "category": "inventory",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5001"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "A-12-03"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-HV-081"}},
        ],
    },
    # ship-by-risk (4)
    {
        "id": "ship-risk-001",
        "template_id": "ship-by-risk",
        "params": {"pick_id": "PK-5002"},
        "category": "outbound",
        "expected_answer": "yes",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5002"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-28", "end_date": "2026-08-30"}},
        ],
    },
    {
        "id": "ship-risk-002",
        "template_id": "ship-by-risk",
        "params": {"pick_id": "PK-5003"},
        "category": "outbound",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5003"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-BKT-3309"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-30", "end_date": "2026-09-02"}},
        ],
    },
    {
        "id": "ship-risk-003",
        "template_id": "ship-by-risk",
        "params": {"pick_id": "PK-5005"},
        "category": "outbound",
        "expected_answer": "yes",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5005"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-27", "end_date": "2026-08-30"}},
        ],
    },
    {
        "id": "ship-risk-004",
        "template_id": "ship-by-risk",
        "params": {"pick_id": "PK-5008"},
        "category": "outbound",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5008"}},
            {"tool": "wh_get_warehouse_date", "args": {}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "rag_search", "args": {"query": "ship-by SLA"}},
        ],
    },
    # lot-recall (4)
    {
        "id": "lot-recall-001",
        "template_id": "lot-recall",
        "params": {"lot_id": "LOT-GR-044"},
        "category": "inventory",
        "expected_answer": "PK-5002",
        "expected_tool_calls": [
            {"tool": "wh_find_picks_by_lot", "args": {"lot_id": "LOT-GR-044"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-044"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "rag_search", "args": {"query": "lot traceability recall"}},
        ],
    },
    {
        "id": "lot-recall-002",
        "template_id": "lot-recall",
        "params": {"lot_id": "LOT-BK-210"},
        "category": "inventory",
        "expected_answer": "PK-5005",
        "expected_tool_calls": [
            {"tool": "wh_find_picks_by_lot", "args": {"lot_id": "LOT-BK-210"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-BK-210"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5003"}},
            {"tool": "rag_search", "args": {"query": "traceability"}},
        ],
    },
    {
        "id": "lot-recall-003",
        "template_id": "lot-recall",
        "params": {"lot_id": "LOT-IC-009"},
        "category": "inventory",
        "expected_answer": "PK-5007",
        "expected_tool_calls": [
            {"tool": "wh_find_picks_by_lot", "args": {"lot_id": "LOT-IC-009"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-IC-009"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5007"}},
            {"tool": "rag_search", "args": {"query": "lot traceability"}},
        ],
    },
    {
        "id": "lot-recall-004",
        "template_id": "lot-recall",
        "params": {"lot_id": "LOT-CD-019"},
        "category": "inventory",
        "expected_answer": "PK-5002",
        "expected_tool_calls": [
            {"tool": "wh_find_picks_by_lot", "args": {"lot_id": "LOT-CD-019"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-CD-019"}},
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "rag_search", "args": {"query": "cold chain"}},
        ],
    },
    # equipment-check (4)
    {
        "id": "equip-001",
        "template_id": "equipment-check",
        "params": {"zone": "PICK-FACE"},
        "category": "operations",
        "expected_answer": "down",
        "expected_tool_calls": [
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "PICK-FACE"}},
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "PICK-FACE"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7001"}},
            {"tool": "rag_search", "args": {"query": "equipment assignment"}},
        ],
    },
    {
        "id": "equip-002",
        "template_id": "equipment-check",
        "params": {"zone": "BULK-A"},
        "category": "operations",
        "expected_answer": "available",
        "expected_tool_calls": [
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "BULK-A"}},
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "BULK-A"}},
            {"tool": "wms_get_equipment", "args": {"equipment_id": "FL-01"}},
            {"tool": "rag_search", "args": {"query": "equipment"}},
        ],
    },
    {
        "id": "equip-003",
        "template_id": "equipment-check",
        "params": {"zone": "COLD"},
        "category": "operations",
        "expected_answer": "available",
        "expected_tool_calls": [
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "COLD"}},
            {"tool": "wh_get_replenishment_tasks", "args": {"zone": "COLD"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7003"}},
            {"tool": "rag_search", "args": {"query": "equipment assignment"}},
        ],
    },
    {
        "id": "equip-004",
        "template_id": "equipment-check",
        "params": {"zone": "PICK-FACE"},
        "category": "operations",
        "expected_answer": "FL-02",
        "expected_tool_calls": [
            {"tool": "wms_list_equipment_by_zone", "args": {"zone": "PICK-FACE"}},
            {"tool": "wms_get_equipment", "args": {"equipment_id": "FL-02"}},
            {"tool": "wms_search_incidents", "args": {"query": "FL-02"}},
            {"tool": "rag_search", "args": {"query": "replenishment blocked"}},
        ],
        "difficulty": "hard",
    },
    # cycle-count (4)
    {
        "id": "cycle-001",
        "template_id": "cycle-count",
        "params": {"location_id": "B-08-05"},
        "category": "inventory",
        "expected_answer": "damaged",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "B-08-05"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "B-08-05"}},
            {"tool": "wms_search_incidents", "args": {"query": "B-08-05"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7002"}},
        ],
    },
    {
        "id": "cycle-002",
        "template_id": "cycle-count",
        "params": {"location_id": "A-04-01"},
        "category": "inventory",
        "expected_answer": "stockout",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "A-04-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "A-04-01"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "wms_search_incidents", "args": {"query": "SKU-FST-M8"}},
        ],
    },
    {
        "id": "cycle-003",
        "template_id": "cycle-count",
        "params": {"location_id": "Q-03-01"},
        "category": "inventory",
        "expected_answer": "qc_hold",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "Q-03-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "Q-03-01"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-GR-043"}},
            {"tool": "wms_search_incidents", "args": {"query": "LOT-GR-043"}},
        ],
    },
    {
        "id": "cycle-004",
        "template_id": "cycle-count",
        "params": {"location_id": "R-01-01"},
        "category": "inventory",
        "expected_answer": "receiving",
        "expected_tool_calls": [
            {"tool": "wh_get_location", "args": {"location_id": "R-01-01"}},
            {"tool": "wh_get_bin_contents", "args": {"location_id": "R-01-01"}},
            {"tool": "wh_get_inbound", "args": {"inbound_id": "INB-3004"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7001"}},
        ],
    },
    # cold-chain (4)
    {
        "id": "cold-001",
        "template_id": "cold-chain",
        "params": {"pick_id": "PK-5002"},
        "category": "outbound",
        "expected_answer": "temp_check_passed",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-COLD-110"}},
            {"tool": "wh_get_lot_trace", "args": {"lot_id": "LOT-CD-019"}},
            {"tool": "rag_search", "args": {"query": "cold chain compliance"}},
        ],
    },
    {
        "id": "cold-002",
        "template_id": "cold-chain",
        "params": {"pick_id": "PK-5005"},
        "category": "outbound",
        "expected_answer": "cold_chain",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-GR-7782"}},
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-003"}},
            {"tool": "rag_search", "args": {"query": "cold chain"}},
        ],
    },
    {
        "id": "cold-003",
        "template_id": "cold-chain",
        "params": {"pick_id": "PK-5001"},
        "category": "outbound",
        "expected_answer": "not required",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-HVA-4421"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-FST-M8"}},
            {"tool": "rag_search", "args": {"query": "cold chain"}},
        ],
    },
    {
        "id": "cold-004",
        "template_id": "cold-chain",
        "params": {"pick_id": "PK-5002"},
        "category": "outbound",
        "expected_answer": "WK-002",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5002"}},
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-002"}},
            {"tool": "wms_get_work_order", "args": {"work_order_id": "WO-7003"}},
            {"tool": "rag_search", "args": {"query": "cold chain certification"}},
        ],
    },
    # hazmat-pick (4)
    {
        "id": "hazmat-001",
        "template_id": "hazmat-pick",
        "params": {"pick_id": "PK-5007"},
        "category": "operations",
        "expected_answer": "hazmat",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5007"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-CTL-9901"}},
            {"tool": "wms_get_shift_roster", "args": {"shift_id": "SHIFT-DAY"}},
            {"tool": "rag_search", "args": {"query": "hazmat pick rules"}},
        ],
    },
    {
        "id": "hazmat-002",
        "template_id": "hazmat-pick",
        "params": {"pick_id": "PK-5001"},
        "category": "operations",
        "expected_answer": "safe",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5001"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-HVA-4421"}},
            {"tool": "wms_get_shift_roster", "args": {"shift_id": "SHIFT-DAY"}},
            {"tool": "rag_search", "args": {"query": "hazmat"}},
        ],
    },
    {
        "id": "hazmat-003",
        "template_id": "hazmat-pick",
        "params": {"pick_id": "PK-5007"},
        "category": "operations",
        "expected_answer": "WK-001",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5007"}},
            {"tool": "wms_search_incidents", "args": {"query": "PK-5007 hazmat"}},
            {"tool": "wms_get_shift_roster", "args": {"shift_id": "SHIFT-DAY"}},
            {"tool": "wh_get_worker", "args": {"worker_id": "WK-001"}},
        ],
    },
    {
        "id": "hazmat-004",
        "template_id": "hazmat-pick",
        "params": {"pick_id": "PK-5005"},
        "category": "operations",
        "expected_answer": "safe",
        "expected_tool_calls": [
            {"tool": "wh_get_pick_order", "args": {"pick_id": "PK-5005"}},
            {"tool": "wh_get_sku", "args": {"sku": "SKU-BKT-3309"}},
            {"tool": "wms_get_shift_roster", "args": {"shift_id": "SHIFT-DAY"}},
            {"tool": "rag_search", "args": {"query": "hazmat pick"}},
        ],
    },
]


def main() -> None:
    templates = json.loads((ROOT / "data" / "eval" / "templates.json").read_text())["templates"]
    template_map = {t["id"]: t for t in templates}

    questions = []
    for spec in INSTANCES:
        template = template_map[spec["template_id"]]
        question_text = template["template"]
        for key, value in spec["params"].items():
            question_text = question_text.replace(f"{{{key}}}", str(value))
        questions.append(
            {
                **spec,
                "question": question_text,
                "min_tool_calls": template["min_tool_calls"],
                "difficulty": spec.get("difficulty", "medium"),
                "notes": spec.get("notes", ""),
            }
        )

    assert len(questions) == 60
    for q in questions:
        assert len(q["expected_tool_calls"]) >= 3, q["id"]

    payload = {
        "version": "0.3.0",
        "description": "Warehouse agent eval — 15 templates x 4 instances, 3-4 tool calls each.",
        "questions": questions,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {len(questions)} questions to {OUT}")


if __name__ == "__main__":
    main()
