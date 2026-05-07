#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
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


def write_output_file(path: str, payload: Any) -> None:
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, str):
        out_path.write_text(payload, encoding="utf-8")
        return
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def truncate_text(text: str, limit: int) -> str:
    if limit <= 0:
        return ""
    normalized = re.sub(r"\s+", " ", text).strip()
    if len(normalized) <= limit:
        return normalized
    return normalized[: max(limit - 1, 0)].rstrip() + "…"


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def emit_summary_or_full(
    *,
    full: bool,
    method: str,
    path: str,
    summarizer,
    json_body: Any = None,
) -> None:
    if full:
        if json_body is None:
            http_request(method, path)
        else:
            http_request(method, path, json_body=json_body)
        return
    payload = http_request_capture(method, path, json_body=json_body, quiet=True)
    print_json(summarizer(payload))


def maybe_json_print(
    text: str,
    text_only: bool = False,
    *,
    no_sources: bool = False,
    no_metrics: bool = False,
    sources_limit: int | None = None,
    json_output: str | None = None,
) -> None:
    try:
        obj = json.loads(text)
    except Exception:
        if json_output:
            write_output_file(json_output, text)
        print(text)
        return
    if json_output:
        write_output_file(json_output, obj)
    if text_only and isinstance(obj, dict):
        response_text = obj.get("textResponse")
        if isinstance(response_text, str):
            print(response_text)
            return
    display_obj = obj
    if isinstance(obj, dict):
        display_obj = dict(obj)
        if no_sources:
            display_obj.pop("sources", None)
        elif sources_limit is not None and isinstance(display_obj.get("sources"), list):
            display_obj["sources"] = display_obj["sources"][:sources_limit]
        if no_metrics:
            display_obj.pop("metrics", None)
    print(json.dumps(display_obj, ensure_ascii=False, indent=2))


def summarize_workspace(
    payload: dict[str, Any],
    *,
    max_docs: int = 5,
    docs_only: bool = False,
    threads_only: bool = False,
) -> dict[str, Any]:
    workspace = payload.get("workspace")
    if isinstance(workspace, list):
        workspace = workspace[0] if workspace else {}
    if not isinstance(workspace, dict):
        return payload

    documents = workspace.get("documents") if isinstance(workspace.get("documents"), list) else []
    threads = workspace.get("threads") if isinstance(workspace.get("threads"), list) else []
    docs_preview = [
        {
            "filename": item.get("filename"),
            "docpath": item.get("docpath"),
        }
        for item in documents[: max(max_docs, 0)]
        if isinstance(item, dict)
    ]
    threads_preview = [
        {"slug": item.get("slug"), "user_id": item.get("user_id")}
        for item in threads[: max(max_docs, 0)]
        if isinstance(item, dict)
    ]

    if docs_only:
        return {
            "slug": workspace.get("slug"),
            "name": workspace.get("name"),
            "documentsCount": len(documents),
            "documentsPreview": docs_preview,
        }
    if threads_only:
        return {
            "slug": workspace.get("slug"),
            "name": workspace.get("name"),
            "threadsCount": len(threads),
            "threadsPreview": threads_preview,
        }
    return {
        "id": workspace.get("id"),
        "slug": workspace.get("slug"),
        "name": workspace.get("name"),
        "chatMode": workspace.get("chatMode"),
        "topN": workspace.get("topN"),
        "similarityThreshold": workspace.get("similarityThreshold"),
        "lastUpdatedAt": workspace.get("lastUpdatedAt"),
        "documentsCount": len(documents),
        "threadsCount": len(threads),
        "documentsPreview": docs_preview,
        "threadsPreview": threads_preview,
    }


def summarize_workspace_list(payload: dict[str, Any], *, max_items: int = 10) -> dict[str, Any]:
    workspaces = payload.get("workspaces") if isinstance(payload.get("workspaces"), list) else []
    preview: list[dict[str, Any]] = []

    for workspace in workspaces[: max(max_items, 0)]:
        if not isinstance(workspace, dict):
            continue
        threads = workspace.get("threads") if isinstance(workspace.get("threads"), list) else []
        preview.append(
            compact_dict(
                {
                    "id": workspace.get("id"),
                    "slug": workspace.get("slug"),
                    "name": workspace.get("name"),
                    "chatMode": workspace.get("chatMode"),
                    "chatProvider": workspace.get("chatProvider"),
                    "chatModel": workspace.get("chatModel"),
                    "topN": workspace.get("topN"),
                    "lastUpdatedAt": workspace.get("lastUpdatedAt"),
                    "threadsCount": len(threads),
                    "threadsPreview": [
                        compact_dict(
                            {
                                "slug": thread.get("slug"),
                                "name": thread.get("name"),
                                "user_id": thread.get("user_id"),
                            }
                        )
                        for thread in threads[:2]
                        if isinstance(thread, dict)
                    ],
                }
            )
        )

    return {
        "workspacesCount": len(workspaces),
        "workspaces": preview,
    }


def result_score(result: dict[str, Any]) -> float | None:
    score = result.get("score")
    if isinstance(score, (int, float)):
        return float(score)
    distance = result.get("distance")
    if isinstance(distance, (int, float)):
        return 1 - float(distance)
    return None


def summarize_search_results(
    payload: dict[str, Any],
    *,
    snippet_chars: int = 180,
    hide_404: bool = False,
    dedupe: bool = False,
    min_score: float | None = None,
    titles_only: bool = False,
) -> dict[str, Any]:
    raw_results = payload.get("results") if isinstance(payload.get("results"), list) else []
    seen: set[tuple[str | None, str | None, str]] = set()
    results: list[dict[str, Any]] = []

    for item in raw_results:
        if not isinstance(item, dict):
            continue
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        title = metadata.get("title") or item.get("title")
        source = metadata.get("chunkSource") or metadata.get("url") or item.get("url")
        snippet = truncate_text(str(item.get("text") or ""), snippet_chars)
        if hide_404 and "404 Not Found" in snippet:
            continue
        score = result_score(item)
        if min_score is not None and score is not None and score < min_score:
            continue
        if dedupe:
            signature = (source, title, snippet)
            if signature in seen:
                continue
            seen.add(signature)
        summary: dict[str, Any] = {
            "rank": len(results) + 1,
            "score": round(score, 4) if score is not None else None,
            "title": title,
            "source": source,
        }
        if not titles_only:
            summary["snippet"] = snippet
        results.append(summary)

    return {
        "resultsCount": len(results),
        "results": results,
    }


def summarize_document_tree(payload: dict[str, Any], *, max_items: int = 20) -> dict[str, Any]:
    root = payload.get("localFiles")
    if not isinstance(root, dict):
        return payload

    preview: list[dict[str, Any]] = []
    folders_count = 0
    files_count = 0

    def walk(node: dict[str, Any], parent_path: str = "") -> None:
        nonlocal folders_count, files_count
        node_type = node.get("type")
        name = str(node.get("name") or "")
        path = f"{parent_path}/{name}" if parent_path and name else name or parent_path
        children = node.get("items") if isinstance(node.get("items"), list) else []

        if node_type == "folder":
            folders_count += 1
            if path != root.get("name") and len(preview) < max(max_items, 0):
                preview.append(
                    {
                        "type": "folder",
                        "path": path,
                        "childrenCount": len(children),
                    }
                )
            for child in children:
                if isinstance(child, dict):
                    walk(child, path)
            return

        files_count += 1
        if len(preview) < max(max_items, 0):
            preview.append(
                compact_dict(
                    {
                        "type": "file",
                        "path": path,
                        "title": node.get("title"),
                        "tokenEstimate": node.get("token_count_estimate"),
                        "cached": node.get("cached"),
                    }
                )
            )

    walk(root)
    total_entries = max(folders_count - 1, 0) + files_count
    return {
        "root": root.get("name"),
        "foldersCount": max(folders_count - 1, 0),
        "filesCount": files_count,
        "itemsPreview": preview,
        "truncated": total_entries > len(preview),
    }


def summarize_system_settings(payload: dict[str, Any]) -> dict[str, Any]:
    settings = payload.get("settings")
    if not isinstance(settings, dict):
        return payload

    secret_markers = (
        "apikey",
        "token",
        "secret",
        "password",
        "connectionstring",
        "authtoken",
        "accesskey",
    )

    configured_secret_count = 0
    for key, value in settings.items():
        lowered = key.lower()
        if any(marker in lowered for marker in secret_markers) and bool(value):
            configured_secret_count += 1

    storage_dir = settings.get("StorageDir")
    storage_dir_name = None
    if isinstance(storage_dir, str) and storage_dir:
        storage_dir_name = Path(storage_dir).name

    return {
        "settingsCount": len(settings),
        "configuredSecretsCount": configured_secret_count,
        "auth": compact_dict(
            {
                "requiresAuth": settings.get("RequiresAuth"),
                "multiUserMode": settings.get("MultiUserMode"),
                "simpleSSOEnabled": settings.get("SimpleSSOEnabled"),
                "disableViewChatHistory": settings.get("DisableViewChatHistory"),
            }
        ),
        "storage": compact_dict(
            {
                "storageDirName": storage_dir_name,
                "hasExistingEmbeddings": settings.get("HasExistingEmbeddings"),
                "hasCachedEmbeddings": settings.get("HasCachedEmbeddings"),
                "vectorDB": settings.get("VectorDB"),
            }
        ),
        "embedding": compact_dict(
            {
                "engine": settings.get("EmbeddingEngine"),
                "model": settings.get("EmbeddingModelPref"),
                "outputDimensions": settings.get("EmbeddingOutputDimensions"),
                "batchSize": settings.get("OllamaEmbeddingBatchSize"),
            }
        ),
        "llm": compact_dict(
            {
                "provider": settings.get("LLMProvider"),
                "model": settings.get("LLMModel"),
                "defaultTokenLimit": settings.get("GenericOpenAiTokenLimit")
                or settings.get("AwsBedrockLLMTokenLimit")
                or settings.get("AzureOpenAiTokenLimit"),
                "maxTokens": settings.get("GenericOpenAiMaxTokens") or settings.get("AwsBedrockLLMMaxOutputTokens"),
            }
        ),
        "speech": compact_dict(
            {
                "provider": settings.get("SpeechToTextProvider"),
                "localWhisperModel": settings.get("SpeechToTextLocalWhisperModel"),
                "ttsProvider": settings.get("TextToSpeechProvider"),
                "whisperProvider": settings.get("WhisperProvider"),
            }
        ),
        "agent": compact_dict(
            {
                "maxToolCalls": settings.get("AgentSkillMaxToolCalls"),
                "rerankerEnabled": settings.get("AgentSkillRerankerEnabled"),
                "rerankerTopN": settings.get("AgentSkillRerankerTopN"),
                "networkDiscovery": settings.get("NetworkDiscovery"),
                "telemetryDisabled": settings.get("DisableTelemetry"),
            }
        ),
    }


def extract_response_preview(value: Any, *, snippet_chars: int) -> tuple[str, int | None, str | None]:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    sources_count = None
    model = None
    try:
        parsed = json.loads(text) if isinstance(text, str) else value
    except Exception:
        return truncate_text(str(text), snippet_chars), sources_count, model

    if isinstance(parsed, dict):
        sources = parsed.get("sources") if isinstance(parsed.get("sources"), list) else None
        if sources is not None:
            sources_count = len(sources)
        metrics = parsed.get("metrics") if isinstance(parsed.get("metrics"), dict) else {}
        if metrics:
            metric_model = metrics.get("model")
            model = metric_model if isinstance(metric_model, str) else None
        preview_text = parsed.get("text") or parsed.get("textResponse") or parsed.get("content") or text
        return truncate_text(str(preview_text), snippet_chars), sources_count, model

    return truncate_text(str(parsed), snippet_chars), sources_count, model


def summarize_chat_history(
    payload: dict[str, Any],
    *,
    max_items: int = 8,
    snippet_chars: int = 220,
) -> dict[str, Any]:
    if isinstance(payload.get("history"), list):
        history = payload.get("history")
        entries: list[dict[str, Any]] = []
        for index, item in enumerate(history[: max(max_items, 0)], start=1):
            if not isinstance(item, dict):
                continue
            metrics = item.get("metrics") if isinstance(item.get("metrics"), dict) else {}
            entries.append(
                compact_dict(
                    {
                        "index": index,
                        "role": item.get("role"),
                        "type": item.get("type") or "message",
                        "chatId": item.get("chatId"),
                        "sentAt": item.get("sentAt"),
                        "preview": truncate_text(str(item.get("content") or ""), snippet_chars),
                        "sourcesCount": len(item.get("sources")) if isinstance(item.get("sources"), list) else None,
                        "totalTokens": metrics.get("total_tokens"),
                        "model": metrics.get("model"),
                    }
                )
            )
        return {
            "entriesCount": len(history),
            "entries": entries,
        }

    chats = payload.get("chats") if isinstance(payload.get("chats"), list) else []
    entries = []
    for item in chats[: max(max_items, 0)]:
        if not isinstance(item, dict):
            continue
        response_preview, sources_count, model = extract_response_preview(item.get("response"), snippet_chars=snippet_chars)
        metrics = None
        if isinstance(item.get("response"), str):
            try:
                parsed_response = json.loads(item["response"])
            except Exception:
                parsed_response = None
            if isinstance(parsed_response, dict) and isinstance(parsed_response.get("metrics"), dict):
                metrics = parsed_response["metrics"]
        entries.append(
            compact_dict(
                {
                    "id": item.get("id"),
                    "workspace": item.get("workspace", {}).get("slug") if isinstance(item.get("workspace"), dict) else None,
                    "threadId": item.get("thread_id"),
                    "createdAt": item.get("createdAt"),
                    "promptPreview": truncate_text(str(item.get("prompt") or ""), snippet_chars),
                    "responsePreview": response_preview,
                    "sourcesCount": sources_count,
                    "totalTokens": metrics.get("total_tokens") if isinstance(metrics, dict) else None,
                    "model": model or (metrics.get("model") if isinstance(metrics, dict) else None),
                }
            )
        )

    return {
        "entriesCount": len(chats),
        "entries": entries,
    }


def filter_chat_payload(
    payload: dict[str, Any],
    *,
    no_sources: bool = False,
    no_metrics: bool = False,
    sources_limit: int | None = None,
) -> dict[str, Any]:
    display = dict(payload)
    if no_sources:
        display.pop("sources", None)
    elif sources_limit is not None and isinstance(display.get("sources"), list):
        display["sources"] = display["sources"][:sources_limit]
    if no_metrics:
        display.pop("metrics", None)
    return display


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
    text_only: bool = False,
    no_sources: bool = False,
    no_metrics: bool = False,
    sources_limit: int | None = None,
    json_output: str | None = None,
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
                    if json_output:
                        write_output_file(json_output, event)
                    event = filter_chat_payload(
                        event,
                        no_sources=no_sources,
                        no_metrics=no_metrics,
                        sources_limit=sources_limit,
                    )
                    text = event.get("textResponse", "")
                    if text:
                        print(text, end="", flush=True)
                    if event.get("close"):
                        break
                print()
                return
            body = resp.read().decode("utf-8", "replace")
            maybe_json_print(
                body,
                text_only=text_only,
                no_sources=no_sources,
                no_metrics=no_metrics,
                sources_limit=sources_limit,
                json_output=json_output,
            )
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        die(f"HTTP {exc.code}: {body}")
    except error.URLError as exc:
        die(f"request failed: {exc}")


def workspace_list(args: argparse.Namespace) -> None:
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path="/workspaces",
        summarizer=lambda payload: summarize_workspace_list(payload, max_items=args.max_items),
    )


def workspace_create(args: argparse.Namespace) -> None:
    http_request("POST", "/workspace/new", json_body={"name": args.name})


def workspace_get(args: argparse.Namespace) -> None:
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=f"/workspace/{args.slug}",
        summarizer=lambda payload: summarize_workspace(
            payload,
            max_docs=args.max_docs,
            docs_only=args.docs_only,
            threads_only=args.threads_only,
        ),
    )


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
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=path,
        summarizer=lambda payload: summarize_chat_history(payload, max_items=args.max_items, snippet_chars=args.snippet_chars),
    )


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
    http_request(
        "POST",
        endpoint,
        json_body=body,
        stream=stream,
        text_only=args.text_only,
        no_sources=args.no_sources,
        no_metrics=args.no_metrics,
        sources_limit=args.sources_limit,
        json_output=args.json_output,
    )


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
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=path,
        summarizer=lambda payload: summarize_document_tree(payload, max_items=args.max_items),
    )


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
    http_request("POST", "/document/move-files", json_body={"files": payload})


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
        http_request(
            "POST",
            f"/workspace/{args.workspace}/thread/{args.thread}/stream-chat",
            json_body=body,
            stream=True,
            text_only=args.text_only,
            no_sources=args.no_sources,
            no_metrics=args.no_metrics,
            sources_limit=args.sources_limit,
            json_output=args.json_output,
        )
    else:
        http_request(
            "POST",
            f"/workspace/{args.workspace}/thread/{args.thread}/chat",
            json_body=body,
            text_only=args.text_only,
            no_sources=args.no_sources,
            no_metrics=args.no_metrics,
            sources_limit=args.sources_limit,
            json_output=args.json_output,
        )


def thread_update(args: argparse.Namespace) -> None:
    http_request(
        "POST",
        f"/workspace/{args.workspace}/thread/{args.thread}/update",
        json_body={"name": args.name},
    )


def thread_get_chats(args: argparse.Namespace) -> None:
    path = f"/workspace/{args.workspace}/thread/{args.thread}/chats"
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=path,
        summarizer=lambda payload: summarize_chat_history(payload, max_items=args.max_items, snippet_chars=args.snippet_chars),
    )


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
        http_request(
            "POST",
            f"/workspace/{args.workspace}/thread/{thread}/stream-chat",
            json_body=body,
            stream=True,
            text_only=args.text_only,
            no_sources=args.no_sources,
            no_metrics=args.no_metrics,
            sources_limit=args.sources_limit,
            json_output=args.json_output,
        )
    else:
        http_request(
            "POST",
            f"/workspace/{args.workspace}/thread/{thread}/chat",
            json_body=body,
            text_only=args.text_only,
            no_sources=args.no_sources,
            no_metrics=args.no_metrics,
            sources_limit=args.sources_limit,
            json_output=args.json_output,
        )


def vector_search(args: argparse.Namespace) -> None:
    body: dict[str, Any] = {"query": read_text_source(args.query)}
    if args.top_n is not None:
        body["topN"] = args.top_n
    emit_summary_or_full(
        full=args.full,
        method="POST",
        path=f"/workspace/{args.workspace}/vector-search",
        json_body=body,
        summarizer=lambda payload: summarize_search_results(
            payload,
            snippet_chars=args.snippet_chars,
            hide_404=args.hide_404,
            dedupe=args.dedupe,
            min_score=args.min_score,
            titles_only=args.titles_only,
        ),
    )


def auth_verify(_: argparse.Namespace) -> None:
    http_request("GET", "/auth")


def user_list(_: argparse.Namespace) -> None:
    http_request("GET", "/users")


def system_get(_: argparse.Namespace) -> None:
    emit_summary_or_full(
        full=_.full,
        method="GET",
        path="/system",
        summarizer=summarize_system_settings,
    )


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
    emit_summary_or_full(
        full=args.full,
        method="POST",
        path="/admin/workspace-chats",
        json_body=payload,
        summarizer=lambda result: summarize_chat_history(result, max_items=args.max_items, snippet_chars=args.snippet_chars),
    )


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
    path = f"/embed/{args.embed_uuid}/chats"
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=path,
        summarizer=lambda payload: summarize_chat_history(payload, max_items=args.max_items, snippet_chars=args.snippet_chars),
    )


def embed_session_chats(args: argparse.Namespace) -> None:
    path = f"/embed/{args.embed_uuid}/chats/{args.session_uuid}"
    emit_summary_or_full(
        full=args.full,
        method="GET",
        path=path,
        summarizer=lambda payload: summarize_chat_history(payload, max_items=args.max_items, snippet_chars=args.snippet_chars),
    )


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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认摘要列表")
    sp.add_argument("--max-items", type=int, default=10, help="摘要模式下最多展示多少个工作区")
    sp.set_defaults(func=workspace_list)

    sp = ws.add_parser("create", help="创建工作区")
    sp.add_argument("name")
    sp.set_defaults(func=workspace_create)

    sp = ws.add_parser("get", help="查看单个工作区详情")
    sp.add_argument("slug")
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认摘要")
    sp.add_argument("--max-docs", type=int, default=5, help="摘要模式下最多展示多少条文档/线程预览")
    sp.add_argument("--docs-only", action="store_true", help="摘要模式下仅输出文档摘要")
    sp.add_argument("--threads-only", action="store_true", help="摘要模式下仅输出线程摘要")
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
    sp.add_argument("--text-only", action="store_true", help="只输出 textResponse 正文，适合重定向保存代码/文稿")
    sp.add_argument("--no-sources", action="store_true", help="隐藏返回中的 sources 字段，减少 stdout 体积")
    sp.add_argument("--sources-limit", type=int, help="仅保留前 N 条 sources")
    sp.add_argument("--no-metrics", action="store_true", help="隐藏返回中的 metrics 字段")
    sp.add_argument("--json-output", help="将完整 JSON 响应写入文件，stdout 只打印过滤后的结果")
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: workspace_chat(args, stream=False))

    sp = ws.add_parser("stream-chat", help="向工作区发送流式聊天请求")
    sp.add_argument("slug")
    sp.add_argument("--message", help="消息文本、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--session-id")
    sp.add_argument("--attachments", help="附件 JSON 数组、文件路径，或 - 从 stdin 读取")
    sp.add_argument("--text-only", action="store_true", help="只输出 textResponse 正文（流式模式下通常与默认输出一致）")
    sp.add_argument("--no-sources", action="store_true", help="隐藏返回中的 sources 字段，减少 stdout 体积")
    sp.add_argument("--sources-limit", type=int, help="仅保留前 N 条 sources")
    sp.add_argument("--no-metrics", action="store_true", help="隐藏返回中的 metrics 字段")
    sp.add_argument("--json-output", help="将完整 JSON 响应写入文件，stdout 只打印过滤后的结果")
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: workspace_chat(args, stream=True))

    sp = ws.add_parser("chats", help="读取工作区历史聊天")
    sp.add_argument("slug")
    sp.add_argument("--api-session-id")
    sp.add_argument("--limit", type=int)
    sp.add_argument("--order-by", choices=["asc", "desc"])
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    sp.add_argument("--max-items", type=int, default=8, help="摘要模式下最多展示多少条聊天记录")
    sp.add_argument("--snippet-chars", type=int, default=220, help="摘要模式下 prompt/response 预览的截断长度")
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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认目录摘要")
    sp.add_argument("--max-items", type=int, default=20, help="摘要模式下最多展示多少个目录/文件预览")
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
    sp.add_argument("--text-only", action="store_true", help="只输出 textResponse 正文，适合重定向保存代码/文稿")
    sp.add_argument("--no-sources", action="store_true", help="隐藏返回中的 sources 字段，减少 stdout 体积")
    sp.add_argument("--sources-limit", type=int, help="仅保留前 N 条 sources")
    sp.add_argument("--no-metrics", action="store_true", help="隐藏返回中的 metrics 字段")
    sp.add_argument("--json-output", help="将完整 JSON 响应写入文件，stdout 只打印过滤后的结果")
    sp.add_argument("--reset", action="store_true")
    sp.set_defaults(func=lambda args: thread_chat(args, stream=False))

    sp = th.add_parser("stream-chat", help="向线程发送流式聊天请求")
    sp.add_argument("workspace")
    sp.add_argument("thread")
    sp.add_argument("--message", help="message, file path, or - for stdin")
    sp.add_argument("--mode", default="chat", choices=["chat", "query", "automatic"])
    sp.add_argument("--user-id", type=int)
    sp.add_argument("--text-only", action="store_true", help="只输出 textResponse 正文（流式模式下通常与默认输出一致）")
    sp.add_argument("--no-sources", action="store_true", help="隐藏返回中的 sources 字段，减少 stdout 体积")
    sp.add_argument("--sources-limit", type=int, help="仅保留前 N 条 sources")
    sp.add_argument("--no-metrics", action="store_true", help="隐藏返回中的 metrics 字段")
    sp.add_argument("--json-output", help="将完整 JSON 响应写入文件，stdout 只打印过滤后的结果")
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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    sp.add_argument("--max-items", type=int, default=8, help="摘要模式下最多展示多少条聊天记录")
    sp.add_argument("--snippet-chars", type=int, default=220, help="摘要模式下 prompt/response 预览的截断长度")
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
    p.add_argument("--text-only", action="store_true", help="只输出 textResponse 正文，适合重定向保存代码/文稿")
    p.add_argument("--no-sources", action="store_true", help="隐藏返回中的 sources 字段，减少 stdout 体积")
    p.add_argument("--sources-limit", type=int, help="仅保留前 N 条 sources")
    p.add_argument("--no-metrics", action="store_true", help="隐藏返回中的 metrics 字段")
    p.add_argument("--json-output", help="将完整 JSON 响应写入文件，stdout 只打印过滤后的结果")
    p.add_argument("--reset", action="store_true")
    p.set_defaults(func=ask)

    p = sub.add_parser("search", help="在工作区中执行向量检索")
    p.add_argument("workspace")
    p.add_argument("--query", required=True, help="query text, file path, or - for stdin")
    p.add_argument("--top-n", type=int)
    p.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    p.add_argument("--compact", action="store_true", help="兼容性参数：当前紧凑摘要已是默认行为")
    p.add_argument("--snippet-chars", type=int, default=180, help="紧凑模式下 snippet 截断长度")
    p.add_argument("--hide-404", action="store_true", help="过滤正文中含 404 Not Found 的噪声结果")
    p.add_argument("--dedupe", action="store_true", help="按 source/title/snippet 去重结果")
    p.add_argument("--min-score", type=float, help="仅保留 score 不低于该阈值的结果")
    p.add_argument("--titles-only", action="store_true", help="仅输出 title/source/score，不输出 snippet")
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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认摘要")
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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    sp.add_argument("--max-items", type=int, default=8, help="摘要模式下最多展示多少条聊天记录")
    sp.add_argument("--snippet-chars", type=int, default=220, help="摘要模式下 prompt/response 预览的截断长度")
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
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    sp.add_argument("--max-items", type=int, default=8, help="摘要模式下最多展示多少条聊天记录")
    sp.add_argument("--snippet-chars", type=int, default=220, help="摘要模式下 prompt/response 预览的截断长度")
    sp.set_defaults(func=embed_chats)

    sp = embed.add_parser("session-chats", help="读取 embed 某个 session 的聊天")
    sp.add_argument("embed_uuid")
    sp.add_argument("session_uuid")
    sp.add_argument("--full", action="store_true", help="输出完整原始 JSON，而不是默认紧凑摘要")
    sp.add_argument("--max-items", type=int, default=8, help="摘要模式下最多展示多少条聊天记录")
    sp.add_argument("--snippet-chars", type=int, default=220, help="摘要模式下 prompt/response 预览的截断长度")
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
