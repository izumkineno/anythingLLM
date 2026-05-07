import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


class AdminAndSystemCommandTests(unittest.TestCase):
    def parse(self, *argv):
        return cli.build_parser().parse_args(list(argv))

    def test_auth_verify_calls_auth_endpoint(self):
        args = self.parse("auth")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/auth")

    def test_user_list_calls_users_endpoint(self):
        args = self.parse("user", "list")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/users")

    def test_system_export_chats_supports_export_type(self):
        args = self.parse("system", "export-chats", "--type", "csv")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/system/export-chats?type=csv")

    def test_system_get_parses_summary_flag(self):
        args = self.parse("system", "get", "--full")
        self.assertTrue(args.full)

    def test_system_update_env_uses_json_body(self):
        args = self.parse("system", "update-env", "--json", '{"VectorDB":"lancedb"}')
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/system/update-env",
            json_body={"VectorDB": "lancedb"},
        )

    def test_admin_manage_users_uses_workspace_slug_endpoint(self):
        args = self.parse(
            "admin",
            "manage-users",
            "workspace-demo",
            "--json",
            '{"userIds":[1,2],"reset":false}',
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/admin/workspaces/workspace-demo/manage-users",
            json_body={"userIds": [1, 2], "reset": False},
        )

    def test_admin_workspace_chats_parses_summary_flags(self):
        args = self.parse(
            "admin",
            "workspace-chats",
            "--json",
            '{"offset":2}',
            "--full",
            "--max-items",
            "5",
            "--snippet-chars",
            "160",
        )
        self.assertEqual(args.json, '{"offset":2}')
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 5)
        self.assertEqual(args.snippet_chars, 160)

    def test_embed_chats_parses_summary_flags(self):
        args = self.parse("embed", "chats", "embed-1", "--full", "--max-items", "4", "--snippet-chars", "150")
        self.assertEqual(args.embed_uuid, "embed-1")
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 4)
        self.assertEqual(args.snippet_chars, 150)

    def test_embed_session_chats_parses_summary_flags(self):
        args = self.parse(
            "embed",
            "session-chats",
            "embed-1",
            "session-1",
            "--full",
            "--max-items",
            "3",
            "--snippet-chars",
            "120",
        )
        self.assertEqual(args.embed_uuid, "embed-1")
        self.assertEqual(args.session_uuid, "session-1")
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 3)
        self.assertEqual(args.snippet_chars, 120)


if __name__ == "__main__":
    unittest.main()
