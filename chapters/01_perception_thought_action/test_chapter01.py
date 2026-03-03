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

v1_hardcoded = _load_local_module("v1_hardcoded.py", "chapter01_v1_hardcoded")
v3_complete_loop = _load_local_module("v3_complete_loop.py", "chapter01_v3_complete_loop")

hardcoded_act = v1_hardcoded.hardcoded_act
hardcoded_think = v1_hardcoded.hardcoded_think
_safe_join = v3_complete_loop._safe_join
run_append = v3_complete_loop.run_append
run_create = v3_complete_loop.run_create
run_read = v3_complete_loop.run_read


def test_hardcoded_think_create_keyword() -> None:
    action, target = hardcoded_think("请帮我创建文件")
    assert action == "create_file"
    assert target == "test.txt"


def test_hardcoded_act_create_file(tmp_path: Path) -> None:
    out = hardcoded_act("create_file", "a.txt", tmp_path)
    assert "created:" in out
    assert (tmp_path / "a.txt").exists()


def test_safe_join_blocks_escape(tmp_path: Path) -> None:
    try:
        _safe_join(tmp_path, "../evil.txt")
        assert False, "should reject path escape"
    except ValueError:
        assert True


def test_run_create_append_read(tmp_path: Path) -> None:
    assert run_create(tmp_path, "demo.txt", "line1\n").startswith("created")
    assert run_append(tmp_path, "demo.txt", "line2\n").startswith("appended")
    text = run_read(tmp_path, "demo.txt")
    assert "line1" in text and "line2" in text
