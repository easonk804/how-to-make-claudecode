#!/usr/bin/env python3
"""Chapter 08 v1: blocking execution baseline.

All tasks run sequentially in the main thread.
"""

import time
from time import perf_counter


def long_task(name: str, delay: float = 0.2) -> str:
    time.sleep(delay)
    return f"{name} done"


def run_blocking(task_names: list[str], delay: float = 0.2) -> tuple[list[str], float]:
    start = perf_counter()
    results = [long_task(name, delay=delay) for name in task_names]
    elapsed = perf_counter() - start
    return results, elapsed


if __name__ == "__main__":
    out, seconds = run_blocking(["A", "B", "C"], delay=0.2)
    print(out)
    print(f"elapsed={seconds:.3f}s")
