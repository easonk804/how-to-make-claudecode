#!/usr/bin/env python3
"""Chapter 10 v1: insecure executor baseline.

Baseline behavior:
- accepts any command string
- performs no validation, no permission checks, no audit trail
"""


def run(command: str) -> str:
    # Teaching-only demo: do not actually execute shell commands.
    return f"[INSECURE] execute directly: {command}"


def run_batch(commands: list[str]) -> list[str]:
    return [run(cmd) for cmd in commands]


if __name__ == "__main__":
    demo = ["ls -la", "rm -rf /tmp/demo", "curl http://example.com"]
    for line in run_batch(demo):
        print(line)
