# AnythingLLM Developer API 中文详细文档

> 来源：Swagger UI `http://127.0.0.1:3001/api/docs/`
> 生成时间：2026-05-05T10:17:49.627Z
> OpenAPI：3.0.0｜文档版本：1.0.0

## 1. 文档目标与边界

- **目标**：把 AnythingLLM 当前 Swagger/OpenAPI 页面整理成一份便于后续调用的中文离线文档。
- **整理范围**：认证方式、基础地址、全部接口分类、参数、请求体、响应码、示例返回、cURL 调用示例。
- **明确不做**：不解析本仓库中的 `SKILL.md`、不解析任何 `*.py` 脚本、不对后端源码做额外推断。
- **说明**：内容严格以 Swagger 页面暴露的 OpenAPI 规范为准；若服务端实现与 Swagger 不一致，请以实际运行结果为准。

## 2. 基础信息

- **标题**：AnythingLLM Developer API
- **描述**：API endpoints that enable programmatic reading, writing, and updating of your AnythingLLM instance. UI supplied by Swagger.io.
- **基础地址**：`http://127.0.0.1:3001/api`
- **推荐请求头**：`Authorization: Bearer YOUR_API_KEY`
- **鉴权方案**：Swagger 定义了全局安全方案 `BearerAuth`（HTTP Bearer，bearerFormat = JWT）。
- **接口总数**：60 个操作，按 9 个分类整理。

## 3. 通用调用约定

### 3.1 认证

绝大多数接口都受全局 `BearerAuth` 保护。调用前先在请求头中带上 API Key：


```http
Authorization: Bearer YOUR_API_KEY
```
### 3.2 返回格式

- 主要返回格式为 `application/json`。
- 很多错误响应同时声明了 `application/xml`，但 Swagger 示例主要提供 JSON。
- 流式聊天接口会返回 `text/event-stream`。

### 3.3 常见错误

| 状态码 | 含义 | 备注 |
| --- | --- | --- |
| 400 | Bad Request | 请求体或参数不合法 |
| 401 | Unauthorized / Method denied | 常见于未开启多用户模式或未授权场景 |
| 403 | Forbidden | 常见为 API Key 无效 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 上传/解析类请求无法处理 |
| 500 | Internal Server Error | 服务端内部异常 |

### 3.4 通用错误模型：InvalidAPIKey

| 字段 | 类型 | 说明 | 示例 |
| --- | --- | --- | --- |
| message | string | 错误消息 | Invalid API Key |

## 4. 全量接口速览

| 分类 | 方法 | 路径 | 说明 |
| --- | --- | --- | --- |
| Admin | DELETE | `/v1/admin/invite/{id}` | Deactivates (soft-delete) invite by id. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/invite/new` | Create a new invite code for someone to use to register with instance. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | GET | `/v1/admin/invites` | List all existing invitations to instance regardless of status. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | GET | `/v1/admin/is-multi-user-mode` | Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/preferences` | Update multi-user preferences for instance. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | GET | `/v1/admin/users` | Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/users/{id}` | Update existing user settings. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | DELETE | `/v1/admin/users/{id}` | Delete existing user by id. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/users/new` | Create a new user with username and password. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/workspace-chats` | All chats in the system ordered by most recent. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | POST | `/v1/admin/workspaces/{workspaceId}/update-users` | Overwrite workspace permissions to only be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI. |
| Admin | GET | `/v1/admin/workspaces/{workspaceId}/users` | Retrieve a list of users with permissions to access the specified workspace. |
| Admin | POST | `/v1/admin/workspaces/{workspaceSlug}/manage-users` | Set workspace permissions to be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI. |
| Authentication | GET | `/v1/auth` | Verify the attached Authentication header contains a valid API token. |
| Documents | GET | `/v1/document/{docName}` | Get a single document by its unique AnythingLLM document name |
| Documents | GET | `/v1/document/accepted-file-types` | Check available filetypes and MIMEs that can be uploaded. |
| Documents | POST | `/v1/document/create-folder` | Create a new folder inside the documents storage directory. |
| Documents | GET | `/v1/document/metadata-schema` | Get the known available metadata schema for when doing a raw-text upload and the acceptable type of value for each key. |
| Documents | POST | `/v1/document/move-files` | Move files within the documents storage directory. |
| Documents | POST | `/v1/document/raw-text` | Upload a file by specifying its raw text content and metadata values without having to upload a file. |
| Documents | DELETE | `/v1/document/remove-folder` | Remove a folder and all its contents from the documents storage directory. |
| Documents | POST | `/v1/document/upload` | Upload a new file to AnythingLLM to be parsed and prepared for embedding, with optional metadata. |
| Documents | POST | `/v1/document/upload-link` | Upload a valid URL for AnythingLLM to scrape and prepare for embedding. Optionally, specify a comma-separated list of workspace slugs to embed the document into post-upload. |
| Documents | POST | `/v1/document/upload/{folderName}` | Upload a new file to a specific folder in AnythingLLM to be parsed and prepared for embedding. If the folder does not exist, it will be created. |
| Documents | GET | `/v1/documents` | List of all locally-stored documents in instance |
| Documents | GET | `/v1/documents/folder/{folderName}` | Get all documents stored in a specific folder. |
| Embed | GET | `/v1/embed` | List all active embeds |
| Embed | POST | `/v1/embed/{embedUuid}` | Update an existing embed configuration |
| Embed | DELETE | `/v1/embed/{embedUuid}` | Delete an existing embed configuration |
| Embed | GET | `/v1/embed/{embedUuid}/chats` | Get all chats for a specific embed |
| Embed | GET | `/v1/embed/{embedUuid}/chats/{sessionUuid}` | Get chats for a specific embed and session |
| Embed | POST | `/v1/embed/new` | Create a new embed configuration |
| OpenAI Compatible Endpoints | POST | `/v1/openai/chat/completions` | Execute a chat with a workspace with OpenAI compatibility. Supports streaming as well. Model must be a workspace slug from /models. |
| OpenAI Compatible Endpoints | POST | `/v1/openai/embeddings` | Get the embeddings of any arbitrary text string. This will use the embedder provider set in the system. Please ensure the token length of each string fits within the context of your embedder model. |
| OpenAI Compatible Endpoints | GET | `/v1/openai/models` | Get all available "models" which are workspaces you can use for chatting. |
| OpenAI Compatible Endpoints | GET | `/v1/openai/vector_stores` | List all the vector database collections connected to AnythingLLM. These are essentially workspaces but return their unique vector db identifier - this is the same as the workspace slug. |
| System Settings | GET | `/v1/system` | Get all current system settings that are defined. |
| System Settings | GET | `/v1/system/env-dump` | Dump all settings to file storage |
| System Settings | GET | `/v1/system/export-chats` | Export all of the chats from the system in a known format. Output depends on the type sent. Will be send with the correct header for the output. |
| System Settings | DELETE | `/v1/system/remove-documents` | Permanently remove documents from the system. |
| System Settings | POST | `/v1/system/update-env` | Update a system setting or preference. |
| System Settings | GET | `/v1/system/vector-count` | Number of all vectors in connected vector database |
| User Management | GET | `/v1/users` | List all users |
| Workspace Threads | DELETE | `/v1/workspace/{slug}/thread/{threadSlug}` | Delete a workspace thread |
| Workspace Threads | POST | `/v1/workspace/{slug}/thread/{threadSlug}/chat` | Chat with a workspace thread |
| Workspace Threads | GET | `/v1/workspace/{slug}/thread/{threadSlug}/chats` | Get chats for a workspace thread |
| Workspace Threads | POST | `/v1/workspace/{slug}/thread/{threadSlug}/stream-chat` | Stream chat with a workspace thread |
| Workspace Threads | POST | `/v1/workspace/{slug}/thread/{threadSlug}/update` | Update thread name by its unique slug. |
| Workspace Threads | POST | `/v1/workspace/{slug}/thread/new` | Create a new workspace thread |
| Workspaces | GET | `/v1/workspace/{slug}` | Get a workspace by its unique slug. |
| Workspaces | DELETE | `/v1/workspace/{slug}` | Deletes a workspace by its slug. |
| Workspaces | POST | `/v1/workspace/{slug}/chat` | Execute a chat with a workspace |
| Workspaces | GET | `/v1/workspace/{slug}/chats` | Get a workspaces chats regardless of user by its unique slug. |
| Workspaces | POST | `/v1/workspace/{slug}/stream-chat` | Execute a streamable chat with a workspace |
| Workspaces | POST | `/v1/workspace/{slug}/update` | Update workspace settings by its unique slug. |
| Workspaces | POST | `/v1/workspace/{slug}/update-embeddings` | Add or remove documents from a workspace by its unique slug. |
| Workspaces | POST | `/v1/workspace/{slug}/update-pin` | Add or remove pin from a document in a workspace by its unique slug. |
| Workspaces | POST | `/v1/workspace/{slug}/vector-search` | Perform a vector similarity search in a workspace |
| Workspaces | POST | `/v1/workspace/new` | Create a new workspace |
| Workspaces | GET | `/v1/workspaces` | List all current workspaces |

## 5. 分类统计

| 分类 | 接口数量 |
| --- | ---: |
| Admin | 13 |
| Authentication | 1 |
| Documents | 12 |
| Embed | 6 |
| OpenAI Compatible Endpoints | 4 |
| System Settings | 6 |
| User Management | 1 |
| Workspace Threads | 6 |
| Workspaces | 11 |

## 6. 分类详解

### Admin（13）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| DELETE | `/v1/admin/invite/{id}` | Deactivates (soft-delete) invite by id. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/invite/new` | Create a new invite code for someone to use to register with instance. Methods are disabled until multi user mode is enabled via the UI. |
| GET | `/v1/admin/invites` | List all existing invitations to instance regardless of status. Methods are disabled until multi user mode is enabled via the UI. |
| GET | `/v1/admin/is-multi-user-mode` | Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/preferences` | Update multi-user preferences for instance. Methods are disabled until multi user mode is enabled via the UI. |
| GET | `/v1/admin/users` | Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/users/{id}` | Update existing user settings. Methods are disabled until multi user mode is enabled via the UI. |
| DELETE | `/v1/admin/users/{id}` | Delete existing user by id. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/users/new` | Create a new user with username and password. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/workspace-chats` | All chats in the system ordered by most recent. Methods are disabled until multi user mode is enabled via the UI. |
| POST | `/v1/admin/workspaces/{workspaceId}/update-users` | Overwrite workspace permissions to only be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI. |
| GET | `/v1/admin/workspaces/{workspaceId}/users` | Retrieve a list of users with permissions to access the specified workspace. |
| POST | `/v1/admin/workspaces/{workspaceSlug}/manage-users` | Set workspace permissions to be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI. |

#### DELETE /v1/admin/invite/{id}

- **用途**：Deactivates (soft-delete) invite by id. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/invite/1`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | id of the invite in the database. | 1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/admin/invite/1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/admin/invite/new

- **用途**：Create a new invite code for someone to use to register with instance. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/invite/new`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：否
- **说明**：Request body for creation parameters of the invitation
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspaceIds | array<number> | 否 |  | [1,2,45] |

请求体示例：

```json
{
  "workspaceIds": [
    1,
    2,
    45
  ]
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| invite | object | 否 |  | {"id":1,"status":"pending","code":"abc-123"} |
| invite.id | number | 否 |  | 1 |
| invite.status | string | 否 |  | pending |
| invite.code | string | 否 |  | abc-123 |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "invite": {
    "id": 1,
    "status": "pending",
    "code": "abc-123"
  },
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/invite/new" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "workspaceIds": [
    1,
    2,
    45
  ]
}'
```

#### GET /v1/admin/invites

- **用途**：List all existing invitations to instance regardless of status. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/invites`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| invites | array<object> | 否 |  | [{"id":1,"status":"pending","code":"abc-123","claimedBy":null}] |
| invites[].id | number | 否 |  | 1 |
| invites[].status | string | 否 |  | pending |
| invites[].code | string | 否 |  | abc-123 |
| invites[].claimedBy | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "invites": [
    {
      "id": 1,
      "status": "pending",
      "code": "abc-123",
      "claimedBy": null
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/admin/invites" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/admin/is-multi-user-mode

- **用途**：Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/is-multi-user-mode`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| isMultiUser | boolean | 否 |  | true |

**成功响应示例（200）**

```json
{
  "isMultiUser": true
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/admin/is-multi-user-mode" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/admin/preferences

- **用途**：Update multi-user preferences for instance. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/preferences`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Object with setting key and new value to set. All keys are optional and will not update unless specified.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| support_email | string | 否 |  | support@example.com |

请求体示例：

```json
{
  "support_email": "support@example.com"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/preferences" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "support_email": "support@example.com"
}'
```

#### GET /v1/admin/users

- **用途**：Check to see if the instance is in multi-user-mode first. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/users`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| users | array<object> | 否 |  | [{"username":"sample-sam","role":"default"}] |
| users[].username | string | 否 |  | sample-sam |
| users[].role | string | 否 |  | default |

**成功响应示例（200）**

```json
{
  "users": [
    {
      "username": "sample-sam",
      "role": "default"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/admin/users" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/admin/users/{id}

- **用途**：Update existing user settings. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/users/1`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | id of the user in the database. | 1 |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Key pair object that will update the found user. All fields are optional and will not update unless specified.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| username | string | 否 |  | sample-sam |
| password | string | 否 |  | hunter2 |
| role | string | 否 |  | default \| admin |
| suspended | number | 否 |  | 0 |

请求体示例：

```json
{
  "username": "sample-sam",
  "password": "hunter2",
  "role": "default | admin",
  "suspended": 0
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/users/1" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "username": "sample-sam",
  "password": "hunter2",
  "role": "default | admin",
  "suspended": 0
}'
```

#### DELETE /v1/admin/users/{id}

- **用途**：Delete existing user by id. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/users/1`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| id | string | 是 | id of the user in the database. | 1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/admin/users/1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/admin/users/new

- **用途**：Create a new user with username and password. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/users/new`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Key pair object that will define the new user to add to the system.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| username | string | 否 |  | sample-sam |
| password | string | 否 |  | hunter2 |
| role | string | 否 |  | default \| admin |

请求体示例：

```json
{
  "username": "sample-sam",
  "password": "hunter2",
  "role": "default | admin"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| user | object | 否 |  | {"id":1,"username":"sample-sam","role":"default"} |
| user.id | number | 否 |  | 1 |
| user.username | string | 否 |  | sample-sam |
| user.role | string | 否 |  | default |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "user": {
    "id": 1,
    "username": "sample-sam",
    "role": "default"
  },
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/users/new" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "username": "sample-sam",
  "password": "hunter2",
  "role": "default | admin"
}'
```

#### POST /v1/admin/workspace-chats

- **用途**：All chats in the system ordered by most recent. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/workspace-chats`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：否
- **说明**：Page offset to show of workspace chats. All fields are optional and will not update unless specified.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| offset | number | 否 |  | 2 |

请求体示例：

```json
{
  "offset": 2
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/workspace-chats" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "offset": 2
}'
```

#### POST /v1/admin/workspaces/{workspaceId}/update-users

- **用途**：Overwrite workspace permissions to only be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/workspaces/1/update-users`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth
- **状态**：⚠️ Swagger 标记为 deprecated，优先使用替代接口。

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | id of the workspace in the database. | 1 |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Entire array of user ids who can access the workspace. All fields are optional and will not update unless specified.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| userIds | array<number> | 否 |  | [1,2,4,12] |

请求体示例：

```json
{
  "userIds": [
    1,
    2,
    4,
    12
  ]
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/workspaces/1/update-users" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "userIds": [
    1,
    2,
    4,
    12
  ]
}'
```

#### GET /v1/admin/workspaces/{workspaceId}/users

- **用途**：Retrieve a list of users with permissions to access the specified workspace.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/workspaces/1/users`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | id of the workspace. | 1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| users | array<object> | 否 |  | [{"userId":1,"role":"admin"},{"userId":2,"role":"member"}] |
| users[].userId | number | 否 |  | 1 |
| users[].role | string | 否 |  | admin |

**成功响应示例（200）**

```json
{
  "users": [
    {
      "userId": 1,
      "role": "admin"
    },
    {
      "userId": 2,
      "role": "member"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/admin/workspaces/1/users" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/admin/workspaces/{workspaceSlug}/manage-users

- **用途**：Set workspace permissions to be accessible by the given user ids and admins. Methods are disabled until multi user mode is enabled via the UI.
- **完整地址**：`http://127.0.0.1:3001/api/v1/admin/workspaces/sample-workspace/manage-users`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspaceSlug | string | 是 | slug of the workspace in the database | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Array of user ids who will be given access to the target workspace. <code>reset</code> will remove all existing users from the workspace and only add the new users - default <code>false</code>.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| userIds | array<number> | 否 |  | [1,2,4,12] |
| reset | boolean | 否 |  | false |

请求体示例：

```json
{
  "userIds": [
    1,
    2,
    4,
    12
  ],
  "reset": false
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Method denied | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 404 | Not Found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |
| users | array<object> | 否 |  | [{"userId":1,"username":"main-admin","role":"admin"},{"userId":2,"username":"sample-sam","role":"default"}] |
| users[].userId | number | 否 |  | 1 |
| users[].username | string | 否 |  | main-admin |
| users[].role | string | 否 |  | admin |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null,
  "users": [
    {
      "userId": 1,
      "username": "main-admin",
      "role": "admin"
    },
    {
      "userId": 2,
      "username": "sample-sam",
      "role": "default"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/admin/workspaces/sample-workspace/manage-users" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "userIds": [
    1,
    2,
    4,
    12
  ],
  "reset": false
}'
```

### Authentication（1）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/auth` | Verify the attached Authentication header contains a valid API token. |

#### GET /v1/auth

- **用途**：Verify the attached Authentication header contains a valid API token.
- **完整地址**：`http://127.0.0.1:3001/api/v1/auth`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | Valid auth token was found. | application/json |
| 403 | Forbidden | application/json, application/xml |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| authenticated | boolean | 否 |  | true |

**成功响应示例（200）**

```json
{
  "authenticated": true
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/auth" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Documents（12）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/document/{docName}` | Get a single document by its unique AnythingLLM document name |
| GET | `/v1/document/accepted-file-types` | Check available filetypes and MIMEs that can be uploaded. |
| POST | `/v1/document/create-folder` | Create a new folder inside the documents storage directory. |
| GET | `/v1/document/metadata-schema` | Get the known available metadata schema for when doing a raw-text upload and the acceptable type of value for each key. |
| POST | `/v1/document/move-files` | Move files within the documents storage directory. |
| POST | `/v1/document/raw-text` | Upload a file by specifying its raw text content and metadata values without having to upload a file. |
| DELETE | `/v1/document/remove-folder` | Remove a folder and all its contents from the documents storage directory. |
| POST | `/v1/document/upload` | Upload a new file to AnythingLLM to be parsed and prepared for embedding, with optional metadata. |
| POST | `/v1/document/upload-link` | Upload a valid URL for AnythingLLM to scrape and prepare for embedding. Optionally, specify a comma-separated list of workspace slugs to embed the document into post-upload. |
| POST | `/v1/document/upload/{folderName}` | Upload a new file to a specific folder in AnythingLLM to be parsed and prepared for embedding. If the folder does not exist, it will be created. |
| GET | `/v1/documents` | List of all locally-stored documents in instance |
| GET | `/v1/documents/folder/{folderName}` | Get all documents stored in a specific folder. |

#### GET /v1/document/{docName}

- **用途**：Get a single document by its unique AnythingLLM document name
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/custom-documents%2Fsample-document.json`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| docName | string | 是 | Unique document name to find (name in /documents) | custom-documents/sample-document.json |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Not Found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| localFiles | object | 否 |  | {"name":"documents","type":"folder","items":[{"name":"my-stored-document.txt-uuid1234.json","type":"file","id":"bb07c334-4dab-4419-9462-9d00065a49a1","url":"file://my-stored-document.txt","title":"my-stored-document.txt","cached":false}]} |
| localFiles.name | string | 否 |  | documents |
| localFiles.type | string | 否 |  | folder |
| localFiles.items | array<object> | 否 |  | [{"name":"my-stored-document.txt-uuid1234.json","type":"file","id":"bb07c334-4dab-4419-9462-9d00065a49a1","url":"file://my-stored-document.txt","title":"my-stored-document.txt","cached":false}] |

**成功响应示例（200）**

```json
{
  "localFiles": {
    "name": "documents",
    "type": "folder",
    "items": [
      {
        "name": "my-stored-document.txt-uuid1234.json",
        "type": "file",
        "id": "bb07c334-4dab-4419-9462-9d00065a49a1",
        "url": "file://my-stored-document.txt",
        "title": "my-stored-document.txt",
        "cached": false
      }
    ]
  }
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/document/custom-documents%2Fsample-document.json" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/document/accepted-file-types

- **用途**：Check available filetypes and MIMEs that can be uploaded.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/accepted-file-types`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Not Found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| types | object | 否 |  | {"application/mbox":[".mbox"],"application/pdf":[".pdf"],"application/vnd.oasis.opendocument.text":[".odt"],"application/vnd.openxmlformats-officedocument.wordprocessingml.document":[".docx"],"text/plain":[".txt",".md"]} |
| types.application/mbox | array<string> | 否 |  | [".mbox"] |
| types.application/pdf | array<string> | 否 |  | [".pdf"] |
| types.application/vnd.oasis.opendocument.text | array<string> | 否 |  | [".odt"] |
| types.application/vnd.openxmlformats-officedocument.wordprocessingml.document | array<string> | 否 |  | [".docx"] |
| types.text/plain | array<string> | 否 |  | [".txt",".md"] |

**成功响应示例（200）**

```json
{
  "types": {
    "application/mbox": [
      ".mbox"
    ],
    "application/pdf": [
      ".pdf"
    ],
    "application/vnd.oasis.opendocument.text": [
      ".odt"
    ],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
      ".docx"
    ],
    "text/plain": [
      ".txt",
      ".md"
    ]
  }
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/document/accepted-file-types" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/document/create-folder

- **用途**：Create a new folder inside the documents storage directory.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/create-folder`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Name of the folder to create.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| name | string | 否 |  | new-folder |

请求体示例：

```json
{
  "name": "new-folder"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/create-folder" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "name": "new-folder"
}'
```

#### GET /v1/document/metadata-schema

- **用途**：Get the known available metadata schema for when doing a raw-text upload and the acceptable type of value for each key.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/metadata-schema`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| schema | object | 否 |  | {"keyOne":"string \| number \| nullable","keyTwo":"string \| number \| nullable","specialKey":"number","title":"string"} |
| schema.keyOne | string | 否 |  | string \| number \| nullable |
| schema.keyTwo | string | 否 |  | string \| number \| nullable |
| schema.specialKey | string | 否 |  | number |
| schema.title | string | 否 |  | string |

**成功响应示例（200）**

```json
{
  "schema": {
    "keyOne": "string | number | nullable",
    "keyTwo": "string | number | nullable",
    "specialKey": "number",
    "title": "string"
  }
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/document/metadata-schema" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/document/move-files

- **用途**：Move files within the documents storage directory.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/move-files`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Array of objects containing source and destination paths of files to move.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| files | array<object> | 否 |  | [{"from":"custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json","to":"folder/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"}] |
| files[].from | string | 否 |  | custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json |
| files[].to | string | 否 |  | folder/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json |

请求体示例：

```json
{
  "files": [
    {
      "from": "custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json",
      "to": "folder/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"
    }
  ]
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/move-files" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "files": [
    {
      "from": "custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json",
      "to": "folder/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"
    }
  ]
}'
```

#### POST /v1/document/raw-text

- **用途**：Upload a file by specifying its raw text content and metadata values without having to upload a file.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/raw-text`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Text content and metadata of the file to be saved to the system. Use metadata-schema endpoint to get the possible metadata keys
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| textContent | string | 否 |  | This is the raw text that will be saved as a document in AnythingLLM. |
| addToWorkspaces | string | 否 |  | workspace1,workspace2 |
| metadata | object | 否 |  | {"title":"This key is required. See in /server/endpoints/api/document/index.js:287","keyOne":"valueOne","keyTwo":"valueTwo","etc":"etc"} |
| metadata.title | string | 否 |  | This key is required. See in /server/endpoints/api/document/index.js:287 |
| metadata.keyOne | string | 否 |  | valueOne |
| metadata.keyTwo | string | 否 |  | valueTwo |
| metadata.etc | string | 否 |  | etc |

请求体示例：

```json
{
  "textContent": "This is the raw text that will be saved as a document in AnythingLLM.",
  "addToWorkspaces": "workspace1,workspace2",
  "metadata": {
    "title": "This key is required. See in /server/endpoints/api/document/index.js:287",
    "keyOne": "valueOne",
    "keyTwo": "valueTwo",
    "etc": "etc"
  }
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 422 | Unprocessable Entity | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |
| documents | array<object> | 否 |  | [{"id":"c530dbe6-bff1-4b9e-b87f-710d539d20bc","url":"file://my-document.txt","title":"hello-world.txt","docAuthor":"no author found","description":"No description found.","docSource":"My custom description set during upload","chunkSource":"no chunk source specified","published":"1/16/2024, 3:46:33 PM","wordCount":252,"pageContent":"AnythingLLM is the best....","token_count_estimate":447,"location":"custom-documents/raw-my-doc-text-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json"}] |
| documents[].id | string | 否 |  | c530dbe6-bff1-4b9e-b87f-710d539d20bc |
| documents[].url | string | 否 |  | file://my-document.txt |
| documents[].title | string | 否 |  | hello-world.txt |
| documents[].docAuthor | string | 否 |  | no author found |
| documents[].description | string | 否 |  | No description found. |
| documents[].docSource | string | 否 |  | My custom description set during upload |
| documents[].chunkSource | string | 否 |  | no chunk source specified |
| documents[].published | string | 否 |  | 1/16/2024, 3:46:33 PM |
| documents[].wordCount | number | 否 |  | 252 |
| documents[].pageContent | string | 否 |  | AnythingLLM is the best.... |
| documents[].token_count_estimate | number | 否 |  | 447 |
| documents[].location | string | 否 |  | custom-documents/raw-my-doc-text-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null,
  "documents": [
    {
      "id": "c530dbe6-bff1-4b9e-b87f-710d539d20bc",
      "url": "file://my-document.txt",
      "title": "hello-world.txt",
      "docAuthor": "no author found",
      "description": "No description found.",
      "docSource": "My custom description set during upload",
      "chunkSource": "no chunk source specified",
      "published": "1/16/2024, 3:46:33 PM",
      "wordCount": 252,
      "pageContent": "AnythingLLM is the best....",
      "token_count_estimate": 447,
      "location": "custom-documents/raw-my-doc-text-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/raw-text" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "textContent": "This is the raw text that will be saved as a document in AnythingLLM.",
  "addToWorkspaces": "workspace1,workspace2",
  "metadata": {
    "title": "This key is required. See in /server/endpoints/api/document/index.js:287",
    "keyOne": "valueOne",
    "keyTwo": "valueTwo",
    "etc": "etc"
  }
}'
```

#### DELETE /v1/document/remove-folder

- **用途**：Remove a folder and all its contents from the documents storage directory.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/remove-folder`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Name of the folder to remove.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| name | string | 否 |  | my-folder |

请求体示例：

```json
{
  "name": "my-folder"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| message | string | 否 |  | Folder removed successfully |

**成功响应示例（200）**

```json
{
  "success": true,
  "message": "Folder removed successfully"
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/document/remove-folder" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "name": "my-folder"
}'
```

#### POST /v1/document/upload

- **用途**：Upload a new file to AnythingLLM to be parsed and prepared for embedding, with optional metadata.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/upload`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：File to be uploaded.
- **Content-Type**：multipart/form-data

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| file | string | 是 | The file to upload |  |
| addToWorkspaces | string | 否 | comma-separated text-string of workspace slugs to embed the document into post-upload. eg: workspace1,workspace2 |  |
| metadata | object | 否 | Key:Value pairs of metadata to attach to the document in JSON Object format. Only specific keys are allowed - see example. | {"title":"Custom Title","docAuthor":"Author Name","description":"A brief description","docSource":"Source of the document"} |
| metadata.title | string | 否 |  | Custom Title |
| metadata.docAuthor | string | 否 |  | Author Name |
| metadata.description | string | 否 |  | A brief description |
| metadata.docSource | string | 否 |  | Source of the document |

请求体示例：

```
{
  "metadata": {
    "title": "Custom Title",
    "docAuthor": "Author Name",
    "description": "A brief description",
    "docSource": "Source of the document"
  }
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 422 | Unprocessable Entity | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |
| documents | array<object> | 否 |  | [{"location":"custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json","name":"anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json","url":"file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt","title":"anythingllm.txt","docAuthor":"Unknown","description":"Unknown","docSource":"a text file uploaded by the user.","chunkSource":"anythingllm.txt","published":"1/16/2024, 3:07:00 PM","wordCount":93,"token_count_estimate":115}] |
| documents[].location | string | 否 |  | custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json |
| documents[].name | string | 否 |  | anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json |
| documents[].url | string | 否 |  | file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt |
| documents[].title | string | 否 |  | anythingllm.txt |
| documents[].docAuthor | string | 否 |  | Unknown |
| documents[].description | string | 否 |  | Unknown |
| documents[].docSource | string | 否 |  | a text file uploaded by the user. |
| documents[].chunkSource | string | 否 |  | anythingllm.txt |
| documents[].published | string | 否 |  | 1/16/2024, 3:07:00 PM |
| documents[].wordCount | number | 否 |  | 93 |
| documents[].token_count_estimate | number | 否 |  | 115 |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null,
  "documents": [
    {
      "location": "custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json",
      "name": "anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json",
      "url": "file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt",
      "title": "anythingllm.txt",
      "docAuthor": "Unknown",
      "description": "Unknown",
      "docSource": "a text file uploaded by the user.",
      "chunkSource": "anythingllm.txt",
      "published": "1/16/2024, 3:07:00 PM",
      "wordCount": 93,
      "token_count_estimate": 115
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/upload" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -F "file=@/path/to/file" \\n  -F "addToWorkspaces=workspace1,workspace2" \\n  -F "metadata={\"title\":\"Custom Title\",\"docAuthor\":\"Author Name\",\"description\":\"A brief description\",\"docSource\":\"Source of the document\"}"
```

#### POST /v1/document/upload-link

- **用途**：Upload a valid URL for AnythingLLM to scrape and prepare for embedding. Optionally, specify a comma-separated list of workspace slugs to embed the document into post-upload.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/upload-link`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Link of web address to be scraped and optionally a comma-separated list of workspace slugs to embed the document into post-upload, and optional metadata.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| link | string | 否 |  | https://anythingllm.com |
| addToWorkspaces | string | 否 |  | workspace1,workspace2 |
| scraperHeaders | object | 否 |  | {"Authorization":"Bearer token123","My-Custom-Header":"value"} |
| scraperHeaders.Authorization | string | 否 |  | Bearer token123 |
| scraperHeaders.My-Custom-Header | string | 否 |  | value |
| metadata | object | 否 |  | {"title":"Custom Title","docAuthor":"Author Name","description":"A brief description","docSource":"Source of the document"} |
| metadata.title | string | 否 |  | Custom Title |
| metadata.docAuthor | string | 否 |  | Author Name |
| metadata.description | string | 否 |  | A brief description |
| metadata.docSource | string | 否 |  | Source of the document |

请求体示例：

```json
{
  "link": "https://anythingllm.com",
  "addToWorkspaces": "workspace1,workspace2",
  "scraperHeaders": {
    "Authorization": "Bearer token123",
    "My-Custom-Header": "value"
  },
  "metadata": {
    "title": "Custom Title",
    "docAuthor": "Author Name",
    "description": "A brief description",
    "docSource": "Source of the document"
  }
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 422 | Unprocessable Entity | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |
| documents | array<object> | 否 |  | [{"id":"c530dbe6-bff1-4b9e-b87f-710d539d20bc","url":"file://useanything_com.html","title":"useanything_com.html","docAuthor":"no author found","description":"No description found.","docSource":"URL link uploaded by the user.","chunkSource":"https:anythingllm.com.html","published":"1/16/2024, 3:46:33 PM","wordCount":252,"pageContent":"AnythingLLM is the best....","token_count_estimate":447,"location":"custom-documents/url-useanything_com-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json"}] |
| documents[].id | string | 否 |  | c530dbe6-bff1-4b9e-b87f-710d539d20bc |
| documents[].url | string | 否 |  | file://useanything_com.html |
| documents[].title | string | 否 |  | useanything_com.html |
| documents[].docAuthor | string | 否 |  | no author found |
| documents[].description | string | 否 |  | No description found. |
| documents[].docSource | string | 否 |  | URL link uploaded by the user. |
| documents[].chunkSource | string | 否 |  | https:anythingllm.com.html |
| documents[].published | string | 否 |  | 1/16/2024, 3:46:33 PM |
| documents[].wordCount | number | 否 |  | 252 |
| documents[].pageContent | string | 否 |  | AnythingLLM is the best.... |
| documents[].token_count_estimate | number | 否 |  | 447 |
| documents[].location | string | 否 |  | custom-documents/url-useanything_com-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null,
  "documents": [
    {
      "id": "c530dbe6-bff1-4b9e-b87f-710d539d20bc",
      "url": "file://useanything_com.html",
      "title": "useanything_com.html",
      "docAuthor": "no author found",
      "description": "No description found.",
      "docSource": "URL link uploaded by the user.",
      "chunkSource": "https:anythingllm.com.html",
      "published": "1/16/2024, 3:46:33 PM",
      "wordCount": 252,
      "pageContent": "AnythingLLM is the best....",
      "token_count_estimate": 447,
      "location": "custom-documents/url-useanything_com-c530dbe6-bff1-4b9e-b87f-710d539d20bc.json"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/upload-link" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "link": "https://anythingllm.com",
  "addToWorkspaces": "workspace1,workspace2",
  "scraperHeaders": {
    "Authorization": "Bearer token123",
    "My-Custom-Header": "value"
  },
  "metadata": {
    "title": "Custom Title",
    "docAuthor": "Author Name",
    "description": "A brief description",
    "docSource": "Source of the document"
  }
}'
```

#### POST /v1/document/upload/{folderName}

- **用途**：Upload a new file to a specific folder in AnythingLLM to be parsed and prepared for embedding. If the folder does not exist, it will be created.
- **完整地址**：`http://127.0.0.1:3001/api/v1/document/upload/my-folder`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| folderName | string | 是 | Target folder path (defaults to 'custom-documents' if not provided) | my-folder |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：File to be uploaded, with optional metadata.
- **Content-Type**：multipart/form-data

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| file | string | 是 | The file to upload |  |
| addToWorkspaces | string | 否 | comma-separated text-string of workspace slugs to embed the document into post-upload. eg: workspace1,workspace2 |  |
| metadata | object | 否 | Key:Value pairs of metadata to attach to the document in JSON Object format. Only specific keys are allowed - see example. | {"title":"Custom Title","docAuthor":"Author Name","description":"A brief description","docSource":"Source of the document"} |
| metadata.title | string | 否 |  | Custom Title |
| metadata.docAuthor | string | 否 |  | Author Name |
| metadata.description | string | 否 |  | A brief description |
| metadata.docSource | string | 否 |  | Source of the document |

请求体示例：

```
{
  "metadata": {
    "title": "Custom Title",
    "docAuthor": "Author Name",
    "description": "A brief description",
    "docSource": "Source of the document"
  }
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 422 | Unprocessable Entity | 未声明 |
| 500 | Internal Server Error | application/json |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |
| documents | array<object> | 否 |  | [{"location":"custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json","name":"anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json","url":"file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt","title":"anythingllm.txt","docAuthor":"Unknown","description":"Unknown","docSource":"a text file uploaded by the user.","chunkSource":"anythingllm.txt","published":"1/16/2024, 3:07:00 PM","wordCount":93,"token_count_estimate":115}] |
| documents[].location | string | 否 |  | custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json |
| documents[].name | string | 否 |  | anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json |
| documents[].url | string | 否 |  | file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt |
| documents[].title | string | 否 |  | anythingllm.txt |
| documents[].docAuthor | string | 否 |  | Unknown |
| documents[].description | string | 否 |  | Unknown |
| documents[].docSource | string | 否 |  | a text file uploaded by the user. |
| documents[].chunkSource | string | 否 |  | anythingllm.txt |
| documents[].published | string | 否 |  | 1/16/2024, 3:07:00 PM |
| documents[].wordCount | number | 否 |  | 93 |
| documents[].token_count_estimate | number | 否 |  | 115 |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null,
  "documents": [
    {
      "location": "custom-documents/anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json",
      "name": "anythingllm.txt-6e8be64c-c162-4b43-9997-b068c0071e8b.json",
      "url": "file://Users/tim/Documents/anything-llm/collector/hotdir/anythingllm.txt",
      "title": "anythingllm.txt",
      "docAuthor": "Unknown",
      "description": "Unknown",
      "docSource": "a text file uploaded by the user.",
      "chunkSource": "anythingllm.txt",
      "published": "1/16/2024, 3:07:00 PM",
      "wordCount": 93,
      "token_count_estimate": 115
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/document/upload/my-folder" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -F "file=@/path/to/file" \\n  -F "addToWorkspaces=workspace1,workspace2" \\n  -F "metadata={\"title\":\"Custom Title\",\"docAuthor\":\"Author Name\",\"description\":\"A brief description\",\"docSource\":\"Source of the document\"}"
```

#### GET /v1/documents

- **用途**：List of all locally-stored documents in instance
- **完整地址**：`http://127.0.0.1:3001/api/v1/documents`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| localFiles | object | 否 |  | {"name":"documents","type":"folder","items":[{"name":"my-stored-document.json","type":"file","id":"bb07c334-4dab-4419-9462-9d00065a49a1","url":"file://my-stored-document.txt","title":"my-stored-document.txt","cached":false}]} |
| localFiles.name | string | 否 |  | documents |
| localFiles.type | string | 否 |  | folder |
| localFiles.items | array<object> | 否 |  | [{"name":"my-stored-document.json","type":"file","id":"bb07c334-4dab-4419-9462-9d00065a49a1","url":"file://my-stored-document.txt","title":"my-stored-document.txt","cached":false}] |

**成功响应示例（200）**

```json
{
  "localFiles": {
    "name": "documents",
    "type": "folder",
    "items": [
      {
        "name": "my-stored-document.json",
        "type": "file",
        "id": "bb07c334-4dab-4419-9462-9d00065a49a1",
        "url": "file://my-stored-document.txt",
        "title": "my-stored-document.txt",
        "cached": false
      }
    ]
  }
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/documents" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/documents/folder/{folderName}

- **用途**：Get all documents stored in a specific folder.
- **完整地址**：`http://127.0.0.1:3001/api/v1/documents/folder/my-folder`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| folderName | string | 是 | Name of the folder to retrieve documents from | my-folder |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| folder | string | 否 |  | custom-documents |
| documents | array<object> | 否 |  | [{"name":"document1.json","type":"file","cached":false,"pinnedWorkspaces":[],"watched":false,"more":"data"},{"name":"document2.json","type":"file","cached":false,"pinnedWorkspaces":[],"watched":false,"more":"data"}] |
| documents[].name | string | 否 |  | document1.json |
| documents[].type | string | 否 |  | file |
| documents[].cached | boolean | 否 |  | false |
| documents[].pinnedWorkspaces | array<any> | 否 |  | [] |
| documents[].watched | boolean | 否 |  | false |
| documents[].more | string | 否 |  | data |

**成功响应示例（200）**

```json
{
  "folder": "custom-documents",
  "documents": [
    {
      "name": "document1.json",
      "type": "file",
      "cached": false,
      "pinnedWorkspaces": [],
      "watched": false,
      "more": "data"
    },
    {
      "name": "document2.json",
      "type": "file",
      "cached": false,
      "pinnedWorkspaces": [],
      "watched": false,
      "more": "data"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/documents/folder/my-folder" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Embed（6）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/embed` | List all active embeds |
| POST | `/v1/embed/{embedUuid}` | Update an existing embed configuration |
| DELETE | `/v1/embed/{embedUuid}` | Delete an existing embed configuration |
| GET | `/v1/embed/{embedUuid}/chats` | Get all chats for a specific embed |
| GET | `/v1/embed/{embedUuid}/chats/{sessionUuid}` | Get chats for a specific embed and session |
| POST | `/v1/embed/new` | Create a new embed configuration |

#### GET /v1/embed

- **用途**：List all active embeds
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embeds | array<object> | 否 |  | [{"id":1,"uuid":"embed-uuid-1","enabled":true,"chat_mode":"query","createdAt":"2023-04-01T12:00:00Z","workspace":{"id":1,"name":"Workspace 1"},"chat_count":10},{"id":2,"uuid":"embed-uuid-2","enabled":false,"chat_mode":"chat","createdAt":"2023-04-02T14:30:00Z","workspace":{"id":1,"name":"Workspace 1"},"chat_count":10}] |
| embeds[].id | number | 否 |  | 1 |
| embeds[].uuid | string | 否 |  | embed-uuid-1 |
| embeds[].enabled | boolean | 否 |  | true |
| embeds[].chat_mode | string | 否 |  | query |
| embeds[].createdAt | string | 否 |  | 2023-04-01T12:00:00Z |
| embeds[].workspace | object | 否 |  | {"id":1,"name":"Workspace 1"} |
| embeds[].chat_count | number | 否 |  | 10 |

**成功响应示例（200）**

```json
{
  "embeds": [
    {
      "id": 1,
      "uuid": "embed-uuid-1",
      "enabled": true,
      "chat_mode": "query",
      "createdAt": "2023-04-01T12:00:00Z",
      "workspace": {
        "id": 1,
        "name": "Workspace 1"
      },
      "chat_count": 10
    },
    {
      "id": 2,
      "uuid": "embed-uuid-2",
      "enabled": false,
      "chat_mode": "chat",
      "createdAt": "2023-04-02T14:30:00Z",
      "workspace": {
        "id": 1,
        "name": "Workspace 1"
      },
      "chat_count": 10
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/embed" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/embed/{embedUuid}

- **用途**：Update an existing embed configuration
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed/embed-uuid-1`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embedUuid | string | 是 | UUID of the embed to update | embed-uuid-1 |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object containing embed configuration updates
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| enabled | boolean | 否 |  | true |
| chat_mode | string | 否 |  | chat |
| allowlist_domains | array<string> | 否 |  | ["example.com"] |
| allow_model_override | boolean | 否 |  | false |
| allow_temperature_override | boolean | 否 |  | false |
| allow_prompt_override | boolean | 否 |  | false |
| max_chats_per_day | number | 否 |  | 100 |
| max_chats_per_session | number | 否 |  | 10 |

请求体示例：

```json
{
  "enabled": true,
  "chat_mode": "chat",
  "allowlist_domains": [
    "example.com"
  ],
  "allow_model_override": false,
  "allow_temperature_override": false,
  "allow_prompt_override": false,
  "max_chats_per_day": 100,
  "max_chats_per_session": 10
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Embed not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/embed/embed-uuid-1" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "enabled": true,
  "chat_mode": "chat",
  "allowlist_domains": [
    "example.com"
  ],
  "allow_model_override": false,
  "allow_temperature_override": false,
  "allow_prompt_override": false,
  "max_chats_per_day": 100,
  "max_chats_per_session": 10
}'
```

#### DELETE /v1/embed/{embedUuid}

- **用途**：Delete an existing embed configuration
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed/embed-uuid-1`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embedUuid | string | 是 | UUID of the embed to delete | embed-uuid-1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Embed not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "success": true,
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/embed/embed-uuid-1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/embed/{embedUuid}/chats

- **用途**：Get all chats for a specific embed
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed/embed-uuid-1/chats`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embedUuid | string | 是 | UUID of the embed | embed-uuid-1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Embed not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| chats | array<object> | 否 |  | [{"id":1,"session_id":"session-uuid-1","prompt":"Hello","response":"Hi there!","createdAt":"2023-04-01T12:00:00Z"},{"id":2,"session_id":"session-uuid-2","prompt":"How are you?","response":"I'm doing well, thank you!","createdAt":"2023-04-02T14:30:00Z"}] |
| chats[].id | number | 否 |  | 1 |
| chats[].session_id | string | 否 |  | session-uuid-1 |
| chats[].prompt | string | 否 |  | Hello |
| chats[].response | string | 否 |  | Hi there! |
| chats[].createdAt | string | 否 |  | 2023-04-01T12:00:00Z |

**成功响应示例（200）**

```json
{
  "chats": [
    {
      "id": 1,
      "session_id": "session-uuid-1",
      "prompt": "Hello",
      "response": "Hi there!",
      "createdAt": "2023-04-01T12:00:00Z"
    },
    {
      "id": 2,
      "session_id": "session-uuid-2",
      "prompt": "How are you?",
      "response": "I'm doing well, thank you!",
      "createdAt": "2023-04-02T14:30:00Z"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/embed/embed-uuid-1/chats" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/embed/{embedUuid}/chats/{sessionUuid}

- **用途**：Get chats for a specific embed and session
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed/embed-uuid-1/chats/session-uuid-1`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embedUuid | string | 是 | UUID of the embed | embed-uuid-1 |
| sessionUuid | string | 是 | UUID of the session | session-uuid-1 |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 404 | Embed or session not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| chats | array<object> | 否 |  | [{"id":1,"prompt":"Hello","response":"Hi there!","createdAt":"2023-04-01T12:00:00Z"}] |
| chats[].id | number | 否 |  | 1 |
| chats[].prompt | string | 否 |  | Hello |
| chats[].response | string | 否 |  | Hi there! |
| chats[].createdAt | string | 否 |  | 2023-04-01T12:00:00Z |

**成功响应示例（200）**

```json
{
  "chats": [
    {
      "id": 1,
      "prompt": "Hello",
      "response": "Hi there!",
      "createdAt": "2023-04-01T12:00:00Z"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/embed/embed-uuid-1/chats/session-uuid-1" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/embed/new

- **用途**：Create a new embed configuration
- **完整地址**：`http://127.0.0.1:3001/api/v1/embed/new`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object containing embed configuration details
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspace_slug | string | 否 |  | workspace-slug-1 |
| chat_mode | string | 否 |  | chat |
| allowlist_domains | array<string> | 否 |  | ["example.com"] |
| allow_model_override | boolean | 否 |  | false |
| allow_temperature_override | boolean | 否 |  | false |
| allow_prompt_override | boolean | 否 |  | false |
| max_chats_per_day | number | 否 |  | 100 |
| max_chats_per_session | number | 否 |  | 10 |

请求体示例：

```json
{
  "workspace_slug": "workspace-slug-1",
  "chat_mode": "chat",
  "allowlist_domains": [
    "example.com"
  ],
  "allow_model_override": false,
  "allow_temperature_override": false,
  "allow_prompt_override": false,
  "max_chats_per_day": 100,
  "max_chats_per_session": 10
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 404 | Workspace not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| embed | object | 否 |  | {"id":1,"uuid":"embed-uuid-1","enabled":true,"chat_mode":"chat","allowlist_domains":["example.com"],"allow_model_override":false,"allow_temperature_override":false,"allow_prompt_override":false,"max_chats_per_day":100,"max_chats_per_session":10,"createdAt":"2023-04-01T12:00:00Z","workspace_slug":"workspace-slug-1"} |
| embed.id | number | 否 |  | 1 |
| embed.uuid | string | 否 |  | embed-uuid-1 |
| embed.enabled | boolean | 否 |  | true |
| embed.chat_mode | string | 否 |  | chat |
| embed.allowlist_domains | array<string> | 否 |  | ["example.com"] |
| embed.allow_model_override | boolean | 否 |  | false |
| embed.allow_temperature_override | boolean | 否 |  | false |
| embed.allow_prompt_override | boolean | 否 |  | false |
| embed.max_chats_per_day | number | 否 |  | 100 |
| embed.max_chats_per_session | number | 否 |  | 10 |
| embed.createdAt | string | 否 |  | 2023-04-01T12:00:00Z |
| embed.workspace_slug | string | 否 |  | workspace-slug-1 |
| error | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "embed": {
    "id": 1,
    "uuid": "embed-uuid-1",
    "enabled": true,
    "chat_mode": "chat",
    "allowlist_domains": [
      "example.com"
    ],
    "allow_model_override": false,
    "allow_temperature_override": false,
    "allow_prompt_override": false,
    "max_chats_per_day": 100,
    "max_chats_per_session": 10,
    "createdAt": "2023-04-01T12:00:00Z",
    "workspace_slug": "workspace-slug-1"
  },
  "error": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/embed/new" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "workspace_slug": "workspace-slug-1",
  "chat_mode": "chat",
  "allowlist_domains": [
    "example.com"
  ],
  "allow_model_override": false,
  "allow_temperature_override": false,
  "allow_prompt_override": false,
  "max_chats_per_day": 100,
  "max_chats_per_session": 10
}'
```

### OpenAI Compatible Endpoints（4）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| POST | `/v1/openai/chat/completions` | Execute a chat with a workspace with OpenAI compatibility. Supports streaming as well. Model must be a workspace slug from /models. |
| POST | `/v1/openai/embeddings` | Get the embeddings of any arbitrary text string. This will use the embedder provider set in the system. Please ensure the token length of each string fits within the context of your embedder model. |
| GET | `/v1/openai/models` | Get all available "models" which are workspaces you can use for chatting. |
| GET | `/v1/openai/vector_stores` | List all the vector database collections connected to AnythingLLM. These are essentially workspaces but return their unique vector db identifier - this is the same as the workspace slug. |

#### POST /v1/openai/chat/completions

- **用途**：Execute a chat with a workspace with OpenAI compatibility. Supports streaming as well. Model must be a workspace slug from /models.
- **完整地址**：`http://127.0.0.1:3001/api/v1/openai/chat/completions`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Send a prompt to the workspace with full use of documents as if sending a chat in AnythingLLM. Only supports some values of OpenAI API. See example below.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| messages | array<object> | 否 |  | [{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"What is AnythingLLM?"},{"role":"assistant","content":"AnythingLLM is...."},{"role":"user","content":"Follow up question..."}] |
| messages[].role | string | 否 |  | system |
| messages[].content | string | 否 |  | You are a helpful assistant |
| model | string | 否 |  | sample-workspace |
| stream | boolean | 否 |  | true |
| temperature | number | 否 |  | 0.7 |

请求体示例：

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant"
    },
    {
      "role": "user",
      "content": "What is AnythingLLM?"
    },
    {
      "role": "assistant",
      "content": "AnythingLLM is...."
    },
    {
      "role": "user",
      "content": "Follow up question..."
    }
  ],
  "model": "sample-workspace",
  "stream": true,
  "temperature": 0.7
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | 未声明 |
| 400 | Bad Request | 未声明 |
| 401 | Unauthorized | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/openai/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant"
    },
    {
      "role": "user",
      "content": "What is AnythingLLM?"
    },
    {
      "role": "assistant",
      "content": "AnythingLLM is...."
    },
    {
      "role": "user",
      "content": "Follow up question..."
    }
  ],
  "model": "sample-workspace",
  "stream": true,
  "temperature": 0.7
}'
```

#### POST /v1/openai/embeddings

- **用途**：Get the embeddings of any arbitrary text string. This will use the embedder provider set in the system. Please ensure the token length of each string fits within the context of your embedder model.
- **完整地址**：`http://127.0.0.1:3001/api/v1/openai/embeddings`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：The input string(s) to be embedded. If the text is too long for the embedder model context, it will fail to embed. The vector and associated chunk metadata will be returned in the array order provided
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| input | array<string> | 否 |  | ["This is my first string to embed","This is my second string to embed"] |
| model | null | 否 |  | null |

请求体示例：

```json
{
  "input": [
    "This is my first string to embed",
    "This is my second string to embed"
  ],
  "model": null
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/openai/embeddings" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "input": [
    "This is my first string to embed",
    "This is my second string to embed"
  ],
  "model": null
}'
```

#### GET /v1/openai/models

- **用途**：Get all available "models" which are workspaces you can use for chatting.
- **完整地址**：`http://127.0.0.1:3001/api/v1/openai/models`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| object | string | 否 |  | list |
| data | array<object> | 否 |  | [{"id":"model-id-0","object":"model","created":1686935002,"owned_by":"organization-owner"},{"id":"model-id-1","object":"model","created":1686935002,"owned_by":"organization-owner"}] |
| data[].id | string | 否 |  | model-id-0 |
| data[].object | string | 否 |  | model |
| data[].created | number | 否 |  | 1686935002 |
| data[].owned_by | string | 否 |  | organization-owner |

**成功响应示例（200）**

```json
{
  "object": "list",
  "data": [
    {
      "id": "model-id-0",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    },
    {
      "id": "model-id-1",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/openai/models" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/openai/vector_stores

- **用途**：List all the vector database collections connected to AnythingLLM. These are essentially workspaces but return their unique vector db identifier - this is the same as the workspace slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/openai/vector_stores`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| data | array<object> | 否 |  | [{"id":"slug-here","object":"vector_store","name":"My workspace","file_counts":{"total":3},"provider":"LanceDB"}] |
| data[].id | string | 否 |  | slug-here |
| data[].object | string | 否 |  | vector_store |
| data[].name | string | 否 |  | My workspace |
| data[].file_counts | object | 否 |  | {"total":3} |
| data[].provider | string | 否 |  | LanceDB |

**成功响应示例（200）**

```json
{
  "data": [
    {
      "id": "slug-here",
      "object": "vector_store",
      "name": "My workspace",
      "file_counts": {
        "total": 3
      },
      "provider": "LanceDB"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/openai/vector_stores" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### System Settings（6）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/system` | Get all current system settings that are defined. |
| GET | `/v1/system/env-dump` | Dump all settings to file storage |
| GET | `/v1/system/export-chats` | Export all of the chats from the system in a known format. Output depends on the type sent. Will be send with the correct header for the output. |
| DELETE | `/v1/system/remove-documents` | Permanently remove documents from the system. |
| POST | `/v1/system/update-env` | Update a system setting or preference. |
| GET | `/v1/system/vector-count` | Number of all vectors in connected vector database |

#### GET /v1/system

- **用途**：Get all current system settings that are defined.
- **完整地址**：`http://127.0.0.1:3001/api/v1/system`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| settings | object | 否 |  | {"VectorDB":"pinecone","PineConeKey":true,"PineConeIndex":"my-pinecone-index","LLMProvider":"azure","[KEY_NAME]":"KEY_VALUE"} |
| settings.VectorDB | string | 否 |  | pinecone |
| settings.PineConeKey | boolean | 否 |  | true |
| settings.PineConeIndex | string | 否 |  | my-pinecone-index |
| settings.LLMProvider | string | 否 |  | azure |
| settings.[KEY_NAME] | string | 否 |  | KEY_VALUE |

**成功响应示例（200）**

```json
{
  "settings": {
    "VectorDB": "pinecone",
    "PineConeKey": true,
    "PineConeIndex": "my-pinecone-index",
    "LLMProvider": "azure",
    "[KEY_NAME]": "KEY_VALUE"
  }
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/system" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/system/env-dump

- **用途**：Dump all settings to file storage
- **完整地址**：`http://127.0.0.1:3001/api/v1/system/env-dump`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/system/env-dump" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### GET /v1/system/export-chats

- **用途**：Export all of the chats from the system in a known format. Output depends on the type sent. Will be send with the correct header for the output.
- **完整地址**：`http://127.0.0.1:3001/api/v1/system/export-chats?type=json`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| type | string | 否 | Export format jsonl, json, csv, jsonAlpaca | json |

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应示例（200）**

```json
[
  {
    "role": "user",
    "content": "What is AnythinglLM?"
  },
  {
    "role": "assistant",
    "content": "AnythingLLM is a knowledge graph and vector database management system built using NodeJS express server. It provides an interface for handling all interactions, including vectorDB management and LLM (Language Model) interactions."
  }
]
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/system/export-chats?type=json" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### DELETE /v1/system/remove-documents

- **用途**：Permanently remove documents from the system.
- **完整地址**：`http://127.0.0.1:3001/api/v1/system/remove-documents`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Array of document names to be removed permanently.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| names | array<string> | 否 |  | ["custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"] |

请求体示例：

```json
{
  "names": [
    "custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"
  ]
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | Documents removed successfully. | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| success | boolean | 否 |  | true |
| message | string | 否 |  | Documents removed successfully |

**成功响应示例（200）**

```json
{
  "success": true,
  "message": "Documents removed successfully"
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/system/remove-documents" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "names": [
    "custom-documents/file.txt-fc4beeeb-e436-454d-8bb4-e5b8979cb48f.json"
  ]
}'
```

#### POST /v1/system/update-env

- **用途**：Update a system setting or preference.
- **完整地址**：`http://127.0.0.1:3001/api/v1/system/update-env`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Key pair object that matches a valid setting and value. Get keys from GET /v1/system or refer to codebase.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| VectorDB | string | 否 |  | lancedb |
| AnotherKey | string | 否 |  | updatedValue |

请求体示例：

```json
{
  "VectorDB": "lancedb",
  "AnotherKey": "updatedValue"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| newValues | object | 否 |  | {"[ENV_KEY]":"Value"} |
| newValues.[ENV_KEY] | string | 否 |  | Value |
| error | string | 否 |  | error goes here, otherwise null |

**成功响应示例（200）**

```json
{
  "newValues": {
    "[ENV_KEY]": "Value"
  },
  "error": "error goes here, otherwise null"
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/system/update-env" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "VectorDB": "lancedb",
  "AnotherKey": "updatedValue"
}'
```

#### GET /v1/system/vector-count

- **用途**：Number of all vectors in connected vector database
- **完整地址**：`http://127.0.0.1:3001/api/v1/system/vector-count`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| vectorCount | number | 否 |  | 5450 |

**成功响应示例（200）**

```json
{
  "vectorCount": 5450
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/system/vector-count" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### User Management（1）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/users` | List all users |

#### GET /v1/users

- **用途**：List all users
- **完整地址**：`http://127.0.0.1:3001/api/v1/users`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 401 | Instance is not in Multi-User mode. Permission denied. | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| users | array<object> | 否 |  | [{"id":1,"username":"john_doe","role":"admin"},{"id":2,"username":"jane_smith","role":"default"}] |
| users[].id | number | 否 |  | 1 |
| users[].username | string | 否 |  | john_doe |
| users[].role | string | 否 |  | admin |

**成功响应示例（200）**

```json
{
  "users": [
    {
      "id": 1,
      "username": "john_doe",
      "role": "admin"
    },
    {
      "id": 2,
      "username": "jane_smith",
      "role": "default"
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/users" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Workspace Threads（6）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| DELETE | `/v1/workspace/{slug}/thread/{threadSlug}` | Delete a workspace thread |
| POST | `/v1/workspace/{slug}/thread/{threadSlug}/chat` | Chat with a workspace thread |
| GET | `/v1/workspace/{slug}/thread/{threadSlug}/chats` | Get chats for a workspace thread |
| POST | `/v1/workspace/{slug}/thread/{threadSlug}/stream-chat` | Stream chat with a workspace thread |
| POST | `/v1/workspace/{slug}/thread/{threadSlug}/update` | Update thread name by its unique slug. |
| POST | `/v1/workspace/{slug}/thread/new` | Create a new workspace thread |

#### DELETE /v1/workspace/{slug}/thread/{threadSlug}

- **用途**：Delete a workspace thread
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |
| threadSlug | string | 是 | Unique slug of thread | sample-thread |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | Thread deleted successfully | 未声明 |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/workspace/{slug}/thread/{threadSlug}/chat

- **用途**：Chat with a workspace thread
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/chat`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |
| threadSlug | string | 是 | Unique slug of thread | sample-thread |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Send a prompt to the workspace thread and the type of conversation (query or chat).
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| message | string | 否 |  | What is AnythingLLM? |
| mode | string | 否 |  | query \| chat |
| userId | number | 否 |  | 1 |
| attachments | array<object> | 否 |  | [{"name":"image.png","mime":"image/png","contentString":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."}] |
| attachments[].name | string | 否 |  | image.png |
| attachments[].mime | string | 否 |  | image/png |
| attachments[].contentString | string | 否 |  | data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA... |
| reset | boolean | 否 |  | false |

请求体示例：

```json
{
  "message": "What is AnythingLLM?",
  "mode": "query | chat",
  "userId": 1,
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| id | string | 否 |  | chat-uuid |
| type | string | 否 |  | abort \| textResponse |
| textResponse | string | 否 |  | Response to your query |
| sources | array<object> | 否 |  | [{"title":"anythingllm.txt","chunk":"This is a context chunk used in the answer of the prompt by the LLM."}] |
| sources[].title | string | 否 |  | anythingllm.txt |
| sources[].chunk | string | 否 |  | This is a context chunk used in the answer of the prompt by the LLM. |
| close | boolean | 否 |  | true |
| error | string | 否 |  | null \| text string of the failure mode. |

**成功响应示例（200）**

```json
{
  "id": "chat-uuid",
  "type": "abort | textResponse",
  "textResponse": "Response to your query",
  "sources": [
    {
      "title": "anythingllm.txt",
      "chunk": "This is a context chunk used in the answer of the prompt by the LLM."
    }
  ],
  "close": true,
  "error": "null | text string of the failure mode."
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "message": "What is AnythingLLM?",
  "mode": "query | chat",
  "userId": 1,
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}'
```

#### GET /v1/workspace/{slug}/thread/{threadSlug}/chats

- **用途**：Get chats for a workspace thread
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/chats`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |
| threadSlug | string | 是 | Unique slug of thread | sample-thread |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| history | array<object> | 否 |  | [{"role":"user","content":"What is AnythingLLM?","sentAt":1692851630},{"role":"assistant","content":"AnythingLLM is a platform that allows you to convert notes, PDFs, and other source materials into a chatbot. It ensures privacy, cites its answers, and allows multiple people to interact with the same documents simultaneously. It is particularly useful for businesses to enhance the visibility and readability of various written communications such as SOPs, contracts, and sales calls. You can try it out with a free trial to see if it meets your business needs.","sources":[{"source":"object about source document and snippets used"}]}] |
| history[].role | string | 否 |  | user |
| history[].content | string | 否 |  | What is AnythingLLM? |
| history[].sentAt | number | 否 |  | 1692851630 |

**成功响应示例（200）**

```json
{
  "history": [
    {
      "role": "user",
      "content": "What is AnythingLLM?",
      "sentAt": 1692851630
    },
    {
      "role": "assistant",
      "content": "AnythingLLM is a platform that allows you to convert notes, PDFs, and other source materials into a chatbot. It ensures privacy, cites its answers, and allows multiple people to interact with the same documents simultaneously. It is particularly useful for businesses to enhance the visibility and readability of various written communications such as SOPs, contracts, and sales calls. You can try it out with a free trial to see if it meets your business needs.",
      "sources": [
        {
          "source": "object about source document and snippets used"
        }
      ]
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/chats" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/workspace/{slug}/thread/{threadSlug}/stream-chat

- **用途**：Stream chat with a workspace thread
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/stream-chat`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |
| threadSlug | string | 是 | Unique slug of thread | sample-thread |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Send a prompt to the workspace thread and the type of conversation (query or chat).
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| message | string | 否 |  | What is AnythingLLM? |
| mode | string | 否 |  | query \| chat |
| userId | number | 否 |  | 1 |
| attachments | array<object> | 否 |  | [{"name":"image.png","mime":"image/png","contentString":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."},{"name":"this is a document.pdf","mime":"application/anythingllm-document","contentString":"data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."}] |
| attachments[].name | string | 否 |  | image.png |
| attachments[].mime | string | 否 |  | image/png |
| attachments[].contentString | string | 否 |  | data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA... |
| reset | boolean | 否 |  | false |

请求体示例：

```json
{
  "message": "What is AnythingLLM?",
  "mode": "query | chat",
  "userId": 1,
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | text/event-stream |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |

**成功响应示例（200）**

```
[
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "First chunk",
    "sources": [],
    "close": false,
    "error": "null | text string of the failure mode."
  },
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "chunk two",
    "sources": [],
    "close": false,
    "error": "null | text string of the failure mode."
  },
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "final chunk of LLM output!",
    "sources": [
      {
        "title": "anythingllm.txt",
        "chunk": "This is a context chunk used in the answer of the prompt by the LLM. This will only return in the final chunk."
      }
    ],
    "close": true,
    "error": "null | text string of the failure mode."
  }
]
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -N -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/stream-chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "message": "What is AnythingLLM?",
  "mode": "query | chat",
  "userId": 1,
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}'
```

#### POST /v1/workspace/{slug}/thread/{threadSlug}/update

- **用途**：Update thread name by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/update`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |
| threadSlug | string | 是 | Unique slug of thread | sample-thread |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object containing new name to update the thread.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| name | string | 否 |  | Updated Thread Name |

请求体示例：

```json
{
  "name": "Updated Thread Name"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| thread | object | 否 |  | {"id":1,"name":"Updated Thread Name","slug":"thread-uuid","user_id":1,"workspace_id":1} |
| thread.id | number | 否 |  | 1 |
| thread.name | string | 否 |  | Updated Thread Name |
| thread.slug | string | 否 |  | thread-uuid |
| thread.user_id | number | 否 |  | 1 |
| thread.workspace_id | number | 否 |  | 1 |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "thread": {
    "id": 1,
    "name": "Updated Thread Name",
    "slug": "thread-uuid",
    "user_id": 1,
    "workspace_id": 1
  },
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/sample-thread/update" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "name": "Updated Thread Name"
}'
```

#### POST /v1/workspace/{slug}/thread/new

- **用途**：Create a new workspace thread
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/new`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：否
- **说明**：Optional userId associated with the thread, thread slug and thread name
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| userId | number | 否 |  | 1 |
| name | string | 否 |  | Name |
| slug | string | 否 |  | thread-slug |

请求体示例：

```json
{
  "userId": 1,
  "name": "Name",
  "slug": "thread-slug"
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| thread | object | 否 |  | {"id":1,"name":"Thread","slug":"thread-uuid","user_id":1,"workspace_id":1} |
| thread.id | number | 否 |  | 1 |
| thread.name | string | 否 |  | Thread |
| thread.slug | string | 否 |  | thread-uuid |
| thread.user_id | number | 否 |  | 1 |
| thread.workspace_id | number | 否 |  | 1 |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "thread": {
    "id": 1,
    "name": "Thread",
    "slug": "thread-uuid",
    "user_id": 1,
    "workspace_id": 1
  },
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/thread/new" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "userId": 1,
  "name": "Name",
  "slug": "thread-slug"
}'
```

### Workspaces（11）

| 方法 | 路径 | 用途 |
| --- | --- | --- |
| GET | `/v1/workspace/{slug}` | Get a workspace by its unique slug. |
| DELETE | `/v1/workspace/{slug}` | Deletes a workspace by its slug. |
| POST | `/v1/workspace/{slug}/chat` | Execute a chat with a workspace |
| GET | `/v1/workspace/{slug}/chats` | Get a workspaces chats regardless of user by its unique slug. |
| POST | `/v1/workspace/{slug}/stream-chat` | Execute a streamable chat with a workspace |
| POST | `/v1/workspace/{slug}/update` | Update workspace settings by its unique slug. |
| POST | `/v1/workspace/{slug}/update-embeddings` | Add or remove documents from a workspace by its unique slug. |
| POST | `/v1/workspace/{slug}/update-pin` | Add or remove pin from a document in a workspace by its unique slug. |
| POST | `/v1/workspace/{slug}/vector-search` | Perform a vector similarity search in a workspace |
| POST | `/v1/workspace/new` | Create a new workspace |
| GET | `/v1/workspaces` | List all current workspaces |

#### GET /v1/workspace/{slug}

- **用途**：Get a workspace by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to find | sample-workspace |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspace | array<object> | 否 |  | [{"id":79,"name":"My workspace","slug":"my-workspace-123","createdAt":"2023-08-17 00:45:03","openAiTemp":null,"lastUpdatedAt":"2023-08-17 00:45:03","openAiHistory":20,"openAiPrompt":null,"documents":[],"threads":[]}] |
| workspace[].id | number | 否 |  | 79 |
| workspace[].name | string | 否 |  | My workspace |
| workspace[].slug | string | 否 |  | my-workspace-123 |
| workspace[].createdAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace[].openAiTemp | null | 否 |  | null |
| workspace[].lastUpdatedAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace[].openAiHistory | number | 否 |  | 20 |
| workspace[].openAiPrompt | null | 否 |  | null |
| workspace[].documents | array<any> | 否 |  | [] |
| workspace[].threads | array<any> | 否 |  | [] |

**成功响应示例（200）**

```json
{
  "workspace": [
    {
      "id": 79,
      "name": "My workspace",
      "slug": "my-workspace-123",
      "createdAt": "2023-08-17 00:45:03",
      "openAiTemp": null,
      "lastUpdatedAt": "2023-08-17 00:45:03",
      "openAiHistory": 20,
      "openAiPrompt": null,
      "documents": [],
      "threads": []
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/workspace/sample-workspace" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### DELETE /v1/workspace/{slug}

- **用途**：Deletes a workspace by its slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace`
- **动作类型**：删除
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to delete | sample-workspace |

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | 未声明 |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X DELETE "http://127.0.0.1:3001/api/v1/workspace/sample-workspace" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/workspace/{slug}/chat

- **用途**：Execute a chat with a workspace
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/chat`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 |  | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Send a prompt to the workspace and the type of conversation (automatic, query or chat).<br/><b>Query:</b> Will not use LLM unless there are relevant sources from vectorDB & does not recall chat history.<br/><b>Automatic:</b> Will use tool-calling if the provider supports native tool calling without needing to invoke @agent.<br/><b>Chat:</b> Uses LLM general knowledge w/custom embeddings to produce output, uses rolling chat history.<br/><b>Attachments:</b> Can include images and documents.<br/><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Document attachments:</b> must have the mime type <code>application/anythingllm-document</code> - otherwise it will be passed to the LLM as an image and may fail to process. This uses the built-in document processor to first parse the document to text before injecting it into the context window.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| message | string | 否 |  | What is AnythingLLM? |
| mode | string | 否 |  | automatic \| query \| chat |
| sessionId | string | 否 |  | identifier-to-partition-chats-by-external-id |
| attachments | array<object> | 否 |  | [{"name":"image.png","mime":"image/png","contentString":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."},{"name":"this is a document.pdf","mime":"application/anythingllm-document","contentString":"data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."}] |
| attachments[].name | string | 否 |  | image.png |
| attachments[].mime | string | 否 |  | image/png |
| attachments[].contentString | string | 否 |  | data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA... |
| reset | boolean | 否 |  | false |

请求体示例：

```json
{
  "message": "What is AnythingLLM?",
  "mode": "automatic | query | chat",
  "sessionId": "identifier-to-partition-chats-by-external-id",
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| id | string | 否 |  | chat-uuid |
| type | string | 否 |  | abort \| textResponse |
| textResponse | string | 否 |  | Response to your query |
| sources | array<object> | 否 |  | [{"title":"anythingllm.txt","chunk":"This is a context chunk used in the answer of the prompt by the LLM,"}] |
| sources[].title | string | 否 |  | anythingllm.txt |
| sources[].chunk | string | 否 |  | This is a context chunk used in the answer of the prompt by the LLM, |
| close | boolean | 否 |  | true |
| error | string | 否 |  | null \| text string of the failure mode. |

**成功响应示例（200）**

```json
{
  "id": "chat-uuid",
  "type": "abort | textResponse",
  "textResponse": "Response to your query",
  "sources": [
    {
      "title": "anythingllm.txt",
      "chunk": "This is a context chunk used in the answer of the prompt by the LLM,"
    }
  ],
  "close": true,
  "error": "null | text string of the failure mode."
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "message": "What is AnythingLLM?",
  "mode": "automatic | query | chat",
  "sessionId": "identifier-to-partition-chats-by-external-id",
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}'
```

#### GET /v1/workspace/{slug}/chats

- **用途**：Get a workspaces chats regardless of user by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/chats?apiSessionId=api-session-1&limit=100&orderBy=desc`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to find | sample-workspace |

**Query 参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| apiSessionId | string | 否 | Optional apiSessionId to filter by | api-session-1 |
| limit | integer | 否 | Optional number of chat messages to return (default: 100) | 100 |
| orderBy | string | 否 | Optional order of chat messages (asc or desc) | desc |

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| history | array<object> | 否 |  | [{"role":"user","content":"What is AnythingLLM?","sentAt":1692851630},{"role":"assistant","content":"AnythingLLM is a platform that allows you to convert notes, PDFs, and other source materials into a chatbot. It ensures privacy, cites its answers, and allows multiple people to interact with the same documents simultaneously. It is particularly useful for businesses to enhance the visibility and readability of various written communications such as SOPs, contracts, and sales calls. You can try it out with a free trial to see if it meets your business needs.","sources":[{"source":"object about source document and snippets used"}]}] |
| history[].role | string | 否 |  | user |
| history[].content | string | 否 |  | What is AnythingLLM? |
| history[].sentAt | number | 否 |  | 1692851630 |

**成功响应示例（200）**

```json
{
  "history": [
    {
      "role": "user",
      "content": "What is AnythingLLM?",
      "sentAt": 1692851630
    },
    {
      "role": "assistant",
      "content": "AnythingLLM is a platform that allows you to convert notes, PDFs, and other source materials into a chatbot. It ensures privacy, cites its answers, and allows multiple people to interact with the same documents simultaneously. It is particularly useful for businesses to enhance the visibility and readability of various written communications such as SOPs, contracts, and sales calls. You can try it out with a free trial to see if it meets your business needs.",
      "sources": [
        {
          "source": "object about source document and snippets used"
        }
      ]
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/chats?apiSessionId=api-session-1&limit=100&orderBy=desc" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### POST /v1/workspace/{slug}/stream-chat

- **用途**：Execute a streamable chat with a workspace
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/stream-chat`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 |  | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Send a prompt to the workspace and the type of conversation (automatic, query or chat).<br/><b>Query:</b> Will not use LLM unless there are relevant sources from vectorDB & does not recall chat history.<br/><b>Automatic:</b> Will use tool-calling if the provider supports native tool calling without needing to invoke @agent.<br/><b>Chat:</b> Uses LLM general knowledge w/custom embeddings to produce output, uses rolling chat history.<br/><b>Attachments:</b> Can include images and documents.<br/><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Document attachments:</b> must have the mime type <code>application/anythingllm-document</code> - otherwise it will be passed to the LLM as an image and may fail to process. This uses the built-in document processor to first parse the document to text before injecting it into the context window.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| message | string | 否 |  | What is AnythingLLM? |
| mode | string | 否 |  | automatic \| query \| chat |
| sessionId | string | 否 |  | identifier-to-partition-chats-by-external-id |
| attachments | array<object> | 否 |  | [{"name":"image.png","mime":"image/png","contentString":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."},{"name":"this is a document.pdf","mime":"application/anythingllm-document","contentString":"data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."}] |
| attachments[].name | string | 否 |  | image.png |
| attachments[].mime | string | 否 |  | image/png |
| attachments[].contentString | string | 否 |  | data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA... |
| reset | boolean | 否 |  | false |

请求体示例：

```json
{
  "message": "What is AnythingLLM?",
  "mode": "automatic | query | chat",
  "sessionId": "identifier-to-partition-chats-by-external-id",
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | text/event-stream |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |

**成功响应示例（200）**

```
[
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "First chunk",
    "sources": [],
    "close": false,
    "error": "null | text string of the failure mode."
  },
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "chunk two",
    "sources": [],
    "close": false,
    "error": "null | text string of the failure mode."
  },
  {
    "id": "uuid-123",
    "type": "abort | textResponseChunk",
    "textResponse": "final chunk of LLM output!",
    "sources": [
      {
        "title": "anythingllm.txt",
        "chunk": "This is a context chunk used in the answer of the prompt by the LLM. This will only return in the final chunk."
      }
    ],
    "close": true,
    "error": "null | text string of the failure mode."
  }
]
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -N -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/stream-chat" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "message": "What is AnythingLLM?",
  "mode": "automatic | query | chat",
  "sessionId": "identifier-to-partition-chats-by-external-id",
  "attachments": [
    {
      "name": "image.png",
      "mime": "image/png",
      "contentString": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    },
    {
      "name": "this is a document.pdf",
      "mime": "application/anythingllm-document",
      "contentString": "data:application/pdf;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    }
  ],
  "reset": false
}'
```

#### POST /v1/workspace/{slug}/update

- **用途**：Update workspace settings by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to find | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object containing new settings to update a workspace. All keys are optional and will not update unless provided
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| name | string | 否 |  | Updated Workspace Name |
| openAiTemp | number | 否 |  | 0.2 |
| openAiHistory | number | 否 |  | 20 |
| openAiPrompt | string | 否 |  | Respond to all inquires and questions in binary - do not respond in any other format. |

请求体示例：

```json
{
  "name": "Updated Workspace Name",
  "openAiTemp": 0.2,
  "openAiHistory": 20,
  "openAiPrompt": "Respond to all inquires and questions in binary - do not respond in any other format."
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspace | object | 否 |  | {"id":79,"name":"My workspace","slug":"my-workspace-123","createdAt":"2023-08-17 00:45:03","openAiTemp":null,"lastUpdatedAt":"2023-08-17 00:45:03","openAiHistory":20,"openAiPrompt":null,"documents":[]} |
| workspace.id | number | 否 |  | 79 |
| workspace.name | string | 否 |  | My workspace |
| workspace.slug | string | 否 |  | my-workspace-123 |
| workspace.createdAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiTemp | null | 否 |  | null |
| workspace.lastUpdatedAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiHistory | number | 否 |  | 20 |
| workspace.openAiPrompt | null | 否 |  | null |
| workspace.documents | array<any> | 否 |  | [] |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "workspace": {
    "id": 79,
    "name": "My workspace",
    "slug": "my-workspace-123",
    "createdAt": "2023-08-17 00:45:03",
    "openAiTemp": null,
    "lastUpdatedAt": "2023-08-17 00:45:03",
    "openAiHistory": 20,
    "openAiPrompt": null,
    "documents": []
  },
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "name": "Updated Workspace Name",
  "openAiTemp": 0.2,
  "openAiHistory": 20,
  "openAiPrompt": "Respond to all inquires and questions in binary - do not respond in any other format."
}'
```

#### POST /v1/workspace/{slug}/update-embeddings

- **用途**：Add or remove documents from a workspace by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update-embeddings`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to find | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object of additions and removals of documents to add to update a workspace. The value should be the folder + filename with the exclusions of the top-level documents path.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| adds | array<string> | 否 |  | ["custom-documents/my-pdf.pdf-hash.json"] |
| deletes | array<string> | 否 |  | ["custom-documents/anythingllm.txt-hash.json"] |

请求体示例：

```json
{
  "adds": [
    "custom-documents/my-pdf.pdf-hash.json"
  ],
  "deletes": [
    "custom-documents/anythingllm.txt-hash.json"
  ]
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspace | object | 否 |  | {"id":79,"name":"My workspace","slug":"my-workspace-123","createdAt":"2023-08-17 00:45:03","openAiTemp":null,"lastUpdatedAt":"2023-08-17 00:45:03","openAiHistory":20,"openAiPrompt":null,"documents":[]} |
| workspace.id | number | 否 |  | 79 |
| workspace.name | string | 否 |  | My workspace |
| workspace.slug | string | 否 |  | my-workspace-123 |
| workspace.createdAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiTemp | null | 否 |  | null |
| workspace.lastUpdatedAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiHistory | number | 否 |  | 20 |
| workspace.openAiPrompt | null | 否 |  | null |
| workspace.documents | array<any> | 否 |  | [] |
| message | null | 否 |  | null |

**成功响应示例（200）**

```json
{
  "workspace": {
    "id": 79,
    "name": "My workspace",
    "slug": "my-workspace-123",
    "createdAt": "2023-08-17 00:45:03",
    "openAiTemp": null,
    "lastUpdatedAt": "2023-08-17 00:45:03",
    "openAiHistory": 20,
    "openAiPrompt": null,
    "documents": []
  },
  "message": null
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update-embeddings" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "adds": [
    "custom-documents/my-pdf.pdf-hash.json"
  ],
  "deletes": [
    "custom-documents/anythingllm.txt-hash.json"
  ]
}'
```

#### POST /v1/workspace/{slug}/update-pin

- **用途**：Add or remove pin from a document in a workspace by its unique slug.
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update-pin`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to find | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object with the document path and pin status to update.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| docPath | string | 否 |  | custom-documents/my-pdf.pdf-hash.json |
| pinStatus | boolean | 否 |  | true |

请求体示例：

```json
{
  "docPath": "custom-documents/my-pdf.pdf-hash.json",
  "pinStatus": true
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | 未声明 |
| 404 | Document not found | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| message | string | 否 |  | Pin status updated successfully |

**成功响应示例（200）**

```json
{
  "message": "Pin status updated successfully"
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/update-pin" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "docPath": "custom-documents/my-pdf.pdf-hash.json",
  "pinStatus": true
}'
```

#### POST /v1/workspace/{slug}/vector-search

- **用途**：Perform a vector similarity search in a workspace
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/sample-workspace/vector-search`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

| 名称 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| slug | string | 是 | Unique slug of workspace to search in | sample-workspace |

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：Query to perform vector search with and optional parameters
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| query | string | 否 |  | What is the meaning of life? |
| topN | number | 否 |  | 4 |
| scoreThreshold | number | 否 |  | 0.75 |

请求体示例：

```json
{
  "query": "What is the meaning of life?",
  "topN": 4,
  "scoreThreshold": 0.75
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | 未声明 |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| results | array<object> | 否 |  | [{"id":"5a6bee0a-306c-47fc-942b-8ab9bf3899c4","text":"Document chunk content...","metadata":{"url":"file://document.txt","title":"document.txt","author":"no author specified","description":"no description found","docSource":"post:123456","chunkSource":"document.txt","published":"12/1/2024, 11:39:39 AM","wordCount":8,"tokenCount":9},"distance":0.541887640953064,"score":0.45811235904693604}] |
| results[].id | string | 否 |  | 5a6bee0a-306c-47fc-942b-8ab9bf3899c4 |
| results[].text | string | 否 |  | Document chunk content... |
| results[].metadata | object | 否 |  | {"url":"file://document.txt","title":"document.txt","author":"no author specified","description":"no description found","docSource":"post:123456","chunkSource":"document.txt","published":"12/1/2024, 11:39:39 AM","wordCount":8,"tokenCount":9} |
| results[].distance | number | 否 |  | 0.541887640953064 |
| results[].score | number | 否 |  | 0.45811235904693604 |

**成功响应示例（200）**

```json
{
  "results": [
    {
      "id": "5a6bee0a-306c-47fc-942b-8ab9bf3899c4",
      "text": "Document chunk content...",
      "metadata": {
        "url": "file://document.txt",
        "title": "document.txt",
        "author": "no author specified",
        "description": "no description found",
        "docSource": "post:123456",
        "chunkSource": "document.txt",
        "published": "12/1/2024, 11:39:39 AM",
        "wordCount": 8,
        "tokenCount": 9
      },
      "distance": 0.541887640953064,
      "score": 0.45811235904693604
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/sample-workspace/vector-search" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "query": "What is the meaning of life?",
  "topN": 4,
  "scoreThreshold": 0.75
}'
```

#### POST /v1/workspace/new

- **用途**：Create a new workspace
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspace/new`
- **动作类型**：创建/执行
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

- **是否必填**：是
- **说明**：JSON object containing workspace configuration.
- **Content-Type**：application/json

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| name | string | 否 |  | My New Workspace |
| similarityThreshold | number | 否 |  | 0.7 |
| openAiTemp | number | 否 |  | 0.7 |
| openAiHistory | number | 否 |  | 20 |
| openAiPrompt | string | 否 |  | Custom prompt for responses |
| queryRefusalResponse | string | 否 |  | Custom refusal message |
| chatMode | string | 否 |  | chat |
| topN | number | 否 |  | 4 |

请求体示例：

```json
{
  "name": "My New Workspace",
  "similarityThreshold": 0.7,
  "openAiTemp": 0.7,
  "openAiHistory": 20,
  "openAiPrompt": "Custom prompt for responses",
  "queryRefusalResponse": "Custom refusal message",
  "chatMode": "chat",
  "topN": 4
}
```

**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 400 | Bad Request | 未声明 |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspace | object | 否 |  | {"id":79,"name":"Sample workspace","slug":"sample-workspace","createdAt":"2023-08-17 00:45:03","openAiTemp":null,"lastUpdatedAt":"2023-08-17 00:45:03","openAiHistory":20,"openAiPrompt":null} |
| workspace.id | number | 否 |  | 79 |
| workspace.name | string | 否 |  | Sample workspace |
| workspace.slug | string | 否 |  | sample-workspace |
| workspace.createdAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiTemp | null | 否 |  | null |
| workspace.lastUpdatedAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspace.openAiHistory | number | 否 |  | 20 |
| workspace.openAiPrompt | null | 否 |  | null |
| message | string | 否 |  | Workspace created |

**成功响应示例（200）**

```json
{
  "workspace": {
    "id": 79,
    "name": "Sample workspace",
    "slug": "sample-workspace",
    "createdAt": "2023-08-17 00:45:03",
    "openAiTemp": null,
    "lastUpdatedAt": "2023-08-17 00:45:03",
    "openAiHistory": 20,
    "openAiPrompt": null
  },
  "message": "Workspace created"
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X POST "http://127.0.0.1:3001/api/v1/workspace/new" \
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
  "name": "My New Workspace",
  "similarityThreshold": 0.7,
  "openAiTemp": 0.7,
  "openAiHistory": 20,
  "openAiPrompt": "Custom prompt for responses",
  "queryRefusalResponse": "Custom refusal message",
  "chatMode": "chat",
  "topN": 4
}'
```

#### GET /v1/workspaces

- **用途**：List all current workspaces
- **完整地址**：`http://127.0.0.1:3001/api/v1/workspaces`
- **动作类型**：读取
- **认证**：需要 BearerAuth

**路径参数**

无

**Query 参数**

无

**请求体**

无
**响应说明**

| 状态码 | 说明 | Content-Type |
| --- | --- | --- |
| 200 | OK | application/json |
| 403 | Forbidden | application/json, application/xml |
| 500 | Internal Server Error | 未声明 |

**成功响应字段（200）**

| 字段 | 类型 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| workspaces | array<object> | 否 |  | [{"id":79,"name":"Sample workspace","slug":"sample-workspace","createdAt":"2023-08-17 00:45:03","openAiTemp":null,"lastUpdatedAt":"2023-08-17 00:45:03","openAiHistory":20,"openAiPrompt":null,"threads":[]}] |
| workspaces[].id | number | 否 |  | 79 |
| workspaces[].name | string | 否 |  | Sample workspace |
| workspaces[].slug | string | 否 |  | sample-workspace |
| workspaces[].createdAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspaces[].openAiTemp | null | 否 |  | null |
| workspaces[].lastUpdatedAt | string | 否 |  | 2023-08-17 00:45:03 |
| workspaces[].openAiHistory | number | 否 |  | 20 |
| workspaces[].openAiPrompt | null | 否 |  | null |
| workspaces[].threads | array<any> | 否 |  | [] |

**成功响应示例（200）**

```json
{
  "workspaces": [
    {
      "id": 79,
      "name": "Sample workspace",
      "slug": "sample-workspace",
      "createdAt": "2023-08-17 00:45:03",
      "openAiTemp": null,
      "lastUpdatedAt": "2023-08-17 00:45:03",
      "openAiHistory": 20,
      "openAiPrompt": null,
      "threads": []
    }
  ]
}
```
**403 错误示例**

```json
{
  "message": "Invalid API Key"
}
```
**cURL 调用示例**

```bash
curl -X GET "http://127.0.0.1:3001/api/v1/workspaces" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 7. 调用建议

1. 先用 `GET /v1/auth` 验证 API Key 是否有效。
2. 调用工作区聊天前，建议先通过 `GET /v1/workspaces` 或 `GET /v1/openai/models` 获取可用 workspace slug。
3. 上传文档后，如果要让文档立即参与问答，请结合 `addToWorkspaces` 或调用工作区嵌入更新接口。
4. 使用 `/stream-chat` 或 OpenAI 兼容聊天接口的流式模式时，客户端需支持 SSE / chunked stream。
5. 多用户与管理类接口在实例未开启 Multi-User Mode 时会返回 401 或直接拒绝。

## 8. 核对结果

- OpenAPI 路径数：57
- OpenAPI 操作数：60
- 分类数：9
- 安全方案：BearerAuth
