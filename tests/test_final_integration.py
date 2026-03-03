from pathlib import Path
import importlib.util
import sys


def _load_local_module(module_path: Path, alias: str):
    spec = importlib.util.spec_from_file_location(alias, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


root = Path(__file__).resolve().parents[1]
full_path = root / "final" / "claudcode_full.py"
full_mod = _load_local_module(full_path, "final_claudcode_full")

run_full_demo = full_mod.run_full_demo


def test_run_full_demo_output_shape() -> None:
    out = run_full_demo()

    required = {
        "ch01_action",
        "ch02_write",
        "ch02_read",
        "ch03_prompt_preview",
        "ch04_final",
        "ch05_status",
        "ch06_answer",
        "ch07_prompt",
        "ch08_results",
        "ch09_centralized",
        "ch09_decentralized",
        "ch10_decision",
    }
    assert required.issubset(out.keys())

    assert out["ch01_action"] == "create_file"
    assert isinstance(out["ch08_results"], list)
    assert out["ch10_decision"] == "blocked"
