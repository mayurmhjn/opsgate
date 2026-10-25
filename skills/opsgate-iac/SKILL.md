---
name: opsgate-iac
description: Use when writing, reviewing, refactoring, renaming or importing infrastructure as code (Terraform, OpenTofu, AWS CDK, CloudFormation, SAM, Pulumi), passing secrets or passwords into it, reading a plan or diff before apply or deciding whether it is safe to apply, setting up state and environments, or dealing with state locks, drift and imports.
---

# opsgate IaC

Use the tool the repo already uses. For a new project, compare tools against the team's skills and existing setup before choosing (see `opsgate-orchestrator`'s selection procedure if installed).

## New code

- **State is never optional.** Each environment gets its own state in a remote backend with locking and encryption, configured in the code you deliver. Don't leave the backend commented out for later. Use the backend's current native locking where the tool version supports it, and check the current docs instead of copying an older pattern.
- **Guard against the wrong account.** Tie each environment to its account, for example with `allowed_account_ids`, a per-environment role or profile, or separate accounts.
- **Pin versions** with constraints that stay within one major version, for the tool, every provider and every module source (registry `version`, or a git `ref`), and commit the dependency lock file. Look up current versions rather than using remembered ones.
- **Make unknowns required inputs.** Region, account, runtime and names you weren't given become variables without defaults, or are asked for. Tunables with a common convention (log retention, memory) may have defaults, labeled as starting points.
- **Protect stateful resources in code**, not just in your reply. Two different protections exist: one makes a delete fail (`prevent_destroy`, deletion protection, Pulumi `protect`), the other leaves the resource behind when it is removed or replaced (`RemovalPolicy.RETAIN`, `DeletionPolicy` and `UpdateReplacePolicy: Retain`). Retain does not stop a replacement. Add backups or point-in-time recovery too.
- **Build only what was asked.** Mention useful extras (alarms, extra policies) instead of adding them silently.

See `references/checklist.md` for the full list.

## Before any apply or deploy

Tell the user to run the full sequence and to review its output: format check, validate, lint and security scan, then a plan. Terraform and OpenTofu plan files and CloudFormation change sets can be applied exactly as reviewed. A `cdk diff` or `pulumi preview` is only advisory, because deploy computes the changes again. For an exact apply, deploy CDK through a reviewed change set (`cdk deploy --method=prepare-change-set`) or use Pulumi's saved update plans where available. In the review, read every replace and delete, and name the attribute that forces each one. A replaced database or bucket means data loss, or an orphaned copy if it was retained.

Before changing a stateful resource, check that backups or point-in-time recovery are on.

## Existing resources and state

- When a change is cosmetic (a rename for style), first offer the option that changes no infrastructure, such as keeping the resource or construct ID and renaming only the code.
- Adopt with `import` blocks, refactor with `moved` blocks, and stop managing a resource without deleting it with a `removed` block that keeps it (or the tool's equivalent). Continue until the plan shows no unintended changes.
- Don't change existing backend, version or provider settings while doing another task. Suggest those changes separately.
- Before importing, confirm the account and region the resource lives in. Take every value from the real resource (describe output or generated configuration). Leave out what you can't see rather than guessing it.
- `force-unlock`, `state rm`, `state mv` and `-target` need a stated reason and the user's yes. Never edit state by hand.
- Try experimental or unstable commands (for example, generated configuration or refactoring commands behind an unstable flag) on non-production first, and review their output before trusting it.

## When related skills are missing

Without `opsgate-orchestrator`, still never run apply, deploy, delete or destroy without the user's yes for that specific action, given after they have seen the reviewed plan. Blanket pre-approvals don't count. For production, state the rollback path first.
