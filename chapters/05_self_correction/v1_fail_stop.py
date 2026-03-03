#!/usr/bin/env python3
"""Chapter 05 v1: fail and stop.

Baseline behavior:
- execute steps in order
- once a step fails, the whole run stops immediately
"""


def run_step(step_name: str) -> str:
    if step_name == "unstable_step":
        raise RuntimeError("step failed: unstable_step")
    return f"ok: {step_name}"


def run_task_fail_stop(steps: list[str]) -> list[str]:
    logs: list[str] = []
    for step in steps:
        result = run_step(step)
        logs.append(result)
    return logs


if __name__ == "__main__":
    try:
        output = run_task_fail_stop(["prepare", "unstable_step", "finalize"])
        print(output)
    except RuntimeError as e:
        print("error:", e)
