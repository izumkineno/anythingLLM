# AnythingLLM 路由与排查

## 目录结构默认认知

- AnythingLLM 在**大多数情况下**可优先按**单层文件夹嵌套**理解。
- 默认先按“根目录 -> 一级子目录”理解与处理。
- 这是一条默认认知规则，不是绝对限制；如果已有证据表明存在多层嵌套，应以实际结构为准。

## 先决条件

- 必须先检查环境变量：`ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
- 如果缺少任意一个：**立即停止当前调用链**，直接告诉用户缺少环境变量，不能继续
- 如果两者都存在，也必须先做一次轻量认证/连通性验证（优先：`python anythingllm.py auth`）
- 只有在认证成功后，才能继续后续 AnythingLLM 命令或排查流程
- 如果认证失败，先按“key 或接入链接校验失败”处理；不要直接当成业务命令错误
- 不要在对话、示例或文档里输出密钥、Bearer 值、绝对路径、用户目录

## 调用优先级

1. **优先使用仓库内 `anythingllm.py`**
2. 高层命令不够时，再用 `python anythingllm.py api ...`
3. 只有在 CLI 无法覆盖且需要核对规范时，才读文档

## API 文档读取优先级

遇到疑似 API 错误、路径不确定、参数不确定时，按下面顺序处理：

1. **先搜索读取** `anythingllm-developer-api.zh-CN.md`
2. 如果文档无法确认，再看 `/api/docs/`

禁止整文件通读 `anythingllm-developer-api.zh-CN.md`。必须先搜索关键词，再只读取命中的相关片段。

推荐关键词：

- 路径片段：`/v1/workspace`、`/v1/document`
- 命令名：`update-env`、`manage-users`
- 错误码：`403`、`404`、`422`
- 业务词：`embed`、`thread`、`vector-search`

## 操作规则

- 能用已有一等命令就不要手写 REST 路径
- 长 JSON 优先走文件或 stdin，不要把大 JSON 直接塞进提示词
- 上传、原始文本、聊天、向量检索都优先走 `anythingllm.py` 已有子命令
- 文档上传默认按 **“先上传，再显式绑定 workspace”** 理解；不要把 `document upload --workspace <slug>` 当成稳定成功路径
- 涉及路径、目录、文件定位时，默认先按单层文件夹嵌套检查；只有在已有证据表明存在多层结构时，再进入递归或多层推断
- 如果单次调用失败，先检查：
  - 环境变量是否存在
  - 子命令是否已覆盖
  - 是否把“上传成功”误判为“已经加入知识库 / workspace”
  - API 文档片段是否与当前命令一致
  - 是否命中了已知踩坑

## 高频错误模式（先记这组）

自维护踩坑表里，最高频的是“文档上传 / workspace 绑定 / 知识库读取”这一整条链路，优先看：

1. **上传成功 ≠ 已加入 workspace**
   - `document upload --workspace <slug>` 可能上传成功，但 workspace 里仍然没有文档。
   - 标准做法：**先** `document upload --file <path>`，**再** `workspace update-embeddings <slug> --json <file>`。
2. **`workspace update-embeddings` 的 `slug` 是位置参数**
   - 正确：`workspace update-embeddings <slug> --json <file>`
   - 错误：`workspace update-embeddings --slug <slug> --json <file>`
3. **`document upload --folder` 在 Desktop 端可能 404/500**
   - 默认先上传到根目录，不要把 `--folder` 当成稳定路径。
4. **`document list --folder` 不是递归查询**
   - 它只看指定目录的根层文件，不会自动展示子目录内容。
5. **无扩展名文件可能无法上传**
   - `.gitignore`、`LICENSE`、`Makefile` 这类文件要先过滤，或改为带扩展名的副本再上传。

## 通用错误排查顺序

1. 查 `anythingllm-skill-pitfalls.md`（优先看**查询次数**更高的项）
2. 搜索读取 `anythingllm-developer-api.zh-CN.md`
3. 再看 `/api/docs/`
4. 最后才判断为服务端异常或文档过期
