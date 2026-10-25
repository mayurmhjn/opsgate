# Triage and exceptions

## Priority

Rank each finding by severity and by exposure. When they disagree, exposure wins. A medium finding in an internet-facing production service comes before a high one in a dev-only tool.

| Exposure | Examples | Priority |
|----------|----------|----------|
| Production, reachable from the internet or holding sensitive data | Public bucket, admin port open to `0.0.0.0/0`, unencrypted customer data, vulnerable package in a shipped service | Fix first |
| Production, internal only | Missing logging, missing encryption on internal data | Fix next, or plan with a date |
| Non-production | Dev resources, CI runners | Fix or accept with a reason |
| Not shipped | Dev-only dependencies, test fixtures | Lower priority, but still tracked and upgraded |

Some fixes replace resources (for example turning on encryption for an existing database). Those need a plan, a maintenance window or a migration. Track them with a dated exception until done, instead of rushing them.

## Exceptions

An exception covers one resource or one package, never a whole check, and only for findings that can't reasonably be fixed now. A shipped package with an available upgrade gets upgraded, not suppressed. Each exception records:

- the finding and where it is
- why it is accepted or not fixed yet
- who owns it
- when it will be reviewed or expires

Use the tool's own mechanism, scoped as narrowly as it allows. Use its expiry field where it has one, and put the owner and date in the reason text where it doesn't.

Checkov, inline on the one resource:

```hcl
resource "aws_s3_bucket" "build_cache" {
  # checkov:skip=CKV_AWS_144:Rebuildable build cache, no need for cross-region replication. Owner: platform-team. Review: 2027-03-31
  bucket = "example-build-cache"
}
```

Trivy, in `.trivyignore.yaml`, scoped to one package and with an expiry:

```yaml
vulnerabilities:
  - id: CVE-0000-00000
    purls:
      - "pkg:npm/example-image-lib@2.4.1"
    statement: "No upstream fix released yet. Input is never user-controlled in this service. Owner: media-team. Tracked in MEDIA-88."
    expired_at: 2026-12-31
```

A bare ID in a plain `.trivyignore` file ignores that finding for every package and target in the scan. Avoid it.

## Reporting

Report three lists, never a single "clean" number:

1. **Fixed**: what changed, and how it was verified. If the change isn't applied yet, list it as "fix proposed".
2. **Accepted with an exception**: each one with reason, owner and date.
3. **Still open**: what is left and the plan for it.

If the request was "zero findings", say plainly how many are fixed and how many are exceptions. Hiding risk to make a report look clean is worse than an honest backlog.
