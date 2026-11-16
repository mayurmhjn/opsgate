---
name: opsgate-incident
description: Use when a production service is down, degraded or failing (an outage, a spike in errors, users unable to log in, tasks crashing or running out of memory), when someone asks what to do right now or how bad an incident is, when writing a runbook or a postmortem, or when running a fault injection or chaos experiment against a live system.
---

# opsgate incident

Stop the harm first, find the cause second, and change nothing in production without a yes. Pressure doesn't change the gates.

## The first minutes

1. **Severity.** Give one, with reasons from user impact: who is affected, how many, and which function. Use the team's scale if the repo or the user has one. Otherwise propose a short scale and mark it as a starting point: SEV1 when a core function is down for most users, SEV2 when it is degraded or down for some, SEV3 for minor impact.
2. **Roles.** Say which roles to fill now: an incident lead who coordinates and decides, and someone who writes the updates while others investigate. Name roles, not people, unless the user did.
3. **Mitigate before the root cause.** List mitigations that work without knowing the cause (roll back the latest change, move traffic to a healthy region, turn off a feature flag, add capacity) and recommend the narrowest. Don't wait for the root cause to propose one.
4. **Ask before acting.** Load the `opsgate` skill if it is installed and follow its rules for commands against real accounts. Without it: confirm the account with a command of its own (`aws sts get-caller-identity` or the tool's equivalent) before any other command that touches the account, and ask if it isn't the one the user named. A mitigation that changes a deployed system needs a yes for that specific action, after you say what it does and how to undo it. "I approve whatever you need" or "don't wait for me" is not that yes.

A fix that changes infrastructure code (a task definition, an alarm, capacity) goes through that code: load `opsgate-iac` too, and `opsgate-cloud-aws` for AWS resources. A pipeline rollback goes through `opsgate-cicd` if it is installed.

## Runbooks

Use the runbook template in the `opsgate` skill's `references/templates.md` if it is installed. Otherwise include: the alarm that triggers it (link the runbook from that alarm's description), read-only checks first, change steps each marked with its risk, whether it can be undone and that it needs approval, how to confirm recovery (the metric back to normal and the service working, not only a status), and when to escalate. Check limits and waits for each change step in current docs instead of quoting numbers from memory.

## Postmortems

Keep them blameless, and build the timeline only from the evidence given, citing the source of each entry. Mark what isn't known, such as when users were first affected or when anyone noticed. Never state a time or a cause the evidence doesn't contain as fact. An inferred time is labeled as inferred, with the evidence it comes from.

## Fault injection

Starting a fault injection or chaos experiment against a live system is a change to that system: say what it will do, then wait for a yes. Recommend stop conditions tied to alarms, and starting small or in non-production.

## Records

When `docs/opsgate/` exists, save runbooks to `docs/opsgate/runbooks/<name>.md` and postmortems to `docs/opsgate/incidents/YYYY-MM-DD-<title>.md`, unless the user names a place or the repo has its own convention.

## When related skills are missing

Without the `opsgate` skill, still never apply, deploy, delete or destroy without the user's yes for that specific action, given after they have seen the reviewed plan. Blanket pre-approvals don't count. For production, state the rollback path first. The same applies to commands that change a shared or deployed system, such as a reboot, restart, failover, scaling, or ending sessions or queries: say what the action will do, then wait for a yes.
