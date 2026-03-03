#!/usr/bin/env python3
"""Chapter 03 v1: no memory demo.

Every request is handled independently.
The agent cannot understand references to previous turns.
"""


def chat_once(user_input: str) -> str:
    if "继续" in user_input or "continue" in user_input.lower():
        return "[stateless] 我不知道你在继续什么，因为我没有保存历史。"
    return f"[stateless] 收到：{user_input}"


if __name__ == "__main__":
    print(chat_once("请帮我写一个待办清单"))
    print(chat_once("继续刚才任务"))
