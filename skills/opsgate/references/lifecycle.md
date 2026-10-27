# Lifecycle

## Stages

| Stage | What happens | Ends when |
|-------|--------------|-----------|
| Intake | Find out whether this is new work or a bounded task, where to start, and how the user wants questions asked. | The user has answered or chosen a start point. |
| Requirements | Gather functional and non-functional requirements (see the inputs in `selection-procedure.md`). | The user approves `requirements.md`. |
| Architecture | Choose services with the selection procedure, draw diagrams, estimate cost, review against the AWS Well-Architected pillars, take feedback, revise. | The user explicitly locks the architecture. This approval can never be waived. |
| Plan | Turn the locked architecture into phases with clear deliverables and checks. | The user approves `plan.md`. |
| Implement | Write IaC, pipelines, security controls and baseline monitoring, one phase at a time. | Each phase's checks pass. |
| Review | Review code, run security scans, produce a cost diff, check for drift from the locked architecture. | Findings are fixed or accepted by the user. |
| Record | Update the docs trail. Happens at the end of every stage, not only at the end. | The log entry is written. |

## Starting points

- **Architecture design (default):** intake, requirements, architecture. Stop after the lock unless the user asked for more.
- **Planning:** requires a locked architecture. If there is none, say so and offer to do the architecture first.
- **Implementation:** requires an approved plan, or a bounded task. For new work with no plan, offer the plan first.
- **All stages:** run them in order, stopping at each gate unless the user pre-approved stages.

## Pre-approved stages

When the user says "don't stop between stages", move from one stage to the next without waiting. Still stop for:

1. The architecture lock.
2. Each apply, deploy, delete or destroy.

Tell the user up front that you will stop at those two points, so the stop doesn't surprise them.

## Bounded tasks on existing systems

Fix the problem directly. Read the existing code and configuration first and keep their conventions. Follow the safety rules. If the fix changes the architecture (a new service, a new data store, a different compute platform), stop and treat it as a design change.

## Routing

| Work | Skill |
|------|-------|
| Requirements, service selection, diagrams, Well-Architected review, architecture lock | `opsgate-architecture-design` |
| Running-cost estimate, savings, cost diff of an IaC change | `opsgate-cost-estimation` |
| AWS account layout, IAM, networking, tagging, encryption, audit baseline | `opsgate-cloud-aws` |
| Terraform, OpenTofu, CDK, CloudFormation, SAM, Pulumi | `opsgate-iac` |
| Pipelines, releases, rollbacks, failed runs | `opsgate-cicd` |
| Scanners, policy as code, secrets, supply chain, IAM review | `opsgate-devsecops` |

If the skill is not installed, say so in one line and continue with this skill's rules.

## Commands against real accounts

1. Before the first command that touches a cloud account, find out which account, role and environment it reaches: ask, or run `aws sts get-caller-identity` (or the tool's equivalent) as a command on its own. Compare the result with the account or environment the user named. If they don't match, or nothing says which environment this is, say what you found and ask before going on.
2. After that, read-only commands are fine: describe and list calls, pricing queries, logs, and `plan` against non-production environments.
3. Ask before running a plan against production, unless the user asked for that plan, and before installing any tool.
4. Never run apply, deploy, delete or destroy without a yes for that specific action. For production, state the rollback path first.
