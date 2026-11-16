# opsgate-observability results

Run on 2026-11-16 with Claude Code (model `claude-opus-5-5`) in headless mode, with account plugin sync turned off. Each scenario ran twice in three arms: without any skills, with the previous pack (0.1.4, which had no observability skill), and with this skill added. One more run had only this skill installed. A reviewer graded every run against the final criteria.

| Scenario | Without skills | Previous pack | With this skill | This skill alone |
|----------|----------------|---------------|-----------------|------------------|
| slo-checkout-api | 3/4, 3/4 | 3/4, 3/4 | 4/4, 4/4 | 4/4 |
| alert-noise | 3/4, 2/4 | 2/4, 2/4 | 4/4, 4/4 | 4/4 |
| payment-logging | 2/4, 1/4 | 1/4, 2/4 | 4/4, 4/4 | 4/4 |
| tracing-ecs-services | 2/3, 2/3 | 3/3, 2/3 | 3/3, 3/3 | 3/3 |
| **Total** | **10/15, 8/15** | **9/15, 9/15** | **15/15, 15/15** | **15/15** |

The previous pack scored no better than no skills here, because nothing in it covered this work. The skill teaches only what the previous pack missed:

- **Error budget policy.** Both previous-pack runs set up burn-rate alerts but never said what happens when the budget runs out. The skill asks for a policy (for example pausing risky releases) and says the team agrees on it.
- **Pages that say what to do.** No previous-pack run put a runbook link or a first check in a paging alarm's description.
- **Card data and retention.** Payment logging loaded no opsgate skill in the previous pack. One run logged the card expiry date, and neither set a retention period on the log group, which keeps data forever by default.
- **Telemetry cost.** Neither payment logging run, and one tracing run, said what the extra logs or traces cost.

Runs that wrote Terraform also loaded `opsgate-iac` and `opsgate-cloud-aws` in 4 of 8 cases, after a review found that the first version of this skill pushed them out.

## Changes made during testing

- An accuracy review found that "set retention on every log group you touch" could delete old audit logs on an existing group. The rule now sets retention on new groups and, for an existing one, recommends a period and asks for it. The payment logging line now accepts that.
- The SLO line now counts load balancer 5xx responses as well as target 5xx, because target metrics alone read zero errors when every target is down.
- The alert noise line now allows paging on a cause that predicts an outage within hours, matching the skill.
- Rules the previous pack already followed (SLIs from user-facing signals, burn-rate alerts, keeping the existing tracing backend) were cut from the skill.
- All arms were graded again on the final criteria. The previous-pack totals dropped from 10/15 to 9/15, because two runs only proposed moving alarms off the pager.

## Known gaps

- Payment logging replies cite PCI DSS rules that weren't checked against the standard.
- The tracing line about passing trace context can only be judged from the code, not by running it.
