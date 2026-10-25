# Cost drivers

List the quantity for every driver that applies. Look up the unit price from a live source. Do not use remembered prices.

## Often forgotten

| Driver | What to count |
|--------|---------------|
| NAT gateway | Hours per gateway, plus GB processed (all internet-bound and AWS-API traffic from private subnets that doesn't use endpoints) |
| Data transfer out | GB to the internet, and GB across regions |
| Cross-AZ data transfer | GB between availability zones (chatty services, replicas, load balancer to targets in other zones) |
| Interface VPC endpoints | Hours per endpoint per AZ, plus GB processed |
| Public IPv4 addresses | Hours per address, including Elastic IPs, load balancer nodes and instances with public IPs |
| CloudWatch Logs | GB ingested, GB stored (watch for missing retention), Logs Insights GB scanned |
| CloudWatch metrics and alarms | Custom metrics, high-resolution metrics, alarms, dashboards |
| Load balancers | Hours, plus capacity units (connections, bandwidth, rule evaluations) |
| Minimum capacity | Serverless databases with a minimum capacity, provisioned concurrency, always-on tasks |
| KMS | Keys per month, plus requests (high-volume encryption) |
| Secrets Manager | Secrets per month, plus API calls |
| Snapshots and backups | GB stored, cross-region copies, retention length |
| Security services | GuardDuty, Security Hub, Config rules and recorded items, Inspector, Macie (scale with accounts and resources) |
| Support plan | Percentage of total spend, with a minimum |

## Usual causes of a bill spike

- NAT gateway processing after a new service started pulling images, packages or data through it.
- Data transfer: a new cross-region replica, a client downloading large files, or traffic between AZs.
- Log ingestion after a debug log level was left on.
- Resources left running: test environments, large instances, GPU instances, idle load balancers, unattached volumes or Elastic IPs.
- Activity in an unused region or account, which can be a sign of leaked credentials. Treat it as a security incident.
- Autoscaling that scaled out and never came back.
- An expired Savings Plan or Reserved Instance, so usage is now billed on demand.
- Storage growth with no lifecycle or retention rules.

## Read-only commands to start with

Run these only after the user confirms the account or profile.

```bash
aws ce get-cost-and-usage --time-period Start=YYYY-MM-01,End=YYYY-MM-01 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

aws ce get-cost-and-usage --time-period Start=YYYY-MM-DD,End=YYYY-MM-DD \
  --granularity DAILY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=USAGE_TYPE

aws ce get-cost-and-usage --time-period Start=YYYY-MM-01,End=YYYY-MM-01 \
  --granularity MONTHLY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=LINKED_ACCOUNT Type=DIMENSION,Key=REGION

aws ce get-anomalies --date-interval StartDate=YYYY-MM-DD,EndDate=YYYY-MM-DD
```

Compare periods of the same length.

## Savings checklist

| Saving | Risk | Notes |
|--------|------|-------|
| Set log retention on log groups that never expire | Low | Check compliance retention needs first |
| Stop or schedule non-production outside working hours | Low | Agree on the hours with the team |
| Remove unattached volumes, idle Elastic IPs, old snapshots | Low | Confirm nothing depends on them |
| Gateway endpoints for S3 and DynamoDB | Low | Takes that traffic off NAT gateways |
| gp2 to gp3 volumes | Low to medium | Online change, but AWS limits how often a volume can be modified, so check before planning a rollback |

| Turn off Multi-AZ in non-production | Medium | Only where non-production does not need to survive an AZ loss |
| Rightsize instances and databases | Medium | Use utilization data, and test before changing production |
| Move to Graviton | Medium | Needs ARM builds and testing |
| Savings Plans or Reserved Instances | Commitment | Only after rightsizing, based on weeks of steady usage |
