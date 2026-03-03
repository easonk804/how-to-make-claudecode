# 第03章练习题：短期记忆

## 基础题
- 在 `v2_simple_history.py` 实现 `reset_memory()`。
- 重置后再次对话，应看不到旧上下文。

## 进阶题
- 在 `v3_window_management.py` 支持“固定记忆点”（永不删除）。
- 例如：system prompt 和用户偏好标签始终保留。

## 挑战题
- 实现“按重要性打分”的窗口裁剪，而不是简单按时间裁剪。

## 可选进阶（v3）
1. 增加 `estimate_tokens(messages)`，按 token 预算进行裁剪。
2. 为裁剪策略增加模式：`recent_first` / `important_first`。
3. 补充测试：验证 system 消息与固定记忆点不会被裁掉。
