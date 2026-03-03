#!/usr/bin/env python3
"""Chapter 06 v1: hardcoded knowledge.

Baseline behavior:
- agent always answers from a fixed string
- query details are mostly ignored
"""

KNOWLEDGE = "Python 项目中函数命名通常使用 snake_case。"


def answer(q: str) -> str:
    return f"Q: {q}\nA(硬编码): {KNOWLEDGE}"


if __name__ == "__main__":
    print(answer("函数怎么命名"))
