# AnythingLLM 常规上传与读取知识库

## 常规上传步骤（标准路径）

目标：把本地文档稳定放进 AnythingLLM，并确保它真的进入某个 workspace 的知识库。

1. **先做前置检查**
   - 检查 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
   - 先运行：`python anythingllm.py auth`，验证 key 和接入链接
   - 如果缺少 base URL 或 key，立刻停止并询问用户，不要继续上传/读取流程
2. **确认文件类型是否被支持**
   - `python anythingllm.py document accepted-types`
   - 默认过滤无扩展名文件
3. **先上传，不假设自动入库**
   - `python anythingllm.py document upload --file <path>`
   - 默认不要先用 `--folder`
   - 默认不要依赖 `--workspace` 作为唯一入库手段
4. **从上传响应里记录文档名 / 存储键**
   - AnythingLLM 常见会返回类似 `custom-documents/<name>-<uuid>.json` 的条目
   - `workspace update-embeddings` 需要的是这种 **相对 documents 根目录的路径**
5. **显式绑定到 workspace**
   - 准备一个小 JSON 文件，例如：`{"adds":["custom-documents/<name>-<uuid>.json"]}`
   - 执行：`python anythingllm.py workspace update-embeddings <workspace-slug> --json <json-file>`
6. **验证是否真的入库**
   - `python anythingllm.py workspace get <workspace-slug>`
   - 检查 `documents` 是否已包含刚绑定的文档

如果只是“上传成功”但 `workspace get <slug>` 里的 `documents` 还是空的，优先按“上传已成功，但绑定未生效”排查，不要先怀疑问答模型或向量检索。

## 常规读取知识库步骤

目标：区分“读文档目录/元信息”和“读 workspace 内的知识检索结果”。

默认判断：**先分清你要验证的是“文档存在”还是“知识可召回”**。前者走 `document`，后者走 `workspace get` / `search` / `ask`。

### A. 读取文档目录或单个文档

1. 列出全部文档：`python anythingllm.py document list`
2. 按目录查看：`python anythingllm.py document list --folder <folder>`
3. 查看单个文档详情：`python anythingllm.py document get <doc_name>`

注意：`document list --folder <folder>` **只看该目录根层**，不等于递归读取整个知识树。

### B. 读取某个 workspace 的知识库内容

1. 先确认 workspace 已绑定文档：`python anythingllm.py workspace get <workspace-slug>`
2. 做向量检索：`python anythingllm.py search <workspace-slug> --query <query> --top-n <n>`
3. 做基于知识库的问答：`python anythingllm.py ask <workspace-slug> --message <question> --mode query`

建议：

- **先用 `search` 看召回结果**，再用 `ask --mode query` 做问答
- 如果 `search` 没命中，先检查文档是否真的绑定进了 workspace，而不是直接改 prompt
- 如果只是想确认文档是否存在，用 `document list` / `document get`
- 如果是想确认知识是否可检索，用 `workspace get` + `search`
