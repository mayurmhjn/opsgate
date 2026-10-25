---
name: opsgate-devsecops
description: Use when adding or tuning security scanning (SAST, dependency, container, IaC, secrets), triaging or suppressing findings, responding to a leaked secret, reviewing IAM or other access policies, setting up SBOMs, image signing or provenance, writing policy as code, or threat-modeling a change.
---

# opsgate DevSecOps

Security work fails in two ways: findings nobody acts on, and a clean-looking report that hides real risk. Aim for findings that block when they matter and a report that says plainly what is still open.

## Adding scanning

- Pick scanners for what the repo actually contains: code, dependencies, container images, IaC, secrets. Prefer fewer tools that cover more, and say why each one is there (`references/scanner-rollout.md`).
- With an existing backlog, record current findings as a baseline and fail the build on **new** high and critical findings in every category. Don't leave a whole category report-only, and don't fail every PR on old issues.
- Show results where reviewers look: code scanning alerts, PR annotations or a PR comment, not only job logs.
- Scans that need secrets or write access run only on trusted code. Pull requests from forks get read-only scans.
- Pin scanner actions and images to a full SHA or digest. Look up the current release instead of using a remembered version, or leave a marked placeholder.

## Triaging findings

1. Rank by severity and real exposure: production before non-production, internet-facing before internal, shipped code before dev-only tooling.
2. Fix the highest-risk findings first, and say what each fix changes (some force a resource replacement).
3. A suppression covers one resource or package, with a reason, an owner and a review or expiry date (`references/triage-and-exceptions.md`). Never skip a check globally to clear a report.
4. Report three lists: fixed, accepted with an exception, and still open. A report with exceptions isn't "zero findings". Say so.

## Leaked secrets

Treat any exposed secret as compromised, even if it was deleted later. Deactivate and rotate it first. Then check for use (for AWS keys, CloudTrail and billing). History cleanup is optional and comes last. Prevent a repeat with secret scanning, push protection and short-lived credentials.

## Access policy reviews

Flag escalation paths first: `iam:PassRole`, `iam:*`, `sts:AssumeRole` or broad service wildcards on `*`. Propose a scoped replacement with conditions, and suggest IAM Access Analyzer validation and last-accessed data.

## Supply chain

Follow `references/supply-chain.md`: produce an SBOM for the released image digest, sign by digest with keyless or KMS-backed signing, attach the SBOM as an attestation, and verify the signature and the expected signer inside the pipeline and at deploy.

## Design reviews

For a new component or exposed endpoint, run the short threat model, compliance mapping and policy-as-code checks in `references/design-review.md`.

## When related skills are missing

Without `opsgate-orchestrator`, still never apply, deploy, delete or destroy without the user's yes for that specific action, given after they have seen what it will do.
