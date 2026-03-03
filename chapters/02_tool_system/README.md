# 第02章：工具系统（Tool System）

## 1) 问题引入
如果所有动作都写在 if/elif 中，Agent 很快会失控且难维护。

典型症状：
- 新增一个工具就要改主流程代码。
- 工具越多，分支越长，测试越难写。

## 2) 最小实现
- `v1_hardcoded.py`: 硬编码工具选择

运行：
```bash
python chapters/02_tool_system/v1_hardcoded.py
```

你会看到基于关键词的固定路由，适合教学但不易扩展。

## 3) 逐步完善
- `v2_llm_selection.py`: LLM 输出工具名
- `v3_registry_pattern.py`: 工具注册表 + 分发

### v2 核心改进
- 把“选择工具”交给模型（或模拟模型输出）。
- 增加 JSON 解析与兜底逻辑，降低格式错误导致的崩溃风险。

运行：
```bash
python chapters/02_tool_system/v2_llm_selection.py
```

### v3 核心改进
- 用注册表维护工具，而不是写死在 if/elif。
- 支持统一 dispatch，便于动态注册与权限控制。

运行：
```bash
python chapters/02_tool_system/v3_registry_pattern.py
```

预期输出会包含：
- `wrote:` 或 `read:` 之类的工具执行结果
- 非法路径被拒绝（沙箱路径检查）

## 4) 可视化
```text
v1
user input -> if/elif router -> hardcoded function

v2
user input -> LLM/mocked planner -> {tool, args} -> executor

v3
user input -> planner -> registry.dispatch(tool, **args) -> tool result
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v1 增加第三个工具，体验维护成本。
2. 在 v2 增加 JSON 解析失败的 fallback。
3. 在 v3 增加 `list_files` 工具并补充测试。
