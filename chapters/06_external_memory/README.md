# 第06章：外部记忆（RAG）

## 1) 问题引入
模型参数不是你的私有知识库，需把知识外置并可检索。

典型症状：
- 你问项目私有规范，模型回答“看起来对”但经常不准确。
- 知识更新后，模型仍然沿用旧结论。

## 2) 最小实现
- `v1_hardcoded_knowledge.py`: 知识硬编码

运行：
```bash
python chapters/06_external_memory/v1_hardcoded_knowledge.py
```

你会看到固定回答，不随具体问题变化。

## 3) 逐步完善
- `v2_keyword_search.py`: 关键词检索
- `v3_embedding_rag.py`: 向量检索骨架

### v2 核心改进
- 从文档集合中按关键词匹配候选片段。
- 结果比硬编码更贴近问题，但召回能力有限。

运行：
```bash
python chapters/06_external_memory/v2_keyword_search.py
```

### v3 核心改进
- 把 query/doc 转向量，按相似度检索 Top-K。
- 支持语义近似，减少“关键词没命中就失败”的情况。

运行：
```bash
python chapters/06_external_memory/v3_embedding_rag.py
```

预期输出包含：
- `Q: ...`
- `Top-K 检索:`
- 若无命中则提示补充文档

## 4) 可视化
```text
v1
query -> fixed string answer

v2
query -> keyword match -> top docs -> answer

v3 (RAG)
query -> embed -> vector search(top-k) -> build context -> answer
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 给 v2 增加简单打分（关键词频次 + 文档长度惩罚）。
2. 给 v3 增加 `top_k` 可配置项并测试边界值。
3. 增加文档切片（chunking）并比较检索效果。
