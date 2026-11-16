---
name: opsgate-observability
description: Use when setting up or changing monitoring, alarms, alerts, SLOs or error budgets, dashboards, logging or tracing for a deployed service (CloudWatch, Prometheus, Grafana, OpenTelemetry, Datadog and similar), including logging requests or payloads to debug production failures, being paged too often, or reducing alert noise.
---

# opsgate observability

Monitoring exists to tell a person that users are hurting, early enough to act. Every page wakes someone, and every log line, metric and trace costs money.

## SLOs and alerts

- **Give the error budget a use.** With an SLO, say what happens when the budget runs out, for example pausing risky releases or putting reliability work first until it recovers, and that the team agrees on this policy and on who decides.
- **Every page says what to do.** Put a runbook link, or a short "first check" when there is no runbook yet, in each paging alarm's description. Offer to write the runbook (`opsgate-incident`).
- Page on what users feel (errors, latency, availability). Causes such as CPU, memory and disk go to a ticket or dashboard unless they predict an outage within hours.

## Logs

- Never log secrets, tokens, card numbers, card security codes or expiry dates, or full request bodies. Log the fields debugging needs (IDs, amounts, error codes, the upstream status) and mask personal data such as email addresses. Check field names against the code that sets them.
- Set a retention period on every log group you create, because CloudWatch Logs keeps data forever by default unless an account-level retention policy applies (`retention_in_days` in Terraform). For an existing log group without one, recommend a period but ask for it, since audit or compliance needs may require long retention, and say in the plan that a shorter period deletes older data. If the log group isn't in the code, say so and offer to add or import it.

## Cost

Say what new telemetry costs before adding it: log ingestion and storage, custom metrics and their dimensions, and trace volume. Keep volume in proportion: full detail on failures and a short line on success, sampling for traces, and no per-user or per-request values as metric dimensions. For prices, use `opsgate-cost-estimation` if it is installed, never memory.

## Infrastructure code

Production alarms, dashboards and log groups are infrastructure. Before editing the repo's IaC, load `opsgate-iac` too, and `opsgate-cloud-aws` for AWS resources. If either isn't installed, name it in one line and continue.

## When related skills are missing

Without the `opsgate` skill, still never apply, deploy, delete or destroy without the user's yes for that specific action, given after they have seen the reviewed plan. Blanket pre-approvals don't count. For production, state the rollback path first. The same applies to commands that change a shared or deployed system, such as a reboot, restart, failover, scaling, or ending sessions or queries: say what the action will do, then wait for a yes.
