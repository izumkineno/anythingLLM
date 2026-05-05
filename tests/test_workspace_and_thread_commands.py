import unittest
from unittest.mock import patch

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
        args = self.parse("thread", "get-chats", "demo-workspace", "thread-1")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/workspace/demo-workspace/thread/thread-1/chats")


if __name__ == "__main__":
    unittest.main()
