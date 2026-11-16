resource "aws_ecr_repository" "orders_api" {
  name                 = "orders-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# CI pushes every main build as sha-<commit>, and every release as v<semver>.
# Production ECS services run release tags; staging runs sha- tags.
