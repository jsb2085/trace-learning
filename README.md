# Trace Learning

Experimental project for building a **deep agent** that learns and replays multi-tool workflows to reduce token usage and improve accuracy.

## Goals

1. **Deep agent** — LangGraph ReAct agent combining ops tools, MCP tickets/users, RAG policies, and utilities
2. **Parameterized eval** — 60 question instances from 15 reusable templates with varying inputs
3. **Workflow graph** — Capture multi-step tool patterns (e.g. policy lookup → ops query → synthesis)
4. **Trace learning** — Learn workflows from agent traces to skip re-reasoning on repeat patterns

## Project Structure

```
trace-learning/
├── data/
│   ├── mock/                   # Domain data (orders, parts, shipments, inventory, tickets)
│   ├── eval/
│   │   ├── templates.json      # 15 reusable question templates
│   │   ├── questions.json      # 60 instances (template + params + expected tools)
│   │   └── results/
│   ├── graph/workflows.json
│   └── rag/documents.json      # Policy docs (SLA, refunds, QC, holds)
├── src/trace_learning/
│   ├── agent/
│   ├── eval/
│   ├── graph/
│   └── mock/
│       ├── data/               # JSON loaders
│       ├── ops/                # Orders, parts, shipments, inventory
│       ├── mcp/                # Tickets + user directory
│       ├── rag/
│       └── tools/              # days_between, calculator
├── scripts/generate_eval_dataset.py
└── tests/
```

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add OPENAI_API_KEY

python3 -m pytest -v
trace-agent "What orders are late as of 2026-08-30?"
trace-eval --id late-orders-001
```

## Mock Capabilities

All data is deterministic under a fixed business date (`2026-08-30`).

| Group | Tools | Purpose |
|-------|-------|---------|
| **Ops** | `ops_query_orders`, `ops_get_order`, `ops_get_part_history`, `ops_get_shipment`, `ops_get_inventory`, `ops_find_orders_by_part`, `ops_find_late_orders`, `ops_get_business_date` | Fulfillment domain |
| **MCP** | `mcp_get_ticket`, `mcp_search_tickets`, `mcp_get_user` | Support tickets + owners |
| **RAG** | `rag_search` | Policy docs (late orders, refunds, QC, inventory) |
| **Utils** | `days_between`, `calculator` | Date math for SLA questions |

## Eval Dataset Design

Questions are **not** one-shot RAG or MCP lookups. Each instance requires **2+ tools** across groups.

### Templates (reusable, parameterized)

Examples from `data/eval/templates.json`:

| Template | Example instance |
|----------|------------------|
| `What orders are late as of {as_of_date}?` | `2026-08-30` → ORD-2001, ORD-2002, ORD-2005, ORD-2008 |
| `What happened to part {part_number}?` | `PN-7782` → QC failure, rework, carrier delay |
| `Why is order {order_id} delayed?` | `ORD-2008` → customs hold + failed delivery |
| `What is blocking fulfillment of order {order_id}?` | `ORD-2003` → PN-1100 stockout |

15 templates × 4 input variants = **60 instances**.

### Categories

| Category | Count | Example workflow |
|----------|-------|------------------|
| `fulfillment` | 20 | RAG late policy → `ops_find_late_orders` |
| `parts_trace` | 16 | `ops_get_part_history` → `ops_find_orders_by_part` |
| `policy` | 12 | `ops_get_order` → `rag_search` refund rules |
| `support` | 12 | `mcp_search_tickets` → `mcp_get_user` |

### Regenerating instances

Edit `scripts/generate_eval_dataset.py` instance specs, then:

```bash
python3 scripts/generate_eval_dataset.py
```

## Workflow Graph (Next Phase)

Example workflows in `data/graph/workflows.json` mirror eval templates:

- **Late Order Identification** — `rag_search` → `ops_find_late_orders`
- **Part History Investigation** — `ops_get_part_history` → `ops_find_orders_by_part`
- **Order Delay Root Cause** — order → shipment → part events

## Roadmap

- [ ] Wire workflow graph into agent execution path
- [ ] Trace capture during agent runs
- [ ] Structured eval: tool-call sequence matching (not just answer substring)
- [ ] Template sampling for eval (randomize params at runtime)
- [ ] Real MCP server adapter

## Development

```bash
python3 -m pytest -v
```
