# 第02章练习题：工具系统

## 基础题
- 在 `v1_hardcoded.py` 新增 `list_dir` 工具分支。
- 输入包含 `list` 时，返回当前 sandbox 下的文件名。

## 进阶题
- 在 `v2_llm_selection.py` 给每次工具执行加耗时统计。
- 输出格式示例：`tool=read_file elapsed_ms=12`。

## 挑战题
- 在 `v3_registry_pattern.py` 支持工具链：
  1) 先 `write_file`
  2) 再把输出作为参数传给 `read_file`

## 可选进阶（v3）
1. 增加 `list_files` 与 `delete_file` 两个工具，并通过注册表动态注册。
2. 为 `dispatch` 增加统一错误包装（`unknown_tool` / `invalid_args`）。
3. 给工具系统补一组参数化测试（成功、失败、越权路径）。
