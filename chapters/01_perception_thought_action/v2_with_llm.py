#!/usr/bin/env python3
"""
Chapter 01 v2: use LLM for thinking, single action execution.

What changed from v1:
- v1: hardcoded if/else thinking
- v2: LLM decides the action in JSON

Limitation kept intentionally:
- only one think->act pass (not a loop yet)
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from anthropic import Anthropic
from dotenv import load_dotenv

SYSTEM_PROMPT = (
    "你是一个极简Agent。请把用户请求转换为JSON动作。"
    "只允许动作: create_file, append_file, read_file, noop。"
    "输出必须是纯JSON对象，字段: action, path, content。"
)


def parse_action_json(text: str) -> dict[str, Any]:
    """Parse model output; fallback to noop on parse failure."""
    try:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("not object")
        return {
            "action": str(data.get("action", "noop")),
            "path": str(data.get("path", "")),
            "content": str(data.get("content", "")),
        }
    except Exception:
        return {"action": "noop", "path": "", "content": ""}


def execute_action(action: dict[str, str], workspace: Path) -> str:
    workspace.mkdir(parents=True, exist_ok=True)
    kind = action["action"]
    target = workspace / action["path"] if action["path"] else workspace / "test.txt"

    if kind == "create_file":
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(action["content"] or "hello from v2\n", encoding="utf-8")
        return f"created: {target}"

    if kind == "append_file":
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as f:
            f.write(action["content"] or "append from v2\n")
        return f"appended: {target}"

    if kind == "read_file":
        if not target.exists():
            return f"not found: {target}"
        return target.read_text(encoding="utf-8")

    return "no action"


def think_once_with_llm(user_input: str, model_id: str) -> dict[str, Any]:
    client = Anthropic()
    response = client.messages.create(
        model=model_id,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_input}],
    )
    text_blocks = [b.text for b in response.content if getattr(b, "type", "") == "text"]
    output_text = "\n".join(text_blocks).strip()
    return parse_action_json(output_text)


def run_demo(user_input: str = "创建 sandbox/hello.txt 并写入 hello") -> None:
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    model_id = os.getenv("MODEL_ID", "claude-3-5-sonnet-latest")

    if not api_key:
        print("缺少 ANTHROPIC_API_KEY，无法运行 v2（需要真实 LLM 调用）。")
        return

    workspace = Path(__file__).resolve().parent / "sandbox"
    action = think_once_with_llm(user_input, model_id=model_id)
    print("LLM action:", action)
    result = execute_action(action, workspace)
    print("Result:", result)


if __name__ == "__main__":
    print("[v2] LLM thinks once, agent acts once")
    run_demo()
