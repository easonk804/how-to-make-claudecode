# 第08章：并发与后台任务（Concurrency）

## 1) 问题引入
长任务会阻塞 Agent，导致交互卡死。

典型症状：
- 用户发起一个耗时任务（检索、索引、批量分析）后，界面不再响应。
- 任务期间无法处理取消、追问或状态查询。

## 2) 最小实现
- `v1_blocking.py`: 同步阻塞

运行：
```bash
python chapters/08_concurrency/v1_blocking.py
```

你会看到任务按顺序完成，总耗时约等于每个任务耗时之和。

## 3) 逐步完善
- `v2_background_task.py`: 后台线程 + 通知
- `v3_parallel_execution.py`: 并行执行骨架

### v2 核心改进
- 将慢任务放到后台线程执行。
- 主线程通过队列轮询进度，保持“可响应”。

运行：
```bash
python chapters/08_concurrency/v2_background_task.py
```

预期输出会包含：
- `main loop: still responsive`
- `index_docs progress ...`
- `index_docs done`

### v3 核心改进
- 使用 `asyncio.gather` 并行执行多个任务。
- 引入超时控制，避免任务无限等待。

运行：
```bash
python chapters/08_concurrency/v3_parallel_execution.py
```

预期现象：
- `parallel` 耗时明显小于 `sequential`。

## 4) 可视化
```text
v1 (blocking)
User Request -> Task A -> Task B -> Task C -> Response
                 (main loop blocked the whole time)

v2 (background thread)
Main Loop:  Request -> Poll Queue -> Poll Queue -> Respond to user
Worker:                Task Running ----> Progress ----> Done

v3 (parallel asyncio)
             /-> Task A -\
Request --->|-> Task B ---> gather ---> merged result
             \-> Task C -/
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 给 v2 增加“取消任务”标记。
2. 给 v3 增加“部分失败可重试”。
3. 记录每个任务的开始/结束时间并输出统计。
