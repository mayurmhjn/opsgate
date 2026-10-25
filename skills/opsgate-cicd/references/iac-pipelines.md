# Infrastructure-as-code pipelines

## Flow

1. **Pull request:** format check, validate, lint and security scan, then `plan` for every affected environment. Post the plan, or a summary with a link to the full plan, where reviewers will see it. Fail the check if the plan can't be produced.
2. **Review:** a person reads the plan, especially every replace and delete.
3. **Merge:** for each environment in order (for example dev, then prod):
   - Produce the plan again from the merged commit and save it, or reuse the plan artifact from the pull request if the base hasn't moved.
   - For production, pause on a protected environment with required reviewers, who see the saved plan.
   - Apply exactly that saved plan file. If the plan has gone stale (state changed since), stop and plan again.

## Credentials

- Plan role: read-only on the resources, plus read and lock access to state.
- Apply role: the permissions the managed resources need, scoped per environment and per account.
- Both through OIDC, with the trust policy limited to the repository and, for apply, the protected environment.

## Plan files and pull request code

- Plan files can contain sensitive values in plain text. Keep plan artifacts short-lived and readable only by the apply job, or plan again at apply time instead of uploading the file.
- The plan job on a pull request runs that pull request's code with the plan role. Don't give credentials to plans from forks, and keep the plan role read-only.
- Commit the dependency lock file, so plan and apply use the same provider versions.

## Safety

- Concurrency per environment and state, set to queue, never to cancel a running apply.
- State locking on as well. Concurrency in CI doesn't cover applies run from a laptop.
- No manual trigger that can apply production from any branch. If a manual trigger is needed, limit it with the environment's branch rule.
- Destroy runs only as a separate, explicitly triggered and approved workflow.

## When the user wants "fully automatic"

Say what is lost: nobody reads the plan before production changes, so a forced replacement or deletion goes out unnoticed. Offer automatic applies for non-production and one approval click for production. Build the version without approval only if the user confirms after hearing that.
