# Requirements

Status: approved by Priya (platform lead), 2026-10-20

- Workload: internal REST API for order lookups, Python, about 50 requests per second at peak, business hours only.
- Availability target: 99.9%.
- Data: order IDs and customer names (internal, not PCI).
- Region: eu-west-1. Single AWS account per environment (dev, prod).
- Team: three engineers, comfortable with Python and Terraform, no Kubernetes experience.
- Budget: under 400 USD per month for prod.
- Existing tools: GitHub for source and CI.
