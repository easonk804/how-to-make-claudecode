#!/usr/bin/env python3
"""Chapter 02 v1: hardcoded tool routing demo."""

from pathlib import Path


def route_tool(user_text: str) -> str:
    text = user_text.lower()
    if "read" in text:
        return "read_file"
    if "write" in text:
        return "write_file"
    return "unknown"


def execute_tool(tool_name: str, workspace: Path) -> str:
    """Hardcoded tool executor (intentionally not scalable)."""
    demo_file = workspace / "demo.txt"

    if tool_name == "write_file":
        demo_file.write_text("hello from v1\n", encoding="utf-8")
        return "wrote demo.txt"
    if tool_name == "read_file":
        if not demo_file.exists():
            return "demo.txt not found"
        return demo_file.read_text(encoding="utf-8")
    return f"unknown tool: {tool_name}"


if __name__ == "__main__":
    sandbox = Path(__file__).resolve().parent / "sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)

    for user_text in ["write demo.txt", "read demo.txt", "delete demo.txt"]:
        tool = route_tool(user_text)
        result = execute_tool(tool, sandbox)
        print(f"input={user_text!r} -> tool={tool!r} -> {result!r}")
