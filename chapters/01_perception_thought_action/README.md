# 第01章：Agent 的本质 - 感知、思考、行动循环

本章目标：从零理解 Agent 的最小内核，不追求复杂功能，只关注循环本身。

## 1) 问题引入（为什么加这个机制）

普通脚本是一次性执行：输入 -> 处理 -> 输出 -> 结束。

但 Agent 需要：
- 根据用户输入思考动作
- 执行动作并观察结果
- 再基于结果继续思考

也就是一个持续循环，而不是一次函数调用。

## 2) 最小实现（几十行可跑）

- `v1_hardcoded.py`
- 不接 LLM，只用规则写死思考逻辑
- 用最短代码演示 observe -> think -> act

运行：

```bash
python chapters/01_perception_thought_action/v1_hardcoded.py
```

## 3) 逐步完善（v1 -> v2 -> v3）

### v1: `v1_hardcoded.py`
- 思考逻辑是 if/else
- 优点：易懂
- 缺点：不灵活

### v2: `v2_with_llm.py`
- 用 LLM 决定动作（JSON）
- 仍然只执行一轮（非循环）

### v3: `v3_complete_loop.py`
- 增加 agent_loop
- 每次工具执行结果回注 messages
- 直到模型不再调用工具

## 4) 可视化（ASCII）

```text
用户请求
   |
   v
[Observe]
   |
   v
[Think] --(选择动作)--> [Act]
   ^                    |
   |                    v
   +------(结果回注)-----+

当模型停止调用工具时，循环结束。
```

## 5) 练习题

见 `exercises.md`。

建议顺序：
1. 先做基础题（给 v1 增加 read）
2. 再做进阶题（v2 支持 append）
3. 最后做挑战题（v3 限制最大循环步数）

## 快速验证

```bash
pytest chapters/01_perception_thought_action/test_chapter01.py -q
```

如果你没有安装 `anthropic`，第01章测试也能跑（测试只覆盖本地逻辑）。
