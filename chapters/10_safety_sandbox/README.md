# 第10章：安全边界与沙箱（Safety Sandbox）

## 1) 问题引入
Agent 有执行能力就有风险，必须加入安全边界。

典型风险：
- 误执行危险命令（删除文件、改权限、系统级命令）。
- 用户提示被拼接到命令时发生注入。
- 没有审计记录，事后无法追踪“谁在什么时候执行了什么”。

## 2) 最小实现
- `v1_no_protection.py`: 无保护（反例）

运行：
```bash
python chapters/10_safety_sandbox/v1_no_protection.py
```

你会看到任何命令都被“直接执行”（教学中仅打印，不真实执行）。

## 3) 逐步完善
- `v2_blacklist_whitelist.py`: 黑白名单
- `v3_permission_system.py`: 权限分级 + 审计日志 + 沙箱骨架

### v2 核心改进
- 先看白名单前缀（只允许已知安全命令类别）。
- 再看黑名单危险片段（例如 `rm -rf`、`sudo`）。

运行：
```bash
python chapters/10_safety_sandbox/v2_blacklist_whitelist.py
```

预期输出包含：
- `allowed: ls -la`
- `blocked: rm -rf tmp`

### v3 核心改进
- 对命令进行风险分级：`normal` / `system` / `dangerous`。
- 按策略决定：`allow` / `confirm` / `deny`。
- 生成结构化审计记录（时间、命令、级别、决策）。

运行：
```bash
python chapters/10_safety_sandbox/v3_permission_system.py
```

预期现象：
- 普通命令 `allowed`
- 系统命令 `needs_confirmation`（若未自动确认）
- 危险命令 `blocked`

## 4) 可视化
```text
v1 (insecure)
Input Command ----------------------> Execute

v2 (rule based)
Input -> whitelist check -> blacklist check -> allow/block

v3 (policy + audit)
Input -> classify risk -> policy decision -> sandbox execute? -> audit log
           normal/system/dangerous     allow/confirm/deny         structured record
```

## 5) 练习题
见 `exercises.md`。

建议顺序：
1. 在 v3 增加“按目录授权”规则（例如只允许工作目录写入）。
2. 为 `needs_confirmation` 增加一次性确认 token。
3. 把审计日志落盘为 JSONL，支持后续检索。
