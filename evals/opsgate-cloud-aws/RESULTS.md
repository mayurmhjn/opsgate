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

## Known gaps

- One graded run per arm. Two small wording fixes landed after most with-skill runs: the replacement check in the architecture skill and a provider-alias note in the AWS traps. Only brownfield-review and cloudfront-cert-trap were re-run after them.
- iam-policy-lambda gained a criterion for building ARNs from attributes, and root-account-startup gained two (no files before the layout is agreed, and asking for the region). They were added after a review found that both arms scored full marks on the original criteria. Both arms were graded on them.
- cloudfront-cert-trap: even with the trap listed, the agent still said the plan "should replace" the old certificate when the provider alias changes. Terraform leaves it orphaned instead.
- vpc-overlap held the requested file back behind five questions, some of which had safe defaults.
- The evals turn off shell access, so live pricing, Cost Explorer queries, account confirmation and read-only command rules are not exercised. "No prices from memory" partly reflects having no tools to fetch them.
- The test configuration adds a terse response style, so replies are shorter than a stock install would give.
- The with-skill runs always had the whole plugin installed. No run tested a skill installed on its own, so the "say which skills are missing" fallback is untested.
- `SKILL.md` files are above the 500-word target (about 500 to 900 words including frontmatter).
