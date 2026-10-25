# Releases and rollback

## Choosing a release strategy

Compare these against the team's needs: downtime tolerance, how quickly a bad release must be caught, cost of running two versions, and whether the platform supports traffic shifting.

| Strategy | How it works | Good for | Cost |
|----------|--------------|----------|------|
| Rolling | Replace instances or tasks a few at a time | Most stateless services | Low. A bad version reaches users gradually |
| Blue/green | Run the new version alongside the old one, switch traffic, keep the old one for fast rollback | Fast, clean rollback | Two environments during the switch |
| Canary | Send a small share of traffic to the new version, watch metrics, then widen | Catching problems with real traffic | Needs traffic shifting and good metrics |

Whichever one you choose, tie automatic rollback to health checks and alarms (error rate, latency), not only to deploy success.

## Rollback checklist

1. **Find the last known-good artifact.** List the images or packages that were deployed and confirm the tag or digest, for example with the registry's describe or list command. Redeploy that artifact through the normal deploy path. Don't rebuild from old source, because builds aren't guaranteed to be reproducible.
2. **Check what else changed.** Database migrations, config, secrets, feature flags, infrastructure. A migration that dropped or renamed something can make the old version fail even after a clean redeploy.
3. **Protect data first.** Take a database snapshot or backup before running any corrective change to the database.
4. **Get a yes.** Show the exact command or workflow run, the artifact it deploys, and any database steps, then wait for an explicit yes.
5. **Verify.**
   - The deploy finished and the service is stable.
   - Health checks pass.
   - Error rate and latency are back to normal.
   - The broken user flow works again, checked with a smoke test.
6. **Follow up.** Keep the bad version from redeploying automatically, record what happened, and fix forward when ready.

## Migrations that keep rollback possible

Prefer expand and contract: add new columns or tables first, deploy code that works with both, and remove the old ones only in a later release once rollback is no longer needed.
