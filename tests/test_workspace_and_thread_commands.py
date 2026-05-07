import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


class WorkspaceAndThreadCommandTests(unittest.TestCase):
    def parse(self, *argv):
        return cli.build_parser().parse_args(list(argv))

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

    def test_thread_update_uses_expected_body(self):
        args = self.parse("thread", "update", "demo-workspace", "thread-1", "--name", "Renamed Thread")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/workspace/demo-workspace/thread/thread-1/update",
            json_body={"name": "Renamed Thread"},
        )

    def test_thread_get_chats_uses_expected_endpoint(self):
        args = self.parse("thread", "get-chats", "demo-workspace", "thread-1", "--full")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/workspace/demo-workspace/thread/thread-1/chats")

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
