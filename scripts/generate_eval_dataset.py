#!/usr/bin/env python3
"""Generate data/eval/questions.json from templates and instance specs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "eval" / "questions.json"

INSTANCES: list[dict] = [
    # late-orders (4)
    {
        "id": "late-orders-001",
        "template_id": "late-orders",
        "params": {"as_of_date": "2026-08-30"},
        "category": "fulfillment",
        "expected_answer": "ORD-2001",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "ops_find_late_orders", "args": {"as_of_date": "2026-08-30"}},
        ],
        "difficulty": "medium",
        "notes": "Also late: ORD-2002, ORD-2005, ORD-2008",
    },
    {
        "id": "late-orders-002",
        "template_id": "late-orders",
        "params": {"as_of_date": "2026-08-29"},
        "category": "fulfillment",
        "expected_answer": "ORD-2008",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "late order definition"}},
            {"tool": "ops_find_late_orders", "args": {"as_of_date": "2026-08-29"}},
        ],
        "difficulty": "medium",
        "notes": "Also late: ORD-2001, ORD-2005",
    },
    {
        "id": "late-orders-003",
        "template_id": "late-orders",
        "params": {"as_of_date": "2026-08-28"},
        "category": "fulfillment",
        "expected_answer": "ORD-2008",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "ops_find_late_orders", "args": {"as_of_date": "2026-08-28"}},
        ],
        "difficulty": "hard",
        "notes": "Also late: ORD-2005 only",
    },
    {
        "id": "late-orders-004",
        "template_id": "late-orders",
        "params": {"as_of_date": "2026-09-01"},
        "category": "fulfillment",
        "expected_answer": "ORD-2007",
        "expected_tool_calls": [
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "ops_find_late_orders", "args": {"as_of_date": "2026-09-01"}},
        ],
        "difficulty": "hard",
        "notes": "ORD-2007 on_hold also late; plus ORD-2001/2002/2005/2008",
    },
    # part-history (4)
    {
        "id": "part-history-001",
        "template_id": "part-history",
        "params": {"part_number": "PN-7782"},
        "category": "parts_trace",
        "expected_answer": "qc_failed",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-7782"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-7782"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "part-history-002",
        "template_id": "part-history",
        "params": {"part_number": "PN-9901"},
        "category": "parts_trace",
        "expected_answer": "customs hold",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-9901"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-9901"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "part-history-003",
        "template_id": "part-history",
        "params": {"part_number": "PN-4421"},
        "category": "parts_trace",
        "expected_answer": "qc_passed",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-4421"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-4421"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "part-history-004",
        "template_id": "part-history",
        "params": {"part_number": "PN-3309"},
        "category": "parts_trace",
        "expected_answer": "Missed transfer scan",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-3309"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-3309"}},
        ],
        "difficulty": "medium",
    },
    # order-delay-reason (4)
    {
        "id": "order-delay-001",
        "template_id": "order-delay-reason",
        "params": {"order_id": "ORD-2002"},
        "category": "fulfillment",
        "expected_answer": "Weather delay",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2002"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-7782"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "order-delay-002",
        "template_id": "order-delay-reason",
        "params": {"order_id": "ORD-2008"},
        "category": "fulfillment",
        "expected_answer": "Customs hold",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2008"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2008"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-9901"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "order-delay-003",
        "template_id": "order-delay-reason",
        "params": {"order_id": "ORD-2005"},
        "category": "fulfillment",
        "expected_answer": "Missed transfer scan",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2005"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2005"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-3309"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "order-delay-004",
        "template_id": "order-delay-reason",
        "params": {"order_id": "ORD-2001"},
        "category": "fulfillment",
        "expected_answer": "in_transit",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2001"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-4421"}},
        ],
        "difficulty": "medium",
    },
    # refund-eligibility (4)
    {
        "id": "refund-001",
        "template_id": "refund-eligibility",
        "params": {"order_id": "ORD-2003"},
        "category": "policy",
        "expected_answer": "eligible",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2003"}},
            {"tool": "rag_search", "args": {"query": "refund policy"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "refund-002",
        "template_id": "refund-eligibility",
        "params": {"order_id": "ORD-2004"},
        "category": "policy",
        "expected_answer": "delivered",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2004"}},
            {"tool": "rag_search", "args": {"query": "refund policy"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "refund-003",
        "template_id": "refund-eligibility",
        "params": {"order_id": "ORD-2001"},
        "category": "policy",
        "expected_answer": "late",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
            {"tool": "rag_search", "args": {"query": "refund policy late delivery"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "refund-004",
        "template_id": "refund-eligibility",
        "params": {"order_id": "ORD-2006"},
        "category": "policy",
        "expected_answer": "eligible",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2006"}},
            {"tool": "rag_search", "args": {"query": "refund policy"}},
        ],
        "difficulty": "easy",
    },
    # shipment-eta (4)
    {
        "id": "shipment-eta-001",
        "template_id": "shipment-eta",
        "params": {"order_id": "ORD-2001"},
        "category": "fulfillment",
        "expected_answer": "2026-08-31",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2001"}},
            {"tool": "rag_search", "args": {"query": "shipping SLA"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "shipment-eta-002",
        "template_id": "shipment-eta",
        "params": {"order_id": "ORD-2002"},
        "category": "fulfillment",
        "expected_answer": "2026-08-30",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2002"}},
            {"tool": "rag_search", "args": {"query": "express shipping"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "shipment-eta-003",
        "template_id": "shipment-eta",
        "params": {"order_id": "ORD-2005"},
        "category": "fulfillment",
        "expected_answer": "2026-09-01",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2005"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2005"}},
            {"tool": "rag_search", "args": {"query": "shipping SLA"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "shipment-eta-004",
        "template_id": "shipment-eta",
        "params": {"order_id": "ORD-2008"},
        "category": "fulfillment",
        "expected_answer": "2026-08-29",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2008"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2008"}},
            {"tool": "rag_search", "args": {"query": "shipping SLA"}},
        ],
        "difficulty": "hard",
    },
    # qc-on-order (4)
    {
        "id": "qc-order-001",
        "template_id": "qc-on-order",
        "params": {"order_id": "ORD-2002"},
        "category": "parts_trace",
        "expected_answer": "PN-7782",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-7782"}},
            {"tool": "rag_search", "args": {"query": "QC failure"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "qc-order-002",
        "template_id": "qc-on-order",
        "params": {"order_id": "ORD-2008"},
        "category": "parts_trace",
        "expected_answer": "PN-9901",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2008"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-9901"}},
            {"tool": "rag_search", "args": {"query": "QC failure"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "qc-order-003",
        "template_id": "qc-on-order",
        "params": {"order_id": "ORD-2005"},
        "category": "parts_trace",
        "expected_answer": "PN-7782",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2005"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-7782"}},
            {"tool": "rag_search", "args": {"query": "QC failure"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "qc-order-004",
        "template_id": "qc-on-order",
        "params": {"order_id": "ORD-2004"},
        "category": "parts_trace",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2004"}},
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-4421"}},
            {"tool": "rag_search", "args": {"query": "QC failure"}},
        ],
        "difficulty": "medium",
    },
    # inventory-fulfillment (4)
    {
        "id": "inventory-001",
        "template_id": "inventory-fulfillment",
        "params": {"order_id": "ORD-2003"},
        "category": "policy",
        "expected_answer": "cannot",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2003"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-1100"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "inventory-002",
        "template_id": "inventory-fulfillment",
        "params": {"order_id": "ORD-2006"},
        "category": "policy",
        "expected_answer": "cannot",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2006"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-1100"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "inventory-003",
        "template_id": "inventory-fulfillment",
        "params": {"order_id": "ORD-2001"},
        "category": "policy",
        "expected_answer": "can",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-4421"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "inventory-004",
        "template_id": "inventory-fulfillment",
        "params": {"order_id": "ORD-2007"},
        "category": "policy",
        "expected_answer": "can",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2007"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-3309"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "medium",
    },
    # ticket-owner (4)
    {
        "id": "ticket-owner-001",
        "template_id": "ticket-owner",
        "params": {"ticket_id": "TKT-5001"},
        "category": "support",
        "expected_answer": "Carol Wu",
        "expected_tool_calls": [
            {"tool": "mcp_get_ticket", "args": {"ticket_id": "TKT-5001"}},
            {"tool": "mcp_get_user", "args": {"user_id": "u-003"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "ticket-owner-002",
        "template_id": "ticket-owner",
        "params": {"ticket_id": "TKT-5002"},
        "category": "support",
        "expected_answer": "Alice Chen",
        "expected_tool_calls": [
            {"tool": "mcp_get_ticket", "args": {"ticket_id": "TKT-5002"}},
            {"tool": "mcp_get_user", "args": {"user_id": "u-001"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "ticket-owner-003",
        "template_id": "ticket-owner",
        "params": {"ticket_id": "TKT-5004"},
        "category": "support",
        "expected_answer": "Alice Chen",
        "expected_tool_calls": [
            {"tool": "mcp_get_ticket", "args": {"ticket_id": "TKT-5004"}},
            {"tool": "mcp_get_user", "args": {"user_id": "u-001"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "ticket-owner-004",
        "template_id": "ticket-owner",
        "params": {"ticket_id": "TKT-5005"},
        "category": "support",
        "expected_answer": "Carol Wu",
        "expected_tool_calls": [
            {"tool": "mcp_get_ticket", "args": {"ticket_id": "TKT-5005"}},
            {"tool": "mcp_get_user", "args": {"user_id": "u-003"}},
        ],
        "difficulty": "easy",
    },
    # customer-open-orders (4)
    {
        "id": "customer-orders-001",
        "template_id": "customer-open-orders",
        "params": {"customer_id": "C-100"},
        "category": "fulfillment",
        "expected_answer": "ORD-2003",
        "expected_tool_calls": [
            {"tool": "ops_query_orders", "args": {"customer_id": "C-100"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
        ],
        "difficulty": "medium",
        "notes": "C-100 also has ORD-2001 in_transit",
    },
    {
        "id": "customer-orders-002",
        "template_id": "customer-open-orders",
        "params": {"customer_id": "C-101"},
        "category": "fulfillment",
        "expected_answer": "ORD-2006",
        "expected_tool_calls": [
            {"tool": "ops_query_orders", "args": {"customer_id": "C-101"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "customer-orders-003",
        "template_id": "customer-open-orders",
        "params": {"customer_id": "C-103"},
        "category": "fulfillment",
        "expected_answer": "ORD-2005",
        "expected_tool_calls": [
            {"tool": "ops_query_orders", "args": {"customer_id": "C-103"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2005"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "customer-orders-004",
        "template_id": "customer-open-orders",
        "params": {"customer_id": "C-105"},
        "category": "fulfillment",
        "expected_answer": "ORD-2008",
        "expected_tool_calls": [
            {"tool": "ops_query_orders", "args": {"customer_id": "C-105"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2008"}},
        ],
        "difficulty": "easy",
    },
    # orders-with-part (4)
    {
        "id": "orders-part-001",
        "template_id": "orders-with-part",
        "params": {"part_number": "PN-7782"},
        "category": "parts_trace",
        "expected_answer": "ORD-2002",
        "expected_tool_calls": [
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-7782"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "orders-part-002",
        "template_id": "orders-with-part",
        "params": {"part_number": "PN-4421"},
        "category": "parts_trace",
        "expected_answer": "ORD-2001",
        "expected_tool_calls": [
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-4421"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "orders-part-003",
        "template_id": "orders-with-part",
        "params": {"part_number": "PN-1100"},
        "category": "parts_trace",
        "expected_answer": "ORD-2003",
        "expected_tool_calls": [
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-1100"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2006"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "orders-part-004",
        "template_id": "orders-with-part",
        "params": {"part_number": "PN-3309"},
        "category": "parts_trace",
        "expected_answer": "ORD-2005",
        "expected_tool_calls": [
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-3309"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2007"}},
        ],
        "difficulty": "medium",
    },
    # days-late (4)
    {
        "id": "days-late-001",
        "template_id": "days-late",
        "params": {"order_id": "ORD-2001", "as_of_date": "2026-08-30"},
        "category": "fulfillment",
        "expected_answer": "2",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2001"}},
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-28", "end_date": "2026-08-30"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "days-late-002",
        "template_id": "days-late",
        "params": {"order_id": "ORD-2005", "as_of_date": "2026-08-30"},
        "category": "fulfillment",
        "expected_answer": "3",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2005"}},
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-27", "end_date": "2026-08-30"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "days-late-003",
        "template_id": "days-late",
        "params": {"order_id": "ORD-2008", "as_of_date": "2026-08-30"},
        "category": "fulfillment",
        "expected_answer": "4",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2008"}},
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-26", "end_date": "2026-08-30"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "days-late-004",
        "template_id": "days-late",
        "params": {"order_id": "ORD-2002", "as_of_date": "2026-08-30"},
        "category": "fulfillment",
        "expected_answer": "1",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
            {"tool": "rag_search", "args": {"query": "late order"}},
            {"tool": "days_between", "args": {"start_date": "2026-08-29", "end_date": "2026-08-30"}},
        ],
        "difficulty": "medium",
    },
    # restock-check (4)
    {
        "id": "restock-001",
        "template_id": "restock-check",
        "params": {"part_number": "PN-1100"},
        "category": "policy",
        "expected_answer": "2026-09-01",
        "expected_tool_calls": [
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-1100"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-1100"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "restock-002",
        "template_id": "restock-check",
        "params": {"part_number": "PN-7782"},
        "category": "policy",
        "expected_answer": "2026-09-05",
        "expected_tool_calls": [
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-7782"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-7782"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "restock-003",
        "template_id": "restock-check",
        "params": {"part_number": "PN-4421"},
        "category": "policy",
        "expected_answer": "2026-09-10",
        "expected_tool_calls": [
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-4421"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-4421"}},
        ],
        "difficulty": "easy",
    },
    {
        "id": "restock-004",
        "template_id": "restock-check",
        "params": {"part_number": "PN-9901"},
        "category": "policy",
        "expected_answer": "2026-09-20",
        "expected_tool_calls": [
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-9901"}},
            {"tool": "ops_find_orders_by_part", "args": {"part_number": "PN-9901"}},
        ],
        "difficulty": "easy",
    },
    # escalation-for-order (4)
    {
        "id": "escalation-001",
        "template_id": "escalation-for-order",
        "params": {"order_id": "ORD-2001"},
        "category": "support",
        "expected_answer": "TKT-5001",
        "expected_tool_calls": [
            {"tool": "mcp_search_tickets", "args": {"query": "ORD-2001"}},
            {"tool": "rag_search", "args": {"query": "escalation matrix"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "escalation-002",
        "template_id": "escalation-for-order",
        "params": {"order_id": "ORD-2008"},
        "category": "support",
        "expected_answer": "TKT-5004",
        "expected_tool_calls": [
            {"tool": "mcp_search_tickets", "args": {"query": "ORD-2008"}},
            {"tool": "rag_search", "args": {"query": "escalation"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "escalation-003",
        "template_id": "escalation-for-order",
        "params": {"order_id": "ORD-2004"},
        "category": "support",
        "expected_answer": "resolved",
        "expected_tool_calls": [
            {"tool": "mcp_search_tickets", "args": {"query": "ORD-2004"}},
            {"tool": "rag_search", "args": {"query": "escalation"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "escalation-004",
        "template_id": "escalation-for-order",
        "params": {"order_id": "ORD-2003"},
        "category": "support",
        "expected_answer": "no",
        "expected_tool_calls": [
            {"tool": "mcp_search_tickets", "args": {"query": "ORD-2003"}},
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2003"}},
        ],
        "difficulty": "easy",
    },
    # part-delay-cause (4)
    {
        "id": "part-delay-001",
        "template_id": "part-delay-cause",
        "params": {"part_number": "PN-7782"},
        "category": "parts_trace",
        "expected_answer": "qc_failed",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-7782"}},
            {"tool": "rag_search", "args": {"query": "part traceability"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "part-delay-002",
        "template_id": "part-delay-cause",
        "params": {"part_number": "PN-3309"},
        "category": "parts_trace",
        "expected_answer": "Missed transfer scan",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-3309"}},
            {"tool": "rag_search", "args": {"query": "part traceability delays"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "part-delay-003",
        "template_id": "part-delay-cause",
        "params": {"part_number": "PN-9901"},
        "category": "parts_trace",
        "expected_answer": "Customs hold",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-9901"}},
            {"tool": "rag_search", "args": {"query": "part traceability"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "part-delay-004",
        "template_id": "part-delay-cause",
        "params": {"part_number": "PN-4421"},
        "category": "parts_trace",
        "expected_answer": "no delay",
        "expected_tool_calls": [
            {"tool": "ops_get_part_history", "args": {"part_number": "PN-4421"}},
            {"tool": "rag_search", "args": {"query": "part traceability"}},
        ],
        "difficulty": "easy",
    },
    # fulfillment-blocker (4)
    {
        "id": "blocker-001",
        "template_id": "fulfillment-blocker",
        "params": {"order_id": "ORD-2007"},
        "category": "support",
        "expected_answer": "payment_verification",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2007"}},
            {"tool": "rag_search", "args": {"query": "order hold policy"}},
        ],
        "difficulty": "medium",
    },
    {
        "id": "blocker-002",
        "template_id": "fulfillment-blocker",
        "params": {"order_id": "ORD-2003"},
        "category": "support",
        "expected_answer": "inventory",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2003"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-1100"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "blocker-003",
        "template_id": "fulfillment-blocker",
        "params": {"order_id": "ORD-2002"},
        "category": "support",
        "expected_answer": "Weather delay",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2002"}},
            {"tool": "ops_get_shipment", "args": {"order_id": "ORD-2002"}},
            {"tool": "rag_search", "args": {"query": "shipping SLA carrier delays"}},
        ],
        "difficulty": "hard",
    },
    {
        "id": "blocker-004",
        "template_id": "fulfillment-blocker",
        "params": {"order_id": "ORD-2006"},
        "category": "support",
        "expected_answer": "inventory",
        "expected_tool_calls": [
            {"tool": "ops_get_order", "args": {"order_id": "ORD-2006"}},
            {"tool": "ops_get_inventory", "args": {"part_number": "PN-1100"}},
            {"tool": "rag_search", "args": {"query": "inventory allocation"}},
        ],
        "difficulty": "hard",
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
            }
        )

    payload = {
        "version": "0.2.0",
        "description": "60 parameterized multi-tool eval instances (15 templates x 4 inputs each).",
        "questions": questions,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {len(questions)} questions to {OUT}")


if __name__ == "__main__":
    main()
