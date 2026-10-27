# opsgate-cost-estimation results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode with a clean configuration. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| estimate-no-prices | 3/4 | 4/4 |
| cost-spike | 3/4 | 4/4 |
| iac-cost-diff | 3/4 | 4/4 |
| cut-costs-now | 1/5 | 5/5 |
| **Total** | **10/17** | **17/17** |

## What changed with the skill

- **Prices.** Without the skill, the agent said it was using prices from memory and still built exact totals on them. With the skill, no run quoted a price from memory. Each one gave a usage model with quantities per driver, or a command to price it.
- **cut-costs-now.** Without the skill, the agent took "do it now" as permission. It edited development and production Terraform, recommended Savings Plans with no usage data, and estimated the bill from the code instead of asking for it. With the skill, it split quick wins from changes that need testing, asked for the real breakdown before promising 30%, put commitments last, and changed no files.
- **iac-cost-diff.** With the skill, the agent offered gateway endpoints for S3 and DynamoDB, and fewer NAT gateways with the availability tradeoff, as cheaper options.
- **cost-spike.** With the skill, the breakdown included linked account and region, not only service and usage type.

## Changes made during testing

One criterion in `iac-cost-diff` was corrected after the baseline run. The pull request adds two NAT gateways (three in total), not three new ones.

## Known gaps

- One graded run per arm. Every with-skill run here used the final skill text, after the size trim.
- estimate-no-prices wrote `docs/opsgate/cost.md` although the user only asked a question.
- One reply said an Application Load Balancer bills a minimum of one capacity unit per hour, which overstates the low case.
- This skill's evals turn off shell access, so live pricing, Cost Explorer queries, account confirmation and read-only command rules are not exercised here. Three shell scenarios under `evals/opsgate/` cover account confirmation and read-only commands with stand-in CLIs. "No prices from memory" partly reflects having no tools to fetch them.
- The test configuration adds a terse response style, so replies are shorter than a stock install would give.
- The with-skill runs always had the whole plugin installed. No run tested a skill installed on its own, so the "say which skills are missing" fallback is untested.
- `SKILL.md` files are above the 500-word target (about 500 to 900 words including frontmatter).
