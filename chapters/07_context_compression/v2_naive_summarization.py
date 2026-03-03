#!/usr/bin/env python3
"""Chapter 07 v2: naive summarization.

What changed from v1:
- v1: drop all old context by truncation
- v2: compress old messages into a short summary string
"""

from __future__ import annotations


def summarize_text(messages: list[str], keep_recent: int = 3) -> str:
    old = messages[:-keep_recent]
    if not old:
        return "[summary] none"

    first = old[0]
    last = old[-1]
    return f"[summary] old={len(old)} first={first} last={last}"


def summarize_old(messages: list[str], keep_recent: int = 3, trigger_threshold: int = 6) -> list[str]:
    if len(messages) <= trigger_threshold:
        return messages

    summary = summarize_text(messages, keep_recent=keep_recent)
    return [summary] + messages[-keep_recent:]


if __name__ == "__main__":
    demo = [f"m{i}" for i in range(12)]
    print("before:", demo)
    print("after:", summarize_old(demo, keep_recent=3, trigger_threshold=6))
