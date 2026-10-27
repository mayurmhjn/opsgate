"""Check skill folders, their evals and plugin manifests before a release.

Usage: python scripts/lint.py [repo-root]
"""

import json
import sys
from pathlib import Path

from skills_ref import read_properties, validate

ROUTER = "opsgate"
PREFIX = ROUTER + "-"


def lint_skills(root):
    problems = []
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return problems, []
    names = []
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        rel = f"skills/{skill_dir.name}"
        if not (skill_dir / "SKILL.md").is_file():
            problems.append(f"{rel}: missing SKILL.md")
            continue
        names.append(skill_dir.name)
        errors = validate(skill_dir)
        problems += [f"{rel}: {e}" for e in errors]
        name = None if errors else read_properties(skill_dir).name
        if name is not None and name != ROUTER and not name.startswith(PREFIX):
            problems.append(f"{rel}: name must be {ROUTER} or start with {PREFIX}")
    return problems, names


def lint_evals(root, skill_names):
    problems = []
    for name in skill_names:
        evals_dir = root / "evals" / name
        if not any((d / "prompt.md").is_file() and (d / "criteria.md").is_file() for d in evals_dir.glob("*/")):
            problems.append(f"evals/{name}: needs at least one scenario with prompt.md and criteria.md")
    return problems


def lint_manifests(root):
    plugin_dir = root / ".claude-plugin"
    if not plugin_dir.is_dir():
        return []
    problems = []
    data = {}
    for name in ("marketplace.json", "plugin.json"):
        try:
            data[name] = json.loads((plugin_dir / name).read_text())
        except (OSError, json.JSONDecodeError) as e:
            problems.append(f".claude-plugin/{name}: invalid JSON: {e}")
    if problems:
        return problems
    listed = (data["marketplace.json"].get("plugins") or [{}])[0]
    for field in ("name", "version"):
        if listed.get(field) != data["plugin.json"].get(field):
            problems.append(f".claude-plugin: marketplace and plugin.json disagree on {field}")
    return problems


def lint(root):
    problems, names = lint_skills(root)
    return problems + lint_evals(root, names) + lint_manifests(root)


def main(argv=None):
    root = Path(argv[0]) if argv else Path.cwd()
    problems = lint(root)
    for p in problems:
        print(p)
    print(f"{len(lint_skills(root)[1])} skills checked")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
