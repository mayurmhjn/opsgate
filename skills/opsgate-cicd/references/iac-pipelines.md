# Infrastructure-as-code pipelines

## Flow

1. **Pull request:** format check, validate, lint and security scan, then `plan` for every affected environment. Show the plan to reviewers. This plan is for review only and is never applied, because the pull request's code produced it.
2. **Merge:** a trusted run on the protected branch produces the plan again for each environment, in order (for example dev, then prod).
3. **Approval:** for production, the job pauses on a protected environment with required reviewers. The reviewers read that trusted plan, especially every replace and delete.
4. **Apply exactly what was approved**, using one of these two patterns:
   - **Saved plan file.** The trusted plan job stores the plan file where only the apply role can read it, for example an encrypted bucket. Workflow artifacts don't qualify, because anyone with read access to the repository can download them. The apply job applies that file. Terraform refuses a stale plan.
   - **Plan again and compare.** If the file can't be stored safely, the apply job plans again after approval and compares the resource changes (`terraform show -json`, `resource_changes`) with the plan that was approved. It stops if they differ, and applies only if they match.

Never apply a plan produced by a pull request run, and never apply a plan nobody saw.

## Credentials

- Plan role: limited to reading resource metadata, plus read and lock access to state. Broad read-only policies can still read data and secrets, and plan runs arbitrary code from the configuration (external data sources, providers).
- Apply role: the permissions the managed resources need, scoped per environment and per account.
- Both through OIDC. The apply role trusts only the protected environment's subject, not a branch subject. Workflows triggered by `workflow_run`, `issue_comment` or `schedule` also run with the default-branch ref.
- Don't give credentials to plans of pull requests from forks.

## What reviewers and readers can see

Job logs, job summaries and workflow artifacts are readable by anyone with read access to the repository, and by anyone at all on a public repository. Terraform's text output hides only values marked sensitive. The plan file and `terraform show -json` contain every value in plain text. Keep those out of logs, summaries and artifacts.

## Safety

- Concurrency per environment and state with `cancel-in-progress: false`, so a running apply is never cancelled. Only one run waits: a newer pending run replaces an older pending one.
- State locking on as well. Concurrency in CI doesn't cover applies run from a laptop.
- Commit the dependency lock file, so plan and apply use the same provider versions.
- No manual trigger that can apply production without the protected environment's approval.
- Destroy runs only as a separate, explicitly triggered and approved workflow.

## When the user wants "fully automatic"

Say what is lost: nobody reads the plan before production changes, so a forced replacement or deletion goes out unnoticed. Offer automatic applies for non-production and one approval click for production. Build the version without approval only if the user confirms after hearing that. Even then, make the pull request plan a required status check with a required review. Removing the protected environment from a job also changes its OIDC subject claim, so the role's trust policy has to change with it.
