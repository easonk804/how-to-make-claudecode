#!/usr/bin/env python3
"""Chapter 02 v2: LLM-style tool selection demo.

What changed from v1:
- v1: if/elif keyword routing only
- v2: ask an "LLM" to output structured tool call JSON, then execute it
"""

from __future__ import annotations

import json
from pathlib import Path


def mock_llm_tool_call(user_text: str) -> str:
    """Return a model-like JSON tool call string for teaching purpose."""
    text = user_text.lower()
    if "write" in text:
        return json.dumps({"tool": "write_file", "args": {"path": "demo.txt", "content": "hello from v2\n"}})
    if "read" in text:
        return json.dumps({"tool": "read_file", "args": {"path": "demo.txt"}})
    if "list" in text:
        return json.dumps({"tool": "list_dir", "args": {"path": "."}})
    return json.dumps({"tool": "unknown", "args": {}})


def parse_tool_call(raw: str) -> tuple[str, dict]:
    """Parse LLM output and return (tool_name, args)."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return "unknown", {}

    tool_name = payload.get("tool", "unknown")
    args = payload.get("args", {})
    if not isinstance(tool_name, str) or not isinstance(args, dict):
        return "unknown", {}
    return tool_name, args


def execute_tool(tool_name: str, args: dict, workspace: Path) -> str:
    demo_file = workspace / args.get("path", "demo.txt")

    if tool_name == "write_file":
        content = args.get("content", "")
        demo_file.write_text(content, encoding="utf-8")
        return f"wrote: {demo_file.name}"

    if tool_name == "read_file":
        if not demo_file.exists():
            return f"not found: {demo_file.name}"
        return demo_file.read_text(encoding="utf-8")

    if tool_name == "list_dir":
        target = workspace / args.get("path", ".")
        if not target.exists() or not target.is_dir():
            return "invalid directory"
        return ", ".join(sorted(p.name for p in target.iterdir()))

    return f"unknown tool: {tool_name}"


if __name__ == "__main__":
    sandbox = Path(__file__).resolve().parent / "sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)

    for user_text in ["write demo", "read demo", "list files", "compress image"]:
        raw = mock_llm_tool_call(user_text)
        tool_name, args = parse_tool_call(raw)
        result = execute_tool(tool_name, args, sandbox)
        print(f"input={user_text!r}")
        print(f"llm={raw}")
        print(f"result={result!r}\n")
