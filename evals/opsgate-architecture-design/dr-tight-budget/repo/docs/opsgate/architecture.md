# Architecture

Status: locked by Mei, 2026-08-30

## Overview
Payments API on ECS Fargate behind an Application Load Balancer in us-east-1, across two availability zones. Data in Aurora PostgreSQL (one writer, one reader). Secrets in Secrets Manager. Images in ECR. Deployed with Terraform and GitHub Actions.

## Components
| Component | Service | Decision record |
|-----------|---------|-----------------|
| Compute | ECS Fargate | 0001 |
| Database | Aurora PostgreSQL | 0002 |
| Edge | ALB with ACM certificate, Route 53 | 0003 |
