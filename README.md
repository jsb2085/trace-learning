# Trace Learning — Warehouse Agent

Ask a warehouse operations agent questions about **WH-EAST**. The agent is built with [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview) (`create_deep_agent`) — planning, context management, and your warehouse tools.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add your OPENAI_API_KEY
```

## Ask a question

**CLI — single question:**

```bash
trace-agent "Which pick orders are overdue as of 2026-08-30?"
```

**CLI — interactive REPL:**

```bash
trace-agent
```

**Python:**

```python
from trace_learning.agent import ask

print(ask("What happened to SKU SKU-GR-7782 in the warehouse?"))
```

Or with more control:

```python
from trace_learning.agent import create_warehouse_agent

agent = create_warehouse_agent()
answer = agent.ask("Why is pick order PK-5002 delayed?")
print(answer)
```

## What the agent can access

| Group | Tools | Purpose |
|-------|-------|---------|
| Floor | `wh_*` | Pick orders, SKUs, bins, lots, workers, inbound |
| WMS | `wms_*` | Incidents, work orders, equipment, shift roster |
| RAG | `rag_search` | Warehouse SOPs (overdue picks, cold chain, hazmat, etc.) |
| Utils | `days_between`, `calculator` | Date and quantity math |

All mock data lives in `data/mock/` with a fixed reference date (`2026-08-30`) so answers are deterministic.

## Project layout

```
trace-learning/
├── data/mock/          # Warehouse mock data
├── data/rag/           # SOP documents
├── data/eval/          # Eval dataset (for later benchmarking)
└── src/trace_learning/
    ├── agent/          # WarehouseAgent + ask()
    └── mock/           # wh_*, wms_*, rag tools
```

## Tests

```bash
python3 -m pytest -v
```

## Later (not built yet)

- Workflow graph for replaying learned tool sequences
- Eval runner scoring against the 60-question dataset
