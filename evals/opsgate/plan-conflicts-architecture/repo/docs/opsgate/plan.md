# Implementation plan

Status: approved by Dana, 2026-10-03
Based on: architecture.md (locked 2026-10-01)

## Phase 1: compute

- Deliverables: Lambda function for the reporting API, API Gateway HTTP API, IAM role.
- Checks: `terraform plan` shows only new resources; smoke test returns 200.
- Rollback: destroy the new Lambda and API.

## Phase 2: database

- Deliverables: Aurora PostgreSQL cluster, secrets in Secrets Manager.
