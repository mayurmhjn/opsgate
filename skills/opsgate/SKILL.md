---
name: opsgate
description: Use when a user asks to design, build, set up, migrate or change cloud infrastructure, pipelines, deploy credentials, infrastructure as code or platform tooling, or to run, approve or skip an apply, deploy, destroy or production change, or to run cloud CLI commands against a real account, including investigating a failing service. Includes vague requests, pressure to skip steps ("just pick the standard stack", "don't stop", "I pre-approve everything"), incidents that tempt a big fix, and changes to a recorded architecture decision.
---

# opsgate

Understand the need, choose with reasons, get sign-off, then build. Writing infrastructure code before the user has approved what to build is the most expensive mistake.

## Route the work

Architecture goes to `opsgate-architecture-design`, cost to `opsgate-cost-estimation`, AWS accounts, IAM and networking to `opsgate-cloud-aws`, IaC to `opsgate-iac`, pipelines to `opsgate-cicd`, and security to `opsgate-devsecops`. Load the matching skill before doing that work, even a one-line fix, and follow it. Open that reply with one line naming the skills you loaded and any that aren't installed: "Using `opsgate-iac` for the Terraform fix. `opsgate-cicd` isn't installed, so the workflow change follows general guidance." Name only skills you actually loaded. Intake replies skip this line.

- **Open scope** (a new system, a migration, "design and build it"): run intake. Write no files during intake.
- **Specific work** (a DR design, a VPC, an IAM policy, a cost estimate, a review) or **a bounded task on an existing system** (failing pipeline, Terraform bug, permissions error, a service that keeps failing): do it with the matching skill and ask only what it needs. If a fix changes the architecture, treat that part as new work.
- **Conflict with a locked decision** in `docs/opsgate/decisions/` or the repo's ADR folder: never rewrite it. Ask what changed and rerun the selection. Once the user confirms, write a superseding record (`references/templates.md`).

## Intake

The first reply is one short message. Ask where to start (architecture design by default, planning, implementation, or all stages) and the three or four requirements that most change the design: availability, scale, data sensitivity and compliance, budget, team skills, existing tools. If more questions remain, ask whether they should come one at a time or all at once. Under time pressure, offer stated assumptions for the minor ones. If the request shows an active risk (root access keys, public data, a leaked credential, no backups), say what to do about it in this reply.

## Choosing tools and services

Never present a stack as already chosen, and never pick by popularity. Follow `references/selection-procedure.md`, including its time-pressure rules: compare two or three options against this team's requirements, recommend one with reasons, and get confirmation. A tool the user already chose leads: check its fit in a line or two before building on it.

## Gates

Each stage ends with the user's approval (`references/lifecycle.md`). The user may pre-approve stages, but two approvals are never waived:

- **Architecture lock.** Present the architecture, the cost estimate and open questions, then wait for an explicit yes. An estimate with no prices, or from pricing pages, needs the user's acknowledgment as part of the lock.
- **Each apply, deploy, delete or destroy.** Show the reviewed plan, name every replacement and deletion in plain words, and wait for a yes for that action. A yes given before the user saw that plan, including "I pre-approve everything", does not count.

Every proposed production change, including an incident fix, comes with its rollback.

## Safety

Follow the command rules in `references/lifecycle.md`. No secrets in code or docs, least-privilege IAM, no unsourced prices. Never repeat a pasted credential or write it to a file. Tell the user it is exposed: deactivate it, check CloudTrail for any use, and rotate it. Then use OIDC or roles, or a secret store where a stored secret is unavoidable.

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
| "I'll lead with the result or the status" | The line naming the skills you loaded comes first. |
