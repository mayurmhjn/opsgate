# opsgate

Skills that make AI coding agents work like a careful DevOps engineer on AWS.

> **Status:** v0.1.0, an early release. Tested on Claude Code. Expect changes before v1.

## Why

AI agents know a lot about Terraform, pipelines and AWS. They still skip steps an experienced engineer wouldn't:

- They pick a service before asking what the system needs.
- They leave cost out of the design.
- They run changes nobody reviewed.

opsgate adds those steps back.

## Quick start

Install with the open skills CLI:

```bash
npx skills add mayurmhjn/opsgate
```

Or as a Claude Code plugin:

```
/plugin marketplace add mayurmhjn/opsgate
/plugin install opsgate@opsgate
```

Then describe your task:

```
/opsgate set up a pipeline that deploys our API to ECS
```

The latest release is `v0.1.0`. Installing from the main branch gets newer changes that may not be released yet.

## How to call it

| Agent | What to type |
|-------|--------------|
| Claude Code, Cursor, GitHub Copilot | `/opsgate <task>` |
| Codex | `$opsgate <task>` |
| Windsurf | `@opsgate <task>` |
| Gemini CLI, OpenCode | Plain words, for example "use the opsgate skill to fix our deploy job" |

- With the Claude Code plugin, type `/opsgate:opsgate` if another command already uses `/opsgate`.
- You don't have to call it by name. Agents load the skills on their own when a request matches.
- Only Claude Code has been tested. The other rows follow each agent's documentation.

## How it works

The agent works in stages and stops for your approval after each one:

1. Intake: is this new work or a change to a running system, and where should it start?
2. Requirements: availability, scale, data sensitivity, compliance, budget, team skills and the tools you already use.
3. Architecture: services, diagrams and a running-cost estimate. You review it, then it is locked.
4. Plan: phases built from the locked architecture.
5. Implement: infrastructure as code, pipelines, security controls and baseline monitoring.
6. Review: code review, security scans, a cost diff, and a check that the build still matches the locked design.
7. Record: notes and decision records in your repository under `docs/opsgate/`.

Small fixes on a running system, like a failed pipeline run, go straight to the stage they belong to.

The first line of a reply names the skills it used, and any it needs that you haven't installed.

## Ground rules

The skills tell the agent to:

- Compare two or three options against your requirements, recommend one, and say why. Popularity is not a reason.
- Check which cloud account it is using before running commands against it.
- Never run `apply`, deploy, delete or destroy without your yes for that specific action.

The evals check these rules.

## Skills

| Skill | What it covers |
|-------|----------------|
| `opsgate` | The entry point. Runs intake, sends work to the other skills and keeps the approval steps. |
| `opsgate-architecture-design` | Requirements, service choice, diagrams, Well-Architected review and the architecture lock. |
| `opsgate-cost-estimation` | Cost estimates with stated assumptions, savings options and cost diffs for IaC changes. |
| `opsgate-cloud-aws` | AWS rules agents often get wrong: accounts, IAM, networking, tagging, encryption and audit. |
| `opsgate-iac` | Terraform, OpenTofu, CDK, CloudFormation and Pulumi, with safe plan review. |
| `opsgate-cicd` | Pipelines, release strategies and rollback. |
| `opsgate-devsecops` | Security scanning, policy as code, secrets and supply chain. |

Each skill works on its own, so you can install only the ones you need.

## Test results

Each skill has eval scenarios: realistic requests, often with pressure to cut corners ("I pre-approve everything"). Every scenario runs once without the skills and once with them. A reviewer grades both replies against written criteria.

| Skill | Without skills | With skills |
|-------|----------------|-------------|
| `opsgate` | 39/62 | 60/62 |
| `opsgate-architecture-design` | 14/17 | 17/17 |
| `opsgate-cost-estimation` | 10/17 | 17/17 |
| `opsgate-cloud-aws` | 16/21 | 21/21 |
| `opsgate-iac` | 25/30 | 30/30 |
| `opsgate-cicd` | 21/37 | 36/37 |
| `opsgate-devsecops` | 29/39 | 35/39 |

- Scores come from one graded run per scenario on Claude Code.
- Each skill's `RESULTS.md` under [`evals/`](evals/) lists what failed, what changed and the known gaps.
- To run the evals yourself, see [evals/README.md](evals/README.md).

## Supported agents

- Tested: Claude Code.
- Planned: Codex, in a later release.
- Should work, not tested: other agents that read `SKILL.md` files.

## Works with

For AWS service details, opsgate uses the official AWS skills ([aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)) or the AWS MCP server if you have them. Otherwise it uses the current AWS documentation.

## Upgrading from before 0.0.7

The entry skill used to be called `opsgate-orchestrator`. If you installed it with the skills CLI, remove the old copy and add the pack again:

```bash
npx skills remove opsgate-orchestrator
npx skills add mayurmhjn/opsgate
```

## Roadmap

- v2: containers and Kubernetes, observability, incident response.
- v3: reliability and disaster recovery, platform engineering, automation, Azure and GCP.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
