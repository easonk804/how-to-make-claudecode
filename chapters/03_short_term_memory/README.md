# 第03章：短期记忆（Short-term Memory）

## 1) 问题引入
没有消息历史，Agent 无法理解“继续刚才的任务”。

典型症状：
- 用户说“继续”，Agent 却像第一次见到问题。
- 对话越长，消息无限增长，成本上升且容易超上下文窗口。

## 2) 最小实现
- `v1_no_memory.py`: 每次独立调用

运行：
```bash
python chapters/03_short_term_memory/v1_no_memory.py
```

你会看到每次调用互不关联，完全不记得历史。

## 3) 逐步完善
- `v2_simple_history.py`: 维护 messages
- `v3_window_management.py`: 滑动窗口

### v2 核心改进
- 将 user/assistant 消息持续 append 到 history。
- 能回答“接着上次说”的问题，但历史会无限变长。

运行：
```bash
python chapters/03_short_term_memory/v2_simple_history.py
```

### v3 核心改进
- 保留系统提示 + 最近 N 轮对话。
- 超出窗口自动裁剪旧消息，控制 token 成本。

运行：
```bash
python chapters/03_short_term_memory/v3_window_management.py
```

预期现象：
- 历史不再无限膨胀。
- 最近对话保留，旧消息被平滑淘汰。

## 4) 可视化
```text
v1
Request A -> Response A
Request B -> Response B   (A 的信息丢失)

v2
messages = [system, user1, assistant1, user2, assistant2, ...]
              (可记忆，但无限增长)

v3
messages = [system] + recent_k_turns
old messages --> trimmed
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v2 增加 `reset_memory()` 并测试。
2. 在 v3 增加“按 token 估算”而不是“按轮数裁剪”。
3. 为窗口裁剪策略增加可配置参数（不同任务不同窗口）。
