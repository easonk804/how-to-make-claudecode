#!/usr/bin/env python3
"""Chapter 09 v1: single-agent baseline.

One agent handles every subtask in sequence.
"""


def do_all_tasks(project_goal: str) -> list[str]:
    subtasks = ["design ui", "build api", "write tests"]
    logs: list[str] = [f"goal: {project_goal}"]
    for task in subtasks:
        logs.append(f"single_agent handles: {task}")
    logs.append("single_agent done")
    return logs


if __name__ == "__main__":
    for line in do_all_tasks("发布一个待办应用"):
        print(line)
