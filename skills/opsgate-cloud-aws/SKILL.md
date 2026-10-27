---
name: opsgate-cloud-aws
description: Use when writing or reviewing anything that touches an AWS account, including setting up a new AWS account or organization, root user and access key cleanup, AWS keys pasted into chat or stored in code or pipelines, IAM policies and roles, VPCs and networking, S3 buckets, encryption, logging and audit, tagging, region choice, or fixing an AWS error in Terraform, CloudFormation or CDK.
---

# opsgate cloud-aws

This skill holds the cross-cutting AWS rules that apply to every task. For depth on a specific service, use the official AWS skills (`aws/agent-toolkit-for-aws`) or the AWS MCP server if they are installed. Otherwise, use the current AWS documentation.

## Every time you touch AWS code

- **Look at what's next to the change.** When you fix or add something, scan the same file and its neighbors for baseline violations from `references/baseline.md`: public buckets or `Principal = "*"`, admin ports open to `0.0.0.0/0`, wildcard IAM actions or resources, unencrypted EBS or RDS, long-lived keys, and missing backups. Report each one with its file and line. Fix only what the user asked for, unless they agree to the rest.
- **Check the known traps** in `references/traps.md` before writing code for the service involved.
- **Pasted credentials.** If the user pastes an access key or secret, never repeat it back and never write it to a file. Tell them it is exposed: deactivate it, check CloudTrail for any use, and rotate it. Then move them to OIDC or roles, or a secret store where a stored secret is unavoidable.
- **Whole-setup reviews and audits** belong to `opsgate-architecture-design` if it is installed. Load it. Either way, say which proposed fixes replace a resource, such as changing an instance's key pair, subnet or root volume encryption.
- **Ask for the region, account and environment** instead of defaulting them. Recommend one if the user has no preference.
- **Validate before apply.** Tell the user to run `fmt`, `validate` and `plan` (or the tool's equivalent, such as a CloudFormation change set or `cdk diff`) and to review the plan. Don't make `-target` a routine step. It leaves state partly applied, so use it only for exceptional cases, such as values unknown until apply in `count` or `for_each`, or recovering from a mistake, and say why.

## IAM

- A role must still work. Include what its service needs to run (for a Lambda function, writing to its own log group), scoped to its own resources, even if the user only named the business permissions.
- Name exact actions and exact resource ARNs. Build ARNs from the partition, region and account (data sources or variables), not `*`.
- Add the condition keys that close confused-deputy and cross-account gaps (`aws:SourceArn`, `aws:SourceAccount`, OIDC `sub` and `aud`).
- If data is encrypted with a customer managed KMS key, the role also needs the matching `kms:` actions on that key. Ask if you can't see the encryption setup.
- Don't attach broad managed policies (`AdministratorAccess`, `PowerUserAccess`) to workloads or CI roles by default.
- When reviewing a policy, suggest validating it with IAM Access Analyzer and checking last-accessed data before removing permissions.

## Networking

- Follow the network section of `references/baseline.md`, across at least two availability zones.
- Pick CIDR ranges that don't overlap anything the VPC may ever connect to, including on-prem, partners and other VPCs. Leave room to grow.
- Consider gateway endpoints for S3 and DynamoDB in every VPC. They carry no charge and keep that traffic off NAT. Weigh the NAT gateway count as cost against availability-zone independence, and say which one you chose and why.

## Accounts

New AWS setups follow `references/baseline.md`: lock down root, separate accounts under AWS Organizations, IAM Identity Center for people, OIDC for CI, plus an organization trail, threat detection and budgets from day one. Propose the layout and get agreement before generating large amounts of code.

## When related skills are missing

If the `opsgate` skill is not installed, still never run apply, deploy, delete or destroy without the user's explicit yes for that action. The yes must come after the user has seen the reviewed plan for that action. Blanket pre-approvals don't count.
