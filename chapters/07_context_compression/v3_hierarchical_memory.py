#!/usr/bin/env python3
"""Chapter 07 v3: hierarchical memory.

What changed from v2:
- v2: single summary string + recent messages
- v3: split memory into working / summary / facts layers
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Memory:
    working: list[str] = field(default_factory=list)
    summary: list[str] = field(default_factory=list)
    facts: dict[str, str] = field(default_factory=dict)


def extract_fact(message: str) -> tuple[str, str] | None:
    """Extract tiny fact pattern like 'key=value' from a message."""
    if "=" not in message:
        return None
    key, value = message.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key or not value:
        return None
    return key, value


def compact_memory(mem: Memory, working_limit: int = 4) -> Memory:
    """Keep working memory small and move old info to summary/facts."""
    if len(mem.working) <= working_limit:
        return mem

    overflow = mem.working[:-working_limit]
    mem.working = mem.working[-working_limit:]
    mem.summary.append(f"compressed {len(overflow)} messages")

    for msg in overflow:
        fact = extract_fact(msg)
        if fact is not None:
            k, v = fact
            mem.facts[k] = v

    return mem


def memory_prompt(mem: Memory) -> str:
    summary_block = " | ".join(mem.summary) if mem.summary else "(none)"
    facts_block = ", ".join(f"{k}={v}" for k, v in sorted(mem.facts.items())) if mem.facts else "(none)"
    working_block = "\n".join(f"- {m}" for m in mem.working) if mem.working else "- (empty)"
    return f"Summary: {summary_block}\nFacts: {facts_block}\nWorking:\n{working_block}"


if __name__ == "__main__":
    mem = Memory(
        working=[
            "topic=agent tutorial",
            "chapter=07",
            "need context compression example",
            "user wants short prompt",
            "todo=write tests",
            "style=beginner friendly",
        ]
    )
    compact_memory(mem, working_limit=3)
    print(memory_prompt(mem))
