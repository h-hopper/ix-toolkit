import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("ix-show", "ix-manual", "ix-backup", "ix-configure", "ix-save")


class CodexSkillLayoutTests(unittest.TestCase):
    def test_each_codex_adapter_reuses_existing_skill_and_scripts(self):
        self.assertTrue((ROOT / "scripts" / "ix-ssh.py").is_file())
        self.assertTrue((ROOT / "scripts" / "ix_paths.py").is_file())
        for name in SKILLS:
            adapter = ROOT / ".agents" / "skills" / name / "SKILL.md"
            canonical = adapter.parent / ".." / ".." / ".." / "skills" / name / "SKILL.md"
            with self.subTest(skill=name):
                self.assertTrue(adapter.is_file())
                self.assertTrue(canonical.resolve().is_file())
                text = adapter.read_text(encoding="utf-8")
                match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
                self.assertIsNotNone(match)
                fields = {
                    line.split(":", 1)[0]
                    for line in match.group(1).splitlines()
                    if line and not line[0].isspace() and ":" in line
                }
                self.assertEqual(fields, {"name", "description"})
                self.assertIn(f"name: {name}", text)
                self.assertNotIn("[TODO:", text)

    def test_claude_plugin_and_shared_skill_metadata_remain_present(self):
        self.assertTrue((ROOT / ".claude-plugin" / "plugin.json").is_file())
        for name in SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(skill=name):
                self.assertTrue(text.startswith("---\n"))
                self.assertIn(f"name: {name}", text)
                self.assertIn("description:", text)
                self.assertIn("allowed-tools:", text)
                if name != "ix-manual":
                    self.assertIn("${CLAUDE_PLUGIN_ROOT}", text)


if __name__ == "__main__":
    unittest.main()
