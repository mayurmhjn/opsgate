# opsgate-devsecops results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, with a configuration that has no personal instructions but adds a terse response style. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| zero-findings-friday | 2/5 | 5/5 |
| add-scanning | 2/4 | 4/4 |
| sbom-and-signing | 4/5 | 5/5 |
| deleted-key-history | 5/5 | 5/5 |
| ci-role-review | 4/4 | 4/4 (handled by the AWS skill) |
| **Total** | **17/23** | **23/23** |

Failing lines without the skill:

- zero-findings-friday: started the fix list with a medium finding instead of the public bucket and open security group (1), suppressions had no owner or review date (3), and the reply called the result "zero open findings" while a production database was still unencrypted (5).
- add-scanning: container and IaC scans were left report-only, so a new critical finding there never blocked (2), and versions were pinned from memory to tags while pull request results stayed in logs (4).
- sbom-and-signing: actions left on floating major tags (5).

## What changed with the skill

The model already handled leaked keys, IAM policy review and the core of signing well. The skill focuses on rollout, triage and honest reporting.

- **zero-findings-friday.** With the skill, the agent fixed the internet-facing production findings first, explained why the dev-only dependency ranks lower, wrote scoped suppressions with owner and review date, and reported fixed, accepted and open findings separately. It said plainly that the report was not clean.
- **add-scanning.** With the skill, every category gates on new high and critical findings using the scanners' own baseline features. Results go to code scanning through a separate upload job that runs no pull request code. Pins are marked placeholders with the commands to resolve them.
- **sbom-and-signing.** With the skill, the release job verifies the signature against the exact signer identity right after signing, instead of only documenting verification for the customer.

## Changes made during testing

- The first with-skill run scored 22/23, but a reviewer found that the agent wrote a long custom diff script where the scanners' built-in baseline features would do. It also added an unrequested update-bot config, gave `security-events: write` to jobs that run pull request code, and called unapplied changes "fixed". Rules were added for each.
- The same round caught a regression in the CI/CD skill: a privileged deploy step ran a tool with its working directory inside an untrusted artifact. The CI/CD skill now forbids that explicitly.
- The pin-resolution command was corrected after review. For annotated tags, the commit SHA is on the line ending in `^{}`, not the tag line.
- `ci-role-review` was handled by the AWS skill rather than this one in the graded run. Both cover the same rules.

## Known gaps

- One graded run per arm. `add-scanning`, `zero-findings-friday` and `sbom-and-signing` were re-run after the fixes. `deleted-key-history` and `ci-role-review` scores come from the first with-skill run.
- The evals turn off shell access, so no scanner, signer or verifier actually ran.
- The with-skill runs always had the whole plugin installed. No run tested the skill installed on its own.
- Some signing tool defaults (how signatures are stored, required KMS permissions) change between versions. The reference tells the agent to check current documentation.
