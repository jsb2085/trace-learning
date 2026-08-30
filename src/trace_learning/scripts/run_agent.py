#!/usr/bin/env python3
"""Interactive CLI for the warehouse agent."""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from trace_learning.agent.warehouse_agent import create_warehouse_agent


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run the trace-learning warehouse agent")
    parser.add_argument("question", nargs="?", help="Question to ask (omit for REPL)")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Copy .env.example to .env and add your key.")

    agent = create_warehouse_agent()

    if args.question:
        result = agent.invoke(args.question)
        print(result["messages"][-1].content)
        return

    print("Warehouse Agent — WH-EAST (type 'quit' to exit)")
    print(f"Tools: {[t.name for t in agent.tools]}\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() in {"quit", "exit", "q"}:
            break
        result = agent.invoke(q)
        print(f"Agent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()
