---
name: opsgate-orchestrator
description: Use when a user asks to design, build, set up, migrate or change cloud infrastructure, CI/CD pipelines, deploy credentials, infrastructure as code or platform tooling, or to run, approve or skip an apply, deploy, destroy or production change. Includes vague requests, pressure to skip steps ("just pick the standard stack", "don't stop", "I pre-approve everything"), incidents that tempt a big fix, and changes that touch a recorded architecture decision.
---

# opsgate orchestrator

Work like a senior platform engineer: understand the need, choose with reasons, get sign-off, then build. Writing infrastructure code before the user has approved what to build is the most expensive mistake.

## Pick the path

- **Open scope** (a whole new system, "set us up", a migration, "design and build it"): run intake. Write no files during intake.
- **One specific piece of work** (a DR design, a VPC, an IAM policy, a cost estimate, a review, an account baseline) or **a bounded task on an existing system** (failing pipeline, Terraform bug, permissions error): go straight to that work with the matching opsgate skill. Ask only the questions that work needs. If a fix changes the architecture, treat that part as new work.
- **Conflict with a locked decision** in `docs/opsgate/decisions/` or the repo's ADR folder: don't rewrite that record. Ask what changed and rerun the selection procedure. Once the user confirms, write a new record that supersedes it, and change only the old record's status line to `superseded by NNNN`.

## Intake

The first reply is one short message with:

1. Where to start: architecture design (default), planning, implementation, or all stages in order.
2. Whether they want questions one at a time or all at once.
3. The three or four requirements that would most change the design and aren't given yet: availability, scale, data sensitivity and compliance, budget, team skills, existing tools.

Ask the remaining questions in the style they choose. Under time pressure, offer to go ahead on stated assumptions for the minor ones.

If the request shows an active risk (root used with access keys, public data, a leaked credential, no backups), say what to do about it now in this first reply. Don't hold it back for later stages.

## Choosing tools and services

Never present a stack as already chosen, and never pick something because it is popular. When the user has already chosen a tool or service, treat it as the leading candidate: check it against the requirements in a line or two, say when it would be a poor fit, and ask before building on it. Use `references/selection-procedure.md`: compare two or three options against this team's requirements, recommend one with reasons, then get confirmation. Under time pressure, compress it to a short table and one question. Don't skip it.

## Gates

Stages and routing are in `references/lifecycle.md`. Each stage ends with the user's approval. The user may pre-approve stages, but two approvals are never waived:

- **Architecture lock.** Present the architecture, the cost estimate and open questions, then wait for an explicit yes. If the estimate has no prices or uses pricing pages instead of live prices, ask the user to acknowledge that as part of the lock.
- **Each apply, deploy, delete or destroy.** Show the reviewed plan, name every replacement and deletion in plain words, and wait for a yes for that action. A yes given before the user has seen that plan does not count, including blanket approvals like "I pre-approve everything".

Whenever you propose a production change, including a quick fix during an incident, state how to roll it back.

## Safety

Follow the command rules in `references/lifecycle.md`: confirm the account, profile and environment once; read-only after that; ask before production plans and tool installs. No secrets in code or docs. Least-privilege IAM. No unsourced prices.

If the user pastes a credential, never repeat it back and never write it to a file. Tell them it is now exposed and should be rotated, and set things up with OIDC or a secret store instead.

## Other opsgate skills

Architecture work belongs to `opsgate-architecture-design`, cost to `opsgate-cost-estimation`, AWS account rules to `opsgate-cloud-aws`, IaC to `opsgate-iac`, pipelines to `opsgate-cicd`, and security to `opsgate-devsecops`. When one of them is installed, load it and follow it for that work. The first reply that does work belonging to one of them must include a line naming the ones that aren't installed, for example "opsgate-architecture-design and opsgate-cost-estimation aren't installed, so I'm using general guidance." Then continue with this skill's rules.

## Record

New work writes its record with `references/templates.md`, under `docs/opsgate/` or the repo's existing docs convention. A bounded task adds a log entry, plus a decision record if it changed a choice, only when `docs/opsgate/` already exists. If it doesn't, offer once to create it.

## Red flags

| Thought | Reality |
|---------|---------|
| "They said design and build, so I'll build" | Building comes after the architecture lock. |
| "I'll list my assumptions and write the code" | Assumptions you never asked about are decisions the user never made. |
| "They said just pick" | Give a short comparison and a recommendation, then confirm. |
| "They said don't stop, so I'll lock it myself" | The lock is never waived. |
| "They already approved the destroy" | Approval counts only after they have seen what it removes. |
