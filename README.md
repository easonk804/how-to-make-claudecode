# How to Make a ClaudeCode (从零构建 Claude Code)

一个面向初学者的 AI Agent 教学项目：
- 每章只讲一个机制（控制变量）
> 核心目标：帮助你理解 Agent = LLM + 工具 + 记忆 + 推理 + 协作 + 安全。

## 学习路径（10章）

1. `01_perception_thought_action`：感知-思考-行动循环
2. `02_tool_system`：工具系统与注册表
3. `03_short_term_memory`：对话历史与窗口管理
4. `04_chain_of_thought`：显式推理与 ReAct
5. `05_self_correction`：反思与重试
6. `06_external_memory`：RAG 外部知识检索
7. `07_context_compression`：上下文压缩与分层记忆
8. `08_concurrency`：并发和后台任务
9. `09_multi_agent`：多 Agent 协作
10. `10_safety_sandbox`：安全边界与沙箱

## 快速开始

### 环境要求

- Python 3.10 或更高版本
- pip 包管理器

### 1) 克隆仓库

```bash
git clone https://github.com/yourusername/how-to-make-a-claudcode.git
cd how-to-make-a-claudcode
```

### 2) 安装依赖

```bash
pip install -r requirements.txt
```

或者使用虚拟环境（推荐）：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3) 配置 API Key

复制 `.env.example` 为 `.env`，并填写：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
ANTHROPIC_API_KEY=your_api_key_here
MODEL_ID=claude-3-5-sonnet-latest
```

> 获取 API Key：https://console.anthropic.com/

### 4) 验证安装

```bash
pytest -q
```

预期输出：`51 passed`

### 5) 从第一章开始

```bash
python chapters/01_perception_thought_action/v1_hardcoded.py
python chapters/01_perception_thought_action/v2_with_llm.py
python chapters/01_perception_thought_action/v3_complete_loop.py
```

### 4) 运行测试

```bash
pytest -q
```

### 6) 运行最终集成 Demo

```bash
python final/claudcode_full.py
```

## 常见问题排查

### 测试失败
- 确保已安装 `pytest`：`pip install pytest`
- 检查 Python 版本：`python --version`（需 >= 3.10）

### API Key 错误
- 检查 `.env` 文件是否存在且格式正确
- 确认 `ANTHROPIC_API_KEY` 有效且未过期

### 章节代码运行失败
- 检查是否已运行 `pip install -r requirements.txt`
- 检查 `chapters/XX_*/sandbox/` 目录是否有写入权限

## 项目结构

```text
how-to-make-a-claudcode/
├── chapters/
├── final/
├── knowledge_base/
├── tests/
├── README.md
├── 开发文档.md
├── requirements.txt
└── .env.example
```

## 当前实现状态

- [x] 项目脚手架
- [x] 第01章完整实现（v1/v2/v3 + 测试 + 练习）
- [x] 第02-10章章节说明与代码骨架
- [x] 第02-10章完整可运行实现（v1/v2/v3 + 测试）
- [x] `final/claudcode_full.py` 端到端集成 Demo

## 许可

MIT
