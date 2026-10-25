---
name: opsgate-architecture-design
description: Use when designing a cloud architecture from requirements, choosing services for a new system, reviewing an existing AWS setup for risks or an audit, planning disaster recovery against RTO and RPO targets, or deciding whether an architecture is ready to lock.
---

# opsgate architecture design

A design is a proposal until the user locks it. Present it, show its weak points, and ask. Do not build on it.

## Designing from requirements

1. **Check the requirements for gaps** that change the design: availability target, RPO and RTO, scale and peaks, data classification, compliance and residency, budget as a number, regions, team skills. Ask for missing ones, or state an assumption and list it as open. "Tight budget" is not a number. Ask for one.
2. **Choose each significant component with a comparison.** That covers compute, data store, edge, network egress (NAT count, endpoints), IaC tool, CI/CD, and support plan. For each one, compare two or three options against these requirements and recommend one with reasons. If `opsgate-orchestrator` is installed, use its selection procedure.
3. **Draw it.** Use one Mermaid diagram showing users, entry point, compute, data stores, external dependencies and network boundaries (VPC, public and private subnets, accounts).
4. **Walk the failure modes.** Fill in the table from `references/failure-modes.md`: one availability zone lost, a dependency down, a bad deploy, data corruption or deletion, a region lost, credentials leaked. Every tier needs an answer, including compute. One instance behind a load balancer is still a single point of failure.
5. **Review against the six Well-Architected pillars** using `references/well-architected.md`. Write one or two specific lines per pillar, not slogans.
6. **Cost.** Use `opsgate-cost-estimation` if it is installed. Otherwise give a usage model and say where prices come from. Never quote prices from memory. Check the always-on cost floor against the budget.
7. **Ask for the lock.** List the open questions and the assumptions, then ask the user to approve or change the design. If the cost estimate has no prices or comes from pricing pages, ask the user to acknowledge that as part of the lock. Write `docs/opsgate/architecture.md` marked `Status: draft` if the repo uses that trail, and a decision record for each locked choice. Nothing gets built until the user locks it.

Don't choose regions, accounts or recovery regions for the user. Recommend one and ask.

## Reviewing an existing setup

Read the IaC and docs first, and say what you could not see (for example, the live account). Then report findings ordered by risk:

- **Critical:** exposure or data loss, such as open admin ports, public data, no backups, unencrypted sensitive data, or long-lived keys.
- **High:** single points of failure and missing recovery.
- **Medium:** operability, cost and drift.

For each finding, give the file and line, why it matters, and the smallest fix. Check every fix for whether it replaces the resource: in Terraform, changing fields such as encryption, `username`, `key_name`, the AMI or the subnet usually forces a new instance or database. Say so, and never call a replacing change "no downtime". Propose an order of work. Change no files until the user picks what to do.

## Disaster recovery

Map RTO and RPO to a strategy with `references/dr-strategies.md`, and show why the targets rule out the cheaper tiers. State what each tier costs to run, then ask for the budget, or whether the targets can move. Follow the reference's failover checklist, so that traffic never reaches a recovery region whose data store isn't promoted yet. Include how failover is tested and how traffic comes back.

## When related skills are missing

If `opsgate-cost-estimation` or `opsgate-cloud-aws` is not installed, say so in one line and continue. For service details, use the official AWS skills or the AWS documentation.
