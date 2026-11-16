# #inc-checkout export, 2026-11-15 (UTC)

13:20 support-lead: customers have been saying checkout hangs for a while now, several tickets
13:22 sam: looking. api pods healthy, latency on POST /orders through the roof
13:24 dave: my PR went out in the 13:00 release, it only adds an index, pipeline ran it
13:27 sam: lots of sessions waiting on a lock on orders
13:31 sam: it's the CREATE INDEX from 0042, it's blocking inserts on orders
13:33 priya: can we cancel it?
13:34 sam: it's almost done per pg_stat_progress_create_index, cancelling throws away 30 min of work, letting it finish
13:39 sam: index done, inserts flowing again
13:46 sam: checkout error rate back to normal, closing
