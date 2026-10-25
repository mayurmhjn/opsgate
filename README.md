# opsgate

DevOps, platform engineering and SRE skills for AI agents.

> **Status:** pre-release and under active development. Nothing is published yet, and the skills listed below are still being written.

## What it does

AI coding agents know a lot about Terraform, pipelines and AWS, yet they often skip the habits an experienced engineer brings to the job. They pick a service before asking what the system needs, leave cost out of the design, and run changes nobody reviewed. opsgate is a set of skills that makes the agent work through those steps.

Work moves through stages, and the agent stops for your approval at the end of each one:

1. Intake: is this a new project or a change to a running system, and where do you want to start?
2. Requirements: availability, scale, data sensitivity, compliance, budget, team skills, and the tools you already use.
3. Architecture: services, diagrams and a running-cost estimate, reviewed with you and then locked.
4. Plan: a phased implementation plan built from the locked architecture.
5. Implement: infrastructure as code, pipelines, security controls and baseline monitoring.
6. Review: code review, security scans, a cost diff, and a check that the build still matches the locked design.
7. Record: each stage leaves Markdown notes and decision records in your repository under `docs/opsgate/`.

Small jobs on an existing system, like fixing a failed pipeline run, go straight to the stage they belong to.

When the agent has to choose a tool or service, it compares two or three candidates against your requirements, recommends one, and explains why. It does not fall back on a default because it is popular. It never runs `apply`, deploy, delete or destroy without your explicit approval for that specific action.

## Modules

| Skill | Purpose | Status |
|-------|---------|--------|
| `opsgate-orchestrator` | Entry point. Runs intake, routes work to the other skills and enforces the approval gates. | in testing |
| `opsgate-architecture-design` | Requirements, service selection, diagrams, Well-Architected review and the architecture lock. | planned |
| `opsgate-cost-estimation` | Running-cost estimates with stated assumptions, savings options and cost diffs for IaC changes. | planned |
| `opsgate-cloud-aws` | AWS rules agents often get wrong: account layout, IAM, networking, tagging, encryption and audit. | planned |
| `opsgate-iac` | Writes, reviews and updates Terraform, OpenTofu, CDK, CloudFormation or Pulumi with safe plan review. | planned |
| `opsgate-cicd` | Designs, writes and debugs pipelines, including release strategies and rollback. | planned |
| `opsgate-devsecops` | Security scanning, policy as code, secrets handling and supply-chain controls. | planned |

Each skill is built to work on its own, so you can install only the ones you need.

## Works with

opsgate does not duplicate AWS service documentation. For service detail, it uses the official AWS skills ([aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)) or the AWS MCP server if you have them installed. Otherwise it uses the current AWS documentation.

## Install

Available from v0.1.

With the open skills CLI:

```bash
npx skills add mayurmhjn/devops-skills
```

As a Claude Code plugin:

```
/plugin marketplace add mayurmhjn/devops-skills
/plugin install opsgate@opsgate
```

## Supported agents

v0.1 will be tested on Claude Code and Codex. Other agents that read `SKILL.md` files should work, but they have not been tested.

## Roadmap

- v2: containers and Kubernetes, observability, incident response.
- v3: reliability and disaster recovery, platform engineering, automation, Azure and GCP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
