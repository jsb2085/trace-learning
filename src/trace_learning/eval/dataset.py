"""Eval dataset schema and loader.

Target: 60 questions with deterministic expected outputs.
Organized by category so we can track accuracy per capability.
"""

from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

DEFAULT_DATASET_PATH = Path(__file__).resolve().parents[3] / "data" / "eval" / "questions.json"

TARGET_QUESTION_COUNT = 60


class QuestionCategory(str, Enum):
    RAG = "rag"
    MCP = "mcp"
    BUILTIN = "builtin"
    MULTI_STEP = "multi_step"
    WORKFLOW = "workflow"


class ExpectedToolCall(BaseModel):
    tool: str
    args: dict[str, Any] = Field(default_factory=dict)


class EvalQuestion(BaseModel):
    id: str
    category: QuestionCategory
    question: str
    expected_answer: str
    expected_tool_calls: list[ExpectedToolCall] = Field(default_factory=list)
    workflow_id: str | None = Field(
        default=None,
        description="If set, this question should match a workflow graph entry",
    )
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    notes: str = ""


class EvalDataset(BaseModel):
    version: str = "0.1.0"
    description: str = ""
    questions: list[EvalQuestion]

    @classmethod
    def load(cls, path: Path | None = None) -> EvalDataset:
        p = path or DEFAULT_DATASET_PATH
        with p.open() as f:
            raw = json.load(f)
        return cls.model_validate(raw)

    def save(self, path: Path | None = None) -> None:
        p = path or DEFAULT_DATASET_PATH
        with p.open("w") as f:
            json.dump(self.model_dump(), f, indent=2)

    def by_category(self, category: QuestionCategory) -> list[EvalQuestion]:
        return [q for q in self.questions if q.category == category]

    def coverage_report(self) -> dict[str, int]:
        counts: dict[str, int] = {c.value: 0 for c in QuestionCategory}
        for q in self.questions:
            counts[q.category.value] += 1
        counts["total"] = len(self.questions)
        counts["target"] = TARGET_QUESTION_COUNT
        counts["remaining"] = TARGET_QUESTION_COUNT - len(self.questions)
        return counts
