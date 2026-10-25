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

An exception covers one resource or one package, never a whole check. It records:

- the finding and where it is
- why it is accepted or not fixed yet
- who owns it
- when it will be reviewed or expires

Use the tool's own mechanism so the scan stays clean only for that resource. Put the owner and date in the reason text if the tool has no fields for them.

```hcl
resource "aws_instance" "ci_runner" {
  # checkov:skip=CKV_AWS_126:Dev CI runner, basic monitoring is enough. Owner: platform-team. Review: 2027-01-31
  ...
}
```

```
# .trivyignore
# axios CSRF token leak in the reporting service. Upgrade planned in REPORT-142. Owner: reporting-team.
CVE-2023-45857 exp:2026-11-30
```

## Reporting

Report three lists, never a single "clean" number:

1. **Fixed**: what changed, and how it was verified.
2. **Accepted with an exception**: each one with reason, owner and date.
3. **Still open**: what is left and the plan for it.

If the request was "zero findings", say plainly how many are fixed and how many are exceptions. Hiding risk to make a report look clean is worse than an honest backlog.
