from pathlib import Path
import importlib.util
import sys
import asyncio


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


v1_blocking = _load_local_module("v1_blocking.py", "chapter08_v1_blocking")
v2_background_task = _load_local_module("v2_background_task.py", "chapter08_v2_background")
v3_parallel_execution = _load_local_module("v3_parallel_execution.py", "chapter08_v3_parallel")

run_blocking = v1_blocking.run_blocking
run_in_background = v2_background_task.run_in_background
run_parallel = v3_parallel_execution.run_parallel
run_sequential = v3_parallel_execution.run_sequential


def test_v1_blocking_runs_all_tasks() -> None:
    results, elapsed = run_blocking(["A", "B"], delay=0.01)
    assert results == ["A done", "B done"]
    assert elapsed >= 0.0


def test_v2_background_has_progress_and_done() -> None:
    logs = run_in_background("index_docs")
    assert any("progress" in line for line in logs)
    assert any("done" in line for line in logs)


def test_v3_parallel_and_sequential() -> None:
    tasks = [("A", 0.01), ("B", 0.01)]

    seq = asyncio.run(run_sequential(tasks))
    par = asyncio.run(run_parallel(tasks, timeout=1.0))

    assert seq == ["A done", "B done"]
    assert par == ["A done", "B done"]


def test_v3_parallel_timeout() -> None:
    tasks = [("A", 0.05), ("B", 0.05)]
    out = asyncio.run(run_parallel(tasks, timeout=0.001))
    assert out == ["timeout"]
