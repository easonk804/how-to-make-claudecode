#!/usr/bin/env python3
"""Chapter 07 v1: hard truncation.

Baseline behavior:
- keep only the latest N messages
- old context is dropped permanently
"""


def truncate(messages: list[str], keep_last: int = 5) -> list[str]:
    if keep_last <= 0:
        return []
    return messages[-keep_last:]


if __name__ == "__main__":
    demo_messages = [f"msg-{i}" for i in range(1, 11)]
    print("before:", demo_messages)
    print("after:", truncate(demo_messages, keep_last=3))
