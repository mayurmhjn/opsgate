---
name: opsgate-cost-estimation
description: Use when estimating what an AWS architecture or change will cost, reviewing the cost impact of an infrastructure-as-code pull request, investigating a bill increase or cost spike, or asked to cut cloud costs or hit a savings target.
---

# opsgate cost estimation

Cost answers people act on must come from data, not memory. A wrong price stated with confidence does more harm than a usage model with blanks.

## Prices

Use prices only from a live source, and name it with the date: the AWS Price List API (`aws pricing get-products`), the AWS Pricing Calculator, Infracost, or the official pricing pages. If you cannot reach one, give the usage model (quantities per cost driver) and tell the user how to price it. Do not fill in unit prices from memory, even with a disclaimer.

## Estimating an architecture

1. List every cost driver per component with its quantity and the assumption behind it. Use `references/cost-drivers.md`, because the drivers people forget are often the large ones: NAT gateway processing per GB, data transfer, log ingestion, interface endpoints, public IPv4 addresses and minimum capacity.
2. Give low, expected and high cases, and name the two or three drivers that move the total most.
3. Separate the always-on floor from the usage-driven part.
4. Write the result to `cost.md` with the source and date if the repo keeps a `docs/opsgate/` trail.

## Cost of an IaC change

Name each resource the change adds, removes or resizes, and the drivers each one brings. Use `infracost diff` if it is available. For each costly change, offer a cheaper option and its tradeoff. For example, gateway endpoints for S3 and DynamoDB carry no charge and take that traffic off the NAT gateways. Fewer NAT gateways cost less but lose availability-zone independence.

## Investigating a bill increase

Confirm the account or profile first. Then compare equal periods. A month-to-date total against a full month misleads. Break the bill down by service, usage type, linked account, region and day with Cost Explorer or the Cost and Usage Report, and check Cost Anomaly Detection. Only name a cause once the data shows it. `references/cost-drivers.md` lists the usual suspects to check.

## Cutting costs

"Do it now" is a deadline, not approval to change infrastructure.

1. Ask for the actual breakdown (top services and usage types) before promising a percentage.
2. List savings ranked by expected impact and risk, in two groups: quick wins that are safe to do now, and changes that need testing or a maintenance window. Without prices, rank by relative size of the usage each saving removes.
3. Commitments (Savings Plans, Reserved Instances) come last. They need at least a few weeks of steady usage data and Cost Explorer's recommendations, and should follow rightsizing.
4. Production changes need approval, a plan, and a rollback path. Check limits that can slow a rollback, such as how often a volume can be modified.

Edit files only after the user picks which savings to make.

## When related skills are missing

If `opsgate-orchestrator` is not installed, still follow the approval rules above: no apply, resize or delete without a yes for that action.
