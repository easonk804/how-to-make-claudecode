#!/usr/bin/env python3
"""Chapter 08 v3: asyncio parallel execution.

What changed from v2:
- v2: single background task
- v3: run multiple tasks in parallel with timeout control
"""

from __future__ import annotations

import asyncio
from time import perf_counter


async def task(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done"


async def run_parallel(tasks: list[tuple[str, float]], timeout: float | None = None) -> list[str]:
    coros = [task(name, delay) for name, delay in tasks]
    if timeout is None:
        return await asyncio.gather(*coros)

    try:
        return await asyncio.wait_for(asyncio.gather(*coros), timeout=timeout)
    except asyncio.TimeoutError:
        return ["timeout"]


async def run_sequential(tasks: list[tuple[str, float]]) -> list[str]:
    results: list[str] = []
    for name, delay in tasks:
        results.append(await task(name, delay))
    return results


async def main() -> None:
    demo_tasks = [("A", 0.2), ("B", 0.2), ("C", 0.2)]

    t1 = perf_counter()
    sequential = await run_sequential(demo_tasks)
    s_elapsed = perf_counter() - t1

    t2 = perf_counter()
    parallel = await run_parallel(demo_tasks, timeout=1.0)
    p_elapsed = perf_counter() - t2

    print("sequential:", sequential, f"elapsed={s_elapsed:.3f}s")
    print("parallel:", parallel, f"elapsed={p_elapsed:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
