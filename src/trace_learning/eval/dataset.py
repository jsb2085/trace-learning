"""Eval dataset schema — warehouse agent parameterized multi-tool questions."""

from __future__ import annotations

import json
import re
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

EVAL_DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "eval"
DEFAULT_DATASET_PATH = EVAL_DATA_DIR / "questions.json"
DEFAULT_TEMPLATES_PATH = EVAL_DATA_DIR / "templates.json"

TARGET_QUESTION_COUNT = 60
MIN_TOOL_CALLS = 3


class QuestionCategory(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"
    INVENTORY = "inventory"
    OPERATIONS = "operations"


class ExpectedToolCall(BaseModel):
    tool: str
    args: dict[str, Any] = Field(default_factory=dict)


class QuestionTemplate(BaseModel):
    id: str
    template: str
    category: QuestionCategory
    description: str = ""
    min_tool_calls: int = MIN_TOOL_CALLS
    required_tool_groups: list[str] = Field(default_factory=list)

    def render(self, params: dict[str, Any]) -> str:
        question = self.template
        for key, value in params.items():
            question = question.replace(f"{{{key}}}", str(value))
        if re.search(r"\{[a-z_]+\}", question):
            raise ValueError(f"Unresolved placeholders in rendered question: {question}")
        return question


class EvalQuestion(BaseModel):
    id: str
    template_id: str
    params: dict[str, Any] = Field(default_factory=dict)
    question: str
    category: QuestionCategory
    expected_answer: str
    expected_tool_calls: list[ExpectedToolCall] = Field(default_factory=list)
    min_tool_calls: int = MIN_TOOL_CALLS
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    notes: str = ""

    @model_validator(mode="after")
    def _validate_multi_tool(self) -> EvalQuestion:
        if len(self.expected_tool_calls) < MIN_TOOL_CALLS:
            raise ValueError(f"{self.id} must declare at least {MIN_TOOL_CALLS} expected tool calls")
        return self


class EvalDataset(BaseModel):
    version: str = "0.3.0"
    description: str = ""
    templates: list[QuestionTemplate] = Field(default_factory=list)
    questions: list[EvalQuestion]

    @classmethod
    def load(
        cls,
        path: Path | None = None,
        templates_path: Path | None = None,
    ) -> EvalDataset:
        p = path or DEFAULT_DATASET_PATH
        with p.open() as f:
            raw = json.load(f)

        tp = templates_path or DEFAULT_TEMPLATES_PATH
        if tp.exists():
            with tp.open() as f:
                templates_raw = json.load(f)
            raw["templates"] = templates_raw.get("templates", [])

        return cls.model_validate(raw)

    def save(self, path: Path | None = None) -> None:
        p = path or DEFAULT_DATASET_PATH
        payload = self.model_dump(exclude={"templates"})
        with p.open("w") as f:
            json.dump(payload, f, indent=2)

    def get_template(self, template_id: str) -> QuestionTemplate | None:
        for template in self.templates:
            if template.id == template_id:
                return template
        return None

    def by_template(self, template_id: str) -> list[EvalQuestion]:
        return [q for q in self.questions if q.template_id == template_id]

    def by_category(self, category: QuestionCategory) -> list[EvalQuestion]:
        return [q for q in self.questions if q.category == category]

    def coverage_report(self) -> dict[str, Any]:
        category_counts: dict[str, int] = {c.value: 0 for c in QuestionCategory}
        template_counts: dict[str, int] = {}
        tool_call_counts: list[int] = []
        for q in self.questions:
            category_counts[q.category.value] += 1
            template_counts[q.template_id] = template_counts.get(q.template_id, 0) + 1
            tool_call_counts.append(len(q.expected_tool_calls))
        return {
            "total": len(self.questions),
            "target": TARGET_QUESTION_COUNT,
            "remaining": TARGET_QUESTION_COUNT - len(self.questions),
            "by_category": category_counts,
            "by_template": template_counts,
            "unique_templates": len(template_counts),
            "avg_tool_calls": round(sum(tool_call_counts) / len(tool_call_counts), 2)
            if tool_call_counts
            else 0,
            "min_tool_calls": min(tool_call_counts) if tool_call_counts else 0,
            "max_tool_calls": max(tool_call_counts) if tool_call_counts else 0,
        }
