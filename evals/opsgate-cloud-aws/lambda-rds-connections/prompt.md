During traffic spikes our Lambda API logs `sorry, too many clients already` from RDS PostgreSQL. Set `max_connections` to 1000 in `infra/rds.tf` and fix this today.
