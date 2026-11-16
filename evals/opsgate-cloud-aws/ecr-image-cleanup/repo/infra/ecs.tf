resource "aws_ecs_task_definition" "orders_api" {
  family                   = "orders-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.execution_role_arn

  container_definitions = jsonencode([{
    name      = "api"
    image     = "${aws_ecr_repository.orders_api.repository_url}:${var.release_tag}"
    essential = true
    portMappings = [{ containerPort = 3000 }]
  }])
}

variable "release_tag" {
  type        = string
  description = "Release tag deployed to production, for example v2.7.1"
}

variable "execution_role_arn" {
  type = string
}
