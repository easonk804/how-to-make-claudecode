from pathlib import Path


CHAPTERS = [
    "01_perception_thought_action",
    "02_tool_system",
    "03_short_term_memory",
    "04_chain_of_thought",
    "05_self_correction",
    "06_external_memory",
    "07_context_compression",
    "08_concurrency",
    "09_multi_agent",
    "10_safety_sandbox",
]


def test_chapter_directories_exist() -> None:
    root = Path(__file__).resolve().parents[1] / "chapters"
    for name in CHAPTERS:
        assert (root / name).exists(), f"missing chapter dir: {name}"
