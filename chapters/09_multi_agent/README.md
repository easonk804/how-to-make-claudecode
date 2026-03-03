# 第09章：多 Agent 协作（Multi-Agent）

## 1) 问题引入
复杂任务单 Agent 容易上下文混乱，需要分工协作。

典型症状：
- 一个 Agent 同时做前端、后端、测试，提示词越来越长。
- 失败时很难定位是谁出错、哪一步出错。

## 2) 最小实现
- `v1_single_agent.py`: 单体模式

运行：
```bash
python chapters/09_multi_agent/v1_single_agent.py
```

你会看到所有子任务都由 `single_agent` 顺序处理。

## 3) 逐步完善
- `v2_multi_agent_centralized.py`: 中央协调
- `v3_decentralized.py`: 去中心化消息传递

### v2 核心改进（中央协调）
- 协调者根据任务类型分配给专门 Agent。
- 责任边界更清晰，便于扩展更多角色。

运行：
```bash
python chapters/09_multi_agent/v2_multi_agent_centralized.py
```

预期输出包含：
- `coordinator -> frontend_agent`
- `coordinator -> backend_agent`
- `coordinator: all tasks completed`

### v3 核心改进（去中心化）
- Agent 之间可直接发消息，不必每次经过中心节点。
- 更接近真实分布式协作，但调试复杂度上升。

运行：
```bash
python chapters/09_multi_agent/v3_decentralized.py
```

预期输出会有：
- `processed -> from ...`
- 无消息时显示 `idle`

## 4) 可视化
```text
v1 (single agent)
Task List -> One Agent -> One Agent -> One Agent -> Result

v2 (centralized)
                -> Frontend Agent -\
Coordinator --->  Backend Agent  ---> Integrate -> Result
                ->   Test Agent  -/

v3 (decentralized)
Agent A <----> Agent B <----> Agent C
   \_____________________________/
      peer-to-peer messages
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v2 增加 `data_agent` 并添加分配规则。
2. 在 v3 增加消息 `id` 与去重逻辑。
3. 记录每个 Agent 的处理耗时和失败重试次数。
