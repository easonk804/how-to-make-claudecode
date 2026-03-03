# 第06章练习题：外部记忆（RAG）

## 基础题
- 在 `v2_keyword_search.py` 或 `v3_embedding_rag.py` 中实现 TF-IDF 检索版本。

## 进阶题
- 实现文档分块（chunking）并比较不同 `top_k` 的召回效果。

## 挑战题
- 支持增量更新索引：新增文档后无需重建全部向量。

## 可选进阶（v3）
1. 增加 rerank 阶段：先粗召回，再精排。
2. 输出检索解释信息（命中文档、相似度分数）。
3. 增加离线评估脚本（precision@k / recall@k）。
