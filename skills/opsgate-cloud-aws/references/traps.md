# AWS traps

Check the ones for the services you touch. For details and current limits, use the official AWS skills or the AWS documentation. Limits and defaults change.

## Global and regional

- CloudFront only uses ACM certificates from us-east-1. Create the certificate with a us-east-1 provider alias. The same applies to WAF web ACLs attached to CloudFront.
- IAM, CloudFront, Route 53 and Organizations are global. Their API calls and some of their logs live in us-east-1.
- S3 bucket names are global across all accounts. Recreating a deleted bucket name can fail or be taken by someone else.
- Not every service, instance type or feature exists in every region. Check before designing.
- Service quotas are per account and per region. Check them for the planned peak, and for the recovery region too.

## Identity

- IAM changes are eventually consistent. A new role or policy may not work for a few seconds.
- The OIDC `sub` claim changes when a GitHub Actions job uses an `environment:`. It becomes `repo:ORG/REPO:environment:NAME` instead of the branch ref.
- Cross-account access to KMS-encrypted data needs the key policy, the resource policy and the caller's IAM policy to all allow it.
- `iam:PassRole` is needed to hand a role to a service, and it is a privilege escalation path if left unscoped.

## Network

- NAT gateways charge per GB processed as well as per hour. S3 and DynamoDB traffic can use gateway endpoints instead.
- Lambda functions in a VPC have no internet access without a NAT gateway or VPC endpoints.
- Public IPv4 addresses are charged per hour, including those on load balancers and instances.
- Security group rules that reference a CIDR break when IP ranges change. Reference security groups instead.
- Overlapping CIDRs block peering and Transit Gateway routing later.

## Data stores

- RDS `max_connections` depends on instance memory. Connection storms need pooling (RDS Proxy or app-side pooling), not just a bigger instance.
- Enabling encryption on an existing RDS instance or EBS volume needs a new instance or volume from an encrypted snapshot, which means a replacement.
- `skip_final_snapshot = true` and S3 `force_destroy = true` make a destroy delete data permanently.
- AWS limits how often one EBS volume can be modified in a given period. Check the current limit before counting on a quick rollback of a volume change.

## Compute and deploy

- Fargate and Lambda have architecture (x86 or ARM) tied to the image or package. A mismatch fails at start.
- ECS services need the right health check grace period, or tasks get killed while starting.
- `terraform apply -target` leaves state partly applied. Use it only to break a dependency cycle.
