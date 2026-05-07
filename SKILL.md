---
name: anythingllm
description: 通过内置的 CLI 工具与 AnythingLLM 交互，支持 workspace 管理、知识库搜索（search）、智能问答（ask）、对话协作（chat）、文档上传等操作。
---
# AnythingLLM API Skill

AnythingLLM 的轻量入口。

## 核心硬规则（始终生效）

- 默认先按**单层文件夹嵌套**理解 AnythingLLM 的大多数常见结构；这是高命中默认，不是绝对限制
- 如果目录证据、源码引用、导入路径或报错信息明确指向多层结构，再切换为多层递归理解
- `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY` 默认按**全局环境变量**理解；除非用户本轮明确给了新值，否则先以当前 shell 继承到的环境变量为准
- 在任何 `workspace / search / ask / chat / thread chat` 前，必须先验证 **接入链接 + API key**；优先运行轻量认证命令（默认：`python anythingllm.py auth`）确认它们真的可用
- 在 Windows PowerShell 中执行 `anythingllm.py` 时，默认先设置：`$env:PYTHONIOENCODING = "utf-8"`
- 如果要保存 `search` / `chat` / `ask` 输出，默认优先走 UTF-8 文件重定向；**保存后默认只做局部读取**，不要整读回灌上下文
- `anythingllm.py` 默认视为和本 `SKILL.md` 同目录的本地脚本；命令示例默认从当前 skill 目录直接执行 `python anythingllm.py ...`
- 优先使用仓库内 `anythingllm.py`，不要先手写 REST
- 不要整读 `anythingllm-developer-api.zh-CN.md`；必须先搜索关键词，再只读命中片段
- 主流程默认先走 CLI 的摘要/紧凑输出；只有明确需要完整原始 JSON 时才使用 `--full` 或完整回显
- 默认规则只解决主流程首轮路径；上传、document 管理、Desktop 特定 bug、低频参数坑等问题，出错后再按关键词查 `anythingllm-skill-pitfalls.md`
- 不要输出密钥、Bearer、绝对路径、用户目录

## 强制前置门槛

在任何 `workspace` / `search` / `ask` / `chat` / `thread chat` 操作前，按下面顺序执行：

1. 先把 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY` 视为当前 shell 已继承的全局环境变量；若用户本轮给了新值，再以用户最新提供值覆盖
2. 若用户本轮明确提供了新值，以用户最新提供的值为当前事实
3. 若两者任一缺失：**立刻停止**，只询问缺失项；不要继续读文档、跑 CLI、猜路径或尝试 API
4. 默认从本 `SKILL.md` 同目录执行 `python anythingllm.py ...`；若调用位置变了，再显式切到脚本所在目录或写相对路径
5. 若两者齐全：先运行 `python anythingllm.py auth` 做轻量认证 / 连通性验证
6. 复杂整理默认先 `workspace get` 看摘要，再多轮 `search` 抽证据；需要结构化归纳时才进入 `ask --mode query`
7. 直接协写代码 / 文件 / debug 分析时走 `chat`；不要把 `ask` 当成直接产出完整文件的默认入口
8. 若最终要写代码 / demo / 配置片段，不要把第一次 `search` 或 `ask` 输出当最终事实；关键 API / 事件名 / 配置键至少再做一次针对性 `search` 复核
9. 若输出较长，默认先落盘，再局部读取；失败时先按关键词查 `anythingllm-skill-pitfalls.md`，仍不确定再搜索 `anythingllm-developer-api.zh-CN.md`

## 按需加载（只读需要的文件）

- 直接协写代码 / 文件 / debug 分析 / thread chat：读 `workflows-chat.md`
- 查询 workspace / 先 search 抽证据再 ask 归纳：读 `workflows-ask-query.md`
- 上传文档 / 绑定 workspace / 读取知识库：读 `workflows-upload-and-retrieval.md`
- API 路径 / 参数 / 失败排查：读 `routing-and-troubleshooting.md`
- 维护踩坑记录：读 `pitfalls-maintenance.md`
- 当前问题已明显命中历史坑点：先读 `anythingllm-skill-pitfalls.md`

## 最小工作顺序

1. 收集并检查 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
2. 如果缺失任意一项，立刻停止并询问用户；不要继续执行 AnythingLLM 相关操作
3. 在 Windows PowerShell 中先设置：`$env:PYTHONIOENCODING = "utf-8"`
4. 先跑 `python anythingllm.py auth` 验证 key 和接入链接
5. 先判断主流程：复杂整理走 `search -> ask`；直接协写/生成文件/调试走 `chat`
6. 走 `search -> ask` 时，先用 `workspace get` 看摘要，再用多轮 `search` 抽证据，不要把第一次命中直接当最终事实
7. 用 `ask` 归纳后的关键 API / 事件名 / 配置键，写入最终代码或文档前至少再做一次针对性 `search` 复核
8. 如果输出较长或需要落盘，优先使用 UTF-8 重定向；默认结合 `--text-only`、`--no-sources`、`--no-metrics`、`--json-output` 等低 token 选项，并只做局部读取
9. 失败时先按关键词查 `anythingllm-skill-pitfalls.md`；仍不确定时，再搜索 `anythingllm-developer-api.zh-CN.md`

## 低 token 默认路线

- `workspace get`：默认看摘要；只在排查字段缺失时加 `--full`
- `workspace list`：默认看摘要列表；只在确实需要全部字段时加 `--full`
- `search`：默认看紧凑结果；先过滤 `404 Not Found`、极短占位文本和噪声块，只把稳定命中的 API / 能力点带入后续 `ask` 或最终产物；只在需要完整原始向量召回时加 `--full`
- `ask` / `chat` / `thread chat`：
  - 只关心正文 → `--text-only`
  - 只关心正文 + 不要 sources/metrics → `--text-only --no-sources --no-metrics`
  - 需要完整 JSON 但不想把它灌回上下文 → `--json-output <file>`
- 保存长输出后，默认只做局部读取：`Get-Content <file> -TotalCount 40` / `Select-Object -First 40` / `Select-String`
- 非主流程异常：默认不要把规则前置进主 skill；按关键词去 `anythingllm-skill-pitfalls.md` 检索对应案例

## 常用入口

- `python anythingllm.py --help`
- `python anythingllm.py workspace --help`
- `python anythingllm.py thread --help`
- `python anythingllm.py api --help`

## 禁止事项

- 禁止写死绝对路径
- 禁止输出或保存密钥
- 禁止默认整读 `anythingllm-developer-api.zh-CN.md`
- 禁止对长输出文件默认执行整份 `Get-Content <file>` 回灌上下文
- 禁止无必要使用 `workspace get --full` 或 `search --full`
- 禁止跳过环境变量检查
- 禁止在**未验证** base URL 和 API key 前继续执行 AnythingLLM 操作
- 禁止把“环境变量已存在”误判为“key 和接入链接已验证”
- 禁止在已有 CLI 命令可用时优先走手写 HTTP
- 禁止在没有证据时默认按多层目录递归理解 AnythingLLM 结构
- 禁止把第一次 `search` 命中或 `ask` 的整理结果直接当成最终事实写进代码 / demo / 配置
