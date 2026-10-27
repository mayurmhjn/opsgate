# AWS traps

Check the ones for the services you touch. For details and current limits, use the official AWS skills or the AWS documentation. Limits and defaults change.

## Global and regional

- CloudFront only uses ACM certificates from us-east-1. Create the certificate with a us-east-1 provider alias. The same applies to WAF web ACLs attached to CloudFront.
- IAM, CloudFront, Route 53 and Organizations are global. Their API calls and some of their logs live in us-east-1.
- General purpose bucket names in the global namespace are unique across all accounts in a partition. A deleted name can be taken by someone else. S3 also offers account regional namespaces, which avoid this. Check the current S3 documentation before choosing.
- S3 and DynamoDB always encrypt data at rest. For them, the real question is who owns the key (AWS owned, AWS managed or customer managed). Don't report them as unencrypted.
- Not every service, instance type or feature exists in every region. Check before designing.
- Service quotas are per account and per region. Check them for the planned peak, and for the recovery region too.

## Identity

- IAM changes are eventually consistent. A new role or policy may not work for a few seconds.
- The OIDC `sub` claim changes when a GitHub Actions job uses an `environment:`. It becomes `repo:ORG/REPO:environment:NAME` instead of the branch ref.
- Cross-account access to KMS-encrypted data needs the key policy, the resource policy and the caller's IAM policy to all allow it.
- `iam:PassRole` is needed to hand a role to a service, and it is a privilege escalation path if left unscoped.

## Network

- NAT gateways charge per GB processed as well as per hour. S3 and DynamoDB traffic can use gateway endpoints instead.
- Lambda functions in a VPC have no IPv4 internet access without a NAT gateway (IPv6 needs dual-stack subnets and an egress-only internet gateway). VPC endpoints reach AWS services only, not the internet.
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
- Moving a Terraform resource to another provider alias (for example a certificate to a us-east-1 provider) does not destroy the old one. Terraform loses track of it, so the old resource is left behind in the original region and must be removed separately.
- `terraform apply -target` leaves state partly applied. Use it only for exceptional cases, such as values unknown until apply in `count` or `for_each`, or recovering from a mistake.
