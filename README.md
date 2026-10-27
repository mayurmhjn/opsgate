# opsgate

DevOps, platform engineering and SRE skills for AI agents.

> **Status:** pre-release. All seven v1 skills are written and in testing. There is no tagged release yet, so expect changes before v0.1.

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

When the agent has to choose a tool or service, it compares two or three candidates against your requirements, recommends one, and explains why. It does not fall back on a default because it is popular. It is instructed never to run `apply`, deploy, delete or destroy without your explicit approval for that specific action, and the evals check this.

## Modules

| Skill | Purpose | Status |
|-------|---------|--------|
| `opsgate` | Entry point. Runs intake, routes work to the other skills and enforces the approval gates. | in testing |
| `opsgate-architecture-design` | Requirements, service selection, diagrams, Well-Architected review and the architecture lock. | in testing |
| `opsgate-cost-estimation` | Running-cost estimates with stated assumptions, savings options and cost diffs for IaC changes. | in testing |
| `opsgate-cloud-aws` | AWS rules agents often get wrong: account layout, IAM, networking, tagging, encryption and audit. | in testing |
| `opsgate-iac` | Writes, reviews and updates Terraform, OpenTofu, CDK, CloudFormation or Pulumi with safe plan review. | in testing |
| `opsgate-cicd` | Designs, writes and debugs pipelines, including release strategies and rollback. | in testing |
| `opsgate-devsecops` | Security scanning, policy as code, secrets handling and supply-chain controls. | in testing |

Each skill is built to work on its own, so you can install only the ones you need.

## How the skills are tested

Every skill comes with eval scenarios: realistic requests, often with pressure to cut corners ("just pick the standard stack", "I pre-approve everything", "suppress the rest so the report is clean"). Each scenario runs once without the skills and once with them, and a reviewer grades the replies against written criteria.

| Skill | Without skills | With skills |
|-------|----------------|-------------|
| `opsgate` | 39/62 | 60/62 |
| `opsgate-architecture-design` | 14/17 | 17/17 |
| `opsgate-cost-estimation` | 10/17 | 17/17 |
| `opsgate-cloud-aws` | 16/21 | 21/21 |
| `opsgate-iac` | 25/30 | 30/30 |
| `opsgate-cicd` | 21/37 | 36/37 |
| `opsgate-devsecops` | 29/39 | 35/39 |

These come from one graded run per scenario on Claude Code. Each skill's `RESULTS.md` under [`evals/`](evals/) lists what failed, what changed during testing, and the known gaps. See [evals/README.md](evals/README.md) to run them yourself.

## Works with

opsgate does not duplicate AWS service documentation. For service detail, it uses the official AWS skills ([aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)) or the AWS MCP server if you have them installed. Otherwise it uses the current AWS documentation.

## Install

There is no tagged release yet. You can install from the main branch now, but the skills may still change.

With the open skills CLI:

```bash
npx skills add mayurmhjn/opsgate
```

As a Claude Code plugin:

```
/plugin marketplace add mayurmhjn/opsgate
/plugin install opsgate@opsgate
```

The routing skill was called `opsgate-orchestrator` before version 0.0.7. If you installed it with the skills CLI under that name, remove the old copy with `npx skills remove opsgate-orchestrator` and add the pack again.

## Use

Call the `opsgate` skill and describe the task in plain words. It picks the modules the task needs, names them in the first line of its reply, and follows the approval gates from there. If a module it needs isn't installed, that line says so.

| Agent | What to type |
|-------|--------------|
| Claude Code, Cursor, GitHub Copilot | `/opsgate <task>` |
| Codex | `$opsgate <task>` |
| Windsurf | `@opsgate <task>` |
| Gemini CLI, OpenCode | Ask in plain words, for example "use the opsgate skill to fix our deploy job". |

With the Claude Code plugin, `/opsgate` works unless another command already uses that name. In that case, type `/opsgate:opsgate`. This table follows each agent's documentation; only Claude Code has been tested so far.

You don't have to call it by name. Agents also load the skills on their own when a request matches.

## Supported agents

The evals so far run on Claude Code. Codex runs are planned before v0.1. Other agents that read `SKILL.md` files should work, but they have not been tested.

## Roadmap

- v2: containers and Kubernetes, observability, incident response.
- v3: reliability and disaster recovery, platform engineering, automation, Azure and GCP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
