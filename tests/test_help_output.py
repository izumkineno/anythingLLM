import contextlib
import io
import unittest

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

    def test_document_help_lists_management_commands(self):
        help_text = render_help(["document"])
        for command in ["create-folder", "remove-folder", "move-files"]:
            self.assertIn(command, help_text)


if __name__ == "__main__":
    unittest.main()
