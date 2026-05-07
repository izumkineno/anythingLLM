from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class SkillDocsTokenGuidanceTests(unittest.TestCase):
    def read(self, name: str) -> str:
        return (ROOT / name).read_text(encoding="utf-8")

    def test_skill_md_describes_summary_first_and_full_on_demand(self):
        text = self.read("SKILL.md")
        self.assertIn("保存后默认只做局部读取", text)
        self.assertIn("workspace get", text)
        self.assertIn("--full", text)

    def test_workflows_ask_query_prefers_compact_search_and_partial_reads(self):
        text = self.read("workflows-ask-query.md")
        self.assertIn("--compact", text)
        self.assertIn("Get-Content temp.txt -TotalCount 40", text)
        self.assertIn("--text-only --no-sources --no-metrics", text)

    def test_workflows_chat_prefers_text_only_for_file_redirection(self):
        text = self.read("workflows-chat.md")
        self.assertIn("--text-only --no-sources --no-metrics", text)
        self.assertIn("--json-output", text)
        self.assertIn("Get-Content output.html -TotalCount 40", text)

    def test_pitfalls_mentions_token_waste_from_full_dumps_or_unfiltered_output(self):
        text = self.read("anythingllm-skill-pitfalls.md")
        self.assertIn("整份回读进上下文", text)
        self.assertIn("Get-Content -TotalCount", text)


if __name__ == "__main__":
    unittest.main()
