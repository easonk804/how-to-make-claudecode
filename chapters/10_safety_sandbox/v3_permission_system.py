#!/usr/bin/env python3
"""Chapter 10 v3: permission system + audit log.

What changed from v2:
- v2: static blacklist/whitelist rule
- v3: classify risk level, enforce permission policy, and record audits
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time


@dataclass
class AuditRecord:
    ts: float
    command: str
    level: str
    decision: str


PERMISSION_POLICY = {
    "normal": "allow",
    "system": "confirm",
    "dangerous": "deny",
}


def classify(command: str) -> str:
    text = command.lower()
    if "rm" in text or "chmod" in text or "del " in text:
        return "dangerous"
    if "sudo" in text or "sc " in text:
        return "system"
    return "normal"


def enforce(command: str, auto_confirm_system: bool = False) -> tuple[str, AuditRecord]:
    level = classify(command)
    policy = PERMISSION_POLICY[level]

    if policy == "allow":
        decision = "allowed"
    elif policy == "deny":
        decision = "blocked"
    else:
        decision = "allowed" if auto_confirm_system else "needs_confirmation"

    record = AuditRecord(ts=time(), command=command, level=level, decision=decision)
    return decision, record


def run_commands(commands: list[str], auto_confirm_system: bool = False) -> list[AuditRecord]:
    logs: list[AuditRecord] = []
    for cmd in commands:
        _, record = enforce(cmd, auto_confirm_system=auto_confirm_system)
        logs.append(record)
    return logs


if __name__ == "__main__":
    demo = ["mkdir demo", "sudo apt update", "rm -rf /tmp/demo"]
    for rec in run_commands(demo, auto_confirm_system=False):
        print(rec)
