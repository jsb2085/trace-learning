"""Warehouse agent — LangGraph ReAct agent for WMS operations."""

from __future__ import annotations

from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from trace_learning.mock.mcp.tools import get_wms_tools
from trace_learning.mock.rag.retriever import get_rag_tool
from trace_learning.mock.tools.registry import get_utility_tools
from trace_learning.mock.wh.tools import get_wh_tools


class WarehouseAgent:
    """Warehouse operations agent with floor tools, WMS MCP, RAG SOPs, and utilities."""

    def __init__(self, graph: Any, tools: list[BaseTool]) -> None:
        self._graph = graph
        self._tools = tools

    @property
    def tools(self) -> list[BaseTool]:
        return self._tools

    def invoke(self, question: str) -> dict[str, Any]:
        return self._graph.invoke({"messages": [HumanMessage(content=question)]})

    async def ainvoke(self, question: str) -> dict[str, Any]:
        return await self._graph.ainvoke({"messages": [HumanMessage(content=question)]})

    def ask(self, question: str) -> str:
        """Ask the agent a question and return the final text answer."""
        response = self.invoke(question)
        return response["messages"][-1].content


def create_warehouse_agent(
    llm: BaseChatModel | None = None,
    *,
    include_wh: bool = True,
    include_wms: bool = True,
    include_rag: bool = True,
    include_utils: bool = True,
) -> WarehouseAgent:
    """Build the warehouse agent with floor, WMS, RAG, and utility tools."""
    tools: list[BaseTool] = []
    if include_wh:
        tools.extend(get_wh_tools())
    if include_wms:
        tools.extend(get_wms_tools())
    if include_rag:
        tools.append(get_rag_tool())
    if include_utils:
        tools.extend(get_utility_tools())

    model = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
    graph = create_react_agent(model, tools)
    return WarehouseAgent(graph, tools)


# Backward-compatible aliases
DeepAgent = WarehouseAgent
create_deep_agent = create_warehouse_agent


def ask(question: str, *, llm: BaseChatModel | None = None) -> str:
    """One-shot helper: create an agent, ask a question, return the answer."""
    return create_warehouse_agent(llm=llm).ask(question)
