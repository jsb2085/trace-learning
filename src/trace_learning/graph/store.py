"""Persistence layer for workflow graphs."""

from __future__ import annotations

import json
from pathlib import Path

from trace_learning.graph.schema import WorkflowGraph

DEFAULT_GRAPHS_PATH = Path(__file__).resolve().parents[3] / "data" / "graph" / "workflows.json"


class WorkflowGraphStore:
    """Load and query workflow graphs from disk."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or DEFAULT_GRAPHS_PATH
        self._graphs: list[WorkflowGraph] = self._load()

    def _load(self) -> list[WorkflowGraph]:
        with self._path.open() as f:
            raw = json.load(f)
        return [WorkflowGraph.model_validate(g) for g in raw["workflows"]]

    @property
    def graphs(self) -> list[WorkflowGraph]:
        return self._graphs

    def get(self, workflow_id: str) -> WorkflowGraph | None:
        for g in self._graphs:
            if g.id == workflow_id:
                return g
        return None

    def match(self, question: str) -> WorkflowGraph | None:
        """Naive keyword match — replace with embedding/intent classifier later."""
        q = question.lower()
        for graph in self._graphs:
            for pattern in graph.trigger_patterns:
                if pattern.lower() in q:
                    return graph
        return None

    def save(self) -> None:
        payload = {"workflows": [g.model_dump() for g in self._graphs]}
        with self._path.open("w") as f:
            json.dump(payload, f, indent=2)

    def add(self, graph: WorkflowGraph) -> None:
        self._graphs.append(graph)
        self.save()
