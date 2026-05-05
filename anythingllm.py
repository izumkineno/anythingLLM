#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import uuid
from pathlib import Path
from typing import Any
from urllib import error, parse, request

DEFAULT_BASE_URL = os.getenv("ANYTHINGLLM_BASE_URL", "http://localhost:3001").rstrip("/")
DEFAULT_API_ROOT = os.getenv("ANYTHINGLLM_API_ROOT", f"{DEFAULT_BASE_URL}/api/v1").rstrip("/")
DEFAULT_API_KEY = os.getenv("ANYTHINGLLM_API_KEY", "")
USER_AGENT = "anythingllm-cli/1.0"


def die(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def read_text_source(value: str | None) -> str:
    if value is None or value == "-":
        if sys.stdin.isatty():
            return ""
        return sys.stdin.read()
    path = Path(value)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return value


def read_bytes_source(value: str) -> tuple[bytes, str]:
    if value == "-":
        if sys.stdin.isatty():
            die("stdin is empty")
        return sys.stdin.buffer.read(), "stdin.bin"
    path = Path(value)
    if not path.exists():
        die(f"file not found: {value}")
    return path.read_bytes(), path.name


def parse_json_source(value: str | None) -> Any:
    if value is None:
        return None
    text = read_text_source(value).strip()
    if not text:
        return None
    return json.loads(text)


def maybe_json_print(text: str) -> None:
    try:
        obj = json.loads(text)
    except Exception:
        print(text)
        return
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def join_path(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{DEFAULT_API_ROOT}{path}"


def append_query(path: str, **params: Any) -> str:
    clean: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        clean[key] = value
    if not clean:
        return path
    return f"{path}?{parse.urlencode(clean, doseq=True)}"


def require_json(value: str | None, *, arg_name: str = "--json", expected_type: type | tuple[type, ...] | None = None) -> Any:
    payload = parse_json_source(value)
    if payload is None:
        die(f"{arg_name} is required")
    if expected_type is not None and not isinstance(payload, expected_type):
        type_name = (
            ", ".join(t.__name__ for t in expected_type)
            if isinstance(expected_type, tuple)
            else expected_type.__name__
        )
        die(f"{arg_name} must be JSON {type_name}")
    return payload


def optional_json(value: str | None, *, arg_name: str = "--json", expected_type: type | tuple[type, ...] | None = None) -> Any:
    if value is None:
        return None
    payload = parse_json_source(value)
    if expected_type is not None and payload is not None and not isinstance(payload, expected_type):
        type_name = (
            ", ".join(t.__name__ for t in expected_type)
            if isinstance(expected_type, tuple)
            else expected_type.__name__
        )
        die(f"{arg_name} must be JSON {type_name}")
    return payload


def auth_header() -> dict[str, str]:
    if not DEFAULT_API_KEY:
        die("ANYTHINGLLM_API_KEY is not set")
    return {
        "Authorization": f"Bearer {DEFAULT_API_KEY}",
        "User-Agent": USER_AGENT,
    }


def encode_multipart(fields: dict[str, Any] | None, file_field: tuple[str, str] | None = None) -> tuple[bytes, str]:
    boundary = f"----anythingllm-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    def add(name: str, value: str) -> None:
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        chunks.append(value.encode())
        chunks.append(b"\r\n")

    for key, value in (fields or {}).items():
        if value is None:
            continue
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        add(key, str(value))

    if file_field:
        field_name, file_path = file_field
        file_bytes, filename = read_bytes_source(file_path)
        mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(
            f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode()
        )
        chunks.append(f"Content-Type: {mime}\r\n\r\n".encode())
        chunks.append(file_bytes)
        chunks.append(b"\r\n")

    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def http_request(
    method: str,
    path: str,
    *,
    json_body: Any = None,
    form_fields: dict[str, Any] | None = None,
    file_field: tuple[str, str] | None = None,
    extra_headers: dict[str, str] | None = None,
    stream: bool = False,
) -> None:
    url = join_path(path)
    headers = auth_header()
    if extra_headers:
        headers.update(extra_headers)

    data: bytes | None = None
    if json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif form_fields is not None or file_field is not None:
        data, content_type = encode_multipart(form_fields, file_field)
        headers["Content-Type"] = content_type

    req = request.Request(url=url, data=data, headers=headers, method=method.upper())
    try:
        with request.urlopen(req) as resp:
            if stream:
                for raw_line in resp:
                    line = raw_line.decode("utf-8", "replace").rstrip("\n")
                    if not line.startswith("data:"):
                        continue
                    payload = line[5:].strip()
                    if not payload:
                        continue
                    try:
                        event = json.loads(payload)
                    except Exception:
                        print(payload)
                        continue
                    text = event.get("textResponse", "")
                    if text:
                        print(text, end="", flush=True)
                    if event.get("close"):
                        break
                print()
                return
            body = resp.read().decode("utf-8", "replace")
            maybe_json_print(body)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        die(f"HTTP {exc.code}: {body}")
    except error.URLError as exc:
        die(f"request failed: {exc}")


def workspace_list(_: argparse.Namespace) -> None:
    http_request("GET", "/workspaces")


def workspace_create(args: argparse.Namespace) -> None:
    http_request("POST", "/workspace/new", json_body={"name": args.name})


def workspace_get(args: argparse.Namespace) -> None:
    http_request("GET", f"/workspace/{args.slug}")


def workspace_update(args: argparse.Namespace) -> None:
    body: dict[str, Any] = {}
    for key in ["name", "chatProvider", "chatModel", "chatMode", "openAiTemp", "openAiHistory", "openAiPrompt", "similarityThreshold", "topN", "contextWindow"]:
        value = getattr(args, key)
        if value is not None:
            body[key] = value
    http_request("POST", f"/workspace/{args.slug}/update", json_body=body)


def workspace_delete(args: argparse.Namespace) -> None:
    http_request("DELETE", f"/workspace/{args.slug}")


def workspace_chats(args: argparse.Namespace) -> None:
    path = append_query(
        f"/workspace/{args.slug}/chats",
        apiSessionId=args.api_session_id,
        limit=args.limit,
        orderBy=args.order_by,
    )
    http_request("GET", path)


def workspace_chat(args: argparse.Namespace, stream: bool = False) -> None:
    message = read_text_source(args.message)
    body: dict[str, Any] = {"message": message, "mode": args.mode}
    if args.session_id is not None:
        body["sessionId"] = args.session_id
    if args.reset:
        body["reset"] = True
    attachments = optional_json(args.attachments, arg_name="--attachments", expected_type=list)
    if attachments:
        body["attachments"] = attachments
    endpoint = f"/workspace/{args.slug}/stream-chat" if stream else f"/workspace/{args.slug}/chat"
    http_request("POST", endpoint, json_body=body, stream=stream)


def workspace_update_embeddings(args: argparse.Namespace) -> None:
    body = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", f"/workspace/{args.slug}/update-embeddings", json_body=body)


def workspace_update_pin(args: argparse.Namespace) -> None:
    body = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", f"/workspace/{args.slug}/update-pin", json_body=body)


def document_upload(args: argparse.Namespace) -> None:
    metadata = parse_json_source(args.metadata) if args.metadata else None
    fields: dict[str, Any] = {}
    if args.add_to_workspaces:
        fields["addToWorkspaces"] = args.add_to_workspaces
    if metadata is not None:
        fields["metadata"] = metadata
    endpoint = "/document/upload"
    if args.folder:
        endpoint = f"/document/upload/{args.folder}"
    http_request("POST", endpoint, form_fields=fields, file_field=("file", args.file))


def document_raw_text(args: argparse.Namespace) -> None:
    text = read_text_source(args.text)
    metadata = parse_json_source(args.metadata) if args.metadata else None
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        die("metadata must be a JSON object")
    metadata = dict(metadata)
    if args.text and args.text != "-":
        source_path = Path(args.text)
        if source_path.exists():
            default_title = source_path.stem
        else:
            default_title = "raw-text"
    else:
        default_title = "raw-text"
    metadata.setdefault("title", default_title)
    body: dict[str, Any] = {"textContent": text, "metadata": metadata}
    if args.add_to_workspaces:
        body["addToWorkspaces"] = args.add_to_workspaces
    http_request("POST", "/document/raw-text", json_body=body)


def document_upload_link(args: argparse.Namespace) -> None:
    body: dict[str, Any] = {"link": args.link}
    if args.add_to_workspaces:
        body["addToWorkspaces"] = args.add_to_workspaces
    if args.metadata:
        body["metadata"] = parse_json_source(args.metadata)
    headers: dict[str, str] = {}
    for header in args.scraper_header or []:
        if "=" not in header:
            die(f"invalid scraper header: {header}")
        key, value = header.split("=", 1)
        headers[key.strip()] = value.strip()
    if headers:
        body["scraperHeaders"] = headers
    http_request("POST", "/document/upload-link", json_body=body)


def document_list(args: argparse.Namespace) -> None:
    path = "/documents"
    if args.folder:
        path = f"/documents/folder/{args.folder}"
    http_request("GET", path)


def document_info(args: argparse.Namespace) -> None:
    http_request("GET", f"/document/{args.doc_name}")


def document_accepted_types(_: argparse.Namespace) -> None:
    http_request("GET", "/document/accepted-file-types")


def document_metadata_schema(_: argparse.Namespace) -> None:
    http_request("GET", "/document/metadata-schema")


def document_create_folder(args: argparse.Namespace) -> None:
    http_request("POST", "/document/create-folder", json_body={"name": args.name})


def document_remove_folder(args: argparse.Namespace) -> None:
    http_request("DELETE", "/document/remove-folder", json_body={"name": args.name})


def document_move_files(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=list)
    http_request("POST", "/document/move-files", json_body=payload)


def thread_new(args: argparse.Namespace) -> None:
    body: dict[str, Any] = {}
    if args.user_id is not None:
        body["userId"] = args.user_id
    if args.name is not None:
        body["name"] = args.name
    if args.slug is not None:
        body["slug"] = args.slug
    http_request("POST", f"/workspace/{args.workspace}/thread/new", json_body=body)


def thread_chat(args: argparse.Namespace, stream: bool = False) -> None:
    message = read_text_source(args.message)
    body: dict[str, Any] = {"message": message, "mode": args.mode}
    if args.user_id is not None:
        body["userId"] = args.user_id
    if args.reset:
        body["reset"] = True
    if stream:
        http_request("POST", f"/workspace/{args.workspace}/thread/{args.thread}/stream-chat", json_body=body, stream=True)
    else:
        http_request("POST", f"/workspace/{args.workspace}/thread/{args.thread}/chat", json_body=body)


def thread_update(args: argparse.Namespace) -> None:
    http_request(
        "POST",
        f"/workspace/{args.workspace}/thread/{args.thread}/update",
        json_body={"name": args.name},
    )


def thread_get_chats(args: argparse.Namespace) -> None:
    http_request("GET", f"/workspace/{args.workspace}/thread/{args.thread}/chats")


def thread_delete(args: argparse.Namespace) -> None:
    http_request("DELETE", f"/workspace/{args.workspace}/thread/{args.thread}")


def ask(args: argparse.Namespace) -> None:
    if args.thread:
        thread = args.thread
    else:
        result = http_request_capture(
            "POST",
            f"/workspace/{args.workspace}/thread/new",
            json_body={"name": args.thread_name or "Thread"},
            quiet=True,
        )
        thread = result.get("thread", {}).get("slug")
        if not thread:
            die("could not create thread")
    body: dict[str, Any] = {"message": read_text_source(args.message), "mode": args.mode}
    if args.reset:
        body["reset"] = True
    if args.stream:
        http_request("POST", f"/workspace/{args.workspace}/thread/{thread}/stream-chat", json_body=body, stream=True)
    else:
        http_request("POST", f"/workspace/{args.workspace}/thread/{thread}/chat", json_body=body)


def vector_search(args: argparse.Namespace) -> None:
    body: dict[str, Any] = {"query": read_text_source(args.query)}
    if args.top_n is not None:
        body["topN"] = args.top_n
    http_request("POST", f"/workspace/{args.workspace}/vector-search", json_body=body)


def auth_verify(_: argparse.Namespace) -> None:
    http_request("GET", "/auth")


def user_list(_: argparse.Namespace) -> None:
    http_request("GET", "/users")


def system_get(_: argparse.Namespace) -> None:
    http_request("GET", "/system")


def system_vector_count(_: argparse.Namespace) -> None:
    http_request("GET", "/system/vector-count")


def system_env_dump(_: argparse.Namespace) -> None:
    http_request("GET", "/system/env-dump")


def system_export_chats(args: argparse.Namespace) -> None:
    http_request("GET", append_query("/system/export-chats", type=args.type))


def system_update_env(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/system/update-env", json_body=payload)


def system_remove_documents(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("DELETE", "/system/remove-documents", json_body=payload)


def admin_list_users(_: argparse.Namespace) -> None:
    http_request("GET", "/admin/users")


def admin_is_multi_user_mode(_: argparse.Namespace) -> None:
    http_request("GET", "/admin/is-multi-user-mode")


def admin_list_invites(_: argparse.Namespace) -> None:
    http_request("GET", "/admin/invites")


def admin_update_preferences(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/admin/preferences", json_body=payload)


def admin_workspace_chats(args: argparse.Namespace) -> None:
    payload = optional_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/admin/workspace-chats", json_body=payload)


def admin_manage_users(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", f"/admin/workspaces/{args.workspace_slug}/manage-users", json_body=payload)


def embed_list(_: argparse.Namespace) -> None:
    http_request("GET", "/embed")


def embed_create(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/embed/new", json_body=payload)


def embed_update(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", f"/embed/{args.embed_uuid}", json_body=payload)


def embed_delete(args: argparse.Namespace) -> None:
    http_request("DELETE", f"/embed/{args.embed_uuid}")


def embed_chats(args: argparse.Namespace) -> None:
    http_request("GET", f"/embed/{args.embed_uuid}/chats")


def embed_session_chats(args: argparse.Namespace) -> None:
    http_request("GET", f"/embed/{args.embed_uuid}/chats/{args.session_uuid}")


def openai_models(_: argparse.Namespace) -> None:
    http_request("GET", "/openai/models")


def openai_vector_stores(_: argparse.Namespace) -> None:
    http_request("GET", "/openai/vector_stores")


def openai_embeddings(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/openai/embeddings", json_body=payload)


def openai_chat_completions(args: argparse.Namespace) -> None:
    payload = require_json(args.json, arg_name="--json", expected_type=dict)
    http_request("POST", "/openai/chat/completions", json_body=payload)


def api(args: argparse.Namespace) -> None:
    json_body = parse_json_source(args.json) if args.json else None
    form_fields: dict[str, Any] | None = {} if args.form else None
    file_field = None
    if args.form:
        for item in args.form:
            if "=" not in item:
                die(f"invalid form field: {item}")
            key, value = item.split("=", 1)
            if form_fields is not None:
                form_fields[key] = value
    if args.file:
        if form_fields is None:
            form_fields = {}
        file_field = (args.file_field, args.file)
    http_request(args.method, args.path, json_body=json_body, form_fields=form_fields, file_field=file_field)


def http_request_capture(
    method: str,
    path: str,
    *,
    json_body: Any = None,
    form_fields: dict[str, Any] | None = None,
    file_field: tuple[str, str] | None = None,
    extra_headers: dict[str, str] | None = None,
    quiet: bool = False,
) -> dict[str, Any]:
    url = join_path(path)
    headers = auth_header()
    if extra_headers:
        headers.update(extra_headers)
    data: bytes | None = None
    if json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif form_fields is not None or file_field is not None:
        data, content_type = encode_multipart(form_fields, file_field)
        headers["Content-Type"] = content_type
    req = request.Request(url=url, data=data, headers=headers, method=method.upper())
    try:
        with request.urlopen(req) as resp:
            text = resp.read().decode("utf-8", "replace")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        die(f"HTTP {exc.code}: {body}")
    except error.URLError as exc:
        die(f"request failed: {exc}")
    if not quiet:
        maybe_json_print(text)
    try:
        return json.loads(text)
    except Exception:
        return {"raw": text}




def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "AnythingLLM CLI。基于 Swagger 文档封装常用接口，"
            "并保留 api 子命令用于直接调用任意 REST 路径。"
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "api",
        help="直接调用任意 AnythingLLM REST 接口",
        description="低层通用入口：当高层子命令未覆盖某接口时，可直接传 method/path 调用。",
    )
    p.add_argument("method")
    p.add_argument("path")
    p.add_argument("--json", help="JSON string, file path, or - for stdin")
    p.add_argument("--file", help="file path for multipart upload")
    p.add_argument("--file-field", default="file", help="multipart file field name")
    p.add_argument("--form", action="append", help="multipart field key=value")
    p.set_defaults(func=api)

    p = sub.add_parser(
        "workspace",
        help="工作区相关命令",
        description="列出、创建、更新、删除工作区，并执行聊天、历史、向量搜索、文档绑定等操作。",
    )
    ws = p.add_subparsers(dest="ws_command", required=True)

    sp = ws.add_parser("list", help="列出全部工作区")
    sp.set_defaults(func=workspace_list)

    sp = ws.add_parser("create", help="创建工作区")
    sp.add_argument("name")
    sp.set_defaults(func=workspace_create)

    sp = ws.add_parser("get", help="查看单个工作区详情")
    sp.add_argument("slug")
    sp.set_defaults(func=workspace_get)

    sp = ws.add_parser("update", help="更新工作区配置")
    sp.add_argument("slug")
    sp.add_argument("--name")
    sp.add_argument("--chat-provider", dest="chatProvider")
    sp.add_argument("--chat-model", dest="chatModel")
    sp.add_argument("--chat-mode", dest="chatMode")
    sp.add_argument("--openai-temp", dest="openAiTemp", type=float)
    sp.add_argument("--openai-history", dest="openAiHistory", type=int)
    sp.add_argument("--openai-prompt", dest="openAiPrompt")
    sp.add_argument("--similarity-threshold", dest="similarityThreshold", type=float)
    sp.add_argument("--top-n", dest="topN", type=int)
    sp.add_argument("--context-window", dest="contextWindow", type=int)
    sp.set_defaults(func=workspace_update)

    sp = ws.add_parser("delete", help="删除工作区")
    sp.add_argument("slug")
    sp.set_defaults(func=workspace_delete)

    sp = ws.add_parser("chat", help="向工作区发送非流式聊天请求")
    sp.add_argument("slug")
    sp.add_argument("--message", help="消息文本、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--session-id")
    sp.add_argument("--attachments", help="附件 JSON 数组、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: workspace_chat(args, stream=False))

    sp = ws.add_parser("stream-chat", help="向工作区发送流式聊天请求")
    sp.add_argument("slug")
    sp.add_argument("--message", help="消息文本、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--session-id")
    sp.add_argument("--attachments", help="附件 JSON 数组、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: workspace_chat(args, stream=True))

    sp = ws.add_parser("chats", help="读取工作区历史聊天")
    sp.add_argument("slug")
    sp.add_argument("--api-session-id")
    sp.add_argument("--limit", type=int)
    sp.add_argument("--order-by", choices=["asc", "desc"])
    sp.set_defaults(func=workspace_chats)

    sp = ws.add_parser("update-embeddings", help="批量增删工作区文档绑定")
    sp.add_argument("slug")
    sp.add_argument("--json", required=True, help="JSON 对象，包含 adds/deletes")
    sp.set_defaults(func=workspace_update_embeddings)

    sp = ws.add_parser("update-pin", help="更新工作区内文档 pin 状态")
    sp.add_argument("slug")
    sp.add_argument("--json", required=True, help="JSON 对象，包含 docPath/pinStatus")
    sp.set_defaults(func=workspace_update_pin)

    p = sub.add_parser(
        "document",
        help="文档管理命令",
        description="上传、列出、查看、创建目录、移动文件及原始文本导入。",
    )
    doc = p.add_subparsers(dest="doc_command", required=True)

    sp = doc.add_parser("upload", help="上传文件，可选直接加入工作区")
    sp.add_argument("--file", required=True)
    sp.add_argument("--folder")
    sp.add_argument("--workspace", dest="add_to_workspaces")
    sp.add_argument("--metadata")
    sp.set_defaults(func=document_upload)

    sp = doc.add_parser("raw-text", help="按原始文本创建文档")
    sp.add_argument("--text", help="raw text, file path, or - for stdin")
    sp.add_argument("--workspace", dest="add_to_workspaces")
    sp.add_argument("--metadata")
    sp.set_defaults(func=document_raw_text)

    sp = doc.add_parser("upload-link", help="抓取 URL 并导入为文档")
    sp.add_argument("link")
    sp.add_argument("--workspace", dest="add_to_workspaces")
    sp.add_argument("--metadata")
    sp.add_argument("--scraper-header", action="append")
    sp.set_defaults(func=document_upload_link)

    sp = doc.add_parser("list", help="列出文档，可选按目录过滤")
    sp.add_argument("--folder")
    sp.set_defaults(func=document_list)

    sp = doc.add_parser("get", help="查看单个文档详情")
    sp.add_argument("doc_name")
    sp.set_defaults(func=document_info)

    sp = doc.add_parser("accepted-types", help="查看允许上传的文件类型")
    sp.set_defaults(func=document_accepted_types)

    sp = doc.add_parser("metadata-schema", help="查看 raw-text 可接受的 metadata 结构")
    sp.set_defaults(func=document_metadata_schema)

    sp = doc.add_parser("create-folder", help="创建文档目录")
    sp.add_argument("name")
    sp.set_defaults(func=document_create_folder)

    sp = doc.add_parser("remove-folder", help="删除文档目录及其内容")
    sp.add_argument("name")
    sp.set_defaults(func=document_remove_folder)

    sp = doc.add_parser("move-files", help="批量移动文档文件")
    sp.add_argument("--json", required=True, help="JSON 数组，元素包含 from/to")
    sp.set_defaults(func=document_move_files)

    p = sub.add_parser(
        "thread",
        help="线程相关命令",
        description="创建线程、对话、更新名称、获取历史或删除线程。",
    )
    th = p.add_subparsers(dest="thread_command", required=True)

    sp = th.add_parser("new", help="创建工作区线程")
    sp.add_argument("workspace")
    sp.add_argument("--name")
    sp.add_argument("--slug")
    sp.add_argument("--user-id", type=int)
    sp.set_defaults(func=thread_new)

    sp = th.add_parser("chat", help="向线程发送非流式聊天请求")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.add_argument("--message", help="message, file path, or - for stdin")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--user-id", type=int)
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: thread_chat(args, stream=False))

    sp = th.add_parser("stream-chat", help="向线程发送流式聊天请求")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.add_argument("--message", help="message, file path, or - for stdin")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--user-id", type=int)
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: thread_chat(args, stream=True))

    sp = th.add_parser("update", help="更新线程名称")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.add_argument("--name", required=True)
    sp.set_defaults(func=thread_update)

    sp = th.add_parser("get-chats", help="获取线程历史消息")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.set_defaults(func=thread_get_chats)

    sp = th.add_parser("delete", help="删除线程")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.set_defaults(func=thread_delete)

    p = sub.add_parser("ask", help="必要时自动建线程并提问")
    p.add_argument("workspace")
    p.add_argument("--thread")
    p.add_argument("--thread-name")
    p.add_argument("--message", help="message, file path, or - for stdin")
    p.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    p.add_argument("--stream", action="store_true")
    p.add_argument("--reset", action="store_true")
    p.set_defaults(func=ask)

    p = sub.add_parser("search", help="在工作区中执行向量检索")
    p.add_argument("workspace")
    p.add_argument("--query", required=True, help="query text, file path, or - for stdin")
    p.add_argument("--top-n", type=int)
    p.set_defaults(func=vector_search)

    p = sub.add_parser("auth", help="验证当前 API Key 是否有效")
    p.set_defaults(func=auth_verify)

    p = sub.add_parser("user", help="用户相关命令")
    user = p.add_subparsers(dest="user_command", required=True)

    sp = user.add_parser("list", help="列出用户")
    sp.set_defaults(func=user_list)

    p = sub.add_parser("system", help="系统设置与导出命令")
    system = p.add_subparsers(dest="system_command", required=True)

    sp = system.add_parser("get", help="读取当前系统设置")
    sp.set_defaults(func=system_get)

    sp = system.add_parser("vector-count", help="读取向量库中向量总数")
    sp.set_defaults(func=system_vector_count)

    sp = system.add_parser("env-dump", help="导出当前环境配置")
    sp.set_defaults(func=system_env_dump)

    sp = system.add_parser("export-chats", help="导出聊天记录")
    sp.add_argument("--type", choices=["jsonl", "json", "csv", "jsonAlpaca"])
    sp.set_defaults(func=system_export_chats)

    sp = system.add_parser("update-env", help="更新系统环境配置")
    sp.add_argument("--json", required=True, help="JSON 对象，键值对对应待更新配置")
    sp.set_defaults(func=system_update_env)

    sp = system.add_parser("remove-documents", help="永久删除文档")
    sp.add_argument("--json", required=True, help='JSON 对象，例如 {"names": ["doc.json"]}')
    sp.set_defaults(func=system_remove_documents)

    p = sub.add_parser("admin", help="管理员接口命令")
    admin = p.add_subparsers(dest="admin_command", required=True)

    sp = admin.add_parser("is-multi-user-mode", help="检查是否启用多用户模式")
    sp.set_defaults(func=admin_is_multi_user_mode)

    sp = admin.add_parser("users", help="列出管理员可见用户")
    sp.set_defaults(func=admin_list_users)

    sp = admin.add_parser("invites", help="列出邀请记录")
    sp.set_defaults(func=admin_list_invites)

    sp = admin.add_parser("preferences", help="更新多用户偏好设置")
    sp.add_argument("--json", required=True, help="JSON 对象，键为设置项")
    sp.set_defaults(func=admin_update_preferences)

    sp = admin.add_parser("workspace-chats", help="分页读取全系统工作区聊天")
    sp.add_argument("--json", help="可选 JSON 对象，例如 {""offset"": 2}")
    sp.set_defaults(func=admin_workspace_chats)

    sp = admin.add_parser("manage-users", help="按工作区 slug 设置用户访问权限")
    sp.add_argument("workspace_slug")
    sp.add_argument("--json", required=True, help='JSON 对象，例如 {"userIds": [1,2], "reset": false}')
    sp.set_defaults(func=admin_manage_users)

    p = sub.add_parser("embed", help="Embed 配置管理命令")
    embed = p.add_subparsers(dest="embed_command", required=True)

    sp = embed.add_parser("list", help="列出全部 embed 配置")
    sp.set_defaults(func=embed_list)

    sp = embed.add_parser("create", help="创建 embed 配置")
    sp.add_argument("--json", required=True, help="JSON 对象，包含 workspace_slug/chat_mode 等字段")
    sp.set_defaults(func=embed_create)

    sp = embed.add_parser("update", help="更新 embed 配置")
    sp.add_argument("embed_uuid")
    sp.add_argument("--json", required=True, help="JSON 对象，包含待更新字段")
    sp.set_defaults(func=embed_update)

    sp = embed.add_parser("delete", help="删除 embed 配置")
    sp.add_argument("embed_uuid")
    sp.set_defaults(func=embed_delete)

    sp = embed.add_parser("chats", help="读取 embed 的全部聊天")
    sp.add_argument("embed_uuid")
    sp.set_defaults(func=embed_chats)

    sp = embed.add_parser("session-chats", help="读取 embed 某个 session 的聊天")
    sp.add_argument("embed_uuid")
    sp.add_argument("session_uuid")
    sp.set_defaults(func=embed_session_chats)

    p = sub.add_parser("openai", help="OpenAI 兼容接口命令")
    openai = p.add_subparsers(dest="openai_command", required=True)

    sp = openai.add_parser("models", help="列出可用 workspace 模型")
    sp.set_defaults(func=openai_models)

    sp = openai.add_parser("vector-stores", help="列出向量库集合")
    sp.set_defaults(func=openai_vector_stores)

    sp = openai.add_parser("embeddings", help="调用 OpenAI 兼容 embeddings 接口")
    sp.add_argument("--json", required=True, help="JSON 对象，包含 input/model 等字段")
    sp.set_defaults(func=openai_embeddings)

    sp = openai.add_parser("chat-completions", help="调用 OpenAI 兼容 chat completions 接口")
    sp.add_argument("--json", required=True, help="JSON 对象，包含 messages/model/stream 等字段")
    sp.set_defaults(func=openai_chat_completions)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    func = getattr(args, "func", None)
    if not func:
        parser.error("missing command")
    func(args)


if __name__ == "__main__":
    main()
