# 0003: Run the API on ECS Fargate

Status: locked, 2026-09-02

## Context

Two stateless services, steady traffic of about 200 requests per second, a team of four with no Kubernetes experience, and a goal of keeping operations work low.

## Options considered

- ECS Fargate: no cluster or nodes to manage, fits the team's skills, per-task pricing.
- EKS: more flexible and portable, but needs cluster upgrades, add-on management and Kubernetes skills.
- Lambda: request duration and container size limits ruled it out for the report service.

## Decision

ECS Fargate, because it meets the scale with the least operational work for this team.

## Consequences

Kubernetes-specific tooling is out of scope. Revisit if the team grows a platform function or needs Kubernetes-only tools.
