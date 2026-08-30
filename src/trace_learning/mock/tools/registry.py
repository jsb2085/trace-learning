"""Utility tools supporting warehouse date math and quantity calculations."""

from __future__ import annotations

from datetime import date

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(description="Arithmetic expression for quantity or count calculations")


class DateDiffInput(BaseModel):
    start_date: str = Field(description="Start date YYYY-MM-DD")
    end_date: str = Field(description="End date YYYY-MM-DD")


def _calculator(expression: str) -> float:
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        raise ValueError("Expression contains disallowed characters")
    return float(eval(expression))  # noqa: S307 — intentional for mock tool


def _days_between(start_date: str, end_date: str) -> dict[str, int]:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    return {"start_date": start_date, "end_date": end_date, "days": (end - start).days}


UTILITY_TOOLS = [
    StructuredTool.from_function(
        func=_calculator,
        name="calculator",
        description="Evaluate arithmetic for pick quantities, counts, or totals.",
        args_schema=CalculatorInput,
    ),
    StructuredTool.from_function(
        func=_days_between,
        name="days_between",
        description="Calculate days between two dates (e.g. overdue pick days).",
        args_schema=DateDiffInput,
    ),
]


def get_utility_tools() -> list[StructuredTool]:
    return list(UTILITY_TOOLS)


# Backward-compatible alias
get_builtin_tools = get_utility_tools
BUILTIN_TOOLS = UTILITY_TOOLS
