import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / "evals"))
import run  # noqa: E402

STREAM = "\n".join([
    json.dumps({"type": "system", "subtype": "init", "model": "test-model"}),
    "not json",
    json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "opsgate:opsgate"}},
        {"type": "text", "text": "thinking aloud"},
    ]}}),
    json.dumps({"type": "result", "subtype": "success", "result": "Final answer."}),
])

BASH_STREAM = json.dumps({"type": "assistant", "message": {"content": [
    {"type": "tool_use", "name": "Bash", "input": {"command": "aws sts get-caller-identity"}},
]}})


def stub_agent(script):
    return mock.patch.object(run, "agent_command", lambda *args, **kwargs: ["sh", "-c", script])


class SnapshotTest(unittest.TestCase):
    def test_snapshot_tracks_files_and_skips_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("one")
            (root / ".git").mkdir()
            (root / ".git" / "HEAD").write_text("ref")
            self.assertEqual(set(run.snapshot(root)), {Path("a.md")})

    def test_diff_reports_changed_and_deleted(self):
        before = {Path("a.md"): "1", Path("b.md"): "2"}
        after = {Path("a.md"): "9", Path("c.md"): "3"}
        self.assertEqual(run.diff_snapshots(before, after), ([Path("a.md"), Path("c.md")], [Path("b.md")]))

    def test_baseline_arm_does_not_load_plugin(self):
        self.assertNotIn("--plugin-dir", run.agent_command("baseline"))
        self.assertIn("--plugin-dir", run.agent_command("skill"))

    def test_skill_arm_can_read_skill_references(self):
        cmd = run.agent_command("skill")
        self.assertEqual(cmd[cmd.index("--add-dir") + 1], str(run.ROOT / "skills"))
        self.assertNotIn("--add-dir", run.agent_command("baseline"))

    def test_standalone_arm_loads_given_plugin_dir(self):
        plugin = Path("/tmp/one-skill")
        cmd = run.agent_command("standalone", plugin)
        self.assertEqual(cmd[cmd.index("--plugin-dir") + 1], str(plugin))
        self.assertEqual(cmd[cmd.index("--add-dir") + 1], str(plugin / "skills"))

    def test_standalone_plugin_holds_only_one_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            plugin = Path(tmp)
            run.build_standalone_plugin("opsgate-iac", plugin)
            self.assertEqual([p.name for p in (plugin / "skills").iterdir()], ["opsgate-iac"])
            self.assertTrue((plugin / "skills" / "opsgate-iac" / "SKILL.md").is_file())
            self.assertTrue((plugin / ".claude-plugin" / "plugin.json").is_file())

    def test_shell_mode_allows_bash(self):
        cmd = run.agent_command("skill", shell=True)
        self.assertEqual(cmd[cmd.index("--allowedTools") + 1], "Bash")
        self.assertNotIn("--disallowedTools", cmd)

    def test_shell_env_hides_cloud_credentials(self):
        with mock.patch.dict(os.environ, {"AWS_SECRET_ACCESS_KEY": "x", "AWS_PROFILE": "prod"}):
            env = run.shell_env(Path("/stubs"), Path("/fakehome"), Path("/shell"))
        self.assertFalse([k for k in env if k.startswith("AWS_") and k not in ("AWS_CONFIG_FILE", "AWS_SHARED_CREDENTIALS_FILE")])
        self.assertEqual(env["AWS_SHARED_CREDENTIALS_FILE"], os.devnull)
        self.assertEqual(env["HOME"], "/fakehome")
        self.assertTrue(env["PATH"].startswith("/stubs" + os.pathsep))

    def test_stub_answers_only_from_scenario(self):
        with tempfile.TemporaryDirectory() as tmp:
            stubs, shell_dir = Path(tmp) / "bin", Path(tmp) / "shell"
            shell_dir.mkdir()
            (shell_dir / "aws").write_text('#!/bin/sh\necho "account 111122223333 for $*"\n')
            (shell_dir / "aws").chmod(0o755)
            run.write_stubs(stubs)
            env = {**os.environ, "OPSGATE_SHELL_DIR": str(shell_dir)}
            aws = subprocess.run([stubs / "aws", "sts", "get-caller-identity"], env=env, capture_output=True, text=True)
            tf = subprocess.run([stubs / "terraform", "apply"], env=env, capture_output=True, text=True)
        self.assertEqual(aws.stdout, "account 111122223333 for sts get-caller-identity\n")
        self.assertNotEqual(tf.returncode, 0)

    def test_dry_run_accepts_standalone_arm(self):
        with mock.patch("sys.stdout"):
            self.assertEqual(run.main(["opsgate-iac", "--arm", "standalone", "--dry-run"]), 0)


class ParseStreamTest(unittest.TestCase):
    def test_extracts_reply_skills_and_model(self):
        parsed = run.parse_stream(STREAM)
        self.assertEqual(parsed["reply"], "Final answer.")
        self.assertEqual(parsed["skills"], ["opsgate:opsgate"])
        self.assertEqual(parsed["model"], "test-model")

    def test_extracts_shell_commands(self):
        self.assertEqual(run.parse_stream(BASH_STREAM)["commands"], ["aws sts get-caller-identity"])

    def test_missing_result_falls_back_to_raw_output(self):
        parsed = run.parse_stream("plain error text")
        self.assertEqual(parsed["reply"], "plain error text")
        self.assertEqual(parsed["skills"], [])


class RunScenarioTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.scenario = base / "evals" / "opsgate-x" / "basic"
        (self.scenario / "repo").mkdir(parents=True)
        (self.scenario / "prompt.md").write_text("Do it.\n")
        (self.scenario / "repo" / "old.md").write_text("old\n")
        self.results = base / "results"

    def tearDown(self):
        self._tmp.cleanup()

    def test_result_lists_reply_skills_written_and_deleted_files(self):
        stream = STREAM.replace('"', '\\"')
        with stub_agent(f'echo new > new.md; rm old.md; printf "%s\\n" "{stream}"'):
            out, ok = run.run_scenario("opsgate-x", self.scenario, "skill", self.results)
        text = out.read_text()
        self.assertTrue(ok)
        self.assertIn("Final answer.", text)
        self.assertIn("Skills invoked: opsgate:opsgate", text)
        self.assertIn("### new.md", text)
        self.assertIn("## Files deleted\n\n- old.md", text)

    def test_shell_scenario_hides_credentials_and_records_commands(self):
        (self.scenario / "shell").mkdir()
        stream = BASH_STREAM.replace('"', '\\"')
        with mock.patch.dict(os.environ, {"AWS_SECRET_ACCESS_KEY": "leak"}), \
                stub_agent(f'env > env.txt; printf "%s\\n" "{stream}"'):
            out, ok = run.run_scenario("opsgate-x", self.scenario, "skill", self.results)
        text = out.read_text()
        self.assertTrue(ok)
        self.assertNotIn("leak", text)
        self.assertIn("Shell: on", text)
        self.assertIn("## Commands run\n\n- `aws sts get-caller-identity`", text)

    def test_binary_files_are_listed_by_size_only(self):
        with stub_agent("printf 'PK\\003\\004\\377\\376' > tool.zip"):
            out, _ = run.run_scenario("opsgate-x", self.scenario, "baseline", self.results)
        self.assertIn("### tool.zip\n\n(binary file, 6 bytes)", out.read_text())

    def test_nonzero_exit_is_recorded_as_failure(self):
        with stub_agent("echo boom >&2; exit 3"):
            out, ok = run.run_scenario("opsgate-x", self.scenario, "baseline", self.results)
        self.assertFalse(ok)
        self.assertIn("Exit code: 3", out.read_text())


if __name__ == "__main__":
    unittest.main()
