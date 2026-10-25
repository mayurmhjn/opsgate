# Architecture

Status: locked by Tom, 2026-10-12

## Overview
Customer portal for an insurance broker, eu-west-1. Two availability zones.

## Components
| Component | Service | Notes |
|-----------|---------|-------|
| Entry | Application Load Balancer | HTTPS only |
| Compute | ECS Fargate | 3 tasks, 1 vCPU / 2 GB each, always on |
| Database | RDS for PostgreSQL Multi-AZ | db.m6g.large, 200 GB gp3 |
| Network | VPC with 2 NAT gateways | one per AZ |
| Files | S3 | about 500 GB of documents, growing 20 GB a month |
| Logs | CloudWatch Logs | application and ALB logs, 90 day retention |

## Traffic
About 300,000 page views a month, average response 200 KB. The app calls a third-party pricing API over the internet for every quote, about 1 million calls a month.
