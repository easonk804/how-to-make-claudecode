# 第07章练习题：上下文压缩

## 基础题
- 在 `v2_naive_summarization.py` 中实现“消息超过 N 时自动摘要”。

## 进阶题
- 保留最近 3 轮完整消息，其余内容进入 summary。

## 挑战题
- 在 `v3_hierarchical_memory.py` 中提取关键事实写入 `fact memory`。

## 可选进阶（v3）
1. 为 summary 增加长度预算（超限时二次压缩）。
2. 为 facts 增加冲突处理策略（覆盖 / 追加版本历史）。
3. 增加测试：验证 compaction 前后关键信息不丢失。
