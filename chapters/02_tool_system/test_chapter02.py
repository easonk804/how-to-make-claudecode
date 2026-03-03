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

v1_hardcoded = _load_local_module("v1_hardcoded.py", "chapter02_v1_hardcoded")
v2_llm_selection = _load_local_module("v2_llm_selection.py", "chapter02_v2_llm_selection")
v3_registry_pattern = _load_local_module("v3_registry_pattern.py", "chapter02_v3_registry_pattern")

execute_v1 = v1_hardcoded.execute_tool
route_tool = v1_hardcoded.route_tool
parse_tool_call = v2_llm_selection.parse_tool_call
_safe_join = v3_registry_pattern._safe_join
build_registry = v3_registry_pattern.build_registry


def test_route_tool_keywords() -> None:
    assert route_tool("please read file") == "read_file"
    assert route_tool("please write file") == "write_file"
    assert route_tool("please delete file") == "unknown"


def test_v1_execute_write_then_read(tmp_path: Path) -> None:
    assert execute_v1("write_file", tmp_path) == "wrote demo.txt"
    content = execute_v1("read_file", tmp_path)
    assert "hello from v1" in content


def test_parse_tool_call_invalid_json() -> None:
    tool_name, args = parse_tool_call("not json")
    assert tool_name == "unknown"
    assert args == {}


def test_registry_dispatch_and_unknown(tmp_path: Path) -> None:
    registry = build_registry(tmp_path)

    out1 = registry.dispatch("write_file", path="a.txt", content="hi")
    out2 = registry.dispatch("read_file", path="a.txt")
    out3 = registry.dispatch("missing_tool", x=1)

    assert out1.startswith("wrote:")
    assert out2 == "hi"
    assert out3.startswith("unknown tool")


def test_safe_join_blocks_escape(tmp_path: Path) -> None:
    try:
        _safe_join(tmp_path, "../evil.txt")
        assert False, "should reject path escape"
    except ValueError:
        assert True
