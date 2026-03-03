# 第01章练习题：感知-思考-行动循环

## 基础题
让 `v1_hardcoded.py` 支持第二个动作：
- 用户输入包含“读取/read”时，读取 `sandbox/test.txt` 并输出内容。

## 进阶题
修改 `v2_with_llm.py`：
- 支持动作 `append_file`。
- 如果文件不存在，先创建再追加。

## 挑战题
修改 `v3_complete_loop.py`：
- 在每一轮循环打印 `messages` 长度。
- 增加最大轮数 `max_steps`，防止模型进入无限工具调用。

## 参考思路
1. 基础题：在 `hardcoded_think` 和 `hardcoded_act` 各加一个分支。
2. 进阶题：复用 `execute_action` 里的路径处理逻辑。
3. 挑战题：在 `while True` 外增加计数器并在超限时 `break`。

## 可选进阶（v3）
1. 在循环中记录每一步 `Thought/Action/Observation` 到结构化 trace。
2. 增加“安全终止条件”：当连续两轮 action 相同且 observation 无变化时提前停止。
3. 为 `agent_loop` 增加一条回归测试，覆盖“达到 `max_steps` 后退出”场景。
