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


v1_hardcoded_knowledge = _load_local_module("v1_hardcoded_knowledge.py", "chapter06_v1_hardcoded")
v2_keyword_search = _load_local_module("v2_keyword_search.py", "chapter06_v2_keyword")
v3_embedding_rag = _load_local_module("v3_embedding_rag.py", "chapter06_v3_rag")

answer = v1_hardcoded_knowledge.answer
retrieve_keyword = v2_keyword_search.retrieve
answer_with_retrieval = v2_keyword_search.answer_with_retrieval
embed_text = v3_embedding_rag.embed_text
build_index = v3_embedding_rag.build_index
retrieve_rag = v3_embedding_rag.retrieve
answer_with_rag = v3_embedding_rag.answer_with_rag
cosine = v3_embedding_rag.cosine


def test_v1_hardcoded_answer_contains_fixed_knowledge() -> None:
    out = answer("函数怎么命名")
    assert "A(硬编码)" in out
    assert "snake_case" in out


def test_v2_keyword_retrieve_and_answer() -> None:
    hits = retrieve_keyword("命名 注释", top_k=2)
    assert len(hits) >= 1
    out = answer_with_retrieval("命名规范")
    assert "检索结果" in out


def test_v3_embedding_and_cosine() -> None:
    a = embed_text("命名 注释")
    b = embed_text("命名")
    score = cosine(a, b)
    assert 0.0 <= score <= 1.0


def test_v3_rag_retrieval_and_answer() -> None:
    docs = [
        "函数和变量命名推荐使用 snake_case。",
        "文件读写建议显式指定 utf-8。",
        "公共函数建议写 docstring。",
    ]
    index = build_index(docs)
    hits = retrieve_rag("命名 规范", index, top_k=2)
    assert len(hits) >= 1
    out = answer_with_rag("命名 规范", index)
    assert "Top-K 检索" in out
