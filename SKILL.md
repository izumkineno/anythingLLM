# AnythingLLM API Skill

低 token 使用 AnythingLLM 的规则集。

## 先决条件

- 必须先检查环境变量：`ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
- 如果缺少任意一个：**立即停止当前调用链**，直接告诉用户缺少环境变量，不能继续
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
- 如果单次调用失败，先检查：
  - 环境变量是否存在
  - 子命令是否已覆盖
  - API 文档片段是否与当前命令一致
  - 是否命中了已知踩坑

## 疑似 API 错误排查顺序

1. 查 `anythingllm-skill-pitfalls.md`
2. 搜索读取 `anythingllm-developer-api.zh-CN.md`
3. 再看 `/api/docs/`
4. 最后才判断为服务端异常或文档过期

## 踩坑记录

单独维护文件：`anythingllm-skill-pitfalls.md`

规则：

- 如果这次调用不顺利，但最终定位出原因，要补一条踩坑记录
- 记录要短，只写：**现象 / 原因 / 正确做法**
- 下次先读这个文件，再决定是否继续查 API 文档

## 常用入口

只记入口，不重复展开大表：

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
- 禁止在已有 CLI 命令可用时优先走手写 HTTP
