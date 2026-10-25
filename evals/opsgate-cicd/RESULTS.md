# opsgate-cicd results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, with a configuration that has no personal instructions but adds a terse response style. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| terraform-auto-apply | 1/5 | 5/5 |
| rollback-bad-release | 2/4 | 4/4 |
| new-pipeline-ecs | 4/5 | 5/5 |
| pr-target-speedup | 4/4 | 4/4 |
| debug-tag-push | 3/3 | 3/3 |
| **Total** | **14/21** | **21/21** |

## What changed with the skill

- **terraform-auto-apply.** Without the skill, the agent built a blind apply on every push to main: plan and apply in the same job with nobody reading the plan, no plan on pull requests, and one role for everything. It warned about the risk, then built it anyway without asking. With the skill, pull requests get a plan from a read-only role, applies wait on a protected environment and plan again after approval, plan and apply use separate roles, and the agent asked before removing the approval. It also noted that dropping the environment changes the OIDC subject the apply role trusts.
- **rollback-bad-release.** Both arms redeployed the existing image and found the destructive migration. With the skill, the agent also asked for an explicit yes for each production step and gave a verification plan: health checks, error rate and latency, and a real checkout.
- **new-pipeline-ecs.** Without the skill, production approval was "optional" and action pinning was "if you want". With the skill, the production environment and pinned actions were the default, and the agent left clearly marked placeholders instead of guessing commit SHAs.
- **pr-target-speedup.** Both arms spotted the `pull_request_target` hole and the title injection. Without the skill, the delivered file still had the hole open while the agent waited for an answer. With the skill, the hole was closed in the delivered change and the speed work (dependency caching) was done too.

## Changes made during testing

The first with-skill run also scored 21/21, but a reviewer found problems the criteria didn't cover:

- The fix for `pull_request_target` moved the deploy into a `workflow_run` workflow that ran `npx` inside the untrusted build artifact, with the deploy token in the environment. That is artifact poisoning. The skill now treats untrusted artifacts as data that is never executed, and asks the agent to check its own fix for the same holes.
- The skill said to "set up" automated update PRs, and the agent added `dependabot.yml` files nobody asked for. It now says to recommend them and offer the config.
- One reply renamed a workflow, which can break required status checks. The skill now says to keep names stable.
- Concurrency was described as "deploys queue". With `cancel-in-progress: false`, GitHub never cancels a running deploy, but only one run waits, and a newer pending run replaces an older pending one. The wording was corrected.
- A plan file was uploaded as an artifact. On GitHub, anyone with read access to the repository can download artifacts, so the reference now prefers planning again after approval.
- The skill did not load for the failed-run scenario. Its description now mentions failed workflow runs and permission errors.

All five scenarios were re-run after these changes. `terraform-auto-apply` was re-run once more after the last reference fix.

## Known gaps

- One graded run per arm on the final skill text.
- The evals turn off shell access, so no workflow actually ran.
- The with-skill runs always had the whole plugin installed. No run tested the skill installed on its own.
- The grader noted two small slips in otherwise passing replies. A rollback reply took a backup cutoff time from a migration file name instead of the deploy time. A preview deploy step ran from the wrong directory.
