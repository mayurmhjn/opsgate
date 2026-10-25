# opsgate-architecture-design results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode with a clean configuration. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| design-from-requirements | 5/6 | 6/6 |
| brownfield-review | 4/5 | 5/5 |
| dr-tight-budget | 4/5 | 5/5 |
| **Total** | **13/16** | **16/16** |

## What changed with the skill

- **design-from-requirements.** Without the skill, the design was good but ended with no request to approve or lock it, and it picked secondary tools with no comparison. With the skill, every main component had a comparison, the failure-mode table covered every tier, all six Well-Architected pillars were reviewed, and the reply asked the user to lock or change the design.
- **brownfield-review.** Without the skill, the single EC2 instance was not called a single point of failure. With the skill, it was, and each fix said whether it would replace the resource.
- **dr-tight-budget.** Without the skill, the agent priced its own pick and never asked what "tight" meant. With the skill, it ruled out backup and restore and pilot light against the targets, recommended warm standby, asked for the budget as a number, and kept failover consistent ("switch DNS last").

## Changes made during testing

The first with-skill run scored 12/16. In the DR scenario, the orchestrator took the request, ran its intake questions, and never loaded this skill. The orchestrator now sends specific requests like a DR design straight to the matching skill. Reviews also now check whether a fix replaces the resource, after one reply called a replacing change "no downtime".

## Known gaps

- One graded run per arm on the final version.
- The grader noted the design did not check the always-on cost floor against the stated budget before inviting a lock.
