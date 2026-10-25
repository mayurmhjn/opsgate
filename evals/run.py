"""Run a skill's eval scenarios with and without the skill installed.

Usage: python evals/run.py SKILL [--scenario NAME] [--arm baseline|skill|both] [--dry-run]

Results go to evals/results/<skill>/<scenario>/<arm>.md. See evals/README.md.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT_SECONDS = 900


def agent_command(arm):
    cmd = [
        "claude", "-p", "--no-session-persistence",
        "--permission-mode", "acceptEdits",
        "--disallowedTools", "Bash",
    ]
    if arm == "skill":
        cmd += ["--plugin-dir", str(ROOT)]
    return cmd


def snapshot(directory):
    return {
        p.relative_to(directory): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(directory).parts
    }


def run_scenario(skill, scenario_dir, arm):
    prompt = (scenario_dir / "prompt.md").read_text()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        if (scenario_dir / "repo").is_dir():
            shutil.copytree(scenario_dir / "repo", work, dirs_exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=work, check=True)
        before = snapshot(work)
        try:
            result = subprocess.run(
                agent_command(arm), input=prompt, cwd=work,
                capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
            )
            reply = result.stdout.strip() or result.stderr.strip()
        except subprocess.TimeoutExpired:
            reply = f"(timed out after {TIMEOUT_SECONDS}s)"
        after = snapshot(work)
        changed = sorted(p for p, h in after.items() if before.get(p) != h)
        files = [(p, (work / p).read_text(errors="replace")) for p in changed]

    out = ROOT / "evals" / "results" / skill / scenario_dir.name / f"{arm}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    parts = [f"# {skill} / {scenario_dir.name} / {arm}", "## Prompt", prompt.strip(), "## Reply", reply]
    parts.append("## Files written")
    parts += [f"### {p.as_posix()}\n\n```\n{text}\n```" for p, text in files] or ["(none)"]
    out.write_text("\n\n".join(parts) + "\n")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run eval scenarios for one skill.")
    parser.add_argument("skill")
    parser.add_argument("--scenario")
    parser.add_argument("--arm", choices=["baseline", "skill", "both"], default="both")
    parser.add_argument("--dry-run", action="store_true", help="print what would run")
    args = parser.parse_args(argv)

    evals_dir = ROOT / "evals" / args.skill
    scenarios = sorted(d for d in evals_dir.glob("*/") if (d / "prompt.md").is_file())
    if args.scenario:
        scenarios = [d for d in scenarios if d.name == args.scenario]
    if not scenarios:
        print(f"no scenarios found in {evals_dir}", file=sys.stderr)
        return 2
    if "CLAUDE_CONFIG_DIR" not in os.environ:
        print("warning: CLAUDE_CONFIG_DIR is not set, so personal instructions may affect results",
              file=sys.stderr)

    arms = ["baseline", "skill"] if args.arm == "both" else [args.arm]
    for scenario_dir in scenarios:
        for arm in arms:
            if args.dry_run:
                print(f"{scenario_dir.name} [{arm}]: {' '.join(agent_command(arm))}")
                continue
            print(f"{scenario_dir.name} [{arm}] ... ", end="", flush=True)
            print(run_scenario(args.skill, scenario_dir, arm).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
