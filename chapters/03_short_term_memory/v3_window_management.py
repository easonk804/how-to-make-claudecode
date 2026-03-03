#!/usr/bin/env python3
"""Chapter 03 v3: sliding window memory.

What changed from v2:
- v2: keeps all history forever
- v3: keep a bounded window while preserving system prompt
"""

from __future__ import annotations


def add_turn(messages: list[dict[str, str]], user_text: str, assistant_text: str) -> None:
    messages.append({"role": "user", "content": user_text})
    messages.append({"role": "assistant", "content": assistant_text})


def trim_messages(messages: list[dict[str, str]], keep_rounds: int = 3) -> list[dict[str, str]]:
    """Keep system message + recent N rounds (user/assistant pairs)."""
    if keep_rounds <= 0:
        keep_rounds = 1

    if len(messages) <= keep_rounds * 2 + 1:
        return messages

    system = messages[:1]
    recent = messages[-(keep_rounds * 2):]
    return system + recent


def build_prompt(messages: list[dict[str, str]], keep_rounds: int = 3) -> str:
    trimmed = trim_messages(messages, keep_rounds=keep_rounds)
    return "\n".join(f"{m['role']}: {m['content']}" for m in trimmed)


if __name__ == "__main__":
    history = [{"role": "system", "content": "你是一个记忆管理演示 Agent。"}]
    for i in range(1, 7):
        add_turn(history, f"用户问题{i}", f"助手回答{i}")

    print(f"full_messages={len(history)}")
    trimmed = trim_messages(history, keep_rounds=2)
    print(f"trimmed_messages={len(trimmed)}")
    print(build_prompt(history, keep_rounds=2))
