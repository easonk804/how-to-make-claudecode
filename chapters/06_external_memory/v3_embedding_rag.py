#!/usr/bin/env python3
"""Chapter 06 v3: embedding-style RAG (local demo, no external API).

What changed from v2:
- v2: keyword match only
- v3: embed query/doc -> vector similarity -> top-k retrieval
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Doc:
    text: str
    vector: list[float]


FEATURE_WORDS = [
    "命名",
    "注释",
    "异常",
    "编码",
    "历史",
    "安全",
]


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def embed_text(text: str) -> list[float]:
    """Very small local embedding function for teaching purpose."""
    normalized = text.lower()
    return [float(normalized.count(word)) for word in FEATURE_WORDS]


def build_index(texts: list[str]) -> list[Doc]:
    return [Doc(text=t, vector=embed_text(t)) for t in texts]


def retrieve(query: str, index: list[Doc], top_k: int = 2) -> list[Doc]:
    qv = embed_text(query)
    scored = [(cosine(qv, doc.vector), doc) for doc in index]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored if score > 0][:top_k]


def answer_with_rag(query: str, index: list[Doc]) -> str:
    hits = retrieve(query, index, top_k=2)
    if not hits:
        return "未检索到相关知识，请补充文档或改写问题。"

    context = "\n".join(f"- {doc.text}" for doc in hits)
    return f"Q: {query}\nTop-K 检索:\n{context}"


def load_sample_docs() -> list[str]:
    root = Path(__file__).resolve().parents[2]
    kb_file = root / "knowledge_base" / "python_best_practices.md"
    if not kb_file.exists():
        return ["函数和变量命名使用 snake_case。", "文件读写显式指定 utf-8。"]

    lines = [line.strip("- ").strip() for line in kb_file.read_text(encoding="utf-8").splitlines()]
    return [line for line in lines if line and not line.startswith("#")]


if __name__ == "__main__":
    docs = load_sample_docs()
    index = build_index(docs)
    print(answer_with_rag("Python 命名和编码规范", index))
