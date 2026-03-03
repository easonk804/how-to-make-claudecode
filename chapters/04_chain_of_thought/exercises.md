# 第04章练习题：Chain-of-Thought 与 ReAct

## 基础题
- 在 `v2_cot_prompting.py` 输出结构化的步骤列表（Step1/Step2/Step3）。

## 进阶题
- 在 `v3_react_pattern.py` 中，当 Observation 包含失败关键词时触发新的 Thought。

## 挑战题
- 为 ReAct 循环加入最大推理轮数与终止条件，防止无限循环。

## 可选进阶（v3）
1. 增加 `unknown action` 的恢复策略（自动回退到 `read_error_log`）。
2. 给每一步增加 `confidence` 字段并记录到 trace。
3. 增加测试：覆盖“达到最大步数后安全退出”的行为。
