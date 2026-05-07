# AnythingLLM Skill 踩坑记录

只记录高价值、可复用的问题。格式固定：**查询次数 / 现象 / 原因 / 正确做法**。

维护规则：

- 新增记录时：`查询次数：0`
- 当某条记录在后续排查中直接帮助定位、排除或修正问题时：该条 `查询次数 +1`
- 排序暂不强制调整；默认先关注查询次数更高的项

## 1. 文档路径看起来对，但实际调用 404

- 查询次数：0
- 现象：按猜测路径调用成功率低，尤其是文档相关接口容易 404
- 原因：接口应以 AnythingLLM 当前 API 文档为准，不能凭记忆猜路径
- 正确做法：先搜索读取 `anythingllm-developer-api.zh-CN.md`，再决定是否调用 `anythingllm.py` 对应命令或 `api` 兜底命令

## 2. 直接整读 API 文档导致 token 浪费

- 查询次数：0
- 现象：上下文很快膨胀，后续推理质量下降
- 原因：整文件读取 `anythingllm-developer-api.zh-CN.md` 包含大量无关接口
- 正确做法：先搜索关键词，只读取相关命中片段

## 3. 已有 CLI 命令却还在手写 REST

- 查询次数：0
- 现象：路径、query、请求体字段容易拼错
- 原因：绕过了 `anythingllm.py` 已封装的命令层
- 正确做法：优先使用 `anythingllm.py` 的高层子命令；只有未覆盖接口才用 `python anythingllm.py api ...`

## 4. 环境变量缺失时继续尝试调用

- 查询次数：0
- 现象：请求失败，但错误看起来像 API 故障
- 原因：缺少 `ANYTHINGLLM_BASE_URL` 或 `ANYTHINGLLM_API_KEY`
- 正确做法：先检查环境变量；缺失则立即停止并告知用户

## 5. 在文档或示例里暴露隐私信息

- 查询次数：0
- 现象：skill 中出现绝对路径、真实密钥或用户目录
- 原因：直接复制本机示例，未做脱敏
- 正确做法：统一使用相对路径、占位符变量，不写任何真实密钥或用户目录

## 6. 使用 `--folder` 参数上传文档时返回 HTTP 404/500

- 查询次数：0
- 现象：`document upload --file <path> --folder <folder>` 所有上传都失败，返回 HTTP 404 或 HTTP 500
- 原因：AnythingLLM Desktop 版本的 `/document/upload/{folderName}` 端点不工作或不存在
- 正确做法：不使用 `--folder` 参数，直接上传到根目录；AnythingLLM 会自动将文档存储为 `custom-documents/{filename}-{uuid}.json`

## 7. 使用 `--workspace` 参数时文档没有添加到 workspace

- 查询次数：0
- 现象：`document upload --file <path> --workspace <slug>` 上传成功，但 workspace 的 documents 数组为空
- 原因：`--workspace` 参数（即 `addToWorkspaces`）在上传时不生效（可能是 Desktop 版本的 bug）
- 正确做法：使用两步流程：(1) 先用 `document upload --file <path>` 上传文档；(2) 再用 `workspace update-embeddings <slug> --json <file>` 批量添加到 workspace

## 8. `workspace update-embeddings` 命令参数错误

- 查询次数：0
- 现象：使用 `workspace update-embeddings --slug <slug> --json <file>` 时报错 "unrecognized arguments: --slug"
- 原因：`slug` 是位置参数（positional argument），不是选项参数
- 正确做法：`workspace update-embeddings <slug> --json <file>`（slug 直接跟在命令后面，不加 `--slug`）

## 9. AnythingLLM 不保留上传文档的目录结构

- 查询次数：0
- 现象：期望保持 `folder/subfolder/file.md` 的目录结构，但所有文档都被扁平化存储
- 原因：AnythingLLM 的文档存储机制是扁平化的，所有文档存储在 `custom-documents/` 目录，文件名格式为 `{原始文件名}-{uuid}.json`
- 正确做法：接受扁平化存储；如需保留路径信息，可以在文档的 metadata 中记录原始路径（但 Desktop 版本可能不支持自定义 metadata）；同名文件会通过 UUID 自动区分

## 10. `document move-files` CLI 发送裸数组导致 API 返回 HTTP 500

- 查询次数：0
- 现象：`document move-files --json '[{"from":"...","to":"..."}]'` 返回 HTTP 500: Failed to move files
- 原因：CLI 的 `document_move_files` 函数直接将数组作为请求体发送，但 API 期望 `{ "files": [...] }` 格式的对象
- 正确做法：修复 CLI 代码，将 payload 包装为 `{"files": payload}`；调用方式不变，仍传入 JSON 数组

## 11. `document create-folder` 不接受 `--json` 参数

- 查询次数：0
- 现象：`document create-folder --json '{"name":"folder"}'` 报错 "unrecognized arguments: --json"
- 原因：`create-folder` 命令接受 `name` 作为位置参数，不是 JSON 对象
- 正确做法：`document create-folder <folder-name>`（直接传文件夹名，不加 `--json`）

## 12. AnythingLLM Desktop 版不支持无扩展名文件上传

- 查询次数：0
- 现象：上传 `.gitignore` 等无扩展名文件时返回 HTTP 500: "No file extension found. This file cannot be processed."
- 原因：AnythingLLM Desktop 版要求文件必须有扩展名才能识别 MIME 类型
- 正确做法：上传时过滤掉无扩展名的文件（如 `.gitignore`、`LICENSE`、`Makefile` 等）

## 13. `document list --folder` 只返回文件，不显示子文件夹

- 查询次数：0
- 现象：`document list --folder "leafer-test"` 只返回根目录文件，子文件夹中的文件不可见
- 原因：`/v1/documents/folder/{folderName}` API 只返回指定文件夹根级别的文件，不递归显示子文件夹内容
- 正确做法：验证文件结构时使用文件系统直接检查存储目录（`StorageDir/documents/`），或逐级查询子文件夹

## 14. 用户级永久环境变量刚写入后，AnythingLLM CLI 新进程仍提示未设置

- 查询次数：0
- 现象：刚通过 `[Environment]::SetEnvironmentVariable(..., 'User')` 写入 `ANYTHINGLLM_BASE_URL` / `ANYTHINGLLM_API_KEY` 后，立刻执行 `python anythingllm.py auth` 仍报 `ANYTHINGLLM_API_KEY is not set`
- 原因：用户级环境变量已写入注册表，但当前会话或后续被拉起的命令进程不一定立刻继承到最新值
- 正确做法：不要把“已写入用户级环境变量”误判为“本次命令已可见”；在同一条命令里显式注入 `$env:ANYTHINGLLM_BASE_URL` 与 `$env:ANYTHINGLLM_API_KEY` 后再执行 `auth`，或开启新 shell 再验证

## 15. 工作区检索会命中 404 页面或噪声文档块，直接拿来生成代码不稳定

- 查询次数：0
- 现象：`search <workspace> --query ...` 能返回结果，但部分命中文档正文只有 `404 Not Found`、极短占位文本，或只包含很碎的片段
- 原因：AnythingLLM 会把 URL 导入结果和抓取失败页一起索引；向量检索按相似度返回，不会自动过滤“低质量但相似”的文档块
- 正确做法：主 skill 已把“首轮 `search` 不直接当最终事实、先过滤 404/噪声块”提升为默认决策规则；这里保留为错误案例说明，用于解释为什么某次检索结果虽然命中、却不适合直接继续生成代码

## 16. 复杂示例生成时，`search` 适合抽能力点，`ask --mode query` 更适合做结构化归纳

- 查询次数：0
- 现象：围绕同一主题连续 `search` 可以查到 `hoverStyle`、`ZoomEvent`、`RenderEvent`、`animation` 等碎片，但很难直接拼成一个结构完整的 demo / 方案
- 原因：`search` 返回的是离散文档块，适合定位 API 和代码片段；复杂示例需要跨片段整合，单纯堆叠搜索结果容易遗漏依赖关系或结构层次
- 正确做法：主 skill 已把“复杂整理默认走 `search -> ask`”提升为默认主流程；这里保留为案例，说明为什么在复杂示例场景里，单靠 `search` 很容易卡在碎片堆叠，而 `ask --mode query` 更适合做结构化归纳

## 17. 把长输出整份回读进上下文会抵消 CLI 的低 token 优化

- 查询次数：0
- 现象：即使已经把 `workspace get`、`search`、`ask/chat` 输出保存到文件，后续又用 `Get-Content <file>` 整份读回，token 仍然快速膨胀
- 原因：CLI 做的 summary/compact/`--text-only`/`--no-sources`/`--json-output` 优化只能减少 stdout 体积；如果后续再把长文件整份灌回代理上下文，等于把优化抵消了
- 正确做法：主 skill 已把“先落盘，再局部读取”提升为默认低 token 路线；这里保留为失败案例，用于解释为什么一次看似无害的整份 `Get-Content` 会直接抵消前面的 CLI 压缩收益。局部读取优先使用 `Get-Content -TotalCount ...`、`Select-String` 或 `--json-output`

## 18. 历史聊天与文档树命令默认原样输出时，token 膨胀比 search 更严重

- 查询次数：0
- 现象：`workspace chats`、`thread get-chats`、`admin workspace-chats`、`document list` 看起来只是“读列表/读历史”，但一旦命中长 prompt、长 response 或整棵文档树，stdout 会瞬间变成几万到几十万字节
- 原因：这类命令天然返回聚合数据：历史聊天会同时带 prompt/response/sources/metrics，文档树会带整层 `items` 与 metadata；如果默认原样 pretty-print，体积往往比一次 `search` 更大
- 正确做法：主 skill 已把“聚合结果默认看摘要、必要时才 `--full`”提升为默认低 token 路线；这里保留为案例，帮助在历史聊天或文档树输出失控时快速定位原因

## 19. `system get` 默认全量打印时，容易把大量“配置存在但并不需要当前推理”的字段带进上下文

- 查询次数：0
- 现象：`system get` 看起来只有几 KB，但包含几十到上百个设置键；在代理流程里，这些字段大多与当前任务无关，却会持续占用上下文
- 原因：系统配置接口会同时返回认证、存储、Embedding、LLM、语音、Agent、各供应商开关等完整设置；默认 pretty-print 会把低相关度字段一起送进上下文
- 正确做法：主 skill 已把“聚合配置默认看摘要、必要时才 `--full`”提升为默认低 token 路线；这里保留为案例，用于解释为什么 `system get` 虽然体积不大，却很容易把低相关度字段整包带进上下文

## 20. 把 `ask` 的整理结果直接当成最终事实，容易把“未复核的 API 名称”写进代码

- 查询次数：0
- 现象：`ask --mode query` 给出的方案、示例或代码结构看起来很完整，但其中个别 API / 事件名 / 配置键并没有在前面的检索证据中稳定出现
- 原因：`ask` 是受检索约束的整理层，不是严格的逐 token 事实校验器；在缺少二次复核时，模型可能补全一个“很像真的”名称
- 正确做法：主 skill 已把“`ask` 不是事实终审层、关键名称需二次 `search` 复核”提升为默认决策规则；这里保留为案例，用于解释为什么某些看似合理的 API 名称会在最终代码里变成假阳性
