# Documentation templates

Write these under `docs/opsgate/` unless the repository already has its own docs or ADR convention. In that case, follow the existing convention. Use Markdown, and Mermaid for diagrams.

## requirements.md

```markdown
# Requirements

Status: draft | approved by <name>, <date>

## Workload
What the system does and who uses it.

## Non-functional requirements
- Availability target:
- RPO / RTO:
- Scale and traffic pattern:
- Latency:
- Data classification:
- Compliance:
- Regions:
- Budget (running cost):

## Team and existing setup
- Team size and skills:
- Existing tools, accounts and standards:

## Open questions
```

## architecture.md

```markdown
# Architecture

Status: draft | locked by <name>, <date>

## Overview
One paragraph on how the system works.

## Diagram
(Mermaid diagram: users, entry points, compute, data stores, network boundaries.)

## Components
| Component | Service | Decision record |
|-----------|---------|-----------------|

## Well-Architected review
One or two lines each: operational excellence, security, reliability, performance efficiency, cost optimization, sustainability.

## Risks and open questions
```

## cost.md

```markdown
# Cost estimate

Price source: <AWS Price List API | AWS Pricing Calculator | Infracost | AWS pricing pages | usage model only>, retrieved <date>
Region:

## Assumptions
Traffic, storage, data transfer, request counts, hours running.

## Monthly estimate per environment
| Component | Low | Expected | High | Main driver |
|-----------|-----|----------|------|-------------|

## Savings options
```

## plan.md

```markdown
# Implementation plan

Based on: architecture.md (locked <date>)

## Phase 1: <name>
- Deliverables:
- Checks that prove it works:
- Rollback:
```

## decisions/NNNN-title.md

```markdown
# NNNN: <decision>

Status: proposed | locked <date> | superseded by NNNN

## Context
The requirements and constraints that drove this choice.

## Options considered
- Option: one line on fit, cost, operational load and risk.

## Decision
What was chosen and the reasons that decided it.

## Consequences
What this makes easier, what it rules out, and when to revisit it.
```

When a locked decision changes, write a new record with its own number. In the new record, say which record it supersedes and why. In the old record, change only the status line to `superseded by NNNN`.

## log.md

```markdown
# Log

## <date>: <stage or task>
- What was done:
- Approved by:
- Records written or changed:
```
