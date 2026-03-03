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


v1_no_protection = _load_local_module("v1_no_protection.py", "chapter10_v1_no_protection")
v2_blacklist_whitelist = _load_local_module("v2_blacklist_whitelist.py", "chapter10_v2_blacklist")
v3_permission_system = _load_local_module("v3_permission_system.py", "chapter10_v3_permission")

run = v1_no_protection.run
run_batch = v1_no_protection.run_batch
is_safe = v2_blacklist_whitelist.is_safe
run_guarded = v2_blacklist_whitelist.run_guarded
classify = v3_permission_system.classify
enforce = v3_permission_system.enforce
run_commands = v3_permission_system.run_commands


def test_v1_no_protection_accepts_any_command() -> None:
    out = run("rm -rf /tmp/demo")
    assert "INSECURE" in out

    batch = run_batch(["ls", "rm -rf /tmp/demo"])
    assert len(batch) == 2


def test_v2_blacklist_whitelist_guard() -> None:
    assert is_safe("ls -la") is True
    assert is_safe("rm -rf tmp") is False
    assert is_safe("powershell -c whoami") is False

    assert run_guarded("python app.py").startswith("allowed")
    assert run_guarded("rm -rf tmp").startswith("blocked")


def test_v3_classify_levels() -> None:
    assert classify("mkdir demo") == "normal"
    assert classify("sudo apt update") == "system"
    assert classify("rm -rf /tmp/demo") == "dangerous"


def test_v3_enforce_and_audit() -> None:
    decision, record = enforce("sudo apt update", auto_confirm_system=False)
    assert decision == "needs_confirmation"
    assert record.level == "system"

    decision2, record2 = enforce("mkdir demo")
    assert decision2 == "allowed"
    assert record2.level == "normal"


def test_v3_run_commands() -> None:
    records = run_commands(["mkdir demo", "sudo apt update", "rm -rf /tmp/demo"])
    assert len(records) == 3
    assert any(r.decision == "blocked" for r in records)
