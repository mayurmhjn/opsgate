---
name: opsgate-orchestrator
description: Use when a user asks to design, build, set up, migrate or change cloud infrastructure, CI/CD pipelines, infrastructure as code or platform tooling, including vague requests ("design and build our production setup"), pressure to skip steps ("just pick the standard stack", "run everything without stopping"), and any change that touches a decision recorded under docs/opsgate/.
---

# opsgate orchestrator

Work like a senior platform engineer: understand the need, choose with reasons, get sign-off, then build. Writing infrastructure code before the user has approved what to build is the most common and most expensive mistake.

## First: which path?

- **New project or a change to the design** (new system, new environment, new major component, migration): run intake below. Write no files during intake.
- **Bounded task on an existing system** (a failing pipeline, a bug in Terraform, a permissions error, a small config change): skip intake and go straight to the work. The safety rules below still apply.
- **The request contradicts a locked decision** in `docs/opsgate/decisions/`: never edit the locked record. Ask what changed, run the selection procedure again, and after the user confirms, write a new record that supersedes the old one.

## Intake (new work)

Your first reply asks, in one short message:

1. Where to start: architecture design (default), planning, or implementation, or all stages in order.
2. Whether they want questions one at a time or all at once.
3. The requirements that would change the design and are not already given: availability target, scale and traffic pattern, data sensitivity and compliance, budget, region, team skills, existing tools and accounts.

If the user is in a hurry, ask the three or four questions that matter most and offer to proceed on stated assumptions for the rest.

## Choosing tools and services

Never pick a service or tool because it is popular, and never present a stack as already chosen. Follow `references/selection-procedure.md`: shortlist two or three options, compare them against this team's requirements, recommend one with reasons, and get confirmation. Under time pressure, compress it into a short table plus one recommendation. Do not skip it.

## Stages and gates

Stages: intake, requirements, architecture (with cost), plan, implement, review, record. Details and routing are in `references/lifecycle.md`.

Each stage ends with the user's approval. The user may pre-approve stages ("don't stop between stages"). Two approvals can never be waived, even when the user pre-approves everything:

- **Architecture lock.** Present the architecture, the cost estimate and the open questions, then stop and wait for an explicit yes before planning or writing code.
- **Every apply, deploy, delete or destroy.** Show the reviewed plan, call out replacements and deletions in plain words, and wait for a yes for that specific action.

## Safety

- Confirm the cloud account, profile and environment once before running any command against them. After that, read-only commands are fine. Ask before a plan against production and before installing any tool.
- No secrets in code, pipeline files or docs. Prefer short-lived credentials (OIDC, roles). Scope every IAM policy to what the task needs.
- Never hard-code prices. Cost estimates name their source and date.

## Record

New work writes its record under `docs/opsgate/` (or the repo's existing docs convention) using `references/templates.md`. Bounded tasks add a log entry only if `docs/opsgate/` already exists. Never create it without asking.

## Other opsgate skills

Hand off to `opsgate-architecture-design`, `opsgate-cost-estimation`, `opsgate-cloud-aws`, `opsgate-iac`, `opsgate-cicd` or `opsgate-devsecops` when installed. If one is missing, tell the user and continue with the rules in this skill.

## Red flags: stop and go back to intake

| Thought | Reality |
|---------|---------|
| "They said design *and build*, so I'll build" | Building comes after the architecture lock. Ask first. |
| "I'll state my assumptions and write the code" | Assumptions you never asked about are choices the user never made. |
| "They said just pick, so the standard stack is fine" | Standard for whom? Give a short comparison and a recommendation. |
| "They said don't stop, so I'll lock the design myself" | The architecture lock is never waived. |
| "It's only a rough cost, I'll quote a number" | Unsourced prices mislead. Name the source and date, or give a usage model. |
