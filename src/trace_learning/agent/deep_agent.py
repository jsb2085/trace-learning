"""Deep agent orchestrator — wires mock MCP, RAG, and tools into a LangGraph agent."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from trace_learning.mock.mcp.tools import get_mcp_tools
from trace_learning.mock.ops.tools import get_ops_tools
from trace_learning.mock.rag.retriever import get_rag_tool
from trace_learning.mock.tools.registry import get_builtin_tools


class DeepAgent:
    """Wrapper around a LangGraph ReAct agent with all mock capabilities."""

    def __init__(self, graph: Any, tools: list[BaseTool]) -> None:
        self._graph = graph
        self._tools = tools

    @property
    def tools(self) -> list[BaseTool]:
        return self._tools

    def invoke(self, question: str) -> dict[str, Any]:
        """Run the agent on a single question."""
        return self._graph.invoke({"messages": [HumanMessage(content=question)]})

    async def ainvoke(self, question: str) -> dict[str, Any]:
        """Async variant for batch evaluation."""
        return await self._graph.ainvoke({"messages": [HumanMessage(content=question)]})


def create_deep_agent(
    llm: BaseChatModel | None = None,
    *,
    include_ops: bool = True,
    include_mcp: bool = True,
    include_rag: bool = True,
    include_builtin: bool = True,
) -> DeepAgent:
    """Build a deep agent with the requested mock tool groups."""
    tools: list[BaseTool] = []
    if include_ops:
        tools.extend(get_ops_tools())
    if include_mcp:
        tools.extend(get_mcp_tools())
    if include_rag:
        tools.append(get_rag_tool())
    if include_builtin:
        tools.extend(get_builtin_tools())

    model = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
    graph = create_react_agent(model, tools)
    return DeepAgent(graph, tools)
