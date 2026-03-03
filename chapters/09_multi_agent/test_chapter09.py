from pathlib import Path
import importlib.util
import sys


def _load_local_module(module_filename: str, alias: str):
    path = Path(__file__).resolve().parent / module_filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {module_filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


v1_single_agent = _load_local_module("v1_single_agent.py", "chapter09_v1_single")
v2_multi_agent_centralized = _load_local_module("v2_multi_agent_centralized.py", "chapter09_v2_centralized")
v3_decentralized = _load_local_module("v3_decentralized.py", "chapter09_v3_decentralized")

do_all_tasks = v1_single_agent.do_all_tasks
assign = v2_multi_agent_centralized.assign
run_centralized = v2_multi_agent_centralized.run_centralized
Agent = v3_decentralized.Agent
decentralized_run = v3_decentralized.decentralized_run


def test_v1_single_agent_handles_all_tasks() -> None:
    logs = do_all_tasks("发布待办应用")
    assert logs[0].startswith("goal:")
    assert any("single_agent handles" in line for line in logs)
    assert logs[-1] == "single_agent done"


def test_v2_assign_and_run_centralized() -> None:
    assert assign("build ui") == "frontend_agent"
    assert assign("implement api") == "backend_agent"
    assert assign("add test") == "test_agent"

    logs = run_centralized(["build ui", "implement api"])
    assert any("coordinator ->" in line for line in logs)
    assert logs[-1] == "coordinator: all tasks completed"


def test_v3_agent_send_process() -> None:
    alice = Agent("alice")
    bob = Agent("bob")
    alice.send(bob, "hello")
    out = bob.process_once()
    assert "from alice" in out


def test_v3_decentralized_run() -> None:
    logs = decentralized_run()
    assert any("processed" in line for line in logs)
    assert any("idle" in line for line in logs)
