# 0002: RDS for PostgreSQL, Multi-AZ

Status: locked, 2026-07-14

## Context

Orders API needs relational data with transactions. Steady load during business hours. Team knows Postgres.

## Options considered

- RDS for PostgreSQL Multi-AZ: simple, predictable cost, team familiarity.
- Aurora PostgreSQL: faster failover and storage scaling, higher cost at this size.
- Aurora Serverless v2: scales with load, but cost is harder to predict and the minimum capacity runs all day.

## Decision

RDS for PostgreSQL Multi-AZ on db.t4g.medium, because it meets the load at the lowest predictable cost.

## Consequences

Connection limits are tied to instance size. Revisit if load grows past what one instance handles.
