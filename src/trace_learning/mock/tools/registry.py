"""Registry of standalone mock tools with deterministic outputs."""

from __future__ import annotations

from datetime import date
from typing import Any

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression, e.g. '2 + 3 * 4'")


class LookupOrderInput(BaseModel):
    order_id: str = Field(description="Order identifier, e.g. ORD-1001")


class GetWeatherInput(BaseModel):
    city: str = Field(description="City name")


# Deterministic mock data
MOCK_ORDERS: dict[str, dict[str, Any]] = {
    "ORD-1001": {"status": "shipped", "total_usd": 49.99, "items": ["widget-a"]},
    "ORD-1002": {"status": "pending", "total_usd": 129.0, "items": ["widget-b", "widget-c"]},
    "ORD-1003": {"status": "delivered", "total_usd": 19.5, "items": ["widget-a", "widget-d"]},
}

MOCK_WEATHER: dict[str, dict[str, Any]] = {
    "san francisco": {"temp_f": 62, "condition": "foggy"},
    "austin": {"temp_f": 95, "condition": "sunny"},
    "new york": {"temp_f": 78, "condition": "partly cloudy"},
}


def _calculator(expression: str) -> float:
    # Safe eval for simple arithmetic (mock only — not for production)
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        raise ValueError("Expression contains disallowed characters")
    return float(eval(expression))  # noqa: S307 — intentional for mock tool


def _lookup_order(order_id: str) -> dict[str, Any]:
    order = MOCK_ORDERS.get(order_id.upper())
    if order is None:
        return {"error": f"Order not found: {order_id}"}
    return {"order_id": order_id.upper(), **order}


def _get_weather(city: str) -> dict[str, Any]:
    weather = MOCK_WEATHER.get(city.lower())
    if weather is None:
        return {"error": f"No weather data for: {city}"}
    return {"city": city, "date": str(date.today()), **weather}


BUILTIN_TOOLS = [
    StructuredTool.from_function(
        func=_calculator,
        name="calculator",
        description="Evaluate a basic arithmetic expression.",
        args_schema=CalculatorInput,
    ),
    StructuredTool.from_function(
        func=_lookup_order,
        name="lookup_order",
        description="Look up an order by ID in the mock order database.",
        args_schema=LookupOrderInput,
    ),
    StructuredTool.from_function(
        func=_get_weather,
        name="get_weather",
        description="Get today's weather for a supported city.",
        args_schema=GetWeatherInput,
    ),
]


def get_builtin_tools() -> list[StructuredTool]:
    return list(BUILTIN_TOOLS)
