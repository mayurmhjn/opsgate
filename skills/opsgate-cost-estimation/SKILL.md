---
name: opsgate-cost-estimation
description: Use when estimating what an AWS architecture or change will cost, reviewing the cost impact of an infrastructure-as-code pull request, investigating a bill increase or cost spike, breaking costs down by team or tag, setting a budget or spending limit, asked to cut cloud costs or hit a savings target, or buying Savings Plans or Reserved Instances.
---

# opsgate cost estimation

Cost answers people act on must come from data, not memory. A wrong price stated with confidence does more harm than a usage model with blanks.

## Prices

Use prices from a live source and name it with the date: the AWS Price List API (`aws pricing get-products`, called against a Region that serves it), the AWS Pricing Calculator, or Infracost. If none is reachable, the official pricing pages are the fallback, read with the date. Failing that, give the usage model (quantities per cost driver) and tell the user how to price it. Do not fill in unit prices from memory, even with a disclaimer. An estimate based on pricing pages or with no prices must be labeled as such, and the user must acknowledge it before an architecture is locked on it.

## Estimating an architecture

1. List every cost driver per component with its quantity and the assumption behind it. Use `references/cost-drivers.md`, because the drivers people forget are often the large ones: NAT gateway processing per GB, data transfer, log ingestion, interface endpoints, public IPv4 addresses and minimum capacity.
2. Give low, expected and high cases, and name the two or three drivers that move the total most.
3. Separate the always-on floor from the usage-driven part.
4. Estimate each environment separately, and recommend cost allocation tags and a budget alert for each. A budget alerts but doesn't cap spend, and its data lags by hours. Budget actions can attach a deny policy or stop EC2 or RDS instances: explain what an automatic action would break, and get a yes before adding one.
5. Write the result to `docs/opsgate/cost.md` with the source and date if the repo keeps that trail.

## Cost of an IaC change

Name each resource the change adds, removes or resizes, and the drivers each one brings. Use `infracost diff` if it is available. For each costly change, offer a cheaper option and its tradeoff. For example, gateway endpoints for S3 and DynamoDB carry no charge and take that traffic off the NAT gateways. Fewer NAT gateways cost less but lose availability-zone independence.

## Investigating a bill increase

Check the account first: ask, or run `aws sts get-caller-identity` on its own and compare it with the account the user named. Then compare equal periods. A month-to-date total against a full month misleads. Break the bill down by service, usage type, linked account, region and day with Cost Explorer or the Cost and Usage Report, and check Cost Anomaly Detection. Only name a cause once the data shows it. `references/cost-drivers.md` lists the usual suspects to check.

## Cutting costs

"Do it now" is a deadline, not approval to change infrastructure.

1. Ask for the actual breakdown (top services and usage types) before promising a percentage.
2. List savings ranked by expected impact and risk, in two groups: quick wins that are safe to do now, and changes that need testing or a maintenance window. Without prices, rank by relative size of the usage each saving removes.
3. Commitments (Savings Plans, Reserved Instances) come last. They need at least a few weeks of steady usage data and Cost Explorer's recommendations, and should follow rightsizing. Compare the recommendation over the longer lookback periods too, because a short window sized on a busy stretch over-commits. An active commitment can't be cancelled: tell the user they pay the full commitment for the whole term, used or not. A Savings Plan can be returned only shortly after purchase and within limits (check the current rules), and a Reserved Instance not at all. Check the account with `aws sts get-caller-identity` as its own command, show the exact plan (type, term, payment option, hourly commitment, total over the term), and wait for a yes to that purchase, even if the user approved buying beforehand.
4. Production changes need approval, a plan, and a rollback path. Check limits that can slow a rollback, such as how often a volume can be modified.

Edit files only after the user picks which savings to make.

## When related skills are missing

If the `opsgate` skill is not installed, still follow the approval rules above: no apply, deploy, resize, delete, destroy or commitment purchase without a yes for that action. The yes must come after the user has seen the reviewed plan for that action. Blanket pre-approvals don't count. The same applies to commands that change a shared or deployed system, such as a reboot, restart, failover, scaling, or ending sessions or queries: say what the action will do, then wait for a yes.
