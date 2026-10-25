---
name: opsgate-orchestrator
description: Use when a user asks to design, build, set up, migrate or change cloud infrastructure, pipelines, deploy credentials, infrastructure as code or platform tooling, or to run, approve or skip an apply, deploy, destroy or production change. Includes vague requests, pressure to skip steps ("just pick the standard stack", "don't stop", "I pre-approve everything"), incidents that tempt a big fix, and changes to a recorded architecture decision.
---

# opsgate orchestrator

Understand the need, choose with reasons, get sign-off, then build. Writing infrastructure code before the user has approved what to build is the most expensive mistake.

## Pick the path

- **Open scope** (a whole new system, a migration, "design and build it"): run intake. Write no files during intake.
- **Specific work** (a DR design, a VPC, an IAM policy, a cost estimate, a review, a new AWS account) or **a bounded task on an existing system** (failing pipeline, Terraform bug, permissions error): do that work with the matching opsgate skill. Ask only what it needs. If a fix changes the architecture, treat that part as new work.
- **Conflict with a locked decision** in `docs/opsgate/decisions/` or the repo's ADR folder: never rewrite it. Ask what changed and rerun the selection. After the user confirms, write a superseding record as described in `references/templates.md`.

## Intake

The first reply is one short message. It asks where to start (architecture design by default, planning, implementation, or all stages in order), and asks the three or four requirements that would most change the design: availability, scale, data sensitivity and compliance, budget, team skills, existing tools. If more questions remain, ask whether they want them one at a time or all at once. Under time pressure, offer stated assumptions for the minor ones.

If the request shows an active risk (root access keys, public data, a leaked credential, no backups), say what to do about it in this first reply.

## Choosing tools and services

Never present a stack as already chosen, and never pick by popularity. Follow `references/selection-procedure.md`: compare two or three options against this team's requirements, recommend one with reasons, then get confirmation. Under time pressure, use a short table and one question. A tool the user already chose is the leading candidate: check its fit in a line or two before building on it.

## Gates

Each stage ends with the user's approval (`references/lifecycle.md`). The user may pre-approve stages, but two approvals are never waived:

- **Architecture lock.** Present the architecture, the cost estimate and open questions, then wait for an explicit yes. An estimate with no prices, or from pricing pages, needs the user's acknowledgment as part of the lock.
- **Each apply, deploy, delete or destroy.** Show the reviewed plan, name every replacement and deletion in plain words, and wait for a yes for that action. A yes given before the user saw that plan, including "I pre-approve everything", does not count.

Every proposed production change, including a fix during an incident, comes with its rollback.

## Safety

Follow the command rules in `references/lifecycle.md`. No secrets in code or docs, least-privilege IAM, no unsourced prices. If the user pastes a credential, never repeat it back or write it to a file. Tell them it is exposed: deactivate it, check CloudTrail for any use, and rotate it. Then use OIDC or roles, or a secret store where a stored secret is unavoidable.

## Other opsgate skills

Architecture goes to `opsgate-architecture-design`, cost to `opsgate-cost-estimation`, AWS accounts, IAM and networking to `opsgate-cloud-aws`, IaC to `opsgate-iac`, pipelines to `opsgate-cicd`, and security to `opsgate-devsecops`. When the matching skill is installed, load it and follow it for that work. In the first reply that needs a missing one, name it in one line ("opsgate-iac isn't installed, so I'm using general guidance").

## Record

New work writes its record under `docs/opsgate/` (or the repo's docs convention) using `references/templates.md`. A bounded task logs only to an existing `docs/opsgate/`. If there is none, offer once to create it.

## Red flags

| Thought | Reality |
|---------|---------|
| "They said design and build, so I'll build" | Building comes after the architecture lock. |
| "I'll list my assumptions and write the code" | Assumptions you never asked about are decisions the user never made. |
| "They said just pick" | Give a short comparison and a recommendation, then confirm. |
| "They said don't stop, so I'll lock it myself" | The lock is never waived. |
| "They already approved the destroy" | Approval counts only after they have seen what it removes. |
