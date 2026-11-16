provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      team        = "payments"
      environment = "prod"
    }
  }
}

resource "aws_ecs_cluster" "payments" {
  name = "payments-prod"
}

resource "aws_ecs_service" "payments_api" {
  name            = "payments-api"
  cluster         = aws_ecs_cluster.payments.id
  task_definition = var.task_definition_arn
  desired_count   = 3
  launch_type     = "FARGATE"
  propagate_tags  = "SERVICE"

  network_configuration {
    subnets = var.private_subnet_ids
  }
}
