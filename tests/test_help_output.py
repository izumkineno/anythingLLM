import contextlib
import io
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anythingllm as cli


def render_help(argv):
    parser = cli.build_parser()
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        with unittest.TestCase().assertRaises(SystemExit):
            parser.parse_args(argv + ["--help"])
    return stream.getvalue()


class HelpOutputTests(unittest.TestCase):
    def test_root_help_lists_new_command_groups(self):
        help_text = cli.build_parser().format_help()
        for command in ["admin", "system", "embed", "openai", "user", "auth"]:
            self.assertIn(command, help_text)

    def test_workspace_help_lists_gap_commands(self):
        help_text = render_help(["workspace"])
        for command in ["chat", "stream-chat", "chats", "delete", "update-embeddings", "update-pin"]:
            self.assertIn(command, help_text)

    def test_workspace_list_help_lists_summary_flags(self):
        help_text = render_help(["workspace", "list"])
        for flag in ["--full", "--max-items"]:
            self.assertIn(flag, help_text)

    def test_workspace_get_help_lists_summary_flags(self):
        help_text = render_help(["workspace", "get"])
        for flag in ["--full", "--max-docs", "--docs-only", "--threads-only"]:
            self.assertIn(flag, help_text)

    def test_search_help_lists_compact_flags(self):
        help_text = render_help(["search"])
        for flag in ["--full", "--compact", "--snippet-chars", "--hide-404", "--dedupe", "--min-score", "--titles-only"]:
            self.assertIn(flag, help_text)

    def test_ask_help_lists_output_slimming_flags(self):
        help_text = render_help(["ask"])
        for flag in ["--text-only", "--no-sources", "--sources-limit", "--no-metrics", "--json-output"]:
            self.assertIn(flag, help_text)

    def test_document_help_lists_management_commands(self):
        help_text = render_help(["document"])
        for command in ["create-folder", "remove-folder", "move-files"]:
            self.assertIn(command, help_text)

    def test_document_list_help_lists_summary_flags(self):
        help_text = render_help(["document", "list"])
        for flag in ["--full", "--max-items"]:
            self.assertIn(flag, help_text)

    def test_thread_get_chats_help_lists_summary_flags(self):
        help_text = render_help(["thread", "get-chats"])
        for flag in ["--full", "--max-items", "--snippet-chars"]:
            self.assertIn(flag, help_text)

    def test_admin_workspace_chats_help_lists_summary_flags(self):
        help_text = render_help(["admin", "workspace-chats"])
        for flag in ["--full", "--max-items", "--snippet-chars"]:
            self.assertIn(flag, help_text)

    def test_system_get_help_lists_summary_flag(self):
        help_text = render_help(["system", "get"])
        self.assertIn("--full", help_text)

    def test_embed_help_lists_history_commands(self):
        help_text = render_help(["embed"])
        for command in ["chats", "session-chats"]:
            self.assertIn(command, help_text)

    def test_embed_chats_help_lists_summary_flags(self):
        help_text = render_help(["embed", "chats"])
        for flag in ["--full", "--max-items", "--snippet-chars"]:
            self.assertIn(flag, help_text)

    def test_embed_session_chats_help_lists_summary_flags(self):
        help_text = render_help(["embed", "session-chats"])
        for flag in ["--full", "--max-items", "--snippet-chars"]:
            self.assertIn(flag, help_text)


if __name__ == "__main__":
    unittest.main()
