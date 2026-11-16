---
name: opsgate-cicd
description: Use when creating, changing, speeding up or debugging CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, AWS CodePipeline and similar), including a failed workflow run, a flaky test or a permission error in a job, setting up deploys or GitOps sync (Argo CD, Flux) or infrastructure-as-code pipelines, choosing a release strategy, or rolling back a bad release.
---

# opsgate CI/CD

Use the CI system the repo already uses. For a new project, compare options against the team's setup before choosing (with the `opsgate` skill's selection procedure if installed). Pipeline changes ship to everyone who touches the repo, so they follow the same review rules as production code. List every behavior change you make, including steps you removed or replaced. For systems other than GitHub Actions, see `references/other-ci.md`.

## Production deploys are gated

- Deploy to production through a protected environment with required reviewers. On GitHub Free, Pro and Team plans, required reviewers work only in public repositories, so check the plan and say when the environment gives no approval gate (`references/github-actions-hardening.md`). Roles that deploy to production trust only that environment. Concurrency must never cancel a running deploy. Treat these as required, not optional.
- Build once and promote the same artifact through each environment, ending every deploy with a verify step (`references/release-rollback.md`). A new artifact reaches production only after it has deployed to the environment before it (usually staging) and passed its verify step. Earlier environments may run in parallel, and a rollback to a known-good artifact doesn't go through them again. If asked to deploy production in parallel with staging, offer faster options that keep this order (caching, faster slow steps), and ask before removing it.
- For deploys over SSH, pin the server's host key: never `StrictHostKeyChecking=no` or an unchecked `ssh-keyscan`. Prefer AWS Systems Manager Run Command through an OIDC role scoped to that instance and command over a long-lived key, and wait for the command's result, or else a dedicated deploy user limited to the deploy. Check health after the deploy, and keep the previous release to switch back to.
- When the pipeline itself is defined in CloudFormation, CDK or Terraform, don't update it yourself. Give the change, and tell the user to review the change set or plan before deploying it.
- With GitOps sync (Argo CD, Flux), automated prune deletes live resources that disappear from git, so a bad commit, a moved path or a rename deletes them. Before turning prune on for production, protect stateful resources from pruning (Argo CD sync option `Prune=false`, Flux annotation `kustomize.toolkit.fluxcd.io/prune: disabled`), and don't set Argo CD `allowEmpty` on a production app. Argo CD self-heal and Flux reconciliation revert manual fixes, so an incident fix goes through git, or sync for that app is paused first (turn off Argo CD automated sync, or `flux suspend kustomization`). The production approval is then a required review on the branch production syncs from.
- A scheduled job that deletes in bulk, such as a sweep of old preview environments, only lists what it would delete until the user has reviewed that list.
- If the user wants deploys or applies to happen "automatically", explain what is lost, offer a middle ground (automatic for non-production, one approval for production), and ask before removing the approval.

## Infrastructure pipelines

Follow `references/iac-pipelines.md`. Plan on every pull request for review only. After merge, a trusted run plans again, reviewers approve that plan, and the apply job applies exactly the approved plan. Use a read-only role for plan and a separate scoped role for apply.

## Supply chain and permissions

- Pin third-party actions to a full commit SHA, with the version in a comment. This is the default, not an extra. Never guess a SHA or version: look them up, or leave a clearly marked placeholder and give the command that resolves it. To resolve a tag, run `git ls-remote https://github.com/OWNER/ACTION 'refs/tags/vX.Y.Z' 'refs/tags/vX.Y.Z^{}'`. For an annotated tag, use the commit SHA on the line ending in `^{}`. For a lightweight tag, only the plain line comes back, and that SHA is the commit. Recommend automated update PRs and offer to add the config.
- Deploy images by digest, or by a tag the registry keeps immutable.
- Keep workflow and job names stable. Renaming them can break required status checks.
- Keep `permissions` minimal and grant write access per job. Store role ARNs and other non-secret settings as variables, not secrets.
- Keep self-hosted runners off public repositories, and make any self-hosted runner ephemeral or just-in-time (`references/github-actions-hardening.md`).

See `references/github-actions-hardening.md` for the full list.

## Security holes you find

This is an exception to fixing only what was asked. If a workflow you are already editing has a live hole, such as `pull_request_target` running untrusted PR code with secrets, untrusted input used directly in `run`, or a privileged job that executes files from an untrusted artifact or runs tools with the artifact as its working directory, close it in the change you deliver. Check your own fix for the same holes. If the hole was reachable, name the secrets and tokens it exposed, recommend rotating them, and suggest checking past runs triggered from forks. Then do what was asked.

## Debugging a failed run

1. Read the first error in the log, not the last one.
2. Compare with the last successful run: workflow changes, action and dependency versions, runner image, expired secrets.
3. Decide whether it is flaky or deterministic. Re-run once with debug logging if unsure.
4. For permission errors, compare the job's `permissions` and the token's subject with the cloud role's trust policy. The repository or organization token setting is only a default, and a job's `permissions` key can raise it (fork pull requests excepted).
5. Fix the root cause with the smallest scoped change, and say what you changed and why.

For a flaky test, don't add a retry to the whole job or suite: it lets new intermittent failures in every other test pass unnoticed. Quarantine the known flaky test where people can see it (skipped with a reason, or moved to a job that doesn't block merges) with an issue and an owner, keep the rest blocking, and look for the cause in the test, such as a fixed sleep instead of waiting for the condition.

Re-running a failed production deploy is a deploy, and needs a yes.

## Rollback

Follow `references/release-rollback.md`: redeploy the last known-good artifact rather than rebuilding, pause automatic deploys, check migrations and other changes, back up before any database change, wait for an explicit yes, and verify afterwards.

## When related skills are missing

Without the `opsgate` skill, still never run an apply, deploy, delete, destroy or rollback, in any environment, without the user's yes for that specific action, given after they have seen the reviewed plan. Blanket pre-approvals don't count. For production, state the rollback path first. The same applies to commands that change a shared or deployed system, such as a reboot, restart, failover, scaling, or ending sessions or queries: say what the action will do, then wait for a yes.
