import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
