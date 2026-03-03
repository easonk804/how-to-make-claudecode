#!/usr/bin/env python3
"""Chapter 04 v3: ReAct (Thought -> Action -> Observation).

What changed from v2:
- v2: reasoning steps only
- v3: reasoning + tool actions + observations in a loop
"""

from __future__ import annotations


def run_tool(action: str, state: dict[str, object]) -> str:
    """Minimal tool simulator for teaching ReAct."""
    if action == "read_error_log":
        return str(state["error_log"])

    if action == "install_requests":
        installed = state.setdefault("installed", set())
        if isinstance(installed, set):
            installed.add("requests")
        return "installed requests"

    if action == "verify_fix":
        installed = state.get("installed", set())
        if isinstance(installed, set) and "requests" in installed:
            return "check ok"
        return "still failing"

    return "unknown action"


def react_solve(problem_log: str, max_steps: int = 5) -> tuple[list[str], str]:
    state: dict[str, object] = {"error_log": problem_log, "installed": set()}
    trace: list[str] = []
    observation = "start"

    for _ in range(max_steps):
        if observation == "start":
            thought = "先读取错误日志，确认具体异常。"
            action = "read_error_log"
        elif "modulenotfounderror" in observation.lower():
            thought = "日志显示缺少依赖，安装 requests 再验证。"
            action = "install_requests"
        elif "installed requests" in observation.lower():
            thought = "依赖已安装，执行验证命令确认修复。"
            action = "verify_fix"
        elif "check ok" in observation.lower():
            final = "问题已修复：缺失依赖 requests，安装后验证通过。"
            trace.append(f"Thought: {final}")
            return trace, final
        else:
            final = f"无法继续推理，最后观察为: {observation}"
            trace.append(f"Thought: {final}")
            return trace, final

        trace.append(f"Thought: {thought}")
        trace.append(f"Action: {action}")
        observation = run_tool(action, state)
        trace.append(f"Observation: {observation}")

    final = "达到最大推理轮数，停止执行。"
    trace.append(f"Thought: {final}")
    return trace, final


def react_trace() -> list[str]:
    trace, _ = react_solve("ModuleNotFoundError: No module named 'requests'")
    return trace


if __name__ == "__main__":
    lines, final_answer = react_solve("ModuleNotFoundError: No module named 'requests'")
    for line in lines:
        print(line)
    print("Final:", final_answer)
