# 第07章：上下文压缩（Context Compression）

## 1) 问题引入
对话越长，token 越贵且会超窗；不能只靠硬删除。

典型症状：
- 前面说过的重要约束（如风格、路径、目标）在长对话中被“挤掉”。
- 为了省 token 直接截断，导致模型忘记关键背景。

## 2) 最小实现
- `v1_truncation.py`: 超限后直接截断

运行：
```bash
python chapters/07_context_compression/v1_truncation.py
```

你会看到“只保留最近消息”的策略，简单但容易丢失长期信息。

## 3) 逐步完善
- `v2_naive_summarization.py`: 摘要旧消息
- `v3_hierarchical_memory.py`: 分层记忆

### v2 核心改进
- 把旧消息合并成摘要，最近消息保持原文。
- 比纯截断更稳，但摘要质量依赖规则。

运行：
```bash
python chapters/07_context_compression/v2_naive_summarization.py
```

### v3 核心改进
- 把记忆分成三层：working / summary / facts。
- 超出 working 容量时，旧信息进入 summary，并提取结构化事实。

运行：
```bash
python chapters/07_context_compression/v3_hierarchical_memory.py
```

预期输出会包含：
- `Summary: ...`
- `Facts: key=value ...`
- `Working:` 最近上下文

## 4) 可视化
```text
v1
all messages -> keep last N -> prompt

v2
old messages -> summary text
recent messages -> raw text
summary + recent -> prompt

v3 (hierarchical memory)
overflow -> [Summary Layer]
overflow key=value -> [Fact Layer]
recent turns -> [Working Layer]

Prompt = Summary + Facts + Working
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v2 增加“摘要长度上限”控制。
2. 在 v3 为 facts 增加“冲突解决策略”（新值覆盖/保留历史）。
3. 给 v3 增加按主题检索历史摘要的能力。
