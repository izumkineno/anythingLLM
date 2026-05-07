# AnythingLLM Skill

> **AnythingLLM 与编程助手之间的知识桥梁**
> 让 Claude Code、Cursor 等支持 skill 的编程助手能够直接访问你的 AnythingLLM 知识库

## 🎯 项目定位

这是一个**桥接工具**，连接两个世界：

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│  AnythingLLM    │ ◄─────► │  本 Skill    │ ◄─────► │  编程助手       │
│  (知识库)       │         │  (CLI 桥梁)  │         │  (Claude/Codex) │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

**核心价值**：

- 📚 **知识库读取**：从 AnythingLLM 中提取结构化知识
- 🔍 **向量搜索**：利用 AnythingLLM 的向量检索能力
- 🤖 **智能问答**：结合知识库上下文进行精准回答
- 🔗 **无缝集成**：通过 skill 机制让编程助手直接调用

## 💡 适用场景

<details>
<summary>点击展开查看详细场景</summary>

**前提**：你已有本地部署的 AnythingLLM 实例

✅ **适合你，如果：**

- 你在 AnythingLLM 中维护了项目文档、API 规范、技术笔记等知识库
- 你希望在编程时快速检索知识库内容，而不需要切换应用
- 你需要让 Claude 基于知识库内容生成代码、文档或解决方案
- 你想要结构化查询（如"列出所有 API 端点"、"总结架构设计"）

❌ **不适合你，如果：**

- 你还没有 AnythingLLM 实例 → 先查看 [AnythingLLM 官方文档](https://docs.useanything.com/)
- 你只需要简单的文本搜索 → 考虑使用 grep 或 ripgrep
- 你的知识库在其他平台（Notion、Confluence 等）→ 需要其他桥接工具

</details>

## 🚀 快速开始

### 1. 配置环境变量

**Windows PowerShell:**

```powershell
$env:ANYTHINGLLM_BASE_URL = "http://localhost:3001"
$env:ANYTHINGLLM_API_KEY = "your-api-key"
$env:PYTHONIOENCODING = "utf-8"
```

**Bash/Zsh:**

```bash
export ANYTHINGLLM_BASE_URL="http://localhost:3001"
export ANYTHINGLLM_API_KEY="your-api-key"
```

### 2. 安装

```bash
# 克隆或下载本项目到skill目录
git clone https://github.com/izumkineno/anythingLLM.git

# 无需安装依赖！anythingllm.py 仅使用 Python 标准库
# 可直接运行：
python anythingllm.py --help

```

### 3. 在 Claude Code 中使用

在 Claude Code 中，通过 `/anythingllm` skill 调用，无需手动输入命令：

```
/anythingllm search my-workspace --query "API 认证流程"
```

Claude 会自动调用底层的 `anythingllm.py` CLI 工具。

## 📖 核心功能

### 🔍 向量搜索（推荐用于知识检索）

从知识库中快速查找相关内容，利用向量相似度排序：

```bash
# CLI 直接调用
python anythingllm.py search <workspace> --query "关键词"

# 在 Claude Code 中
/anythingllm search <workspace> --query "关键词"
```

**参数说明**：

- `--top-n`: 返回结果数量（默认使用工作区配置）
- `--snippet-chars`: 摘要长度（默认 180）
- `--min-score`: 最低相似度分数过滤
- `--titles-only`: 仅显示标题和来源
- `--full`: 输出完整 JSON（默认为紧凑摘要）

### 💬 智能问答

基于知识库上下文进行结构化查询和归纳：

```bash
# CLI 直接调用
python anythingllm.py ask <workspace> --message "问题" --mode query

# 在 Claude Code 中
/anythingllm ask <workspace> --message "列出所有 API 端点" --mode query
```

**模式说明**：

- `chat`: 对话模式（保留上下文）
- `query`: 查询模式（单次问答，推荐用于知识提取）
- `automatic`: 自动选择

### 📚 工作区管理

列出、查看、创建工作区：

```bash
# 列出所有工作区
python anythingllm.py workspace list

# 查看工作区详情（包含文档和线程）
python anythingllm.py workspace get <workspace-slug>

# 创建新工作区
python anythingllm.py workspace create "项目文档"
```

### 📄 文档管理

上传文档到知识库：

```bash
# 上传文件
python anythingllm.py document upload --file ./doc.pdf --workspace my-workspace

# 上传原始文本
python anythingllm.py document raw-text --text "内容" --workspace my-workspace

# 抓取网页
python anythingllm.py document upload-link https://example.com --workspace my-workspace
```

## 🔧 CLI 完整命令

本工具提供完整的 AnythingLLM API 封装，支持：

- `workspace`: 工作区管理（list, create, get, update, delete, chat, chats）
- `document`: 文档管理（upload, raw-text, upload-link, list, get）
- `thread`: 线程管理（new, chat, stream-chat, update, get-chats, delete）
- `search`: 向量搜索
- `ask`: 智能问答（自动创建线程）
- `system`: 系统设置（get, vector-count, env-dump, export-chats）
- `admin`: 管理员接口（users, invites, preferences, workspace-chats）
- `embed`: Embed 配置管理
- `openai`: OpenAI 兼容接口
- `api`: 直接调用任意 REST 接口

详细命令说明：

```bash
python anythingllm.py --help
python anythingllm.py <command> --help
```

## 📚 更多文档

- **API 参考**：[anythingllm-developer-api.zh-CN.md](./anythingllm-developer-api.zh-CN.md)
- **Skill 配置**：[SKILL.md](./SKILL.md)
- **常见问题**：[anythingllm-skill-pitfalls.md](./anythingllm-skill-pitfalls.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
