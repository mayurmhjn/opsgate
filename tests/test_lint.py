import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import lint  # noqa: E402


def make_skill(root, folder, name, description="Use when testing."):
    skill_dir = root / "skills" / folder
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
    )


def write_manifests(root, marketplace, plugin):
    d = root / ".claude-plugin"
    d.mkdir()
    (d / "marketplace.json").write_text(marketplace)
    (d / "plugin.json").write_text(plugin)


class LintTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_no_skills_dir_passes(self):
        self.assertEqual(lint.lint(self.root), [])

    def test_valid_skill_passes(self):
        make_skill(self.root, "opsgate-iac", "opsgate-iac")
        self.assertEqual(lint.lint(self.root), [])

    def test_folder_without_skill_md_reported(self):
        (self.root / "skills" / "opsgate-empty").mkdir(parents=True)
        self.assertEqual(lint.lint(self.root), ["skills/opsgate-empty: missing SKILL.md"])

    def test_missing_prefix_reported(self):
        make_skill(self.root, "iac", "iac")
        self.assertIn("skills/iac: name must start with opsgate-", lint.lint(self.root))

    def test_name_folder_mismatch_reported(self):
        make_skill(self.root, "opsgate-iac", "opsgate-cicd")
        problems = lint.lint(self.root)
        self.assertTrue(problems)
        self.assertTrue(all(p.startswith("skills/opsgate-iac:") for p in problems))

    def test_invalid_manifest_json_reported(self):
        write_manifests(self.root, "{bad", "{}")
        problems = lint.lint(self.root)
        self.assertTrue(
            any(p.startswith(".claude-plugin/marketplace.json: invalid JSON") for p in problems)
        )

    def test_manifest_version_mismatch_reported(self):
        write_manifests(
            self.root,
            json.dumps({"plugins": [{"name": "opsgate", "version": "0.0.1"}]}),
            json.dumps({"name": "opsgate", "version": "0.0.2"}),
        )
        self.assertEqual(
            lint.lint(self.root),
            [".claude-plugin: marketplace and plugin.json disagree on version"],
        )

    def test_main_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lint.main([str(self.root)]), 0)
            make_skill(self.root, "iac", "iac")
            self.assertEqual(lint.main([str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
