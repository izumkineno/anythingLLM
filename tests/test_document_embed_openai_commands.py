import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


class DocumentEmbedOpenAICommandTests(unittest.TestCase):
    def parse(self, *argv):
        return cli.build_parser().parse_args(list(argv))

    def test_document_create_folder_uses_expected_body(self):
        args = self.parse("document", "create-folder", "project-notes")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/document/create-folder",
            json_body={"name": "project-notes"},
        )

    def test_document_remove_folder_uses_expected_body(self):
        args = self.parse("document", "remove-folder", "project-notes")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "DELETE",
            "/document/remove-folder",
            json_body={"name": "project-notes"},
        )

    def test_document_move_files_uses_json_body(self):
        args = self.parse(
            "document",
            "move-files",
            "--json",
            '[{"from":"custom-documents/a.txt","to":"archive/a.txt"}]',
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/document/move-files",
            json_body={"files": [{"from": "custom-documents/a.txt", "to": "archive/a.txt"}]},
        )

    def test_document_list_parses_summary_flags(self):
        args = self.parse("document", "list", "--folder", "docs", "--full", "--max-items", "12")
        self.assertEqual(args.folder, "docs")
        self.assertTrue(args.full)
        self.assertEqual(args.max_items, 12)

    def test_embed_create_uses_new_endpoint(self):
        args = self.parse(
            "embed",
            "create",
            "--json",
            '{"workspace_slug":"demo","chat_mode":"chat"}',
        )
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with(
            "POST",
            "/embed/new",
            json_body={"workspace_slug": "demo", "chat_mode": "chat"},
        )

    def test_openai_models_uses_models_endpoint(self):
        args = self.parse("openai", "models")
        with patch.object(cli, "http_request") as http_request:
            args.func(args)
        http_request.assert_called_once_with("GET", "/openai/models")


if __name__ == "__main__":
    unittest.main()
