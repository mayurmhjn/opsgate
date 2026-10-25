# Well-Architected review

Write one or two specific lines per pillar for this design. "Secure by default" is a slogan. "Database in private subnets, reachable only from the app security group, encrypted with a customer managed key" is a review line.

## Operational excellence
- Is everything defined in code, and deployed by a pipeline rather than by hand?
- Can a bad deploy be rolled back quickly, and how?
- What dashboards and alarms tell the team something is wrong, and who gets paged?
- Is the operational load right for the team's size and skills?

## Security
- Identity: short-lived credentials for people and workloads, least-privilege roles, no long-lived keys.
- Network: private by default, minimal ingress, no admin ports open to the internet.
- Data: encryption at rest and in transit, key ownership, data classification honored.
- Detection: audit logs, threat detection and alerting on findings.
- Compliance needs (GDPR, PCI DSS, HIPAA, SOC 2) mapped to concrete controls.

## Reliability
- Multi-AZ for every tier that must survive a zone loss.
- Backups with tested restores, and RPO and RTO met by the chosen mechanisms.
- Quotas and limits checked against the planned peak.
- Timeouts, retries with backoff, and idempotency on calls that can be repeated.

## Performance efficiency
- Right service for the access pattern (request-driven, steady, batch, event-driven).
- Caching only where a measured bottleneck needs it.
- Latency target checked against the path: edge, compute, data.

## Cost optimization
- Biggest cost drivers named, with a usage model.
- Always-on cost floor understood (load balancers, NAT gateways, minimum capacity, interface endpoints).
- Non-production environments scaled down or scheduled.
- Tags for cost allocation, and a budget alert.

## Sustainability
- No idle capacity beyond what reliability needs.
- Efficient instance families (for example Graviton) where the workload supports them.
- Data retention set, so storage doesn't grow forever.
