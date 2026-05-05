# AnythingLLM Skill 踩坑记录

只记录高价值、可复用的问题。格式固定：**现象 / 原因 / 正确做法**。

## 1. 文档路径看起来对，但实际调用 404

- 现象：按猜测路径调用成功率低，尤其是文档相关接口容易 404
- 原因：接口应以 AnythingLLM 当前 API 文档为准，不能凭记忆猜路径
- 正确做法：先搜索读取 `anythingllm-developer-api.zh-CN.md`，再决定是否调用 `anythingllm.py` 对应命令或 `api` 兜底命令

## 2. 直接整读 API 文档导致 token 浪费

- 现象：上下文很快膨胀，后续推理质量下降
- 原因：整文件读取 `anythingllm-developer-api.zh-CN.md` 包含大量无关接口
- 正确做法：先搜索关键词，只读取相关命中片段

## 3. 已有 CLI 命令却还在手写 REST

- 现象：路径、query、请求体字段容易拼错
- 原因：绕过了 `anythingllm.py` 已封装的命令层
- 正确做法：优先使用 `anythingllm.py` 的高层子命令；只有未覆盖接口才用 `python anythingllm.py api ...`

## 4. 环境变量缺失时继续尝试调用

- 现象：请求失败，但错误看起来像 API 故障
- 原因：缺少 `ANYTHINGLLM_BASE_URL` 或 `ANYTHINGLLM_API_KEY`
- 正确做法：先检查环境变量；缺失则立即停止并告知用户

## 5. 在文档或示例里暴露隐私信息

- 现象：skill 中出现绝对路径、真实密钥或用户目录
- 原因：直接复制本机示例，未做脱敏
- 正确做法：统一使用相对路径、占位符变量，不写任何真实密钥或用户目录
