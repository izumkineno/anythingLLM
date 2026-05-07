import unittest
import sys
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


WORKSPACES_PAYLOAD = {
    "workspaces": [
        {"id": 1, "slug": "demo-workspace", "name": "Demo Workspace"},
        {"id": 2, "slug": "cn-workspace", "name": "我的工作区"},
        {"id": 3, "slug": "dup-one", "name": "重复工作区"},
        {"id": 4, "slug": "dup-two", "name": "重复工作区"},
    ]
}


class WorkspaceAndThreadCommandTests(unittest.TestCase):
    def parse(self, *argv):
        return cli.build_parser().parse_args(list(argv))

    def test_resolve_workspace_slug_returns_slug_input_unchanged(self):
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD) as http_request_capture:
            self.assertEqual(cli.resolve_workspace_slug("demo-workspace"), "demo-workspace")
        http_request_capture.assert_called_once_with("GET", "/workspaces", quiet=True)

    def test_resolve_workspace_slug_maps_exact_unicode_name(self):
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD):
            self.assertEqual(cli.resolve_workspace_slug("我的工作区"), "cn-workspace")

    def test_resolve_workspace_slug_errors_on_duplicate_name(self):
        stderr = StringIO()
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                cli.resolve_workspace_slug("重复工作区")
        self.assertIn("ambiguous", stderr.getvalue())
        self.assertIn("dup-one", stderr.getvalue())
        self.assertIn("dup-two", stderr.getvalue())

    def test_resolve_workspace_slug_errors_on_unknown_workspace(self):
        stderr = StringIO()
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), redirect_stderr(stderr):
            with self.assertRaises(SystemExit):
                cli.resolve_workspace_slug("不存在的工作区")
        self.assertIn("workspace not found", stderr.getvalue())

    def test_workspace_delete_uses_delete_endpoint(self):
        args = self.parse("workspace", "delete", "demo-workspace")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("DELETE", "/workspace/demo-workspace")

    def test_workspace_chats_supports_query_parameters(self):
        args = self.parse(
            "workspace",
            "chats",
            "demo-workspace",
            "--full",
            "--api-session-id",
            "session-1",
            "--limit",
            "25",
            "--order-by",
            "asc",
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "GET",
            "/workspace/demo-workspace/chats?apiSessionId=session-1&limit=25&orderBy=asc",
        )

    def test_workspace_list_parses_summary_flags(self):
        args = self.parse("workspace", "list", "--full", "--max-items", "6")
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 6)

    def test_workspace_chats_parses_summary_flags(self):
        args = self.parse(
            "workspace",
            "chats",
            "demo-workspace",
            "--full",
            "--max-items",
            "4",
            "--snippet-chars",
            "180",
        )
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 4)
        self.assertEqual(args.snippet_chars, 180)

    def test_workspace_update_embeddings_reads_json_body(self):
        args = self.parse(
            "workspace",
            "update-embeddings",
            "demo-workspace",
            "--json",
            '{"adds":["doc-a"],"deletes":["doc-b"]}',
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/demo-workspace/update-embeddings",
            json_body={"adds": ["doc-a"], "deletes": ["doc-b"]},
        )

    def test_workspace_get_parses_summary_flags(self):
        args = self.parse("workspace", "get", "demo-workspace", "--full", "--max-docs", "3", "--docs-only")
        self.assertTrue(args.full)
        self.assertEqual(args.max_docs, 3)
        self.assertTrue(args.docs_only)
        self.assertFalse(args.threads_only)

    def test_workspace_chat_parses_output_slimming_flags(self):
        args = self.parse(
            "workspace",
            "chat",
            "demo-workspace",
            "--text-only",
            "--no-sources",
            "--sources-limit",
            "2",
            "--no-metrics",
            "--json-output",
            "response.json",
        )
        self.assertTrue(args.text_only)
        self.assertTrue(args.no_sources)
        self.assertEqual(args.sources_limit, 2)
        self.assertTrue(args.no_metrics)
        self.assertEqual(args.json_output, "response.json")

    def test_ask_parses_output_slimming_flags(self):
        args = self.parse(
            "ask",
            "demo-workspace",
            "--text-only",
            "--no-sources",
            "--sources-limit",
            "1",
            "--no-metrics",
            "--json-output",
            "out.json",
        )
        self.assertTrue(args.text_only)
        self.assertTrue(args.no_sources)
        self.assertEqual(args.sources_limit, 1)
        self.assertTrue(args.no_metrics)
        self.assertEqual(args.json_output, "out.json")

    def test_ask_with_explicit_thread_resolves_workspace_name_to_slug(self):
        args = self.parse("ask", "我的工作区", "--thread", "thread-1", "--message", "hello")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD) as http_request_capture, patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request_capture.assert_called_once_with("GET", "/workspaces", quiet=True)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/cn-workspace/thread/thread-1/chat",
            json_body={"message": "hello", "mode": "chat"},
            text_only=False,
            no_sources=False,
            no_metrics=False,
            sources_limit=None,
            json_output=None,
        )

    def test_ask_auto_thread_resolves_workspace_once_and_reuses_slug(self):
        args = self.parse("ask", "我的工作区", "--message", "hello")
        with patch.object(
            cli,
            "http_request_capture",
            side_effect=[WORKSPACES_PAYLOAD, {"thread": {"slug": "thread-2"}}],
        ) as http_request_capture, patch.object(cli, "http_request") as http_request:
            args.func(args)
        self.assertEqual(http_request_capture.call_count, 2)
        self.assertEqual(http_request_capture.call_args_list[0].args, ("GET", "/workspaces"))
        self.assertEqual(http_request_capture.call_args_list[0].kwargs, {"quiet": True})
        self.assertEqual(http_request_capture.call_args_list[1].args, ("POST", "/workspace/cn-workspace/thread/new"))
        self.assertEqual(
            http_request_capture.call_args_list[1].kwargs,
            {"json_body": {"name": "Thread"}, "quiet": True},
        )
        http_request.assert_called_once_with(
            "POST",
            "/workspace/cn-workspace/thread/thread-2/chat",
            json_body={"message": "hello", "mode": "chat"},
            text_only=False,
            no_sources=False,
            no_metrics=False,
            sources_limit=None,
            json_output=None,
        )

    def test_search_parses_compact_flags(self):
        args = self.parse(
            "search",
            "demo-workspace",
            "--query",
            "viewport",
            "--compact",
            "--snippet-chars",
            "120",
            "--hide-404",
            "--dedupe",
            "--min-score",
            "0.9",
            "--titles-only",
        )
        self.assertTrue(args.compact)
        self.assertEqual(args.snippet_chars, 120)
        self.assertTrue(args.hide_404)
        self.assertTrue(args.dedupe)
        self.assertEqual(args.min_score, 0.9)
        self.assertTrue(args.titles_only)

    def test_search_parses_disable_flags(self):
        args = self.parse(
            "search",
            "demo-workspace",
            "--query",
            "viewport",
            "--no-hide-404",
            "--no-dedupe",
        )
        self.assertFalse(args.hide_404)
        self.assertFalse(args.dedupe)

    def test_search_resolves_workspace_name_to_slug(self):
        args = self.parse("search", "我的工作区", "--query", "viewport")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "emit_summary_or_full"
        ) as emit_summary_or_full:
            args.func(args)
        emit_summary_or_full.assert_called_once()
        self.assertEqual(emit_summary_or_full.call_args.kwargs["path"], "/workspace/cn-workspace/vector-search")

    def test_thread_update_uses_expected_body(self):
        args = self.parse("thread", "update", "demo-workspace", "thread-1", "--name", "Renamed Thread")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/demo-workspace/thread/thread-1/update",
            json_body={"name": "Renamed Thread"},
        )

    def test_thread_new_resolves_workspace_name_to_slug(self):
        args = self.parse("thread", "new", "我的工作区", "--name", "Thread Name")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/cn-workspace/thread/new",
            json_body={"name": "Thread Name"},
        )

    def test_thread_chat_resolves_workspace_name_to_slug(self):
        args = self.parse("thread", "chat", "我的工作区", "thread-1", "--message", "hello")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/cn-workspace/thread/thread-1/chat",
            json_body={"message": "hello", "mode": "chat"},
            text_only=False,
            no_sources=False,
            no_metrics=False,
            sources_limit=None,
            json_output=None,
        )

    def test_thread_stream_chat_resolves_workspace_name_to_slug(self):
        args = self.parse("thread", "stream-chat", "我的工作区", "thread-1", "--message", "hello")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/cn-workspace/thread/thread-1/stream-chat",
            json_body={"message": "hello", "mode": "chat"},
            stream=True,
            text_only=False,
            no_sources=False,
            no_metrics=False,
            sources_limit=None,
            json_output=None,
        )

    def test_thread_get_chats_uses_expected_endpoint(self):
        args = self.parse("thread", "get-chats", "demo-workspace", "thread-1", "--full")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "emit_summary_or_full"
        ) as emit_summary_or_full:
            args.func(args)
        emit_summary_or_full.assert_called_once()
        self.assertEqual(emit_summary_or_full.call_args.kwargs["path"], "/workspace/demo-workspace/thread/thread-1/chats")

    def test_thread_get_chats_resolves_workspace_name_to_slug(self):
        args = self.parse("thread", "get-chats", "我的工作区", "thread-1", "--full")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "emit_summary_or_full"
        ) as emit_summary_or_full:
            args.func(args)
        emit_summary_or_full.assert_called_once()
        self.assertEqual(emit_summary_or_full.call_args.kwargs["path"], "/workspace/cn-workspace/thread/thread-1/chats")

    def test_thread_delete_resolves_workspace_name_to_slug(self):
        args = self.parse("thread", "delete", "我的工作区", "thread-1")
        with patch.object(cli, "http_request_capture", return_value=WORKSPACES_PAYLOAD), patch.object(
            cli, "http_request"
        ) as http_request:
            args.func(args)
        http_request.assert_called_once_with("DELETE", "/workspace/cn-workspace/thread/thread-1")

    def test_thread_get_chats_parses_summary_flags(self):
        args = self.parse(
            "thread",
            "get-chats",
            "demo-workspace",
            "thread-1",
            "--full",
            "--max-items",
            "3",
            "--snippet-chars",
            "140",
        )
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 3)
        self.assertEqual(args.snippet_chars, 140)


if __name__ == "__main__":
    unittest.main()
