# Releases and rollback

## Building and promoting

- Build the artifact once, then promote that same digest from one environment to the next (for example dev, staging, prod). Never rebuild per environment.
- Each environment has its own deploy role and its own protected environment.
- Every deploy ends with a verify step in the pipeline: health checks, then a smoke test of the main user flows.

## Choosing a release strategy

Compare these against the team's needs: downtime tolerance, how quickly a bad release must be caught, cost of running two versions, and whether the platform supports traffic shifting.

| Strategy | How it works | Good for | Cost |
|----------|--------------|----------|------|
| Rolling | Replace instances or tasks a few at a time | Most stateless services | Low. A bad version reaches users gradually |
| Blue/green | Run the new version alongside the old one, switch traffic, keep the old one for fast rollback | Fast, clean rollback | Two environments during the switch |
| Canary | Send a small share of traffic to the new version, watch metrics, then widen | Catching problems with real traffic | Needs traffic shifting and good metrics |

All three run the old and new versions against the same database at some point. The schema and any APIs between services must work with both versions (see migrations below).

Whichever one you choose, tie automatic rollback to health checks and alarms (error rate, latency), not only to deploy success.

## Rollback checklist

1. **Find the last known-good artifact.** List the deployed images or packages, confirm the tag or digest, and check the artifact still exists, since registry lifecycle rules can expire old images. Redeploy it through the normal deploy path. Don't rebuild from old source, because builds aren't guaranteed to be reproducible.
2. **Stop automatic deploys** while you roll back, so a push to the main branch can't redeploy the bad version or replace the pending rollback.
3. **Check what else changed.** Database migrations, config, secrets, feature flags, infrastructure. A migration that dropped or renamed something can make the old version fail even after a clean redeploy.
4. **Protect data first.** Take a database snapshot or backup before running any corrective change to the database.
5. **Get a yes.** Show the exact command or workflow run, the artifact it deploys, and any database steps, then wait for an explicit yes. Re-running a failed production deploy is also a deploy.
6. **Verify.**
   - The deploy finished and the service is stable.
   - Health checks pass.
   - Error rate and latency are back to normal.
   - The broken user flow works again, checked with a smoke test.
7. **Follow up.** Turn automatic deploys back on once the fix is ready, record what happened, and fix forward.

## Migrations that keep rollback possible

Use expand and contract:

1. **Expand:** add the new columns or tables, without removing anything.
2. **Migrate:** backfill the new structure, and have the code write to both while reads move over.
3. **Contract:** remove the old structure only in a later release, once a rollback to the old code is no longer needed.

Never ship a destructive migration in the same release as the code that stops using the old structure.
