# 第04章：Chain-of-Thought 与 ReAct

## 1) 问题引入
直接给答案容易错，显式推理有助于降低错误。

典型症状：
- 模型“看起来很自信”，但中间推理路径不可靠。
- 遇到外部事实或环境问题（缺依赖、路径错）时，无法自我验证。

## 2) 最小实现
- `v1_direct_answer.py`: 直接回答

运行：
```bash
python chapters/04_chain_of_thought/v1_direct_answer.py
```

你会得到一个一步到位的回答，但没有中间推理与校验过程。

## 3) 逐步完善
- `v2_cot_prompting.py`: 先分析再执行
- `v3_react_pattern.py`: Thought -> Action -> Observation

### v2 核心改进
- 把问题拆成可解释的步骤（先分析，再结论）。
- 结果更稳定，也更方便排查错误。

运行：
```bash
python chapters/04_chain_of_thought/v2_cot_prompting.py
```

### v3 核心改进
- 在“思考”之外加入“行动”和“观察”。
- 让模型通过工具反馈逐步逼近正确答案。

运行：
```bash
python chapters/04_chain_of_thought/v3_react_pattern.py
```

预期输出会包含：
- `Thought:`
- `Action:`
- `Observation:`
- 最终修复结论

## 4) 可视化
```text
v1
Question -> Direct Answer

v2
Question -> Step1 Analysis -> Step2 Plan -> Final Answer

v3 (ReAct loop)
Thought -> Action(tool) -> Observation
   ^                            |
   +----------------------------+
(直到得到可接受结论或达到最大步数)
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v2 增加“每步置信度”字段。
2. 在 v3 增加一个新工具（如 `check_python_version`）。
3. 为 v3 增加最大步数超限后的降级策略。
