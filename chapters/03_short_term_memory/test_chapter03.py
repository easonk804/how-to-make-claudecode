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


v1_no_memory = _load_local_module("v1_no_memory.py", "chapter03_v1_no_memory")
v2_simple_history = _load_local_module("v2_simple_history.py", "chapter03_v2_simple_history")
v3_window_management = _load_local_module("v3_window_management.py", "chapter03_v3_window_management")

chat_once = v1_no_memory.chat_once
chat = v2_simple_history.chat
messages = v2_simple_history.messages
reset_memory = v2_simple_history.reset_memory
add_turn = v3_window_management.add_turn
build_prompt = v3_window_management.build_prompt
trim_messages = v3_window_management.trim_messages


def test_v1_stateless_continue() -> None:
    reply = chat_once("继续刚才任务")
    assert "没有保存历史" in reply


def test_v2_history_continue() -> None:
    reset_memory()
    chat("请帮我做旅行计划")
    reply = chat("继续刚才的任务")
    assert "你在继续" in reply
    assert len(messages) == 4


def test_v2_reset_memory() -> None:
    reset_memory()
    chat("hello")
    assert len(messages) == 2
    reset_memory()
    assert len(messages) == 0


def test_v3_trim_messages_keeps_system_and_recent_rounds() -> None:
    history = [{"role": "system", "content": "S"}]
    for i in range(1, 6):
        add_turn(history, f"u{i}", f"a{i}")

    trimmed = trim_messages(history, keep_rounds=2)
    assert trimmed[0]["role"] == "system"
    assert len(trimmed) == 5
    assert trimmed[-1]["content"] == "a5"


def test_v3_build_prompt_contains_recent_turns() -> None:
    history = [{"role": "system", "content": "S"}]
    for i in range(1, 4):
        add_turn(history, f"u{i}", f"a{i}")

    prompt = build_prompt(history, keep_rounds=1)
    assert "u3" in prompt and "a3" in prompt
    assert "u1" not in prompt
