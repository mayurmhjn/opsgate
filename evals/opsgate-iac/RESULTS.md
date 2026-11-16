# opsgate-iac results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, with a configuration that has no personal instructions but adds a terse response style. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| new-service-two-envs | 2/5 | 5/5 |
| import-console-rds | 4/5 | 5/5 |
| cdk-construct-rename | 3/4 | 4/4 |
| password-in-tfvars | 4/4 | 4/4 |
| plan-hides-db-replacement | 4/4 | 4/4 (the skill did not load in an earlier run of this scenario) |
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

## Account check before commands (2026-10-27)

The skill used to confirm the account only before an import. In the `opsgate` shell scenario for a production plan, a run with this skill loaded went straight to `terraform plan`. It now confirms the account and region before plan, import or any other command against an account, with `aws sts get-caller-identity` as its own command or by asking. Two shell runs then checked the account first, and a regression run of `plan-hides-db-replacement` still flagged the database replacement as a blocker (only that line was re-checked).

## Installed on its own

On 2026-10-27, `plan-hides-db-replacement` was run with only this skill installed (`--arm standalone`). It scored 4/4. It refused to apply, gave a safe path for the encryption change, and stated a rollback, which is what the skill's rule for a missing `opsgate` skill asks for. Compared with the full-plugin run, it did not mention that the database endpoint changes, and it gave no rollback for the encryption migration itself.

## Removing an item from a count list (2026-11-07)

Run on 2026-11-07 with Claude Code 2.1.319 (model `claude-opus-5-5`). From this date the eval configuration turns off account plugin sync, so account plugins no longer load in either arm; earlier runs had them. The scenario came from a gap review against the devops-exercises repository. One graded run per arm. Before the with-skill run, a grader flagged unclear criteria wording; the reworded criteria were used for both arms. Other scenarios in this file were not re-run on the new text, except the regression runs named below. The with-skill run came before a later edit that added the running-system rule to this skill's fallback for when `opsgate` is not installed.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| remove-queue-from-count-list | 3/4 | 4/4 |

Both arms saw that removing a middle item from a `count` list replaces the queues after it, and both wrote `for_each` with `moved` blocks. Only the skill arm said to check that the queue being deleted is empty. The skill now says to check that a stateful resource is empty or unused before deleting it. Regression runs of `plan-hides-db-replacement` and `stuck-state-lock` kept 4/4.

One criterion first said "switches the resource"; it now accepts writing or showing the change in full, because the baseline stopped to ask before editing.

## Known gaps

- One graded run per arm. Every with-skill run above used the final skill text.
- The skill did not load in an earlier `plan-hides-db-replacement` run, which shows triggering can vary. The graded run above loaded it.
- The evals turn off shell access, so no plan, validate or import command was actually run.
- The test configuration adds a terse response style.
- Only one scenario was run with the skill installed on its own.

## A plan with changes nobody made (2026-11-16)

Run on 2026-11-16 with Claude Code (model `claude-opus-5-5`), with account plugin sync turned off. The scenario came from a gap review against public DevOps best-practice guides: a pull request bumps one Lambda's memory, but the production plan also shrinks the database and removes a security group rule that someone added outside the code.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| plan-shows-unmade-changes | 6/6, 6/6 | 6/6 |

Both arms refused to apply, named both extra changes and their risk, called them drift or a stale branch, and said to find out who made them before applying. The baseline already handles this, so no rule was added and the scenario stays as a regression check. One baseline reply suggested `terraform import` or a refresh to fix the drift. That doesn't help: both resources are already in state, and the next plan would still revert them.

After the baseline runs, a grader found one criterion that bundled three checks. It was split into three lines, and all runs above were graded on the split version.

## Terraform traps (2026-11-16)

Run on 2026-11-16 with Claude Code (model `claude-opus-5-5`), with account plugin sync turned off. The scenarios came from a gap review against public DevOps guides and the devops-exercises repository. Two baseline runs per scenario and one with-skill run, with more runs for the scenario that led to a rule.

| Scenario | Without skills | With skills | This skill alone |
|----------|----------------|-------------|------------------|
| userdata-change-running | 4/4, 4/4 | 4/4 | |
| module-with-provider | 4/4, 4/4 | 4/4 | |
| workspaces-for-prod | 2/4, 1/4 | 4/4, 4/4 | 4/4 |
| local-state-to-s3 | 4/4, 4/4 | 4/4 | |
| ec2-keypair-in-terraform | 4/5, 5/5 | 5/5 | |
| sg-description-replace | 4/4, 4/4 | 4/4 | |

Without the skill, the agent already knew that changing `user_data` stops and starts the instance without running the new script, that a reusable module can't hold a provider block, how to move local state to S3 with `use_lockfile`, that `tls_private_key` puts the key in state, and that a security group whose description changes is replaced and can't be deleted while in use. No rules were added for these; the scenarios stay as regression checks.

Workspaces were the gap. Asked to use workspaces with prod in its own account, both baseline runs built prod as a workspace in the dev state bucket and offered a separate setup only as an option. The skill now says CLI workspaces share one backend and its credentials, so production gets its own root module or backend and role, and that the agent should recommend this and ask before building a prod workspace. With the skill, every run recommended separating prod and asked before writing it.

Regression runs of `plan-hides-db-replacement` and `remove-queue-from-count-list` kept 4/4. After a final review, two criteria were worded more precisely (workspaces share backend credentials; the key pair alternatives are examples). No grade changed.

### Changes made during testing

After the baseline runs, a grader found that the module criterion rejected the resource-level `region` argument from AWS provider 6, which is a valid answer, and that the workspace and key pair criteria bundled several checks. They were reworded before the with-skill runs, and the baseline runs were graded again on the final criteria.

### Known gaps

- The with-skill module reply went beyond the request (versioning, `prevent_destroy`, a name check). Its code comment said a `removed` block can drop a single `for_each` key, which its own README correctly contradicts.
- The state migration fixture uses `var.db_password` without declaring it. Both baseline replies added the declaration; the with-skill reply didn't, so its "plan shows no changes" check can't run as delivered.
- The workspace runs with the skill proposed `allowed_account_ids` per environment but didn't write it, because they stopped to ask first.

## Deleting a bucket that DNS still points at (2026-11-16)

Run on 2026-11-16, same setup as the section above.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| dns-teardown | 3/4, 4/4 | 4/4 |

Both arms noticed that the platform team's Route 53 record still points at the website bucket, warned that anyone could create a bucket with the same name and serve content on the subdomain, and removed the record first. One baseline run gave the steps without saying the destroy needs the user's go-ahead. No rule was added. Two criteria were reworded after the baseline runs because the user asked for steps, not edits; the baseline runs were graded again on the final wording.
