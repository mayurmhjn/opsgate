# Disaster recovery strategies

Recovery targets come from the business. RTO is how long the service can be down. RPO is how much recent data can be lost. Pick the cheapest strategy that meets both, then confirm the cost with the user.

| Strategy | What runs in the recovery region | Typical RTO | Typical RPO | Running cost |
|----------|----------------------------------|-------------|-------------|--------------|
| Backup and restore | Nothing. Backups and images are copied there. | Hours | Hours (time since the last backup copy) | Lowest |
| Pilot light | Data replicated continuously. Compute defined in code but off or at zero. | Tens of minutes to hours | Seconds to minutes | Low |
| Warm standby | Data replicated. A scaled-down copy of the full stack runs and can serve traffic at once, at reduced capacity until it scales up. | Minutes | Seconds to minutes | Medium |
| Active-active | Full stack in both regions serving traffic. | Near zero | Near zero, but writes need a conflict strategy | Highest |

These ranges are typical, not guarantees. Measure them in a failover test.

## Matching targets to mechanisms

- An RPO of minutes or less needs continuous replication of the data store, for example a cross-region database replica, global tables, or S3 replication. Periodic snapshot copies cannot meet it.
- An RTO of minutes needs compute already running, or able to start well inside the RTO, plus capacity and quotas available in the recovery region.
- Replication copies corruption and deletions too. Point-in-time recovery or isolated backups are still needed for those events.

## Failover design checklist

- Failover is either automatic or manual, and every component follows the same choice. Automatic DNS failover only works if the database promotes automatically too. Otherwise, use a runbook that moves traffic as the last step.
- Failover must not depend on control-plane calls that may be unavailable during the event, such as editing DNS records or creating resources. Move traffic with data-plane mechanisms: health-check-driven failover records, or routing controls such as Route 53 Application Recovery Controller.
- Dependencies exist in the recovery region: secrets, keys, images, parameters, DNS, CI/CD access and third-party allowlists.
- Writes are fenced, so the old primary cannot accept writes after failover.
- Failback is planned: how data is resynchronized and how traffic moves back.
- Failover is tested on a schedule, with the measured RTO and RPO recorded.
