# opsgate-devsecops results

Run on 2026-10-25 with Claude Code 2.1.310 (model `claude-opus-5-5`) in headless mode, with a configuration that has no personal instructions but adds a terse response style. The with-skill runs had the whole opsgate plugin installed. Each line in a scenario's `criteria.md` is graded pass or fail by a reviewer reading the transcript.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| zero-findings-friday | 2/5 | 4/5 |
| add-scanning | 2/4 | 4/4 |
| sbom-and-signing | 4/5 | 4/5 |
| deleted-key-history | 5/5 | 5/5 |
| ci-role-review | 4/4 | 4/4 |
| **Total** | **17/23** | **21/23** |

The gain comes from `zero-findings-friday` and `add-scanning`. Signing, leaked keys and IAM review scored the same in both arms.

Failing lines without the skill:

- zero-findings-friday: left the security group open to the internet while fixing a low-severity finding (1), and wrote suppressions with no owner or date (3). It also gave no reason for the dev-only dependency's priority (4).
- add-scanning: container and IaC scans were left report-only, so a new critical finding there never blocked (2), and versions were pinned from memory to tags while pull request results stayed in logs (4).
- sbom-and-signing: actions left on floating major tags (5).

Failing lines with the skill:

- zero-findings-friday (4): the dev-only dependency was upgraded, but the reply didn't say why it ranks lower.
- sbom-and-signing (5): a newly added upload action was left on a floating tag, and the choice of tools had no stated reason.


## What changed with the skill

The model already handled leaked keys, IAM policy review and the core of signing well. The skill focuses on rollout, triage and honest reporting.

- **zero-findings-friday.** With the skill, the agent fixed the public bucket ACL and the open security group in the code first, wrote suppressions scoped to one resource with an owner and an expiry date, and reported proposed fixes, exceptions and open items separately. It said plainly that the result was not zero findings.
- **add-scanning.** With the skill, every category gates on new high and critical findings using the scanners' own baseline features, pull request results appear on the pull request, and pins are marked placeholders with the commands to resolve them.
- **sbom-and-signing.** With the skill, the release job verifies the signature against the exact signer identity right after signing, instead of only documenting verification for the customer.

## Changes made during testing

- The first with-skill run wrote a long custom diff script where the scanners' built-in baseline features would do. It also added an unrequested update-bot config, gave `security-events: write` to jobs that run pull request code, and called unapplied changes "fixed". Rules were added for each.
- The same round caught a regression in the CI/CD skill: a privileged deploy step ran a tool with its working directory inside an untrusted artifact. The CI/CD skill now forbids that explicitly.
- A review then found factual problems. The KMS signing permissions were incomplete (cosign also needs `kms:GetPublicKey` and `kms:DescribeKey`). The `.trivyignore` example used a bare ID, which applies repo-wide, to suppress a shipped package that had a fix. Both exception examples came from the eval fixture. And the tag-to-SHA command matched too broadly. All were corrected, and DAST, secret management and more escalation actions were added.
- The `zero-findings-friday` fixture had no infrastructure files, so neither arm could apply a fix. Real Terraform files and a `package.json` were added, and both arms were re-run. Criterion 1 now asks for the fix in the code.
- Two `add-scanning` criteria were reworded to state the bar they were graded against: a gate in every category, and pinning to a full SHA with pull request results on the pull request. Both arms were re-graded.

## Design review, policy as code and threat modeling (2026-10-27)

Three scenarios were added for the parts of the skill no eval covered. Both arms ran on 2026-10-27. After the first grading, three criteria were changed and disclosed here: `policy-as-code-guardrails` line 1 now also accepts a concrete proposal that waits for the user to confirm the tool, because the skill asks for that confirmation; `threat-model-admin-tool` line 5 was split into "names an owner for each risk" and "asks at least two of the questions that would change the model". Both arms are scored on the current criteria.

| Scenario | Without skills | With skills |
|----------|----------------|-------------|
| design-review-webhook | 5/5 | 5/5 |
| policy-as-code-guardrails | 2/5 | 4/5 |
| threat-model-admin-tool | 5/6 | 5/6 |
| **Total** | **12/16** | **14/16** |

The first with-skill runs matched the baseline (11 of 15 on the old criteria): the policy-as-code rules in `references/design-review.md` never came up, because `SKILL.md` only sent new components there. The skill now sends policy-as-code and guardrail work to that section, with owners, an exception process and the note that service control policies don't apply to the management account, and threat models end with a risk, control and owner table. The scores above are from the re-run on that text.

- Both arms review the webhook well. The model already knows Stripe signature checks, replay protection and log redaction.
- Neither arm names owners: the threat model left every owner as "?", and the policy reply asked who owns the policies without proposing an exception process.
- In the latest webhook run no opsgate skill loaded. In the latest `ci-role-review` run the AWS skill loaded instead of this one and dropped the Access Analyzer suggestion, so `opsgate-cloud-aws` now suggests Access Analyzer and last-accessed data for policy reviews too. Two re-runs both made the suggestion; only that line was re-checked.
- Wrong or loose claims in replies: one said ECR pushes to a repository with a customer managed KMS key need `kms:` permissions on the pushing role (likely wrong, since ECR uses grants), one listed card brand and last four digits as part of a `payment_intent.succeeded` payload, and one put Cognito login under the ALB's `authenticate-oidc` action instead of `authenticate-cognito`.

## Known gaps

- One graded run per arm. All with-skill runs above used the final skill text. The `zero-findings-friday` baseline was re-run on the new fixture; the other baselines are from the first run, on fixtures that did not change.
- The evals turn off shell access, so no scanner, signer or verifier actually ran.
- The with-skill runs always had the whole plugin installed. No run tested the skill installed on its own.
- No scenario covers design review, policy as code or threat modeling yet.
- The grader noted some slips in passing replies: a new log bucket without the policy that lets S3 deliver access logs to it, and an overstated claim that a scan "won't break unrelated PRs" when fixable base-image vulnerabilities still would.
