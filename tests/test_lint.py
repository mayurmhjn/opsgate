import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import lint  # noqa: E402


def make_skill(root, folder, name, description="Use when testing.", evals=True):
    skill_dir = root / "skills" / folder
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n"
    )
    if evals:
        make_scenario(root, folder, "basic")


def make_scenario(root, skill, scenario, files=("prompt.md", "criteria.md")):
    d = root / "evals" / skill / scenario
    d.mkdir(parents=True)
    for f in files:
        (d / f).write_text("x\n")


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
        self.assertIn("skills/iac: name must be opsgate or start with opsgate-", lint.lint(self.root))

    def test_bare_opsgate_name_passes(self):
        make_skill(self.root, "opsgate", "opsgate")
        self.assertEqual(lint.lint(self.root), [])

    def test_name_glued_to_opsgate_reported(self):
        make_skill(self.root, "opsgatex", "opsgatex")
        self.assertIn("skills/opsgatex: name must be opsgate or start with opsgate-", lint.lint(self.root))

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

    def test_skill_without_evals_reported(self):
        make_skill(self.root, "opsgate-iac", "opsgate-iac", evals=False)
        self.assertEqual(
            lint.lint(self.root),
            ["evals/opsgate-iac: needs at least one scenario with prompt.md and criteria.md"],
        )

    def test_skill_with_scenario_passes(self):
        make_skill(self.root, "opsgate-iac", "opsgate-iac", evals=False)
        make_scenario(self.root, "opsgate-iac", "basic")
        self.assertEqual(lint.lint(self.root), [])

    def test_scenario_missing_criteria_reported(self):
        make_skill(self.root, "opsgate-iac", "opsgate-iac", evals=False)
        make_scenario(self.root, "opsgate-iac", "basic", files=("prompt.md",))
        self.assertEqual(
            lint.lint(self.root),
            ["evals/opsgate-iac: needs at least one scenario with prompt.md and criteria.md"],
        )

    def test_main_exit_codes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lint.main([str(self.root)]), 0)
            make_skill(self.root, "iac", "iac")
            self.assertEqual(lint.main([str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
