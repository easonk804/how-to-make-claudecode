#!/usr/bin/env python3
"""Chapter 09 v2: centralized orchestration.

What changed from v1:
- v1: one agent handles everything
- v2: a coordinator assigns tasks to specialized agents
"""

from __future__ import annotations


def assign(task: str) -> str:
    text = task.lower()
    if "ui" in text or "frontend" in text:
        return "frontend_agent"
    if "api" in text or "backend" in text:
        return "backend_agent"
    if "test" in text or "qa" in text:
        return "test_agent"
    return "general_agent"


def run_centralized(tasks: list[str]) -> list[str]:
    logs: list[str] = []
    for task in tasks:
        owner = assign(task)
        logs.append(f"coordinator -> {owner}: {task}")
        logs.append(f"{owner} done: {task}")
    logs.append("coordinator: all tasks completed")
    return logs


if __name__ == "__main__":
    demo_tasks = ["build ui login", "implement api auth", "add test for login"]
    for line in run_centralized(demo_tasks):
        print(line)
