# Expected Outputs

This document shows expected outputs when running each chapter's code. Use it to verify your implementation is working correctly.

---

## Chapter 01: Perception-Thought-Action Loop

### v1_hardcoded.py
```
Obs: 用户想创建一个关于 'agent tutorial' 的文件
Think: 我应该创建这个文件
Act: create_file(agent_tutorial.txt)
Action result: success
```

### v2_with_llm.py
```
[LLM-based think/act]
Action: write_file
Path: tutorial.txt
Content: 这是关于 agent tutorial 的内容
```

### v3_complete_loop.py
```
[循环执行，直到任务完成]
> 用户: 帮我创建文件
> Thought: 需要创建文件
> Action: write_file(path='test.txt')
> Observation: 文件已创建
> Thought: 任务完成
> Final: 成功创建文件
```

---

## Chapter 02: Tool System

### v1_hardcoded.py
```
Input: read test.txt
Output: [file content or not found]
```

### v2_llm_selection.py
```
Tool selected: read_file
Args: {'path': 'test.txt'}
Result: [file content]
```

### v3_registry_pattern.py
```
Registering tools...
Dispatch: write_file -> wrote: test.txt
Dispatch: read_file -> [content]
Dispatch: list_dir -> file1.txt, file2.txt
```

---

## Chapter 03: Short-term Memory

### v1_no_memory.py
```
User: 你好
Bot: [固定回复，无上下文]
User: 继续
Bot: [仍然是固定回复]
```

### v2_simple_history.py
```
User: 请帮我做旅行计划
Bot: [with memory] 已记录本轮输入，总消息数=1
User: 继续刚才的任务
Bot: [with memory] 你在继续：请帮我做旅行计划
messages=4
```

### v3_window_management.py
```
Adding messages...
After trim: kept last 4 messages + system prompt
Working memory: 4 items
```

---

## Chapter 04: Chain-of-Thought

### v1_direct_answer.py
```
Problem: 2+3*4
Answer: 14
```

### v2_cot_prompting.py
```
- 1) 分析问题: ModuleNotFoundError: requests
- 2) 诊断根因: 缺少 Python 依赖包
- 3) 设计方案: 定位缺失包名并执行 pip install
- 4) 执行验证: 复现原命令，确认报错消失
建议方案：定位缺失包名并执行 pip install
```

### v3_react_pattern.py
```
Step 1:
  Thought: 需要先查看文件内容
  Action: read_file('data.txt')
  Observation: 文件包含数字 1,2,3

Step 2:
  Thought: 需要计算总和
  Action: calculate_sum([1,2,3])
  Observation: 6

Final Answer: 6
```

---

## Chapter 05: Self-Correction

### v1_fail_stop.py
```
Task: read missing_file.txt
Attempt 1: Error! File not found
Stopping immediately.
```

### v2_simple_retry.py
```
Attempt 1: Failed - retrying...
Attempt 2: Failed - retrying...
Attempt 3: Failed - giving up
Final: failed
```

### v3_reflective_retry.py
```
Attempt 1: fail=FileNotFoundError
New plan: Create file first, then read
Attempt 2: success
Final: success
```

---

## Chapter 06: External Memory (RAG)

### v1_hardcoded_knowledge.py
```
Query: 什么是Python
Result: Python 是一种编程语言，由 Guido van Rossum 创建。
```

### v2_keyword_search.py
```
Query: Python 创始人
Keywords matched: ['Python', '创始人']
Result: Guido van Rossum 在 1989 年创建了 Python。
```

### v3_embedding_rag.py
```
Indexing 5 documents...
Query: 编程语言设计
Top-2 matches:
  1. doc_python.txt (score: 0.89)
  2. doc_language.txt (score: 0.75)
Answer: Python 由 Guido van Rossum 设计...
```

---

## Chapter 07: Context Compression

### v1_truncation.py
```
Messages: 10 items
After truncation: 5 items (last 5 kept)
```

### v2_naive_summarization.py
```
Messages: 10 items
Summary: User asked about Python, then about file operations...
Compressed to: 1 summary + 3 recent messages
```

### v3_hierarchical_memory.py
```
Initial: 6 items in working
After compact (limit=3):
  Summary: compressed 3 messages
  Facts: topic=agent tutorial, chapter=07, style=beginner friendly
  Working: 3 recent messages
```

---

## Chapter 08: Concurrency

### v1_blocking.py
```
Running tasks sequentially...
Task A: 0.5s
Task B: 0.5s
Task C: 0.5s
Total elapsed: ~1.5s
```

### v2_background_task.py
```
Task status: pending -> running -> completed
Elapsed: ~0.5s
Main thread responsive throughout.
```

### v3_parallel_execution.py
```
Running 3 tasks in parallel...
All completed in ~0.5s (not 1.5s)
Results: [result_A, result_B, result_C]
```

---

## Chapter 09: Multi-Agent

### v1_single_agent.py
```
Agent handling 3 subtasks sequentially...
Subtask 1: done
Subtask 2: done
Subtask 3: done
All tasks completed by single agent.
```

### v2_centralized.py
```
Orchestrator: Distributing tasks...
  -> Agent A: task_1
  -> Agent B: task_2
  -> Agent C: task_3
Results collected: [result_1, result_2, result_3]
```

### v3_decentralized.py
```
Agent A: received task_1, sending msg to B
Agent B: received task_2, sending msg to C
Agent C: received task_3, all done
Collaborative completion via peer messaging.
```

---

## Chapter 10: Safety Sandbox

### v1_no_protection.py
```
Command: rm -rf /
Executing: rm -rf /
Result: [DANGEROUS - would execute!]
```

### v2_blacklist_whitelist.py
```
Command: ls -la
Check: ls in whitelist -> allowed
Result: [directory listing]

Command: rm -rf /
Check: rm in blacklist -> blocked
Result: blocked: rm
```

### v3_permission_system.py
```
Command: delete_file('important.txt')
Risk: high
Policy: requires_approval
Audit: logged
Confirm? (y/n): y
Result: deleted with approval
```

---

## Final Integration

### claudcode_full.py
```
=== Integrated Agent Demo ===

Chapter 01: Perception-Thought-Action
  -> Loop completed successfully

Chapter 02: Tool System
  -> Tool executed: read_file

Chapter 03: Short-term Memory
  -> History length: 4 messages

Chapter 04: Chain-of-Thought
  -> ReAct steps: 3

Chapter 05: Self-Correction
  -> Retry succeeded after 1 attempt

Chapter 06: External Memory
  -> Documents retrieved: 2

Chapter 07: Context Compression
  -> Memory compacted: 6 -> 3 items

Chapter 08: Concurrency
  -> Parallel tasks: 3 completed

Chapter 09: Multi-Agent
  -> Agents collaborated: 3

Chapter 10: Safety Sandbox
  -> Command checked: allowed

=== All chapters integrated successfully ===
```

---

## Testing

### pytest -q
```
......................................................
                                                      [100%]
51 passed in 0.86s
```

All tests passing indicates:
- All chapter implementations work correctly
- Integration tests pass
- No regressions detected
