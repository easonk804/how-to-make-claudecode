#!/usr/bin/env python3
"""Chapter 09 v3: decentralized message passing.

What changed from v2:
- v2: central coordinator dispatches everything
- v3: agents talk to each other directly and coordinate locally
"""

from __future__ import annotations

from queue import Queue


class Agent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.inbox: Queue[str] = Queue()

    def send(self, other: "Agent", message: str) -> None:
        other.inbox.put(f"from {self.name}: {message}")

    def process_once(self) -> str:
        if self.inbox.empty():
            return f"{self.name}: idle"
        message = self.inbox.get()
        return f"{self.name} processed -> {message}"


def decentralized_run() -> list[str]:
    frontend = Agent("frontend")
    backend = Agent("backend")
    tester = Agent("tester")

    frontend.send(backend, "ui contract ready")
    backend.send(tester, "api ready for tests")
    tester.send(frontend, "found ui bug: login button state")

    logs = [
        backend.process_once(),
        tester.process_once(),
        frontend.process_once(),
        frontend.process_once(),
    ]
    return logs


if __name__ == "__main__":
    for line in decentralized_run():
        print(line)
