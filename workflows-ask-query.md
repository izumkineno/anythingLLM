# AnythingLLM ask 查询工作流

适用场景：

- 查询某个 workspace，并把知识库内容整理成答案
- 先检索证据，再输出结构化结论
- 基于知识库生成示例、单文件 demo、文档草稿、操作方案
- 单纯 `search` 结果太碎，需要 `ask --mode query` 做归纳

不适用场景：

- 只想确认接入是否正常 → 先只跑 `auth`
- 只想看命中文档或 API 片段，不需要整理答案 → 只跑 `search`
- 上传文档 / 绑定 workspace → 读 `workflows-upload-and-retrieval.md`

## 核心原则

- `search` 用于**抽证据 / 抽 API 片段 / 抽能力点**
- `ask --mode query` 用于**基于已入库知识做结构化整理**
- 不要把第一次 `search` 命中的结果直接当最终事实
- 如果目标是“生成复杂示例或产物”，默认采用：
  - `workspace get` 了解知识源
  - 多轮 `search` 抽取稳定命中能力点
  - `ask --mode query` 归纳成方案
  - 最后再写入本地产物

## 标准流程

1. **先过前置门槛**
   - 检查 `ANYTHINGLLM_BASE_URL`、`ANYTHINGLLM_API_KEY`
   - 先跑：`python anythingllm.py auth`
   - 未认证成功前，不进入 `workspace / search / ask`

2. **确认 workspace**
   - 不确定 slug 时：`python anythingllm.py workspace list`
   - 已知 slug 时：`python anythingllm.py workspace get <slug>`
   - 重点看：workspace 是否存在、documents 是否有内容、知识源质量是否可用

3. **先做多轮 search 抽证据**
   - 按主题拆成多次查询，不要只搜一轮
   - 示例：初始化、交互、动画、状态、视口、事件分别搜索
   - 目标不是一次搜全，而是抽出：
     - 稳定命中的 API 名称
     - 可复用的代码片段
     - 能落地的能力点

4. **过滤噪声结果**
   - 丢掉：
     - `404 Not Found`
     - 极短占位文本
     - 无上下文的碎片块
   - 保留：
     - 多次稳定命中的 API / 模式
     - 能直接落到目标产物中的知识点

5. **再用 ask 做结构化整理**
   - 命令：`python anythingllm.py ask <slug> --mode query --message <prompt>`
   - prompt 要明确要求：
     - 目标产物类型（示例 / 文档 / 方案）
     - 必须覆盖的能力点
     - 输出结构（要点 / 分层 / 模块）
   - `ask` 的职责是整理，不是替代前面的 `search`

6. **写本地产物（如果任务要求）**
   - 把 `search` 抽到的证据 + `ask` 整理出的结构，一起变成最终文件
   - 最终产物要优先忠于稳定命中的 API，而不是只忠于 `ask` 的自然语言总结

7. **做结果验证**
   - 至少验证：
     - 文件已落盘
     - 关键 API / 关键结构已出现在文件中
     - 结论与检索证据一致，没有脱离知识库乱扩展

## 推荐命令顺序

```powershell
python anythingllm.py auth
python anythingllm.py workspace list
python anythingllm.py workspace get <slug>
python anythingllm.py search <slug> --query "..." --top-n 6
python anythingllm.py search <slug> --query "..." --top-n 6
python anythingllm.py ask <slug> --mode query --message "..."
```

## Windows / PowerShell 注意事项

如果 `search` 或 `ask` 输出触发编码错误，优先按下面方式执行：

```powershell
$env:PYTHONIOENCODING='utf-8'
python anythingllm.py search <slug> --query "..." --top-n 6 2>&1 |
  Out-File -Encoding utf8 temp.txt
Get-Content temp.txt
```

不要把控制台编码错误误判成 AnythingLLM 检索失败。

## search 和 ask 的分工

### 什么时候只用 search

- 只想看知识库里有没有这个 API / 片段
- 只想确认文档命中情况
- 只想拿几段原始证据

### 什么时候必须补 ask

- 需要把多段证据整合成答案
- 需要生成复杂示例 / 方案 / 文档
- 用户问的是“怎么做比较完整”，而不是“某个 API 是什么”

## 一个推荐模板

如果目标是“基于 workspace 生成复杂示例”，推荐这样思考：

1. `workspace get` 看知识源
2. 3~5 轮 `search` 按主题抽能力点
3. 手工过滤噪声
4. `ask --mode query` 要结构化方案
5. 依据证据写最终文件
6. 验证文件与关键 API

## 禁止事项

- 禁止跳过 `auth` 直接 ask
- 禁止只看一次 `search` 就下结论
- 禁止把 `ask` 输出当成无条件真相，必须和前面的检索证据对齐
- 禁止在命中 404 / 噪声结果时继续无筛选地生成代码
- 禁止先写最终产物，再倒推搜索词补证据
