import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


WORKSPACE_PAYLOAD = {
    "workspace": [
        {
            "id": 1,
            "slug": "demo-workspace",
            "name": "Demo Workspace",
            "chatMode": "chat",
            "topN": 8,
            "similarityThreshold": 0.25,
            "lastUpdatedAt": "2026-05-06T08:00:00.000Z",
            "documents": [
                {"filename": "alpha.md", "docpath": "docs/alpha.md"},
                {"filename": "beta.md", "docpath": "docs/beta.md"},
            ],
            "threads": [
                {"slug": "thread-a", "user_id": None},
                {"slug": "thread-b", "user_id": 2},
            ],
            "openAiPrompt": "very long prompt that should not appear in summary",
        }
    ]
}


SEARCH_PAYLOAD = {
    "results": [
        {
            "text": "passage: useful viewport details " + ("A" * 300),
            "metadata": {"title": "Viewport Doc", "chunkSource": "link://viewport"},
            "score": 0.95,
        },
        {
            "text": "404 Not Found nginx/1.22.0",
            "metadata": {"title": "404 Doc", "chunkSource": "link://404"},
            "score": 0.99,
        },
        {
            "text": "passage: useful viewport details " + ("A" * 300),
            "metadata": {"title": "Viewport Doc", "chunkSource": "link://viewport"},
            "score": 0.95,
        },
    ]
}


CHAT_PAYLOAD = {
    "textResponse": "final answer body",
    "sources": [{"title": "Doc 1", "text": "source text"}],
    "metrics": {"total_tokens": 321},
}


WORKSPACE_LIST_PAYLOAD = {
    "workspaces": [
        {
            "id": 1,
            "slug": "demo-workspace",
            "name": "Demo Workspace",
            "chatMode": "chat",
            "chatProvider": "ollama",
            "chatModel": "qwen",
            "topN": 8,
            "lastUpdatedAt": "2026-05-06T08:00:00.000Z",
            "threads": [
                {"slug": "thread-a", "name": "Thread A", "user_id": None},
                {"slug": "thread-b", "name": "Thread B", "user_id": 3},
                {"slug": "thread-c", "name": "Thread C", "user_id": 5},
            ],
            "openAiPrompt": "should not appear",
        }
    ]
}


DOCUMENT_LIST_PAYLOAD = {
    "localFiles": {
        "name": "documents",
        "type": "folder",
        "items": [
            {
                "name": "custom-documents",
                "type": "folder",
                "items": [
                    {
                        "name": "alpha.md.json",
                        "type": "file",
                        "title": "Alpha",
                        "token_count_estimate": 123,
                        "cached": True,
                    }
                ],
            },
            {
                "name": "beta.md.json",
                "type": "file",
                "title": "Beta",
                "token_count_estimate": 456,
                "cached": False,
            },
        ],
    }
}


WORKSPACE_CHATS_PAYLOAD = {
    "history": [
        {
            "role": "user",
            "content": "请生成一个非常长非常长的 prompt " + ("A" * 300),
            "chatId": 10,
            "sentAt": 1778054742,
        },
        {
            "role": "assistant",
            "type": "chat",
            "content": "这是一个非常长非常长的回复 " + ("B" * 300),
            "chatId": 11,
            "sentAt": 1778054743,
            "sources": [{"title": "Doc 1"}],
            "metrics": {"total_tokens": 8054, "model": "gpt-5.4-mini"},
        },
    ]
}


ADMIN_WORKSPACE_CHATS_PAYLOAD = {
    "chats": [
        {
            "id": 99,
            "thread_id": 45,
            "createdAt": "2026-05-06T08:17:16.489Z",
            "prompt": "基于当前知识库，整理一个浏览器端单文件 Leafer 流程图编辑 demo 的稳定实现要点。" + ("P" * 260),
            "response": json.dumps(
                {
                    "text": "推荐做法：使用 App + viewport，节点移动后重算 points。" + ("R" * 260),
                    "sources": [{"title": "editor docs"}, {"title": "viewport docs"}],
                    "metrics": {"total_tokens": 4086, "model": "gpt-5.4-mini"},
                },
                ensure_ascii=False,
            ),
            "workspace": {"slug": "leafer-ai-docs"},
        }
    ]
}


SYSTEM_PAYLOAD = {
    "settings": {
        "RequiresAuth": False,
        "MultiUserMode": False,
        "SimpleSSOEnabled": False,
        "DisableViewChatHistory": False,
        "StorageDir": r"C:\Users\tester\AppData\Roaming\anythingllm-desktop\storage",
        "HasExistingEmbeddings": True,
        "HasCachedEmbeddings": True,
        "VectorDB": "lancedb",
        "EmbeddingEngine": "native",
        "EmbeddingModelPref": "MintplexLabs/multilingual-e5-small",
        "OllamaEmbeddingBatchSize": 1,
        "LLMProvider": "generic-openai",
        "LLMModel": "gpt-5.4-mini",
        "GenericOpenAiTokenLimit": "204800",
        "GenericOpenAiMaxTokens": "1024",
        "SpeechToTextProvider": "local_whisper",
        "SpeechToTextLocalWhisperModel": "Xenova/whisper-tiny",
        "TextToSpeechProvider": "native",
        "WhisperProvider": "local",
        "AgentSkillMaxToolCalls": 10,
        "AgentSkillRerankerEnabled": True,
        "AgentSkillRerankerTopN": 15,
        "NetworkDiscovery": "true",
        "DisableTelemetry": "false",
        "GenericOpenAiKey": False,
        "OpenAiKey": False,
        "AwsBedrockLLMAccessKey": False,
        "TTSElevenLabsKey": False,
        "PGVectorConnectionString": False,
    }
}


EMBED_CHATS_PAYLOAD = {
    "history": [
        {
            "role": "user",
            "content": "嵌入式聊天的 prompt 内容 " + ("C" * 260),
            "chatId": 1,
            "sentAt": 1778055000,
        },
        {
            "role": "assistant",
            "type": "chat",
            "content": "嵌入式聊天的 response 内容 " + ("D" * 260),
            "chatId": 2,
            "sentAt": 1778055001,
            "sources": [{"title": "Embed Doc"}, {"title": "Embed Doc 2"}],
            "metrics": {"total_tokens": 2048, "model": "gpt-5.4-mini"},
        },
    ]
}


class OutputShapingTests(unittest.TestCase):
    def parse(self, *argv):
        return cli.build_parser().parse_args(list(argv))

    def capture_stdout(self, func):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            func()
        return stream.getvalue()

    def test_workspace_get_defaults_to_summary_output(self):
        args = self.parse("workspace", "get", "demo-workspace")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACE_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["slug"], "demo-workspace")
        self.assertEqual(parsed["documentsCount"], 2)
        self.assertEqual(parsed["threadsCount"], 2)
        self.assertNotIn("openAiPrompt", output)

    def test_workspace_get_full_preserves_original_payload(self):
        args = self.parse("workspace", "get", "demo-workspace", "--full")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/workspace/demo-workspace")

    def test_search_compact_outputs_truncated_results_without_verbose_metadata(self):
        args = self.parse("search", "demo-workspace", "--query", "viewport", "--snippet-chars", "60")
        with patch.object(cli, "http_request_capture", return_value=SEARCH_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["resultsCount"], 3)
        snippet = parsed["results"][0]["snippet"]
        self.assertLessEqual(len(snippet), 60)
        self.assertNotIn("metadata", output)

    def test_search_compact_can_hide_404_noise_and_duplicate_sources(self):
        args = self.parse(
            "search",
            "demo-workspace",
            "--query",
            "viewport",
            "--hide-404",
            "--dedupe",
            "--min-score",
            "0.9",
        )
        with patch.object(cli, "http_request_capture", return_value=SEARCH_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["resultsCount"], 1)
        self.assertEqual(parsed["results"][0]["source"], "link://viewport")

    def test_ask_text_only_omits_sources_and_metrics_from_stdout(self):
        args = self.parse("ask", "demo-workspace", "--thread", "thread-a", "--text-only", "--message", "hello")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        kwargs = http_request.call_args.kwargs
        self.assertTrue(kwargs["text_only"])
        self.assertFalse(kwargs["no_sources"])
        self.assertFalse(kwargs["no_metrics"])

        output = self.capture_stdout(lambda: cli.maybe_json_print(json.dumps(CHAT_PAYLOAD), text_only=True))
        self.assertEqual(output.strip(), "final answer body")
        self.assertNotIn('"sources"', output)
        self.assertNotIn('"metrics"', output)

    def test_ask_json_output_writes_full_payload_to_file_while_keeping_stdout_slim(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path = os.path.join(temp_dir, "response.json")
            output = self.capture_stdout(
                lambda: cli.maybe_json_print(
                    json.dumps(CHAT_PAYLOAD),
                    text_only=True,
                    json_output=json_path,
                )
            )
            self.assertEqual(output.strip(), "final answer body")
            with open(json_path, "r", encoding="utf-8") as handle:
                saved = json.load(handle)
            self.assertEqual(saved["textResponse"], "final answer body")
            self.assertIn("sources", saved)
            self.assertIn("metrics", saved)

    def test_workspace_chat_json_output_writes_full_payload_to_file(self):
        args = self.parse(
            "workspace",
            "chat",
            "demo-workspace",
            "--message",
            "hello",
            "--text-only",
            "--json-output",
            "response.json",
            "--no-sources",
            "--no-metrics",
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        kwargs = http_request.call_args.kwargs
        self.assertTrue(kwargs["text_only"])
        self.assertTrue(kwargs["no_sources"])
        self.assertTrue(kwargs["no_metrics"])
        self.assertEqual(kwargs["json_output"], "response.json")

    def test_workspace_list_defaults_to_summary_output(self):
        args = self.parse("workspace", "list", "--max-items", "1")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACE_LIST_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["workspacesCount"], 1)
        self.assertEqual(parsed["workspaces"][0]["slug"], "demo-workspace")
        self.assertEqual(parsed["workspaces"][0]["threadsCount"], 3)
        self.assertNotIn("openAiPrompt", output)

    def test_document_list_defaults_to_tree_summary_output(self):
        args = self.parse("document", "list", "--max-items", "3")
        with patch.object(cli, "http_request_capture", return_value=DOCUMENT_LIST_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["root"], "documents")
        self.assertEqual(parsed["foldersCount"], 1)
        self.assertEqual(parsed["filesCount"], 2)
        self.assertEqual(len(parsed["itemsPreview"]), 3)

    def test_workspace_chats_defaults_to_compact_history_output(self):
        args = self.parse("workspace", "chats", "demo-workspace", "--max-items", "2", "--snippet-chars", "80")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACE_CHATS_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["entriesCount"], 2)
        self.assertLessEqual(len(parsed["entries"][0]["preview"]), 80)
        self.assertEqual(parsed["entries"][1]["sourcesCount"], 1)
        self.assertEqual(parsed["entries"][1]["totalTokens"], 8054)

    def test_thread_get_chats_defaults_to_compact_history_output(self):
        args = self.parse("thread", "get-chats", "demo-workspace", "thread-a", "--max-items", "1")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACE_CHATS_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["entriesCount"], 2)
        self.assertEqual(len(parsed["entries"]), 1)

    def test_admin_workspace_chats_defaults_to_compact_history_output(self):
        args = self.parse("admin", "workspace-chats", "--max-items", "1", "--snippet-chars", "90")
        with patch.object(cli, "http_request_capture", return_value=ADMIN_WORKSPACE_CHATS_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["entriesCount"], 1)
        entry = parsed["entries"][0]
        self.assertEqual(entry["workspace"], "leafer-ai-docs")
        self.assertLessEqual(len(entry["promptPreview"]), 90)
        self.assertEqual(entry["sourcesCount"], 2)
        self.assertEqual(entry["totalTokens"], 4086)

    def test_system_get_defaults_to_summary_output(self):
        args = self.parse("system", "get")
        with patch.object(cli, "http_request_capture", return_value=SYSTEM_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["settingsCount"], len(SYSTEM_PAYLOAD["settings"]))
        self.assertEqual(parsed["configuredSecretsCount"], 2)
        self.assertEqual(parsed["storage"]["storageDirName"], "storage")
        self.assertEqual(parsed["llm"]["provider"], "generic-openai")
        self.assertNotIn("StorageDir", output)

    def test_embed_chats_defaults_to_compact_history_output(self):
        args = self.parse("embed", "chats", "embed-1", "--max-items", "2", "--snippet-chars", "70")
        with patch.object(cli, "http_request_capture", return_value=EMBED_CHATS_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["entriesCount"], 2)
        self.assertLessEqual(len(parsed["entries"][0]["preview"]), 70)
        self.assertEqual(parsed["entries"][1]["sourcesCount"], 2)
        self.assertEqual(parsed["entries"][1]["totalTokens"], 2048)

    def test_embed_session_chats_defaults_to_compact_history_output(self):
        args = self.parse("embed", "session-chats", "embed-1", "session-1", "--max-items", "1")
        with patch.object(cli, "http_request_capture", return_value=EMBED_CHATS_PAYLOAD):
            output = self.capture_stdout(lambda: args.func(args))
        parsed = json.loads(output)
        self.assertEqual(parsed["entriesCount"], 2)
        self.assertEqual(len(parsed["entries"]), 1)


if __name__ == "__main__":
    unittest.main()
