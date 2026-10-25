import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "evals"))
import run  # noqa: E402


class SnapshotTest(unittest.TestCase):
    def test_snapshot_tracks_files_and_skips_git(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.md").write_text("one")
            (root / ".git").mkdir()
            (root / ".git" / "HEAD").write_text("ref")
            before = run.snapshot(root)
            (root / "a.md").write_text("two")
            (root / "docs").mkdir()
            (root / "docs" / "b.md").write_text("new")
            after = run.snapshot(root)
        self.assertEqual(set(before), {Path("a.md")})
        changed = sorted(p for p, h in after.items() if before.get(p) != h)
        self.assertEqual(changed, [Path("a.md"), Path("docs/b.md")])

    def test_baseline_arm_does_not_load_plugin(self):
        self.assertNotIn("--plugin-dir", run.agent_command("baseline"))
        self.assertIn("--plugin-dir", run.agent_command("skill"))


if __name__ == "__main__":
    unittest.main()
