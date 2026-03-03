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


v1_truncation = _load_local_module("v1_truncation.py", "chapter07_v1_truncation")
v2_naive_summarization = _load_local_module("v2_naive_summarization.py", "chapter07_v2_summarization")
v3_hierarchical_memory = _load_local_module("v3_hierarchical_memory.py", "chapter07_v3_hierarchical")

truncate = v1_truncation.truncate
summarize_text = v2_naive_summarization.summarize_text
summarize_old = v2_naive_summarization.summarize_old
Memory = v3_hierarchical_memory.Memory
extract_fact = v3_hierarchical_memory.extract_fact
compact_memory = v3_hierarchical_memory.compact_memory
memory_prompt = v3_hierarchical_memory.memory_prompt


def test_v1_truncate_keep_last() -> None:
    data = [f"m{i}" for i in range(1, 8)]
    assert truncate(data, keep_last=3) == ["m5", "m6", "m7"]
    assert truncate(data, keep_last=0) == []


def test_v2_summarize_text_and_old() -> None:
    data = [f"m{i}" for i in range(1, 10)]
    summary = summarize_text(data, keep_recent=3)
    assert "old=6" in summary

    compressed = summarize_old(data, keep_recent=3, trigger_threshold=6)
    assert len(compressed) == 4
    assert compressed[0].startswith("[summary]")


def test_v3_extract_fact() -> None:
    assert extract_fact("topic=agent") == ("topic", "agent")
    assert extract_fact("no fact here") is None


def test_v3_compact_memory_and_prompt() -> None:
    mem = Memory(
        working=[
            "topic=agent tutorial",
            "chapter=07",
            "need compression",
            "todo=write tests",
            "style=beginner",
        ]
    )
    compact_memory(mem, working_limit=2)

    assert len(mem.working) == 2
    assert mem.summary
    assert mem.facts.get("topic") == "agent tutorial"

    prompt = memory_prompt(mem)
    assert "Summary:" in prompt
    assert "Facts:" in prompt
    assert "Working:" in prompt
