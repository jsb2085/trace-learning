"""Warehouse agent powered by LangChain Deep Agents."""

from __future__ import annotations

import os
from typing import Any

from deepagents import create_deep_agent as build_langchain_deep_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from trace_learning.mock.mcp.tools import get_wms_tools
from trace_learning.mock.rag.retriever import get_rag_tool
from trace_learning.mock.tools.registry import get_utility_tools
from trace_learning.mock.wh.tools import get_wh_tools

WAREHOUSE_SYSTEM_PROMPT = """You are a warehouse operations agent for WH-EAST.

Answer questions by calling the warehouse tools provided to you:
- wh_* — floor operations: pick orders, SKUs, bin locations, lot trace, workers, inbound
- wms_* — WMS: incidents, work orders, equipment, shift roster
- rag_search — warehouse SOPs and policies (overdue picks, cold chain, hazmat, putaway)
- days_between, calculator — date and quantity math

Use multiple tools when needed. Look up policies before applying business rules.
Give concise, factual answers grounded in tool results."""


class WarehouseAgent:
    """Warehouse operations agent using LangChain Deep Agents."""

    def __init__(self, agent: Any, tools: list[BaseTool]) -> None:
        self._agent = agent
        self._tools = tools

    @property
    def tools(self) -> list[BaseTool]:
        return self._tools

    def invoke(self, question: str) -> dict[str, Any]:
        return self._agent.invoke({"messages": [HumanMessage(content=question)]})

    async def ainvoke(self, question: str) -> dict[str, Any]:
        return await self._agent.ainvoke({"messages": [HumanMessage(content=question)]})

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
    system_prompt: str = WAREHOUSE_SYSTEM_PROMPT,
) -> WarehouseAgent:
    """Build a warehouse agent via LangChain's create_deep_agent."""
    tools: list[BaseTool] = []
    if include_wh:
        tools.extend(get_wh_tools())
    if include_wms:
        tools.extend(get_wms_tools())
    if include_rag:
        tools.append(get_rag_tool())
    if include_utils:
        tools.extend(get_utility_tools())

    model: BaseChatModel | str = llm or ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )

    agent = build_langchain_deep_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )
    return WarehouseAgent(agent, tools)


def ask(question: str, *, llm: BaseChatModel | None = None) -> str:
    """One-shot helper: create an agent, ask a question, return the answer."""
    return create_warehouse_agent(llm=llm).ask(question)
