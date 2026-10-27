"""Run a skill's eval scenarios with and without the skill installed.

Usage: python evals/run.py SKILL [--scenario NAME] [--arm baseline|skill|both|standalone] [--dry-run]

Results go to evals/results/<skill>/<scenario>/<arm>.md. See evals/README.md.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "evals" / "results"
TIMEOUT_SECONDS = 900


def agent_command(arm, plugin_dir=ROOT):
    cmd = [
        "claude", "-p", "--no-session-persistence",
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits",
        "--disallowedTools", "Bash",
    ]
    if arm in ("skill", "standalone"):
        # Headless mode denies reads outside the working directory, so allow the skill folders.
        cmd += ["--plugin-dir", str(plugin_dir), "--add-dir", str(plugin_dir / "skills")]
    return cmd


def build_standalone_plugin(skill, dest):
    """Lay out a plugin in dest that holds only one skill, as if the user installed just that one."""
    shutil.copytree(ROOT / ".claude-plugin", dest / ".claude-plugin")
    shutil.copytree(ROOT / "skills" / skill, dest / "skills" / skill)


def snapshot(directory):
    return {
        p.relative_to(directory): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(directory).parts
    }


def diff_snapshots(before, after):
    changed = sorted(p for p, h in after.items() if before.get(p) != h)
    deleted = sorted(p for p in before if p not in after)
    return changed, deleted


def parse_stream(output):
    """Pull the final reply, invoked skills and model out of stream-json output."""
    parsed = {"reply": None, "skills": [], "model": None}
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            parsed["model"] = event.get("model")
        elif event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    parsed["skills"].append(block.get("input", {}).get("skill"))
        elif event.get("type") == "result":
            parsed["reply"] = event.get("result")
    if parsed["reply"] is None:
        parsed["reply"] = output.strip()
    return parsed


def run_agent(arm, prompt, cwd, plugin_dir=ROOT):
    """Return (exit code or None, combined output)."""
    try:
        result = subprocess.run(
            agent_command(arm, plugin_dir), input=prompt, cwd=cwd,
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
        return result.returncode, result.stdout if result.returncode == 0 else result.stdout + result.stderr
    except subprocess.TimeoutExpired as e:
        partial = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        return None, partial + f"\n(timed out after {TIMEOUT_SECONDS}s)"


def run_scenario(skill, scenario_dir, arm, results_dir=RESULTS_DIR):
    """Run one scenario arm. Return (result path, True if the agent exited cleanly)."""
    prompt = (scenario_dir / "prompt.md").read_text()
    with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as plugin_tmp:
        work = Path(tmp)
        plugin_dir = ROOT
        if arm == "standalone":
            plugin_dir = Path(plugin_tmp)
            build_standalone_plugin(skill, plugin_dir)
        if (scenario_dir / "repo").is_dir():
            shutil.copytree(scenario_dir / "repo", work, dirs_exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=work, check=True)
        before = snapshot(work)
        code, output = run_agent(arm, prompt, work, plugin_dir)
        changed, deleted = diff_snapshots(before, snapshot(work))
        files = [(p, (work / p).read_text(errors="replace")) for p in changed]

    parsed = parse_stream(output)
    out = results_dir / skill / scenario_dir.name / f"{arm}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    parts = [
        f"# {skill} / {scenario_dir.name} / {arm}",
        f"Model: {parsed['model'] or 'unknown'}\n"
        f"Exit code: {'timeout' if code is None else code}\n"
        f"Skills invoked: {', '.join(parsed['skills']) or 'none'}",
        "## Prompt", prompt.strip(),
        "## Reply", parsed["reply"],
        "## Files written",
    ]
    parts += [f"### {p.as_posix()}\n\n```\n{text}\n```" for p, text in files] or ["(none)"]
    parts += ["## Files deleted", "\n".join(f"- {p.as_posix()}" for p in deleted) or "(none)"]
    out.write_text("\n\n".join(parts) + "\n")
    return out, code == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run eval scenarios for one skill.")
    parser.add_argument("skill")
    parser.add_argument("--scenario")
    parser.add_argument("--arm", choices=["baseline", "skill", "both", "standalone"], default="both")
    parser.add_argument("--dry-run", action="store_true", help="print what would run")
    args = parser.parse_args(argv)

    evals_dir = ROOT / "evals" / args.skill
    scenarios = sorted(d for d in evals_dir.glob("*/") if (d / "prompt.md").is_file())
    if args.scenario:
        scenarios = [d for d in scenarios if d.name == args.scenario]
    if not scenarios:
        print(f"no scenarios found in {evals_dir}", file=sys.stderr)
        return 2
    if not args.dry_run and shutil.which("claude") is None:
        print("claude CLI not found on PATH", file=sys.stderr)
        return 2
    if "CLAUDE_CONFIG_DIR" not in os.environ:
        print("warning: CLAUDE_CONFIG_DIR is not set, so personal instructions may affect results",
              file=sys.stderr)

    arms = ["baseline", "skill"] if args.arm == "both" else [args.arm]
    failures = 0
    for scenario_dir in scenarios:
        for arm in arms:
            if args.dry_run:
                plugin_dir = Path(f"<temp plugin with only {args.skill}>") if arm == "standalone" else ROOT
                print(f"{scenario_dir.name} [{arm}]: {' '.join(agent_command(arm, plugin_dir))}")
                continue
            print(f"{scenario_dir.name} [{arm}] ... ", end="", flush=True)
            out, ok = run_scenario(args.skill, scenario_dir, arm)
            failures += not ok
            print(f"{out.relative_to(ROOT)}{'' if ok else '  (agent failed, see exit code)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
