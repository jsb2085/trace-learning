"""Run evaluation against the deep agent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from trace_learning.agent.deep_agent import DeepAgent
from trace_learning.eval.dataset import EvalDataset, EvalQuestion


class EvalResult(BaseModel):
    question_id: str
    question: str
    expected_answer: str
    actual_answer: str
    passed: bool
    tool_calls_matched: bool | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class EvalRunner:
    """Execute eval questions and compare outputs."""

    def __init__(self, agent: DeepAgent, dataset: EvalDataset) -> None:
        self._agent = agent
        self._dataset = dataset

    def _extract_answer(self, response: dict[str, Any]) -> str:
        messages = response.get("messages", [])
        if not messages:
            return ""
        last = messages[-1]
        return getattr(last, "content", str(last))

    def run_question(self, question: EvalQuestion) -> EvalResult:
        response = self._agent.invoke(question.question)
        actual = self._extract_answer(response)
        # Simple substring match for scaffolding — refine with structured checks later
        passed = question.expected_answer.lower() in actual.lower()
        return EvalResult(
            question_id=question.id,
            question=question.question,
            expected_answer=question.expected_answer,
            actual_answer=actual,
            passed=passed,
        )

    def run_all(self) -> list[EvalResult]:
        return [self.run_question(q) for q in self._dataset.questions]

    def summary(self, results: list[EvalResult]) -> dict[str, Any]:
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": round(passed / total, 3) if total else 0.0,
        }

    def save_results(self, results: list[EvalResult], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "summary": self.summary(results),
            "results": [r.model_dump() for r in results],
        }
        with path.open("w") as f:
            json.dump(payload, f, indent=2)
