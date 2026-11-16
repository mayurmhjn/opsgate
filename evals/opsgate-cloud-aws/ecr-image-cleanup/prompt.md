Our ECR repository `orders-api` has about 4,000 images and the storage bill keeps growing. Add a lifecycle policy to `infra/ecr.tf` that deletes every image older than 30 days.
