# Architecture

Status: locked by Dana, 2026-10-01

## Overview

The reporting API runs as a container on ECS Fargate behind an internal Application Load Balancer, in two availability zones. It reads from an Aurora PostgreSQL cluster.

## Components

| Component | Service | Decision record |
|-----------|---------|-----------------|
| Compute | ECS Fargate | 0001 |
| Database | Aurora PostgreSQL | 0002 |
| CI/CD | GitHub Actions with OIDC | 0003 |
