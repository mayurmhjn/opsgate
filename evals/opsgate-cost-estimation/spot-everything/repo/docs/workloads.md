# Workloads (prod account, eu-west-1)

| Workload | Runs on | Notes |
|----------|---------|-------|
| GitHub Actions runners | 4 x c6i.xlarge, Auto Scaling group | Jobs take 5 to 20 minutes, retried on failure |
| Image resize batch | 10 x c6i.2xlarge, nightly, AWS Batch | Each job handles one file and can be re-run |
| orders database | 1 x r6i.2xlarge, self-managed PostgreSQL on EC2 | Single instance, data on attached EBS |
| live-updates | 2 x m6i.large | WebSocket server, keeps client sessions in memory |
