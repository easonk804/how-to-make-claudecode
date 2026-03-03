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


v1_direct_answer = _load_local_module("v1_direct_answer.py", "chapter04_v1_direct_answer")
v2_cot_prompting = _load_local_module("v2_cot_prompting.py", "chapter04_v2_cot_prompting")
v3_react_pattern = _load_local_module("v3_react_pattern.py", "chapter04_v3_react_pattern")

answer_direct = v1_direct_answer.answer_direct
cot_steps = v2_cot_prompting.cot_steps
solve_with_cot = v2_cot_prompting.solve_with_cot
react_solve = v3_react_pattern.react_solve
run_tool = v3_react_pattern.run_tool


def test_v1_direct_answer_module_error() -> None:
    out = answer_direct("ModuleNotFoundError: requests")
    assert "pip install" in out


def test_v2_cot_steps_structure() -> None:
    steps = cot_steps("ModuleNotFoundError: requests")
    assert len(steps) == 4
    assert steps[0].startswith("1)")
    assert "缺少 Python 依赖包" in steps[1]


def test_v2_solve_with_cot() -> None:
    out = solve_with_cot("Permission denied")
    assert "确认当前用户权限" in out


def test_v3_run_tool_install_then_verify() -> None:
    state: dict[str, object] = {"error_log": "ModuleNotFoundError", "installed": set()}
    assert run_tool("install_requests", state) == "installed requests"
    assert run_tool("verify_fix", state) == "check ok"


def test_v3_react_solve_success() -> None:
    trace, final = react_solve("ModuleNotFoundError: No module named 'requests'")
    assert "修复" in final
    assert any(item.startswith("Thought:") for item in trace)
    assert any(item.startswith("Action:") for item in trace)
    assert any(item.startswith("Observation:") for item in trace)
