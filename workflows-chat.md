# AnythingLLM chat 工作流

适用场景：

- 直接让对端 LLM 基于某个 workspace 生成一段代码、一个模块、一个函数或一个完整文件
- 让对端协助 debug 某段代码、报错、思路或实现方案
- 让对端先给实现草稿、重构建议、补丁思路，再由本地继续集成
- 让对端扮演“协写者 / 协查者”，而不是只做知识检索整理

不适用场景：

- 只想拿知识库证据、文档片段、API 命中结果 → 优先 `search`
- 需要严格的“先 search 抽证据，再 ask 结构化整理” → 读 `workflows-ask-query.md`
- 上传文档 / 绑定 workspace → 读 `workflows-upload-and-retrieval.md`

## 核心定位

`chat` 的作用不是单纯“查知识库”，而是：

- 让对端 LLM **基于 workspace 背景直接参与工作**
- 输出可以是：
  - 完整文件
  - 某个模块
  - 某个函数/片段
  - debug 分析
  - 重构建议
  - 需要你再集成的实现草稿

一句话：

`search` 更像检索器，`ask --mode query` 更像整理器，`chat` 更像协作者。

## 先决条件

任何 chat / stream-chat / thread chat 前，仍然必须先做：

1. 检查 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
2. 跑 `python anythingllm.py auth`
3. 确认目标 workspace 存在：
   - `python anythingllm.py workspace list`
   - `python anythingllm.py workspace get <slug>`

不要跳过 `auth`，也不要在 workspace 未确认前直接 chat。

## chat 的几种常见用法

### 1. 直接产出完整文件

适合：

- 单文件 HTML demo
- 一份独立脚本
- 一份可直接保存的文档草稿

建议 prompt 明确要求：

- 只输出最终内容
- 不要解释
- 不要 markdown 代码围栏
- 不要省略必要代码
- 说明目标文件类型与运行方式

如果要直接写文件，优先使用：

```powershell
python anythingllm.py workspace chat <slug> --mode chat --text-only --message -
```

然后再重定向到文件。

### 2. 只产出某个模块 / 某段代码

适合：

- 让对端只写某个组件、函数、类、hook、工具模块
- 让对端补某个文件里的一部分逻辑

prompt 应明确：

- 只输出目标片段
- 不要生成完整项目
- 说明它会插入到哪个上下文中
- 说明依赖的现有变量/函数名

这类场景通常不一定直接落盘，更常见的是：

- 先看输出
- 再手动或本地脚本集成到现有文件

### 3. 用于 debug / 协查

适合：

- 让对端根据报错、代码片段、现象给出 root cause 假设
- 让对端提供排查步骤
- 让对端指出某段实现的问题

建议 prompt 包含：

- 最小代码片段
- 报错信息
- 当前现象
- 你希望对端输出什么：
  - root cause
  - 排查步骤
  - 最小修复建议

这类场景通常**不要直接要求落盘为文件**，而是把 chat 当成分析器或 code reviewer。

### 4. 用于重构 / 改写思路

适合：

- 让对端把一段代码改写成更清晰版本
- 让对端给出某个模块的替代实现
- 让对端只输出 diff 思路或替代代码块

建议 prompt 明确：

- 保持行为不变 / 或允许哪些行为变化
- 输出完整替代片段，还是只输出变更部分
- 是否允许改接口

## workspace chat / thread chat / ask 的分工

### `workspace chat`

适合：

- 一次性让对端基于整个 workspace 背景输出内容
- 不强调长期会话上下文
- 临时生成代码、方案、分析

### `thread chat`

适合：

- 你已经有一个 thread，想在连续上下文里追问
- 多轮迭代同一个模块 / 同一个 bug / 同一个文件

### `ask`

适合：

- 你不想自己先建 thread
- 想让脚本“必要时自动建线程并提问”
- 更偏“工作入口”，不是底层会话控制

## 输出形态怎么选

### 只看结果，不直接存文件

适合：

- debug 分析
- 模块草稿
- 重构建议
- 设计讨论

默认直接输出到终端即可。

### 直接存到文件

适合：

- 完整 HTML / JS / MD / TXT
- 你已经明确要求“只输出最终正文”

推荐：

```powershell
python anythingllm.py workspace chat <slug> --mode chat --text-only --message - |
  Out-File -Encoding utf8 output.html
```

### 存临时文件，再人工筛选

适合：

- 你不确定输出质量
- 输出可能带额外解释
- 想先审阅再集成

## prompt 设计建议

### 如果你要完整文件

至少明确：

- 只输出最终内容
- 不要解释
- 不要 markdown fence
- 说明文件类型
- 说明必须包含的功能点

### 如果你要某个模块

至少明确：

- 只输出模块代码
- 说明模块边界
- 说明已存在的上下文 / 依赖
- 说明不要补整个项目

### 如果你要 debug

至少明确：

- 错误信息
- 现象
- 相关代码片段
- 你要它输出 root cause / 排查步骤 / 最小修复建议中的哪一种

## `--text-only` 的使用原则

当你要把 chat 输出直接重定向到文件时，优先使用：

- `workspace chat --text-only`
- `thread chat --text-only`
- `ask --text-only`

因为默认非流式 chat 输出的是整包 JSON，包含：

- `textResponse`
- `sources`
- `metrics`

直接落盘时通常不希望把这些元数据一起写进去。

## 非流式 vs 流式

### 非流式 `chat`

优点：

- 输出结构稳定
- 搭配 `--text-only` 很适合直接落盘

缺点：

- 大输出要等整段响应结束
- 超时前可能文件一直为空

### 流式 `stream-chat`

优点：

- 可以持续看到生成过程
- 大输出更不容易“等到超时才发现没内容”

缺点：

- 更适合人看或实时记录
- 不一定适合需要“最终一次性干净正文”的场景

经验规则：

- **直接保存成最终文件** → 优先非流式 `chat --text-only`
- **担心长输出卡住 / 想实时观察** → 用 `stream-chat`

## 推荐流程

### A. chat 生成完整文件

1. `auth`
2. `workspace get <slug>`
3. 写严格 prompt
4. `workspace chat --mode chat --text-only`
5. 落盘到目标文件
6. 验证文件结构与运行结果

### B. chat 生成某个模块

1. `auth`
2. `workspace get <slug>`
3. 明确模块边界与上下文
4. `workspace chat` 或 `thread chat`
5. 审阅输出
6. 再集成进现有文件

### C. chat 协助 debug

1. `auth`
2. `workspace get <slug>`
3. 把报错 + 代码片段 + 现象喂给 chat
4. 要它输出 root cause / 排查步骤 / 最小修复建议
5. 本地验证，而不是直接相信 chat 结论

## 禁止事项

- 禁止跳过 `auth` 直接 chat
- 禁止把 chat 输出当成无条件真相，必须本地验证
- 禁止在需要直接落盘时忘记考虑 `--text-only`
- 禁止把“适合 ask-query 的整理任务”硬塞进 chat，导致 prompt 失焦
- 禁止让对端自由发挥却又期待它精确改某个模块——模块边界必须说清楚
- 禁止生成代码后不做运行/结构验证
