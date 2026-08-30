# Trace Learning

Experimental project for building a **deep agent** that learns and replays workflows to reduce token usage and improve accuracy.

## Goals

1. **Deep agent** — LangChain / LangGraph ReAct agent with access to mock MCP, RAG, and built-in tools
2. **Eval dataset** — 60 questions with deterministic expected outputs (we control the mocks)
3. **Workflow graph** — Store recurring tool-call patterns so the agent can execute known workflows faster
4. **Trace learning** — Use agent execution traces to populate and refine the workflow graph over time

## Project Structure

```
trace-learning/
├── data/
│   ├── eval/
│   │   ├── questions.json      # 60 eval questions + expected outputs
│   │   └── results/            # Eval run outputs (gitignored)
│   ├── graph/
│   │   └── workflows.json      # Learned / hand-authored workflow graphs
│   └── rag/
│       └── documents.json      # Knowledge base for mock RAG
├── src/trace_learning/
│   ├── agent/                  # Deep agent (LangGraph ReAct)
│   ├── eval/                   # Dataset schema + eval runner
│   ├── graph/                  # Workflow graph schema + store
│   └── mock/
│       ├── mcp/                # Mock MCP filesystem + user directory
│       ├── rag/                # Mock RAG retriever
│       └── tools/              # Built-in tools (calculator, orders, weather)
├── scripts/                    # CLI entry points (via pyproject scripts)
└── tests/
```

## Quick Start

### 1. Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure

```bash
cp .env.example .env
# Add your OPENAI_API_KEY
```

### 3. Run tests (no API key needed)

```bash
pytest
```

### 4. Run the agent

```bash
trace-agent "What is the refund policy?"
# or interactive REPL:
trace-agent
```

### 5. Run evaluation

```bash
trace-eval
trace-eval --id rag-001        # single question
```

## Mock Capabilities

All mock implementations return **deterministic** data so eval expected outputs are knowable.

| Group | Tools | Mock Data |
|-------|-------|-----------|
| **MCP** | `mcp_read_file`, `mcp_search_files`, `mcp_get_user` | Filesystem, user directory |
| **RAG** | `rag_search` | `data/rag/documents.json` |
| **Built-in** | `calculator`, `lookup_order`, `get_weather` | Orders, weather, math |

## Eval Dataset

`data/eval/questions.json` contains **60 questions** in four categories:

| Category | Count | Description |
|----------|-------|-------------|
| `rag` | 15 | Knowledge retrieval from mock docs |
| `mcp` | 15 | Filesystem and user lookups |
| `builtin` | 15 | Calculator, orders, weather |
| `multi_step` | 15 | Questions requiring 2+ tool calls |

Each question includes:

- `expected_answer` — substring the agent response should contain
- `expected_tool_calls` — tools (and args) the agent should invoke
- `difficulty` — easy / medium / hard

Check coverage:

```python
from trace_learning.eval.dataset import EvalDataset
print(EvalDataset.load().coverage_report())
```

## Workflow Graph (Next Phase)

The graph layer (`src/trace_learning/graph/`) stores workflows as directed graphs of tool and LLM nodes. Example workflows live in `data/graph/workflows.json`.

**Planned capabilities** (not yet implemented):

- Match incoming questions to known workflows
- Execute workflow tool sequences directly (skip ReAct reasoning)
- Learn new workflows from successful agent traces
- Measure token savings vs. baseline ReAct

## Roadmap

- [ ] Wire workflow graph into agent execution path
- [ ] Trace capture during agent runs
- [ ] Workflow learning from traces
- [ ] Structured eval scoring (tool-call sequence matching)
- [ ] Embedding-based RAG and workflow matching
- [ ] Real MCP server adapter (replace mock transport)

## Development

```bash
ruff check src tests
pytest -v
```

## License

Experimental — internal use.
