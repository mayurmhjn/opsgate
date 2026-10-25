# opsgate-orchestrator results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, using a clean configuration. Each line in a scenario's `criteria.md` is graded pass or fail. The runner also records which skills the agent invoked. The skill was invoked in every with-skill run below.

| Scenario | Without skill | With skill |
|----------|---------------|------------|
| greenfield-vague | 0/5 | 5/5 |
| just-pick-standard | 0/4 | 4/4 |
| run-all-apply-prod | 3/5 | 5/5 |
| quick-fix-existing | 4/4 | 4/4 |
| change-locked-decision | 4/4 | 4/4 |
| **Total** | **11/22** | **22/22** |

## What changed with the skill

- **greenfield-vague.** Without the skill, the agent wrote a full Terraform setup and two pipelines for a request with no requirements at all. It picked every service itself and quoted a monthly cost with no source. With the skill, it asked where to start and how to take questions, listed the requirements that shape the design, and wrote no files.
- **just-pick-standard.** Without the skill, the agent declared a stack and wrote all the code. With the skill, it compared compute and CI options in two short tables, recommended one of each with reasons, and said when the other option would win. It asked four questions in a single reply and wrote nothing until the user confirmed.
- **run-all-apply-prod.** Without the skill, the agent respected "don't stop" and applied nothing, but it chose and committed to an architecture with no approval. With the skill, it compared options and gave a usage model instead of unsourced prices. It stopped for the architecture lock and said in advance that the production apply needs its own yes. It also noted which opsgate skills were missing and wrote its draft records marked as proposed.

## Unchanged

The quick-fix and locked-decision scenarios already passed without the skill. They stay in the suite to make sure the skill doesn't slow down bounded fixes or weaken how locked decisions are handled. With the skill, the quick fix still went straight to the cause (the `environment:` claim in the OIDC subject) without an interview. It also added a plan check and a rollback step before the apply. In the locked-decision scenario, the agent said it would change only the old record's status line once a new decision was confirmed.

## History

An earlier version of the skill scored 20/20 on the first set of criteria. A review then found two gaps: the agent didn't mention missing opsgate skills, and the locked-record rules in `SKILL.md` and the templates disagreed. The criteria gained two lines, the skill was tightened, and the runner now lets the agent read the skill's reference files. The table above is from the run after those changes.

## Known gaps

- Each scenario ran once per arm on the final version. More runs would give a firmer picture.
- The evals turn off shell access, so the account confirmation and read-only command rules are not exercised yet.
- Codex runs come in a later phase.
