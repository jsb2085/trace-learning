#!/usr/bin/env python3
"""Run the eval dataset against the deep agent."""

from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from trace_learning.agent.warehouse_agent import create_warehouse_agent
from trace_learning.eval.dataset import DEFAULT_DATASET_PATH
from trace_learning.eval.runner import EvalRunner


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Evaluate the deep agent")
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="Path to questions.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/eval/results/latest.json"),
        help="Where to write results",
    )
    parser.add_argument("--id", help="Run a single question by ID")
    args = parser.parse_args()

    from trace_learning.eval.dataset import EvalDataset

    dataset = EvalDataset.load(args.dataset)
    print("Dataset coverage:", dataset.coverage_report())

    agent = create_warehouse_agent()
    runner = EvalRunner(agent, dataset)

    if args.id:
        question = next((q for q in dataset.questions if q.id == args.id), None)
        if question is None:
            raise SystemExit(f"Question not found: {args.id}")
        result = runner.run_question(question)
        print(result.model_dump_json(indent=2))
        return

    results = runner.run_all()
    runner.save_results(results, args.output)
    print("Summary:", runner.summary(results))
    print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
