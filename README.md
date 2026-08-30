# Trace Learning — Warehouse Agent

Experimental **warehouse operations agent** that learns and replays multi-tool workflows to reduce token usage and improve pick/inventory accuracy.

## What it does

The agent manages **WH-EAST**, a mock warehouse with outbound picks, inbound receipts, bin locations, lot traceability, workers, and WMS incidents. Every eval question requires **3–4 tool calls** across floor tools, WMS MCP, RAG SOPs, and utilities.

## Project Structure

```
trace-learning/
├── data/
│   ├── mock/                   # Warehouse domain data
│   │   ├── warehouse.json      # Reference date, warehouse ID
│   │   ├── pick_orders.json    # Outbound picks
│   │   ├── skus.json           # SKU master
│   │   ├── locations.json      # Bins, zones, contents
│   │   ├── lots.json           # Lot event timelines
│   │   ├── inbound.json        # ASNs / receipts
│   │   ├── workers.json        # Pickers, replen tasks
│   │   └── wms.json            # Work orders, incidents, equipment
│   ├── eval/
│   │   ├── templates.json      # 15 parameterized question templates
│   │   └── questions.json      # 60 instances (4 tools each)
│   ├── graph/workflows.json
│   └── rag/documents.json      # Warehouse SOPs
├── src/trace_learning/
│   ├── agent/warehouse_agent.py
│   ├── mock/wh/                # Floor tools (wh_*)
│   ├── mock/mcp/               # WMS tools (wms_*)
│   └── mock/rag/               # SOP search
└── scripts/generate_eval_dataset.py
```

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add OPENAI_API_KEY

python3 -m pytest -v
trace-agent "Which pick orders are overdue as of 2026-08-30?"
trace-eval --id overdue-picks-001
```

## Tool Groups

| Group | Prefix | Examples |
|-------|--------|----------|
| **Floor** | `wh_*` | `wh_get_pick_order`, `wh_find_overdue_picks`, `wh_get_lot_trace`, `wh_get_bin_contents` |
| **WMS (MCP)** | `wms_*` | `wms_search_incidents`, `wms_get_work_order`, `wms_list_equipment_by_zone` |
| **RAG** | `rag_search` | Overdue pick rules, cold chain SOP, hazmat rules, putaway policy |
| **Utils** | — | `days_between`, `calculator` |

## Eval Design

**15 templates × 4 input variants = 60 questions.** Each instance declares **4 expected tool calls**.

| Template | Example |
|----------|---------|
| `Which pick orders are overdue as of {as_of_date}?` | RAG → date → overdue query → worker |
| `What happened to SKU {sku} in the warehouse?` | SKU → lot trace → open picks → SOP |
| `Why is pick order {pick_id} delayed?` | Pick → lot → incidents → worker assignments |
| `Can pick order {pick_id} be picked safely on the current shift?` | Pick → hazmat SKU → shift roster → SOP |

Regenerate after editing instance specs:

```bash
python3 scripts/generate_eval_dataset.py
```

Check coverage:

```python
from trace_learning.eval.dataset import EvalDataset
print(EvalDataset.load().coverage_report())
```

## Roadmap

- [ ] Wire workflow graph into warehouse agent
- [ ] Trace capture and workflow learning
- [ ] Structured tool-call sequence scoring
- [ ] Runtime template param sampling

## Development

```bash
python3 -m pytest -v
```
