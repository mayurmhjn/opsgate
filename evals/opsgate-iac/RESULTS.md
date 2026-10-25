# opsgate-iac results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, with a configuration that has no personal instructions but adds a terse response style. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| new-service-two-envs | 2/5 | 5/5 |
| import-console-rds | 4/5 | 5/5 |
| cdk-construct-rename | 3/4 | 4/4 |
| password-in-tfvars | 4/4 | 4/4 |
| plan-hides-db-replacement | 4/4 | 4/4 (skill not loaded on one run) |
| rename-into-module | 4/4 | 4/4 |
| stuck-state-lock | 4/4 | 4/4 |
| **Total** | **25/30** | **30/30** |

## What changed with the skill

The model already handles most IaC safety well without help. It reads plans for forced replacements, uses `moved` and `import` blocks, refuses a blind `force-unlock`, keeps passwords out of variable files, and spots that a CDK construct rename replaces a table. The skill is kept small and covers only what was missing.

- **new-service-two-envs.** Without the skill, the remote backend was left commented out ("or the state stays local"). Version constraints spanned two major versions, the region and runtime were guessed as defaults, and only `init && plan` was suggested. With the skill, each environment had its own locked remote state, versions were pinned within one major, `allowed_account_ids` guarded against the wrong account, unknowns were required inputs, and the full format, validate and reviewed-plan sequence was given.
- **import-console-rds.** Both arms used an `import` block and generated configuration. With the skill, the agent also confirmed the account and region before importing and flagged that configuration generation is experimental.
- **cdk-construct-rename.** Both arms recommended keeping the construct IDs. With the skill, the agent also checked point-in-time recovery before any change.

## Changes made during testing

- The first version of the skill did worse than baseline in two places. It recommended an unstable CDK refactoring command directly against production, and it changed an existing backend and version constraint nobody asked about. Rules were added: offer the no-op option for cosmetic changes, try unstable commands outside production first, and leave existing backend and version settings alone.
- An import run wrote guessed values next to TODO comments. The skill now says to take imported values from the real resource and leave out anything unseen.
- `plan-hides-db-replacement` was rebuilt after a review found its fixture was wrong. It showed an RDS `identifier` change as forcing replacement, but current AWS provider versions rename the instance in place. The scenario now uses turning on `storage_encrypted`, which does force replacement. Both arms were re-run on the new fixture.
- `cdk-construct-rename` and `password-in-tfvars` were added after the first five scenarios turned out too easy to show the skill's value.
- A review found the skill treated a CDK diff or Pulumi preview as an exact plan, and treated retain policies as if they blocked deletion. Both were corrected, along with module version pinning and native tests. Two criteria were reworded to match the facts: a CDK table replacement orphans the old table rather than deleting it, and version pins must stay within one major version. Both arms were re-graded on them.

## Known gaps

- One graded run per arm. Every with-skill run above used the final skill text.
- The skill did not load in one `plan-hides-db-replacement` run, so its score partly reflects the model alone.
- The evals turn off shell access, so no plan, validate or import command was actually run.
- The test configuration adds a terse response style.
- The with-skill runs always had the whole plugin installed. No run tested the skill installed on its own.
