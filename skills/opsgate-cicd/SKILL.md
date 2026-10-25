---
name: opsgate-cicd
description: Use when creating, changing, speeding up or debugging CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, AWS CodePipeline and similar), setting up deploys or infrastructure-as-code pipelines, choosing a release strategy, or rolling back a bad release.
---

# opsgate CI/CD

Use the CI system the repo already uses. Pipeline changes ship to everyone who touches the repo, so they follow the same review rules as production code.

## Production deploys are gated

- Deploy to production through a protected environment with required reviewers and a branch rule that allows only the release branch. Concurrency for production deploys must queue rather than cancel. Treat these as required, not optional.
- If the user wants deploys or applies to happen "automatically", explain what is lost, offer a middle ground (automatic for non-production, one approval for production), and ask before removing the approval.

## Infrastructure pipelines

Follow `references/iac-pipelines.md`: plan on every pull request with the plan visible to reviewers, then apply only that reviewed plan after approval. Use a read-only role for plan and a separate scoped role for apply. Don't add manual triggers that can apply production from any branch.

## Supply chain and permissions

- Pin third-party actions and images to a full commit SHA or digest, with the version in a comment, and set up automated update PRs. This is the default, not an extra.
- Keep `permissions` minimal and grant write access per job.
- Turn on tag immutability in the image registry so an image tag can't be overwritten.
- Store role ARNs and other non-secret settings as variables, not secrets.

See `references/github-actions-hardening.md` for the full list.

## Security holes you find

If a workflow you touch has a live hole, such as `pull_request_target` running untrusted PR code with secrets, or untrusted input used directly in `run`, close it in the change you deliver. Do this even if the user asked for something else. Don't ship the file with the hole still open while you wait for an answer. Then do what they asked.

## Debugging a failed run

Read the log and find the step and the error before changing anything. Fix the root cause with the smallest scoped change, and say what you changed and why.

## Rollback

Follow `references/release-rollback.md`:

1. Redeploy the last known-good artifact. Don't rebuild old source.
2. Check what the bad release changed outside the artifact, such as database migrations, config and feature flags.
3. Take a backup before any database change.
4. Give the exact command, and wait for an explicit yes before running anything in production.
5. Verify afterwards: service health, error rates, and the broken user flow.

## When related skills are missing

Without `opsgate-orchestrator`, still never run a production deploy, apply or rollback without the user's yes for that specific action, given after they have seen what it will do.
