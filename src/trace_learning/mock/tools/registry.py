"""Registry of utility tools that support multi-step reasoning."""

from __future__ import annotations

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression, e.g. '2026-08-30' comparisons use day counts")


class DateDiffInput(BaseModel):
    start_date: str = Field(description="Start date YYYY-MM-DD")
    end_date: str = Field(description="End date YYYY-MM-DD")


def _calculator(expression: str) -> float:
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        raise ValueError("Expression contains disallowed characters")
    return float(eval(expression))  # noqa: S307 — intentional for mock tool


def _days_between(start_date: str, end_date: str) -> dict[str, int]:
    from datetime import date

    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    delta = (end - start).days
    return {"start_date": start_date, "end_date": end_date, "days": delta}


BUILTIN_TOOLS = [
    StructuredTool.from_function(
        func=_calculator,
        name="calculator",
        description="Evaluate a basic arithmetic expression (e.g. days late, totals).",
        args_schema=CalculatorInput,
    ),
    StructuredTool.from_function(
        func=_days_between,
        name="days_between",
        description="Calculate the number of days between two ISO dates.",
        args_schema=DateDiffInput,
    ),
]


def get_builtin_tools() -> list[StructuredTool]:
    return list(BUILTIN_TOOLS)
