from pathlib import Path
import importlib.util


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v1_fail_stop = _load_local_module("v1_fail_stop.py", "chapter05_v1_fail_stop")
v2_simple_retry = _load_local_module("v2_simple_retry.py", "chapter05_v2_simple_retry")
v3_reflective_retry = _load_local_module("v3_reflective_retry.py", "chapter05_v3_reflective_retry")

run_step = v1_fail_stop.run_step
run_task_fail_stop = v1_fail_stop.run_task_fail_stop
run_with_retry = v2_simple_retry.run_with_retry
classify_error = v3_reflective_retry.classify_error
reflective_retry = v3_reflective_retry.reflective_retry
run_with_reflection = v3_reflective_retry.run_with_reflection


def test_v1_fail_stop_raises_on_unstable_step() -> None:
    try:
        run_task_fail_stop(["prepare", "unstable_step", "finalize"])
        assert False, "should stop on first failure"
    except RuntimeError as exc:
        assert "unstable_step" in str(exc)


def test_v1_run_step_success() -> None:
    assert run_step("prepare") == "ok: prepare"


def test_v2_retry_eventual_success() -> None:
    result, logs = run_with_retry(max_retries=3, fail_until=2)
    assert result == "ok on attempt 3"
    assert len(logs) == 3


def test_v2_retry_failure_when_budget_small() -> None:
    result, logs = run_with_retry(max_retries=1, fail_until=3)
    assert result == "failed"
    assert len(logs) == 2


def test_v3_error_classification() -> None:
    assert classify_error("file not found") == "not_found"
    assert classify_error("permission denied") == "permission"
    assert classify_error("network timeout") == "timeout"
    assert classify_error("other") == "unknown"


def test_v3_reflective_retry_plan() -> None:
    plan = reflective_retry(["permission denied"])
    assert "writable path" in plan


def test_v3_run_with_reflection_success() -> None:
    status, trace = run_with_reflection(
        simulated_errors=["file not found", "permission denied"],
        max_retries=4,
    )
    assert status == "success"
    assert any("plan:" in line for line in trace)
