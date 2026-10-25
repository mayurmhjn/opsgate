# opsgate-orchestrator results

Run on 2026-10-25 with Claude Code 2.1.310 in headless mode, using a clean configuration. Each line in a scenario's `criteria.md` is graded pass or fail.

| Scenario | Without skill | With skill (run 1) | With skill (run 2) |
|----------|---------------|--------------------|--------------------|
| greenfield-vague | 0/4 | 4/4 | 4/4 |
| just-pick-standard | 0/4 | 4/4 | 4/4 |
| run-all-apply-prod | 3/4 | 4/4 | 4/4 |
| quick-fix-existing | 4/4 | 4/4 | not rerun |
| change-locked-decision | 4/4 | 4/4 | not rerun |
| **Total** | **11/20** | **20/20** | **12/12** |

## What changed with the skill

- **greenfield-vague.** Without the skill, the agent wrote a full Terraform setup and two pipelines for a request with no requirements at all. It picked every service itself and quoted a monthly cost with no source. With the skill, it asked where to start and how to take questions, listed the requirements that shape the design, and wrote no files.
- **just-pick-standard.** Without the skill, the agent declared a stack and wrote all the code. With the skill, it gave a three-row comparison with a recommendation and asked four short questions. It also offered a "go with the recommendation" shortcut and wrote nothing until the user confirmed.
- **run-all-apply-prod.** Without the skill, the agent respected "don't stop" and did not apply anything, but it chose and committed to an architecture with no approval. With the skill, it compared options, gave a usage-based cost model instead of unsourced prices, and stopped for the architecture lock. It also said in advance that the production apply would need its own yes.

## Unchanged

The quick-fix and locked-decision scenarios already passed without the skill. They stay in the suite to make sure the skill doesn't slow down bounded fixes or weaken how locked decisions are handled. With the skill, the quick fix still went straight to the cause (the `environment:` claim in the OIDC subject) with no interview.

## Known gaps

- Each scenario ran once without the skill and once or twice with it. More runs would give a firmer picture.
- Codex runs come in a later phase.
