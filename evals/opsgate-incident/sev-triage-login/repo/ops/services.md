# Services

| Service | Regions | Notes |
|---------|---------|-------|
| auth | eu-west-1, us-east-1 | Login and sessions. Route 53 latency routing sends each user to the nearest region. |
| web | eu-west-1, us-east-1 | Frontend |
| orders | eu-west-1 | Single region |

Deploys: auth deploys region by region through the `auth-deploy` pipeline. Last eu-west-1 deploy: today 09:42 UTC.
