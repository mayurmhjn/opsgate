# opsgate-cloud-aws results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode with a clean configuration. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| iam-policy-lambda | 5/6 | 6/6 |
| root-account-startup | 5/7 | 7/7 |
| cloudfront-cert-trap | 3/4 | 4/4 |
| vpc-overlap | 3/4 | 4/4 |
| **Total** | **16/21** | **21/21** |

## What changed with the skill

- **cloudfront-cert-trap.** Without the skill, the agent fixed the certificate region but left the public-read bucket policy in the same file unmentioned. With the skill, it flagged the public bucket and recommended origin access control with Block Public Access.
- **vpc-overlap.** With the skill, the design included gateway endpoints for S3 and DynamoDB and weighed NAT gateway count against availability.
- **root-account-startup.** Both arms covered the content. Without the skill, the agent wrote about 1,100 lines of organization Terraform in one go without asking anything. With the skills, it told the user to lock down root today, proposed the account layout with a comparison of Control Tower and hand-built Terraform, and asked before writing code.

## Changes made during testing

The first with-skill run scored 12/18. The orchestrator took the root-account and VPC requests, ran intake, and this skill never loaded. Specific requests now go straight to the matching skill, and setting up a new account now routes here. The final root-account run was graded on its own after the fix. The other three were graded by an independent reviewer.

- Later phases added three rules to this skill: handle pasted credentials, hand whole-setup reviews to the architecture skill and flag replacing fixes, and keep the permissions a role needs to run (one run left a Lambda role with no log permissions after a scope rule was added elsewhere). All four scenarios were re-run on the final text: 20/21 graded by a reviewer, then the IAM scenario passed 6/6 after the last fix.
- In one final run of cloudfront-cert-trap the skill did not load. The reply still passed every criterion.

## Policy review suggestion (2026-10-27)

The IAM section now suggests IAM Access Analyzer validation and last-accessed data when reviewing a policy. An `opsgate-devsecops` scenario loaded this skill instead of that one and lost the suggestion. Two re-runs of that scenario made it. This skill's own scenarios were not re-run.

## Link preview instance (2026-11-07)

Run on 2026-11-07 with Claude Code 2.1.319 (model `claude-opus-5-5`). From this date the eval configuration turns off account plugin sync, so account plugins no longer load in either arm; earlier runs had them. The scenario came from a gap review against the devops-exercises repository. One graded run per arm. Before the with-skill run, a grader flagged unclear criteria wording; the reworded criteria were used for both arms. Other scenarios in this file were not re-run on the new text, except the regression runs named below. The with-skill run came before a later edit that added the running-system rule to this skill's fallback for when `opsgate` is not installed.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| link-preview-ec2 | 4/4 | 4/4 |

The baseline already required IMDSv2, kept the hop limit at 1, named the SSRF risk and scoped the role to the bucket, so no rule was added. The scenario stays as a regression check.

The with-skill reply added `aws:SourceAccount` to the EC2 trust policy. AWS documentation doesn't confirm that EC2 sends this key when it assumes an instance role, and a condition on a missing key fails. The rule now says to add these keys where the service documents support for them. That wording was not re-run. A regression run of `iam-policy-lambda` kept 6/6.

## Known gaps

- One graded run per arm. Every with-skill run here used the final skill text, after the size trim.
- iam-policy-lambda gained a criterion for building ARNs from attributes, and root-account-startup gained two (no files before the layout is agreed, and asking for the region). They were added after a review found that both arms scored full marks on the original criteria. Both arms were graded on them.
- cloudfront-cert-trap: even with the trap listed, the agent still said the plan "should replace" the old certificate when the provider alias changes. Terraform leaves it orphaned instead.
- Earlier runs of vpc-overlap held the requested file back behind questions. The final run wrote it.
- This skill's evals turn off shell access, so live pricing, Cost Explorer queries, account confirmation and read-only command rules are not exercised here. Three shell scenarios under `evals/opsgate/` cover account confirmation and read-only commands with stand-in CLIs. "No prices from memory" partly reflects having no tools to fetch them.
- The test configuration adds a terse response style, so replies are shorter than a stock install would give.
- The with-skill runs always had the whole plugin installed. No run tested a skill installed on its own, so the "say which skills are missing" fallback is untested.
- `SKILL.md` files are above the 500-word target (about 500 to 900 words including frontmatter).

## Replicas, ECS deploys, scaling, bastions and backups (2026-11-16)

Run on 2026-11-16 with Claude Code (model `claude-opus-5-5`), with account plugin sync turned off. The scenarios came from a gap review against public DevOps guides and the devops-exercises repository. Two baseline runs per scenario and one with-skill run, with more runs for the replica scenario.

| Scenario | Without skills | With skills | This skill alone |
|----------|----------------|-------------|------------------|
| replica-stale-reads | 3/4, 3/4 | 3/4, 3/4 | 3/4 |
| ecs-new-service | 4/4, 4/4 | 4/4 | |
| autoscaling-flap | 5/5, 3/5 | 3/5 | |
| bastion-for-rds | 4/4, 4/4 | 2/4 | |
| backup-good-enough | 4/4, 4/4 | 4/4 | |

No rule was added. Without the skills, the agent already turned on the ECS deployment circuit breaker with rollback, shortened the deregistration delay, moved the flapping group to target tracking with a warmup (one of the two runs missed the short alarm period and said nothing about what to watch afterwards), chose Session Manager port forwarding over an SSH bastion, and found the gaps in snapshot-only database backups.

The one gap was replica lag: no run in any arm suggested watching or alarming on `ReplicaLag`. A rule for it was written and then removed, because the replica prompt reads as an application bug and loaded no opsgate skill in any arm, including with only this skill installed, so the rule could never reach it.

The with-skill bastion run stopped to ask five intake questions instead of writing Terraform. It recommended Session Manager but left the database security group and per-developer access open, which cost two points. The with-skill autoscaling run fixed the policy but didn't explain the one-minute alarms and short cooldown as a cause or say what to watch afterwards.

Regression runs of `iam-policy-lambda` (6/6) and `vpc-overlap` (4/4) passed.

### Changes made during testing

After the baseline runs, a grader found several criteria that bundled two or three checks, and one (the bastion port 22 line) that could only pass by default. They were split or reworded before the with-skill runs, and the baseline runs were graded again on the final criteria. A final review then reworded the backup line on crash-consistent snapshots, because PostgreSQL can recover from one when the data and WAL share a volume, and made two autoscaling lines more precise. Checked against the graders' notes on each transcript, no grade changes under the new wording.

### Known gaps

- Replies in both arms said Session Manager logs "every session" in CloudTrail. CloudTrail records the session start; Session Manager doesn't log what passes through a port forwarding session.
- The replica scenario shows the pack doesn't load for database problems that look like application bugs.
- The with-skill `vpc-overlap` reply added flow logs, a state backend and three NAT gateways beyond the request.
- Two scenarios scored lower with the skills than without, each on a single with-skill run: `bastion-for-rds` (2/4 against 4/4 and 4/4) and `autoscaling-flap` (3/5 against 5/5 and 3/5). That is why the README shows only one point between the arms for this skill.

## Description change (2026-11-16)

The description now starts "Use when writing or changing anything that touches an AWS account" and says "writing IAM policies and roles", so reviews of existing policies go to `opsgate-devsecops`. Regression runs of `iam-policy-lambda` (6/6), `cloudfront-cert-trap` (4/4), `root-account-startup`, `link-preview-ec2`, `vpc-overlap` and `pasted-secret` (3/4 in one run; two more runs both told the user to deactivate the exposed key) still loaded this skill. The others were checked for which skill loaded, not scored. Details are in `evals/opsgate/RESULTS.md`.
