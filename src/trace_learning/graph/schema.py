"""Pydantic models for the workflow graph.

The graph captures recurring tool-call sequences so the agent can replay
known workflows instead of re-reasoning from scratch every time.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    START = "start"
    TOOL = "tool"
    LLM = "llm"
    END = "end"


class WorkflowNode(BaseModel):
    id: str
    type: NodeType
    label: str
    tool_name: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowEdge(BaseModel):
    source: str
    target: str
    condition: str | None = None


class WorkflowGraph(BaseModel):
    """A named workflow the agent can match and execute."""

    id: str
    name: str
    description: str
    trigger_patterns: list[str] = Field(
        description="Question patterns/intents that activate this workflow"
    )
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]
    expected_tools: list[str] = Field(
        default_factory=list,
        description="Ordered tool names this workflow should invoke",
    )

    def tool_sequence(self) -> list[str]:
        """Return the ordered list of tool nodes in this workflow."""
        tool_nodes = [n for n in self.nodes if n.type == NodeType.TOOL]
        return [n.tool_name for n in tool_nodes if n.tool_name]
