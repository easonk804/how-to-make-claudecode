#!/usr/bin/env python3
"""Chapter 10 v2: blacklist + whitelist checks.

What changed from v1:
- v1: no checks at all
- v2: block dangerous patterns and allow only known-safe command prefixes
"""

from __future__ import annotations

BLACKLIST = ["rm -rf", "sudo", "curl |", "wget |"]
WHITELIST_PREFIXES = ["ls", "cat", "echo", "mkdir", "python"]


def is_safe(command: str) -> bool:
    text = command.lower()
    if not any(text.startswith(prefix) for prefix in WHITELIST_PREFIXES):
        return False
    return not any(bad in text for bad in BLACKLIST)


def run_guarded(command: str) -> str:
    if not is_safe(command):
        return f"blocked: {command}"
    return f"allowed: {command}"


if __name__ == "__main__":
    for cmd in ["ls -la", "python app.py", "rm -rf tmp", "powershell -c whoami"]:
        print(run_guarded(cmd))
