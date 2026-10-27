# Design review: threat model, compliance and policy as code

## Short threat model

For each new component, data flow or exposed endpoint, answer one line per STRIDE category:

| Threat | Question |
|--------|----------|
| Spoofing | Who can call this, and how is the caller authenticated? |
| Tampering | Can data or code be changed in transit, at rest or in the pipeline? |
| Repudiation | Are actions logged with who did them, in a place the actor can't edit? |
| Information disclosure | What sensitive data is stored, logged or returned, and who can read it? |
| Denial of service | What limits stop one caller or a bug from exhausting it? |
| Elevation of privilege | Can a caller or a compromised component gain more access than intended? |

Turn each real risk into a control or an accepted risk with an owner, listed in a table (risk, control or accepted risk, owner). Ask the questions that would change the model, such as who uses it, what money or rate limits apply, and which data it shows.

## Compliance mapping

When a standard applies (PCI DSS, HIPAA, SOC 2, GDPR, ISO 27001), map each relevant requirement to a concrete control and its evidence: the setting, the log, the review record. Keep the mapping next to the architecture record. Don't claim compliance from configuration alone, because most standards also need processes and audits.

## Policy as code

Use policy checks for rules that must always hold, so reviews can focus on judgment:

- IaC policies in the pipeline (for example Checkov custom policies, or OPA with Conftest) for rules like "no public buckets" or "required tags".
- Cloud guardrails that hold even outside the pipeline, such as service control policies that deny disabling audit logging. Service control policies don't apply to the management account or to service-linked roles.
- Admission policies in Kubernetes clusters for image signatures and pod security.

Each policy names its owner and the exception process, so a blocked team knows how to proceed.
