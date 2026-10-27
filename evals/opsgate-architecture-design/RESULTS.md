# opsgate-architecture-design results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode with a clean configuration. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| design-from-requirements | 5/6 | 6/6 |
| brownfield-review | 5/6 | 6/6 |
| dr-tight-budget | 4/5 | 5/5 |
| **Total** | **14/17** | **17/17** |

## What changed with the skill

- **design-from-requirements.** Without the skill, the design was good but ended with no request to approve or lock it, and it picked secondary tools with no comparison. With the skill, every main component had a comparison, the failure-mode table covered every tier, all six Well-Architected pillars were reviewed, and the reply asked the user to lock or change the design.
- **brownfield-review.** Without the skill, the single EC2 instance was not called a single point of failure. With the skill, it was, and each fix said whether it would replace the resource.
- **dr-tight-budget.** Without the skill, the agent priced its own pick and never asked what "tight" meant. With the skill, it ruled out backup and restore and pilot light against the targets, recommended warm standby, asked for the budget as a number, and kept failover consistent ("switch DNS last").

## Changes made during testing

The first with-skill run scored 12/16. In the DR scenario, the orchestrator took the request, ran its intake questions, and never loaded this skill. The orchestrator now sends specific requests like a DR design straight to the matching skill. Reviews also now check whether a fix replaces the resource, after one reply called a replacing change "no downtime".

## Installed on its own

On 2026-10-27, `design-from-requirements` was run with only this skill installed (`--arm standalone`). The first run scored 6/6 and said `opsgate-cost-estimation` was missing, with no prices from memory. It did not say `opsgate-cloud-aws` was missing, although it designed accounts, SCPs and the network. The skill now names either missing skill whenever the design covers its area. A re-run on that text scored 6/6 and named both.

The first standalone run's draft pointed twice to the wrong section number. The second run was not checked for this.

## Known gaps

- One graded run per arm. Every with-skill run here used the final skill text, after the size trim.
- brownfield-review gained a criterion after the first runs: "says which proposed fixes replace a resource". Both arms were graded on it.
- In one run, the agent called a cross-region binlog replica an option for Aurora PostgreSQL, but binlog replicas exist only for Aurora MySQL.
- The evals turn off shell access, so live pricing, Cost Explorer queries, account confirmation and read-only command rules are not exercised. "No prices from memory" partly reflects having no tools to fetch them.
- The test configuration adds a terse response style, so replies are shorter than a stock install would give.
- Only one scenario was run with the skill installed on its own.
- `SKILL.md` files are above the 500-word target (about 500 to 900 words including frontmatter).
