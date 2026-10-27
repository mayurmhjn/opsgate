---
name: opsgate-devsecops
description: Use when adding or tuning security scanning (SAST, dependency, container, IaC, secrets), triaging or suppressing findings, responding to a leaked secret, reviewing IAM or other access policies, setting up SBOMs, image signing or provenance, writing policy as code, or threat-modeling a change.
---

# opsgate DevSecOps

Security work fails in two ways: findings nobody acts on, and a clean-looking report that hides real risk. Aim for findings that block when they matter and a report that says plainly what is still open.

## Adding scanning

- Pick scanners for what the repo actually contains: code, dependencies, container images, IaC, secrets, and the running application where a preview environment exists. Compare the options and confirm the choice with the user (with the `opsgate` skill's selection procedure if installed). Prefer fewer tools that cover more, say why each one is there, and use their built-in diff or baseline features or maintained workflows before writing custom scripts (`references/scanner-rollout.md`).
- With an existing backlog, record current findings as a baseline and fail the build on **new** high and critical findings in every category. Don't leave a whole category report-only, and don't fail every PR on old issues.
- Show results where reviewers look: code scanning alerts, PR annotations or a PR comment, not only job logs.
- Scans that need secrets or write access run only on trusted code. Pull requests from forks get read-only scans.
- Pin scanner actions and images to a full SHA or digest. Look up the current release instead of using a remembered version. If you can't, leave a marked placeholder and give the command that resolves each one, so the workflow can be made runnable quickly.
- Add only the files asked for. Offer extras such as update-bot config instead of adding them.

## Triaging findings

1. Rank by severity and real exposure: production before non-production, internet-facing before internal, shipped code before dev-only tooling. Say why each finding sits where it does.
2. Fix the highest-risk findings first, and say what each fix changes (some force a resource replacement).
3. A suppression covers one resource or package, with a reason, an owner and a review or expiry date (`references/triage-and-exceptions.md`). Never skip a check globally to clear a report.
4. Report three lists: fixed, accepted with an exception, and still open. "Fixed" means the change is applied and verified. Otherwise call it "fix proposed". A report with exceptions isn't "zero findings". Say so, and check that the counts match the lists.

## Leaked secrets

Treat any exposed secret as compromised, even if it was deleted later. Deactivate it first, check for use (for AWS keys, CloudTrail and billing), and rotate it. History cleanup is optional and comes last. Prevent a repeat with secret scanning, push protection and short-lived credentials.

## Managing secrets

Prefer no secret at all: OIDC and roles for CI and workloads. Where a secret is unavoidable, keep it in a secret store (a cloud secrets manager or the CI's environment secrets), give each one an owner and a rotation schedule, and keep it out of logs, environment dumps, error messages and build artifacts.

## Access policy reviews

Flag escalation paths first, for example `iam:PassRole` without an `iam:PassedToService` condition, `iam:*`, `iam:CreatePolicyVersion`, `iam:AttachRolePolicy` or `iam:PutRolePolicy`, `iam:UpdateAssumeRolePolicy`, `iam:CreateAccessKey`, the user and group variants (`iam:AttachUserPolicy`, `iam:PutUserPolicy`, `iam:AddUserToGroup`, `iam:CreateLoginProfile`, `iam:UpdateLoginProfile`), `iam:SetDefaultPolicyVersion`, `sts:AssumeRole` on `*`, and compute actions that run code under another role (for example `lambda:UpdateFunctionCode` or `ecs:ExecuteCommand`). Then broad service wildcards. Propose a scoped replacement with conditions, and suggest IAM Access Analyzer validation and last-accessed data.

## Supply chain

Follow `references/supply-chain.md`: produce an SBOM for the released image digest, sign by digest with keyless or KMS-backed signing, attach the SBOM as an attestation, and verify the signature and the expected signer inside the pipeline and at deploy.

## Design reviews

For a new component or exposed endpoint, run the short threat model, compliance mapping and policy-as-code checks in `references/design-review.md`. For policy as code or organization guardrails, follow its policy-as-code section: name each policy's owner and exception process, and say that service control policies don't apply to the management account.

## When related skills are missing

Without the `opsgate` skill, still never apply, deploy, delete or destroy without the user's yes for that specific action, given after they have seen what it will do.
