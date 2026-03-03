# 第05章：自我纠错（Self-Correction）

## 1) 问题引入
Agent 会失败，关键是如何识别失败并调整策略重试。

典型症状：
- 一次失败就直接终止，任务体验差。
- 虽然重试了，但每次都用同一个错误策略，无法收敛。

## 2) 最小实现
- `v1_fail_stop.py`: 出错即停止

运行：
```bash
python chapters/05_self_correction/v1_fail_stop.py
```

你会看到只要一步失败，流程立即中断。

## 3) 逐步完善
- `v2_simple_retry.py`: 固定次数重试
- `v3_reflective_retry.py`: 记录失败原因并调整

### v2 核心改进
- 引入固定次数重试，处理偶发性错误。
- 适合网络抖动等暂时失败，但对“逻辑错误”帮助有限。

运行：
```bash
python chapters/05_self_correction/v2_simple_retry.py
```

### v3 核心改进
- 根据错误类型（not found / permission / timeout）生成不同下一步计划。
- 重试不是“重复”，而是“带策略调整的尝试”。

运行：
```bash
python chapters/05_self_correction/v3_reflective_retry.py
```

预期输出会包含：
- `attempt N: fail=...`
- `attempt N: plan: ...`
- 最终 `success` 或 `failed`

## 4) 可视化
```text
v1
attempt1 -> fail -> stop

v2
attempt1 -> fail -> attempt2 -> fail -> attempt3 -> success/failed
                     (策略不变)

v3
attempt1 -> fail(type A) -> reflect(plan A)
attempt2 -> fail(type B) -> reflect(plan B)
attempt3 -> success
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v2 增加指数退避（backoff）。
2. 在 v3 增加“同类错误连续出现”的特别处理。
3. 给重试过程加结构化日志，便于可视化分析。
