#!/usr/bin/env python3
"""
Chapter 01 v1: Hardcoded perception-thought-action.

Goal:
- Show the minimal idea of "observe -> think -> act" without any LLM call.
- Keep implementation tiny and readable for beginners.
"""

from pathlib import Path


def hardcoded_think(user_input: str) -> tuple[str, str]:
    """Return (action, target_path) based on a simple keyword rule."""
    text = user_input.strip().lower()
    if "create" in text or "创建" in text:
        return "create_file", "test.txt"
    return "noop", ""


def hardcoded_act(action: str, target: str, workspace: Path) -> str:
    """Perform the selected action."""
    workspace.mkdir(parents=True, exist_ok=True)
    if action == "create_file":
        path = workspace / target
        path.write_text("hello from v1\n", encoding="utf-8")
        return f"created: {path}"
    return "no action"


def run_demo(user_input: str = "帮我创建一个文件") -> str:
    workspace = Path(__file__).resolve().parent / "sandbox"
    action, target = hardcoded_think(user_input)
    return hardcoded_act(action, target, workspace)


if __name__ == "__main__":
    print("[v1] hardcoded agent")
    result = run_demo()
    print(result)
