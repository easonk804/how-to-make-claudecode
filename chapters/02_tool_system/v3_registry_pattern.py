#!/usr/bin/env python3
"""Chapter 02 v3: registry pattern + dispatcher.

What changed from v2:
- v2: model output -> parse -> if/elif execute
- v3: register handlers once, dispatch by tool name, easy to extend
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

ToolHandler = Callable[..., str]


def _safe_join(workspace: Path, rel_path: str) -> Path:
    target = (workspace / rel_path).resolve()
    base = workspace.resolve()
    if not str(target).startswith(str(base)):
        raise ValueError("path escapes sandbox")
    return target


class ToolRegistry:
    """Simple registry for tool metadata and executable handlers."""

    def __init__(self) -> None:
        self.tools: list[dict] = []
        self.handlers: dict[str, ToolHandler] = {}

    def register(self, tool_spec: dict, handler: ToolHandler) -> None:
        name = tool_spec["name"]
        self.tools.append(tool_spec)
        self.handlers[name] = handler

    def dispatch(self, tool_name: str, **kwargs: object) -> str:
        handler = self.handlers.get(tool_name)
        if handler is None:
            return f"unknown tool: {tool_name}"
        try:
            return handler(**kwargs)
        except Exception as exc:
            return f"error: {exc}"


def build_registry(workspace: Path) -> ToolRegistry:
    registry = ToolRegistry()

    def write_file(path: str, content: str) -> str:
        target = _safe_join(workspace, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote: {target.relative_to(workspace)}"

    def read_file(path: str) -> str:
        target = _safe_join(workspace, path)
        if not target.exists():
            return "not found"
        return target.read_text(encoding="utf-8")

    def list_dir(path: str = ".") -> str:
        target = _safe_join(workspace, path)
        if not target.exists() or not target.is_dir():
            return "invalid directory"
        names = sorted(p.name for p in target.iterdir())
        return ", ".join(names) if names else "(empty)"

    registry.register({"name": "write_file", "description": "Write content to file"}, write_file)
    registry.register({"name": "read_file", "description": "Read file content"}, read_file)
    registry.register({"name": "list_dir", "description": "List files in directory"}, list_dir)

    return registry


if __name__ == "__main__":
    sandbox = Path(__file__).resolve().parent / "sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    registry = build_registry(sandbox)

    tool_calls = [
        ("write_file", {"path": "demo.txt", "content": "hello from v3\n"}),
        ("read_file", {"path": "demo.txt"}),
        ("list_dir", {"path": "."}),
        ("bash", {"command": "rm -rf /"}),
    ]

    for tool_name, args in tool_calls:
        result = registry.dispatch(tool_name, **args)
        print(f"{tool_name}({args}) => {result}")
