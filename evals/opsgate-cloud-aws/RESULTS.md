# opsgate-cloud-aws results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode with a clean configuration. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| iam-policy-lambda | 5/5 | 5/5 |
| root-account-startup | 5/5 | 5/5 |
| cloudfront-cert-trap | 3/4 | 4/4 |
| vpc-overlap | 3/4 | 4/4 |
| **Total** | **16/18** | **18/18** |

## What changed with the skill

- **cloudfront-cert-trap.** Without the skill, the agent fixed the certificate region but left the public-read bucket policy in the same file unmentioned. With the skill, it flagged the public bucket and recommended origin access control with Block Public Access.
- **vpc-overlap.** With the skill, the design included gateway endpoints for S3 and DynamoDB and weighed NAT gateway count against availability.
- **root-account-startup.** Both arms covered the content. Without the skill, the agent wrote about 1,100 lines of organization Terraform in one go without asking anything. With the skills, it told the user to lock down root today, proposed the account layout with a comparison of Control Tower and hand-built Terraform, and asked before writing code.

## Changes made during testing

The first with-skill run scored 12/18. The orchestrator took the root-account and VPC requests, ran intake, and this skill never loaded. Specific requests now go straight to the matching skill, and setting up a new account now routes here. The final root-account run was graded on its own after the fix. The other three were graded by an independent reviewer.

## Known gaps

- One graded run per arm on the final version.
- The grader found two factual slips in passing. One reply called `10.16.0.0/12` free when only `10.16.0.0/14` was. Another said changing the certificate's provider would replace it, when Terraform would leave the old certificate orphaned instead.
