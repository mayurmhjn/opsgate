---
name: opsgate-iac
description: Use when writing, reviewing, refactoring, renaming or importing infrastructure as code (Terraform, OpenTofu, AWS CDK, CloudFormation, SAM, Pulumi), passing secrets or passwords into it, reading a plan or diff before apply, setting up state and environments, or dealing with state locks, drift and imports.
---

# opsgate IaC

Use the tool the repo already uses. For a new project, compare tools against the team's skills and existing setup before choosing (see `opsgate-orchestrator`'s selection procedure if installed).

## New code

- **State is never optional.** Each environment gets its own state in a remote backend with locking and encryption, configured in the code you deliver. Don't leave the backend commented out for later. Use the backend's current native locking where the tool version supports it, and check the current docs instead of copying an older pattern.
- **Guard against the wrong account.** Tie each environment to its account, for example with `allowed_account_ids`, a per-environment role or profile, or separate accounts.
- **Pin versions** with constraints that stay within one major version, for the tool and every provider, and commit the dependency lock file. Look up current versions rather than using remembered ones.
- **Make unknowns required inputs.** Region, account, runtime and names you weren't given become variables without defaults, or are asked for. Tunables with a common convention (log retention, memory) may have defaults, labeled as starting points.
- **Protect stateful resources in code**, not just in your reply: `prevent_destroy` or `RemovalPolicy.RETAIN`, deletion protection, backups or point-in-time recovery.
- **Build only what was asked.** Mention useful extras (alarms, extra policies) instead of adding them silently.

See `references/checklist.md` for the full list.

## Before any apply or deploy

Tell the user to run the full sequence and to review its output: format check, validate, lint and security scan, then a saved plan (`terraform plan -out`, a CloudFormation change set, `cdk diff`, `pulumi preview`). They then apply that exact plan. In the review, read every replace and delete, and name the attribute that forces each one. A replaced database or bucket means data loss unless it is restored.

Before changing a stateful resource, check that backups or point-in-time recovery are on.

## Existing resources and state

- When a change is cosmetic (a rename for style), first offer the option that changes no infrastructure, such as keeping the resource or construct ID and renaming only the code.
- Adopt with `import` blocks, and refactor with `moved` blocks (or the tool's equivalent), until the plan shows no unintended changes.
- Don't change existing backend, version or provider settings while doing another task. Suggest those changes separately.
- Before importing, confirm the account and region the resource lives in. Take every value from the real resource (describe output or generated configuration). Leave out what you can't see rather than guessing it.
- `force-unlock`, `state rm`, `state mv` and `-target` need a stated reason and the user's yes. Never edit state by hand.
- Try experimental or unstable commands (for example, generated configuration or refactoring commands behind an unstable flag) on non-production first, and review their output before trusting it.

## When related skills are missing

Without `opsgate-orchestrator`, still never run apply, deploy or destroy without the user's yes, given after they have seen the reviewed plan.
