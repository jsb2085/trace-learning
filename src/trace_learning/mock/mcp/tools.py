"""Mock MCP tool definitions.

MCP exposes tickets, users, and supplier communications — systems the agent
must combine with ops tools and RAG policy lookup.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from trace_learning.mock.data.loader import load_tickets


class GetUserInput(BaseModel):
    user_id: str = Field(description="User identifier, e.g. u-001")


class GetTicketInput(BaseModel):
    ticket_id: str = Field(description="Ticket identifier, e.g. TKT-5001")


class SearchTicketsInput(BaseModel):
    query: str = Field(description="Search term matched against subject, notes, order, or part")


MOCK_USERS: dict[str, dict[str, str]] = {
    "u-001": {"name": "Alice Chen", "team": "platform", "role": "engineer"},
    "u-002": {"name": "Bob Rivera", "team": "support", "role": "analyst"},
    "u-003": {"name": "Carol Wu", "team": "fulfillment", "role": "manager"},
}


def _get_user(user_id: str) -> dict[str, Any]:
    user = MOCK_USERS.get(user_id)
    if user is None:
        return {"error": f"User not found: {user_id}"}
    return {"user_id": user_id, **user}


def _get_ticket(ticket_id: str) -> dict[str, Any]:
    tid = ticket_id.upper()
    for ticket in load_tickets()["tickets"]:
        if ticket["ticket_id"] == tid:
            return ticket
    return {"error": f"Ticket not found: {ticket_id}"}


def _search_tickets(query: str) -> list[dict[str, Any]]:
    q = query.lower()
    results: list[dict[str, Any]] = []
    for ticket in load_tickets()["tickets"]:
        blob = " ".join(
            str(ticket.get(k, ""))
            for k in ("subject", "notes", "related_order_id", "related_part_number", "ticket_id")
        ).lower()
        if q in blob:
            results.append(ticket)
    return results


MOCK_MCP_TOOLS = [
    StructuredTool.from_function(
        func=_get_ticket,
        name="mcp_get_ticket",
        description="Fetch a support or escalation ticket by ID.",
        args_schema=GetTicketInput,
    ),
    StructuredTool.from_function(
        func=_search_tickets,
        name="mcp_search_tickets",
        description="Search tickets by keyword across subject, notes, order, and part fields.",
        args_schema=SearchTicketsInput,
    ),
    StructuredTool.from_function(
        func=_get_user,
        name="mcp_get_user",
        description="Look up an internal user record (ticket owner, engineer, etc.).",
        args_schema=GetUserInput,
    ),
]


def get_mcp_tools() -> list[StructuredTool]:
    return list(MOCK_MCP_TOOLS)
