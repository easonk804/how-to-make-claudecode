#!/usr/bin/env python3
"""Chapter 06 v2: keyword retrieval.

What changed from v1:
- v1: one hardcoded answer
- v2: retrieve relevant snippets by keyword matching
"""

from __future__ import annotations

KB = {
    "命名": "函数和变量命名推荐使用 snake_case。",
    "注释": "公共函数建议写 docstring，便于维护。",
    "异常": "优先抛出具体异常，不要裸 except。",
    "编码": "文件读写建议显式指定 utf-8。",
}


def keyword_score(query: str, text: str) -> int:
    tokens = [t for t in query.lower().replace("_", " ").split() if t]
    if not tokens:
        return 0
    return sum(1 for token in tokens if token in text.lower())


def retrieve(query: str, top_k: int = 2) -> list[str]:
    scored: list[tuple[int, str]] = []
    for key, snippet in KB.items():
        score = keyword_score(query + " " + key, snippet)
        if key in query:
            score += 2
        if score > 0:
            scored.append((score, snippet))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [snippet for _, snippet in scored[:top_k]]


def answer_with_retrieval(query: str) -> str:
    hits = retrieve(query, top_k=2)
    if not hits:
        return "未命中知识库，请补充更多信息。"
    context = "\n".join(f"- {h}" for h in hits)
    return f"Q: {query}\n检索结果:\n{context}"


if __name__ == "__main__":
    print(answer_with_retrieval("Python 命名和注释规范"))
