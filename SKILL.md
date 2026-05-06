---
name: anythingllm
description: Use when working with AnythingLLM through the local skill or CLI, especially when API paths, parameters, environment variables, or troubleshooting steps need to stay consistent and low-token. AnythingLLM 在大多数常见场景下更适合先按单层文件夹嵌套理解；有证据再扩展到多层。
---

# AnythingLLM API Skill

低 token 使用 AnythingLLM 的轻量入口。

## 核心硬规则（始终生效）

- 默认先按**单层文件夹嵌套**理解 AnythingLLM 的大多数常见结构；这是高命中默认，不是绝对限制
- 如果目录证据、源码引用、导入路径或报错信息明确指向多层结构，再切换为多层递归理解
- 必须先检查：`ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
- 在任何 AnythingLLM 操作前，必须先验证 **接入链接 + API key**；优先运行轻量认证命令（默认：`python anythingllm.py auth`）确认它们真的可用
- 在 Windows PowerShell 中执行 `anythingllm.py` 时，默认先设置：`$env:PYTHONIOENCODING = "utf-8"`
- 如果要保存 `search` / `chat` / `ask` 输出，默认优先走 UTF-8 文件重定向：`... 2>&1 | Out-File -Encoding utf8 <file>; Get-Content <file>`
- 如果当前环境和用户本轮消息里**没有提供** `ANYTHINGLLM_BASE_URL` 或 `ANYTHINGLLM_API_KEY`，必须**立刻停止**当前调用链，并直接询问用户补充缺失项；未补齐前不得继续
- 如果只提供了其中一项，也必须立刻停止并询问另一项；不要假设可从别处自动补全
- 仅仅“环境变量存在”不等于“已验证可用”；认证成功后才能继续执行后续 AnythingLLM 命令
- 优先使用仓库内 `anythingllm.py`，不要先手写 REST
- 不要整读 `anythingllm-developer-api.zh-CN.md`；必须先搜索关键词，再只读命中片段
- 不要输出密钥、Bearer、绝对路径、用户目录

## 强制前置门槛

在任何 `workspace` / `document` / `thread` / `search` / `admin` / `api` / `embed` 操作前，按下面顺序执行：

1. 收集 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
2. 若用户本轮明确提供了新值，以用户最新提供的值为当前事实
3. 若两者任一缺失：**立刻停止**，只询问缺失项；不要继续读文档、跑 CLI、猜路径或尝试 API
4. 若两者齐全：先运行 `python anythingllm.py auth` 做轻量认证 / 连通性验证
5. 只有在认证成功后，才继续后续 AnythingLLM 操作
6. 若认证失败：先报告“key 或接入链接校验失败”，然后再进入排查；不要把失败当成业务命令异常

## 按需加载（只读需要的文件）

根据任务类型，继续读取：

- **上传文档 / 绑定 workspace / 读取知识库**
  - 读：`workflows-upload-and-retrieval.md`
- **使用 chat / stream-chat / thread chat 直接协写代码、模块、debug 分析或文件产物**
  - 读：`workflows-chat.md`
- **查询 workspace / 先 search 抽证据，再 ask 结构化整理 / 生成示例或文档产物**
  - 读：`workflows-ask-query.md`
- **API 路径不确定 / 参数不确定 / 命令失败排查**
  - 读：`routing-and-troubleshooting.md`
- **维护自定义错误表 / 查询次数 / 追加踩坑记录**
  - 读：`pitfalls-maintenance.md`
- **查具体历史坑点**
  - 读：`anythingllm-skill-pitfalls.md`

如果当前问题已经明显命中历史坑点，先读 `anythingllm-skill-pitfalls.md`，再决定是否继续查 API 文档。

如果任务目标是：

- 直接让对端 LLM 生成代码、模块、debug 分析、重构建议或某个文件产物
- 需要使用 `workspace chat` / `thread chat` / `stream-chat`
- 需要判断是否配合 `--text-only` 直接落盘

则优先读取：`workflows-chat.md`

如果任务目标是：

- 查询某个 workspace 并整理答案
- 基于知识库生成复杂示例 / 单文件 demo / 文档草稿
- 先 search，再 ask 做结构化归纳

则优先读取：`workflows-ask-query.md`

## 最小工作顺序

1. 收集并检查 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
2. 如果缺失任意一项，立刻停止并询问用户；不要继续执行 AnythingLLM 相关操作
3. 在 Windows PowerShell 中先设置：`$env:PYTHONIOENCODING = "utf-8"`
4. 先跑 `python anythingllm.py auth` 验证 key 和接入链接
5. 判断任务类型，只加载对应子文件
6. 优先跑 `anythingllm.py` 高层命令
7. 如果输出较长或需要落盘，优先使用 UTF-8 重定向输出
8. 失败时先查 `anythingllm-skill-pitfalls.md`
9. 仍不确定时，再搜索 `anythingllm-developer-api.zh-CN.md`

## 常用入口

- `python anythingllm.py --help`
- `python anythingllm.py workspace --help`
- `python anythingllm.py document --help`
- `python anythingllm.py thread --help`
- `python anythingllm.py admin --help`
- `python anythingllm.py system --help`
- `python anythingllm.py embed --help`
- `python anythingllm.py openai --help`
- `python anythingllm.py api --help`

## 禁止事项

- 禁止写死绝对路径
- 禁止输出或保存密钥
- 禁止默认整读 `anythingllm-developer-api.zh-CN.md`
- 禁止跳过环境变量检查
- 禁止在**未验证** base URL 和 API key 前继续执行 AnythingLLM 操作
- 禁止把“环境变量已存在”误判为“key 和接入链接已验证”
- 禁止在已有 CLI 命令可用时优先走手写 HTTP
- 禁止在没有证据时默认按多层目录递归理解 AnythingLLM 结构
