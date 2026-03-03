#!/usr/bin/env python3
"""
ClaudCode Full (integrated demo)

This script stitches together simplified pieces from chapter 01-10
to show a compact end-to-end agent pipeline.
"""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(relative_path: str, alias: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {relative_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


def run_full_demo() -> dict[str, object]:
    # chapter 01: perception-thought-action
    ch01 = _load_module("chapters/01_perception_thought_action/v1_hardcoded.py", "final_ch01_v1")
    action, target = ch01.hardcoded_think("请创建一个演示文件")

    # chapter 02: tool registry
    ch02 = _load_module("chapters/02_tool_system/v3_registry_pattern.py", "final_ch02_v3")
    workspace = Path(__file__).resolve().parent / "sandbox"
    workspace.mkdir(parents=True, exist_ok=True)
    registry = ch02.build_registry(workspace)
    write_out = registry.dispatch("write_file", path=target, content="hello from final demo\n")
    read_out = registry.dispatch("read_file", path=target)

    # chapter 03: short-term memory window
    ch03 = _load_module("chapters/03_short_term_memory/v3_window_management.py", "final_ch03_v3")
    messages = [
        {"role": "system", "content": "你是一个集成 Agent。"},
        {"role": "user", "content": "创建了什么文件？"},
        {"role": "assistant", "content": write_out},
        {"role": "user", "content": "读取结果是什么？"},
        {"role": "assistant", "content": read_out},
    ]
    prompt_preview = ch03.build_prompt(messages, keep_rounds=2)

    # chapter 04: reasoning loop (ReAct)
    ch04 = _load_module("chapters/04_chain_of_thought/v3_react_pattern.py", "final_ch04_v3")
    react_trace, react_final = ch04.react_solve("ModuleNotFoundError: No module named 'requests'")

    # chapter 05: self-correction
    ch05 = _load_module("chapters/05_self_correction/v3_reflective_retry.py", "final_ch05_v3")
    correction_status, correction_logs = ch05.run_with_reflection(
        simulated_errors=["file not found", "permission denied"],
        max_retries=4,
    )

    # chapter 06: external memory (RAG)
    ch06 = _load_module("chapters/06_external_memory/v3_embedding_rag.py", "final_ch06_v3")
    docs = ch06.load_sample_docs()
    index = ch06.build_index(docs)
    rag_answer = ch06.answer_with_rag("Python 命名和编码规范", index)

    # chapter 07: context compression
    ch07 = _load_module("chapters/07_context_compression/v3_hierarchical_memory.py", "final_ch07_v3")
    mem = ch07.Memory(working=[
        "topic=final integration",
        "chapter=07",
        "need short prompt",
        "todo=add tests",
        "style=beginner",
    ])
    ch07.compact_memory(mem, working_limit=2)
    compressed_prompt = ch07.memory_prompt(mem)

    # chapter 08: concurrency
    ch08 = _load_module("chapters/08_concurrency/v3_parallel_execution.py", "final_ch08_v3")
    async_results = asyncio.run(ch08.run_parallel([("A", 0.01), ("B", 0.01)], timeout=1.0))

    # chapter 09: multi-agent collaboration
    ch09_v2 = _load_module("chapters/09_multi_agent/v2_multi_agent_centralized.py", "final_ch09_v2")
    ch09_v3 = _load_module("chapters/09_multi_agent/v3_decentralized.py", "final_ch09_v3")
    centralized_logs = ch09_v2.run_centralized(["build ui", "implement api"])
    decentralized_logs = ch09_v3.decentralized_run()

    # chapter 10: safety
    ch10 = _load_module("chapters/10_safety_sandbox/v3_permission_system.py", "final_ch10_v3")
    safety_decision, safety_record = ch10.enforce("rm -rf /tmp/demo")

    return {
        "ch01_action": action,
        "ch02_write": write_out,
        "ch02_read": read_out,
        "ch03_prompt_preview": prompt_preview,
        "ch04_final": react_final,
        "ch04_steps": len(react_trace),
        "ch05_status": correction_status,
        "ch05_logs": correction_logs,
        "ch06_answer": rag_answer,
        "ch07_prompt": compressed_prompt,
        "ch08_results": async_results,
        "ch09_centralized": centralized_logs,
        "ch09_decentralized": decentralized_logs,
        "ch10_decision": safety_decision,
        "ch10_audit": str(safety_record),
    }


def main() -> None:
    result = run_full_demo()
    print("=== ClaudCode Full Demo ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
