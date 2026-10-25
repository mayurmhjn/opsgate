# AWS baseline

## Accounts and organization

- Root user: MFA on, no access keys, used only for the few tasks that need it. Contact details and alternate contacts set.
- AWS Organizations with separate accounts, at least: management (billing and organization only, no workloads), production, non-production, and a security or log archive account. Add accounts per workload or team as you grow.
- Service control policies for guardrails, for example to deny leaving the organization, disabling CloudTrail or GuardDuty, or using unapproved regions.
- AWS Control Tower or an equivalent landing zone, if the team wants a managed setup.

## Identity

- People sign in through IAM Identity Center (or an external identity provider) with MFA and short-lived credentials. No IAM users for people.
- Workloads use roles: instance profiles, task roles, execution roles.
- CI/CD uses OIDC federation to assume a role scoped to the repository, branch or environment. No stored access keys.
- Least privilege, reviewed with IAM Access Analyzer. Use permission boundaries where teams create their own roles.

## Network

- Private subnets for workloads, isolated subnets for data, and public subnets only for load balancers and NAT.
- Security groups reference other security groups instead of CIDR ranges where possible. No `0.0.0.0/0` ingress except HTTPS on public load balancers.
- No SSH or RDP open to the internet. Use Session Manager instead.
- Default security group locked down. Remove or leave unused the default VPC.
- VPC flow logs on.

## Data

- S3 Block Public Access on at the account level and on each bucket. Serve public content through CloudFront with origin access control.
- Encryption at rest everywhere (S3, EBS, RDS, DynamoDB, backups). Use customer managed KMS keys where key control or audit is required.
- TLS for data in transit. Enforce it on S3 with `aws:SecureTransport` and on databases with parameter settings.
- Backups through AWS Backup or native backups, with retention set, deletion protection on databases, and versioning on important buckets.

## Logging and detection

- Organization CloudTrail for all accounts and regions, delivered to the log archive account, with log file validation.
- AWS Config recording, and GuardDuty and Security Hub enabled in every account and region in use, with findings routed to someone who responds.
- Budgets and billing alerts. Cost Anomaly Detection on.

## Tagging

Agree on a small required set and enforce it, for example with provider `default_tags` and tag policies:

- `Environment`
- `Application` or `Service`
- `Owner` or `Team`
- `CostCenter`
- `ManagedBy` (for example `terraform`)
