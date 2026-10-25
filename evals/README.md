# Evals

Each skill is tested by running realistic requests through an agent twice: once without the skill (the baseline) and once with it. A skill earns its place when the second run follows the behavior the first run misses.

## Layout

```
evals/<skill>/<scenario>/
  prompt.md      the request, written the way a user would type it
  criteria.md    what a passing reply does, one checkable line each
  repo/          optional files copied into the working directory first
evals/<skill>/RESULTS.md   latest graded results for that skill
```

The lint script fails if a skill has no scenario with both `prompt.md` and `criteria.md`.

## Writing a scenario

- Write the prompt as a real request. Don't hint at the behavior you want to see.
- Add pressure where real users apply it: "just pick the standard stack", "we need this today", "don't stop between stages".
- Keep criteria to three to five lines, each one something a reader can check against the reply as pass or fail.
- Put any existing project state (workflows, Terraform, decision records) under `repo/`.

## Running

The runner uses the Claude Code CLI in headless mode. Run it with a clean configuration so your own instructions and installed skills don't change the result:

```bash
mkdir -p ~/.opsgate-eval-config
ln -sf ~/.claude/.credentials.json ~/.opsgate-eval-config/.credentials.json
CLAUDE_CONFIG_DIR=~/.opsgate-eval-config .venv/bin/python evals/run.py opsgate-orchestrator
```

The symlink works where the CLI stores its login in `~/.claude/.credentials.json`, as it does on Linux. On macOS the login lives in the Keychain, so set `ANTHROPIC_API_KEY` for the run instead.

Options: `--scenario NAME` runs one scenario, `--arm baseline` or `--arm skill` runs one side, and `--dry-run` prints the commands without running them.

The agent can read and write files in a temporary copy of `repo/`, but it can't run shell commands. With the clean configuration above, that means nothing touches a real cloud account. Results land in `evals/results/<skill>/<scenario>/<arm>.md`, which git ignores. Each one records the model, the exit code, which skills the agent invoked, the prompt, the reply, and every file the agent created, changed or deleted.

## Grading

Read each result against `criteria.md` and mark every line pass or fail. Record the totals and any notable failures in the skill's `RESULTS.md`. Grading is done by hand for now, because automated scoring tends to miscount quoted examples as real behavior.
