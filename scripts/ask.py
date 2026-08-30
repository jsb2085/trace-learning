#!/usr/bin/env python3
"""Minimal entry point — ask the warehouse agent one question."""

from trace_learning.agent import ask

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print('Usage: python scripts/ask.py "Your question here"')
        raise SystemExit(1)
    print(ask(" ".join(sys.argv[1:])))
