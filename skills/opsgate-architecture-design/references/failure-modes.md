# Failure modes

Fill in one row per event for the proposed design. An empty cell means the design has no answer yet, so list it as a risk.

| Event | Compute | Data | Network and edge | User impact | Recovery |
|-------|---------|------|------------------|-------------|----------|
| One availability zone lost | | | | | |
| Key dependency down (database, queue, third-party API, identity provider) | | | | | |
| Bad deploy or bad config change | | | | | |
| Data corrupted or deleted (including by ransomware or a script) | | | | | |
| Region lost | | | | | |
| Credentials leaked | | | | | |
| Traffic spike above the planned peak | | | | | |

## Questions to ask for each tier

- How many copies run, and in how many availability zones?
- What happens to requests in flight when one copy dies?
- Is there a limit that blocks scaling, such as connection limits, service quotas, concurrency or IP space?
- How is it backed up, how far back can it be restored, and has a restore been tested?
- Can one person's mistake delete it? Check deletion protection, versioning and backup vault locks.

## Common single points of failure

- One instance, task or node behind a load balancer.
- One NAT gateway serving all availability zones.
- A single-AZ database, cache or file system.
- One region for DNS, secrets or the CI system that deploys the fix.
- A single person who holds the only admin access.
