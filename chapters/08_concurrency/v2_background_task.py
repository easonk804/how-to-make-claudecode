#!/usr/bin/env python3
"""Chapter 08 v2: background thread + responsive main loop.

What changed from v1:
- v1: everything blocks main thread
- v2: long task runs in background and reports status via queue
"""

from __future__ import annotations

from queue import Queue
from threading import Thread
import time


def worker(queue: Queue[str], task_name: str, total_steps: int = 3, delay: float = 0.15) -> None:
    for i in range(1, total_steps + 1):
        time.sleep(delay)
        queue.put(f"{task_name} progress {i}/{total_steps}")
    queue.put(f"{task_name} done")


def run_in_background(task_name: str) -> list[str]:
    queue: Queue[str] = Queue()
    thread = Thread(target=worker, args=(queue, task_name), daemon=True)
    thread.start()

    logs: list[str] = []
    while thread.is_alive() or not queue.empty():
        try:
            msg = queue.get(timeout=0.05)
            logs.append(msg)
        except Exception:
            logs.append("main loop: still responsive")

    thread.join()
    return logs


if __name__ == "__main__":
    for line in run_in_background("index_docs"):
        print(line)
