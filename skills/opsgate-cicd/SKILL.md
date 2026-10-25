---
name: opsgate-cicd
description: Use when creating, changing, speeding up or debugging CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, AWS CodePipeline and similar), including a failed workflow run or a permission error in a job, setting up deploys or infrastructure-as-code pipelines, choosing a release strategy, or rolling back a bad release.
---

# opsgate CI/CD

Use the CI system the repo already uses. For a new project, compare options against the team's setup before choosing (with `opsgate-orchestrator`'s selection procedure if installed). Pipeline changes ship to everyone who touches the repo, so they follow the same review rules as production code. List every behavior change you make, including steps you removed or replaced. For systems other than GitHub Actions, see `references/other-ci.md`.

## Production deploys are gated

- Deploy to production through a protected environment with required reviewers. Roles that deploy to production trust only that environment. Concurrency must never cancel a running deploy. Treat these as required, not optional.
- Build once and promote the same artifact through each environment, ending every deploy with a verify step (`references/release-rollback.md`).
- If the user wants deploys or applies to happen "automatically", explain what is lost, offer a middle ground (automatic for non-production, one approval for production), and ask before removing the approval.

## Infrastructure pipelines

Follow `references/iac-pipelines.md`. Plan on every pull request for review only. After merge, a trusted run plans again, reviewers approve that plan, and the apply job applies exactly the approved plan. Use a read-only role for plan and a separate scoped role for apply.

## Supply chain and permissions

- Pin third-party actions to a full commit SHA, with the version in a comment. This is the default, not an extra. Never guess a SHA or version: look them up, or leave a clearly marked placeholder and give the command that resolves it. To resolve a tag, run `git ls-remote https://github.com/OWNER/ACTION 'refs/tags/vX.Y.Z' 'refs/tags/vX.Y.Z^{}'`. For an annotated tag, use the commit SHA on the line ending in `^{}`. For a lightweight tag, only the plain line comes back, and that SHA is the commit. Recommend automated update PRs and offer to add the config.
- Deploy images by digest, or by a tag the registry keeps immutable.
- Keep workflow and job names stable. Renaming them can break required status checks.
- Keep `permissions` minimal and grant write access per job. Store role ARNs and other non-secret settings as variables, not secrets.

See `references/github-actions-hardening.md` for the full list.

## Security holes you find

This is an exception to fixing only what was asked. If a workflow you are already editing has a live hole, such as `pull_request_target` running untrusted PR code with secrets, untrusted input used directly in `run`, or a privileged job that executes files from an untrusted artifact or runs tools with the artifact as its working directory, close it in the change you deliver. Check your own fix for the same holes. If the hole was reachable, name the secrets and tokens it exposed, recommend rotating them, and suggest checking past runs triggered from forks. Then do what was asked.

## Debugging a failed run

1. Read the first error in the log, not the last one.
2. Compare with the last successful run: workflow changes, action and dependency versions, runner image, expired secrets.
3. Decide whether it is flaky or deterministic. Re-run once with debug logging if unsure.
4. For permission errors, compare the job's `permissions` and the token's subject with the cloud role's trust policy. The repository or organization token setting is only a default, and a job's `permissions` key can raise it (fork pull requests excepted).
5. Fix the root cause with the smallest scoped change, and say what you changed and why.

Re-running a failed production deploy is a deploy, and needs a yes.

## Rollback

Follow `references/release-rollback.md`: redeploy the last known-good artifact rather than rebuilding, pause automatic deploys, check migrations and other changes, back up before any database change, wait for an explicit yes, and verify afterwards.

## When related skills are missing

Without `opsgate-orchestrator`, still never run a production deploy, apply or rollback without the user's yes for that specific action, given after they have seen what it will do.
