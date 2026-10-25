# Contributing to opsgate

Thanks for helping. These rules keep the skills consistent and useful across different agents.

## Skill layout

Each skill lives in its own folder under `skills/`, named `opsgate-<area>`:

```
skills/opsgate-<area>/
  SKILL.md        required: frontmatter with name and description, then the instructions
  references/     optional: checklists, templates and examples the skill loads when needed
```

The `name` in the frontmatter must match the folder name.

## Writing a skill

- Keep `SKILL.md` short. Move checklists, templates and long examples into `references/` so they load only when the task needs them.
- Write instructions any agent can follow ("ask the user", "run the command"). Do not name tools that exist in only one agent.
- Make each skill work when it is installed alone. If it relies on another opsgate skill, say what to do when that skill is missing.
- Do not hard-code prices, service quotas or tool versions. They go stale. Tell the agent where to look them up instead.
- When a skill picks a tool or service, it must follow the selection procedure: collect the requirements, compare two or three candidates, recommend one with reasons, and get the user's confirmation. A tool is never picked just because it is common.
- Destructive or production-affecting actions always need the user's explicit approval.
- When you change a skill, bump `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`. Plugin users only get the update after the version changes. The lint script checks that the two files match.

## Evals

Every new or changed skill needs eval scenarios in `evals/`. See [evals/README.md](evals/README.md) for the format and how to run them.

## Checks before a pull request

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/lint.py
```

The lint script validates every skill against the Agent Skills format, checks the name prefix, and confirms the plugin manifests agree with each other. CI runs the same checks on every pull request.
