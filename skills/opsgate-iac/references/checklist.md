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

- Tool version, every provider and every module source pinned with constraints within one major version.
- Dependency lock file committed.
- Upgrades done on purpose, with a plan review, not by an unpinned constraint.

## Inputs and secrets

- No account IDs, regions or ARNs hard-coded where a data source or variable fits.
- No secrets in code, variable files or committed files. Prefer the service managing its own secret (for example RDS-managed master passwords), or read secrets from a secret store. Mark sensitive variables, and use write-only or ephemeral options where the tool supports them.
- Variables have types, descriptions and validation where a wrong value would hurt.

## Safety

- Delete protection on stateful resources (`prevent_destroy`, deletion protection, termination protection, Pulumi `protect`).
- Retain policies where a removed or replaced resource must survive. They leave it orphaned rather than blocking the change.
- Backups or point-in-time recovery on before risky changes.
- Default tags applied at the provider level.

## Workflow

1. Format check.
2. Validate.
3. Lint (for example `tflint`) and security scan (with `opsgate-devsecops` if installed).
4. Native tests for modules and constructs (`terraform test` or `tofu test`, CDK assertions, Pulumi unit tests).
5. A plan or change set, reviewed by a person.
6. Apply exactly what was reviewed where the tool supports it. Otherwise, re-check the deploy output.
7. In CI, plan on pull requests and apply only after approval (with `opsgate-cicd` if installed).

## Equivalents in other tools

Check the current documentation for anything marked unstable or preview. These features change.

| Need | Terraform / OpenTofu | CloudFormation / SAM | CDK | Pulumi |
|------|----------------------|----------------------|-----|--------|
| Preview | `plan -out` (exact apply) | change set (exact apply) | `cdk diff` (advisory), or a prepared change set | `preview` (advisory), or a saved update plan |
| Fail on delete | `prevent_destroy` | termination protection, stack policy | termination protection | `protect` |
| Keep a resource when removed or replaced | `removed` block that keeps it | `DeletionPolicy` and `UpdateReplacePolicy: Retain` | `RemovalPolicy.RETAIN` | `retainOnDelete` |
| Rename without replacing | `moved` block | stack refactoring | keep the construct ID, `overrideLogicalId`, or `cdk refactor` (unstable) | `aliases` |
| Adopt an existing resource | `import` block | resource import | `cdk import` | `import` |
| Detect drift without changing state | `plan -refresh-only` | drift detection | CloudFormation drift detection | `preview --refresh` |
