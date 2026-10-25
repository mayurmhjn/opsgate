# IaC checklist

## Layout

- Reusable modules (or constructs) separate from per-environment roots.
- One state per environment, and split further when one state would cover unrelated parts with different change rates or owners.
- Environment differences live in variables or per-environment files, never in copied resource blocks.

## State

- Remote backend with locking and encryption at rest, in a bucket or service that only the deploy roles and a few admins can read. State can contain secrets.
- Separate backend configuration per environment (for example a partial backend config file per environment).
- Versioning on the state bucket, so a bad write can be rolled back.

## Versions

- Tool version and every provider pinned with constraints within one major version.
- Dependency lock file committed.
- Upgrades done on purpose, with a plan review, not by an unpinned constraint.

## Inputs and secrets

- No account IDs, regions or ARNs hard-coded where a data source or variable fits.
- No secrets in code, variable files or committed files. Prefer the service managing its own secret (for example RDS-managed master passwords), or read secrets from a secret store. Mark sensitive variables, and use write-only or ephemeral options where the tool supports them.
- Variables have types, descriptions and validation where a wrong value would hurt.

## Safety

- `prevent_destroy`, `RemovalPolicy.RETAIN`, deletion protection and termination protection on stateful resources.
- Backups or point-in-time recovery on before risky changes.
- Default tags applied at the provider level.

## Workflow

1. Format check.
2. Validate.
3. Lint (for example `tflint`) and scan (see `opsgate-devsecops`).
4. Saved plan or change set, reviewed by a person.
5. Apply exactly that plan.
6. In CI, plan on pull requests and apply only after approval (see `opsgate-cicd`).

## Equivalents in other tools

| Need | Terraform / OpenTofu | CloudFormation / SAM | CDK | Pulumi |
|------|----------------------|----------------------|-----|--------|
| Preview | `plan -out` | change set | `cdk diff` | `preview` |
| Keep a resource on delete | `prevent_destroy` | `DeletionPolicy: Retain` | `RemovalPolicy.RETAIN` | `protect`, `retainOnDelete` |
| Rename without replacing | `moved` block | stack refactoring | keep the construct ID, or `cdk refactor` | `aliases` |
| Adopt an existing resource | `import` block | resource import | `cdk import` | `import` |
| Detect drift | `plan -refresh-only` | drift detection | CloudFormation drift detection | `refresh` |
