# Final Integration Architecture (`final/claudcode_full.py`)

本文档描述最终集成 Demo 的执行路径，帮助你把 10 章机制串成一条完整链路。

## 1) 端到端流程（高层）

```text
User Goal
   |
   v
[Ch01 Perception/Think/Act baseline]
   |
   v
[Ch02 Tool Registry Dispatch]
   |
   v
[Ch03 Short-term Memory Window]
   |
   v
[Ch04 ReAct Reasoning Loop]
   |
   v
[Ch05 Reflective Retry]
   |
   v
[Ch06 External Memory (RAG)]
   |
   v
[Ch07 Context Compression]
   |
   v
[Ch08 Concurrency (Async Parallel)]
   |
   v
[Ch09 Multi-Agent Collaboration]
   |
   v
[Ch10 Safety Policy + Audit]
   |
   v
Structured Demo Output (dict)
```

## 2) 模块装配方式

`final/claudcode_full.py` 不直接 import 各章节模块名，而是通过动态加载：

- `_load_module(relative_path, alias)`
- 使用 `importlib.util.spec_from_file_location`
- 将模块注册到 `sys.modules[alias]`

这样做的目的是避免跨章节同名文件（如多个 `v1_*.py`）造成导入冲突。

## 3) 各章节在 final 中的职责

1. **Ch01**：基于用户意图给出初始 action。
2. **Ch02**：通过 registry 执行具体工具（读写文件）。
3. **Ch03**：把消息历史裁剪成可控窗口，生成 prompt 预览。
4. **Ch04**：通过 ReAct 循环完成“思考-行动-观察”。
5. **Ch05**：失败后反思并调整重试策略。
6. **Ch06**：从外部知识中检索并拼接上下文回答。
7. **Ch07**：把历史压缩到 summary/facts/working 三层。
8. **Ch08**：并发执行异步任务，演示性能收益。
9. **Ch09**：展示 centralized 与 decentralized 两种协作模式。
10. **Ch10**：执行前做风险分级与权限决策，生成审计记录。

## 4) 运行与验证

```bash
python final/claudcode_full.py
pytest tests/test_final_integration.py -q
```

如果你要扩展 final：
- 优先保持“每章一个明确职责”的可解释结构。
- 避免把所有逻辑堆进一个函数；保留章节边界有助于教学。
