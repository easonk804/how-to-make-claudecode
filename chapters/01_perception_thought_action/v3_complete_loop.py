#!/usr/bin/env python3
"""
Chapter 01 v3: complete observation-thought-action loop.

What changed from v2:
- v2: one-shot think->act
- v3: while-loop with tool_result feedback until model stops using tools
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Callable

from dotenv import load_dotenv

SYSTEM = (
    "你是一个教学Agent。"
    "请优先通过工具逐步完成任务。"
    "当任务完成时，用自然语言总结并停止调用工具。"
)

TOOLS = [
    {
        "name": "create_file",
        "description": "Create or overwrite a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "append_file",
        "description": "Append content to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "read_file",
        "description": "Read file content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"],
        },
    },
]


def _safe_join(workspace: Path, rel: str) -> Path:
    target = (workspace / rel).resolve()
    base = workspace.resolve()
    if not str(target).startswith(str(base)):
        raise ValueError("Path escapes sandbox")
    return target


def run_create(workspace: Path, path: str, content: str) -> str:
    target = _safe_join(workspace, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"created: {target.relative_to(workspace)}"


def run_append(workspace: Path, path: str, content: str) -> str:
    target = _safe_join(workspace, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as f:
        f.write(content)
    return f"appended: {target.relative_to(workspace)}"


def run_read(workspace: Path, path: str) -> str:
    target = _safe_join(workspace, path)
    if not target.exists():
        return "not found"
    return target.read_text(encoding="utf-8")


def build_handlers(workspace: Path) -> dict[str, Callable[..., str]]:
    return {
        "create_file": lambda **kw: run_create(workspace, kw["path"], kw["content"]),
        "append_file": lambda **kw: run_append(workspace, kw["path"], kw["content"]),
        "read_file": lambda **kw: run_read(workspace, kw["path"]),
    }


def extract_text(content_blocks: list[object]) -> str:
    parts: list[str] = []
    for block in content_blocks:
        if getattr(block, "type", "") == "text":
            parts.append(getattr(block, "text", ""))
    return "\n".join(parts).strip()


def _import_anthropic() -> object:
    # Delayed import so local tests can run without anthropic installed.
    from anthropic import Anthropic

    return Anthropic


def agent_loop(user_prompt: str) -> None:
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    model_id = os.getenv("MODEL_ID", "claude-3-5-sonnet-latest")

    if not api_key:
        print("缺少 ANTHROPIC_API_KEY，无法运行 v3。")
        return

    Anthropic = _import_anthropic()
    client = Anthropic()
    workspace = Path(__file__).resolve().parent / "sandbox"
    workspace.mkdir(parents=True, exist_ok=True)
    handlers = build_handlers(workspace)

    messages: list[dict] = [{"role": "user", "content": user_prompt}]

    while True:
        response = client.messages.create(
            model=model_id,
            system=SYSTEM,
            messages=messages,
            tools=TOOLS,
            max_tokens=1000,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            final_text = extract_text(response.content)
            print("\nFinal answer:\n", final_text)
            break

        tool_results = []
        for block in response.content:
            if getattr(block, "type", "") != "tool_use":
                continue
            name = block.name
            handler = handlers.get(name)
            if handler is None:
                output = f"unknown tool: {name}"
            else:
                try:
                    output = handler(**block.input)
                except Exception as exc:  # minimal teaching demo
                    output = f"error: {exc}"
            print(f"$ {name} {json.dumps(block.input, ensure_ascii=False)}")
            print(output)
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("[v3] full observation-thought-action loop")
    demo_prompt = "在 sandbox/demo.txt 写入第一行，再追加第二行，然后读取该文件并总结。"
    agent_loop(demo_prompt)
