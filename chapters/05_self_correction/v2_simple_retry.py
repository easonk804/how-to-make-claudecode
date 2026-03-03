#!/usr/bin/env python3
"""Chapter 05 v2: fixed retry.

What changed from v1:
- v1: fail once and stop
- v2: retry the same strategy for a fixed number of times
"""

from __future__ import annotations


def flaky_step(attempt: int, fail_until: int = 2) -> str:
    """Fail before `fail_until`, then succeed."""
    if attempt <= fail_until:
        raise RuntimeError(f"transient error on attempt {attempt}")
    return f"ok on attempt {attempt}"


def run_with_retry(max_retries: int = 2, fail_until: int = 2) -> tuple[str, list[str]]:
    """Retry with same plan until success or retry budget exhausted."""
    attempt = 0
    logs: list[str] = []

    while attempt <= max_retries:
        attempt += 1
        try:
            result = flaky_step(attempt, fail_until=fail_until)
            logs.append(f"attempt {attempt}: success")
            return result, logs
        except RuntimeError as exc:
            logs.append(f"attempt {attempt}: {exc}")

    return "failed", logs


if __name__ == "__main__":
    result, trace = run_with_retry(max_retries=3, fail_until=2)
    for line in trace:
        print(line)
    print("final:", result)
