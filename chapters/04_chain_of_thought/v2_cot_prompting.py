#!/usr/bin/env python3
"""Chapter 04 v2: chain-of-thought style prompting.

What changed from v1:
- v1: directly output a suggestion
- v2: decompose into explicit reasoning steps before final answer
"""

from __future__ import annotations


def cot_steps(problem: str) -> list[str]:
    text = problem.lower()
    hypothesis = "可能是配置或依赖问题"
    action = "先检查错误关键词，再给出最小修复命令"

    if "modulenotfounderror" in text:
        hypothesis = "缺少 Python 依赖包"
        action = "定位缺失包名并执行 pip install"
    elif "permission" in text:
        hypothesis = "权限不足或路径受限"
        action = "确认当前用户权限并重试"

    return [
        f"1) 分析问题: {problem}",
        f"2) 诊断根因: {hypothesis}",
        f"3) 设计方案: {action}",
        "4) 执行验证: 复现原命令，确认报错消失",
    ]


def solve_with_cot(problem: str) -> str:
    steps = cot_steps(problem)
    summary = steps[2].split(":", 1)[-1].strip()
    return f"建议方案：{summary}"


if __name__ == "__main__":
    demo_problem = "ModuleNotFoundError: requests"
    for s in cot_steps(demo_problem):
        print("-", s)
    print(solve_with_cot(demo_problem))
