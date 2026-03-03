#!/usr/bin/env python3
"""Chapter 03 v2: simple message history.

What changed from v1:
- v1: no memory, each request is isolated
- v2: keep all messages in a growing list
"""

messages: list[dict[str, str]] = []


def reset_memory() -> None:
    """Clear all history (useful for tests and demos)."""
    messages.clear()


def chat(user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})

    if "继续" in user_input or "continue" in user_input.lower():
        previous_users = [m["content"] for m in messages[:-1] if m["role"] == "user"]
        if previous_users:
            reply = f"[with memory] 你在继续：{previous_users[-1]}"
        else:
            reply = "[with memory] 目前没有可继续的历史。"
    else:
        reply = f"[with memory] 已记录本轮输入，总消息数={len(messages)}"

    messages.append({"role": "assistant", "content": reply})
    return reply


if __name__ == "__main__":
    reset_memory()
    print(chat("请帮我做旅行计划"))
    print(chat("继续刚才的任务"))
    print(f"messages={len(messages)}")
