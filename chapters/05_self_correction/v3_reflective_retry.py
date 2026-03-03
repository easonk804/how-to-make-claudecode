#!/usr/bin/env python3
"""Chapter 05 v3: reflective retry.

What changed from v2:
- v2: fixed retries using the same strategy
- v3: analyze error type and change plan before retrying
"""

from __future__ import annotations


def classify_error(error_text: str) -> str:
    text = error_text.lower()
    if "not found" in text:
        return "not_found"
    if "permission" in text:
        return "permission"
    if "timeout" in text:
        return "timeout"
    return "unknown"


def reflective_retry(error_history: list[str]) -> str:
    if not error_history:
        return "plan: run original command"

    error_kind = classify_error(error_history[-1])
    if error_kind == "not_found":
        return "plan: list directory and verify path"
    if error_kind == "permission":
        return "plan: switch to writable path and retry"
    if error_kind == "timeout":
        return "plan: reduce workload and increase timeout"
    return "plan: narrow scope and collect more logs"


def run_with_reflection(simulated_errors: list[str], max_retries: int = 3) -> tuple[str, list[str]]:
    """Replay failures and generate adaptive plans until success or limit."""
    trace: list[str] = []

    for attempt in range(1, max_retries + 1):
        if attempt - 1 < len(simulated_errors):
            error = simulated_errors[attempt - 1]
            plan = reflective_retry(simulated_errors[:attempt])
            trace.append(f"attempt {attempt}: fail={error}")
            trace.append(f"attempt {attempt}: {plan}")
            continue

        trace.append(f"attempt {attempt}: success")
        return "success", trace

    return "failed", trace


if __name__ == "__main__":
    status, logs = run_with_reflection(
        simulated_errors=["file not found", "permission denied"],
        max_retries=4,
    )
    for line in logs:
        print(line)
    print("final:", status)
