resource "aws_ecs_task_definition" "reports" {
  family                   = "reports"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 2048
  execution_role_arn       = var.execution_role_arn

  container_definitions = jsonencode([{
    name      = "reports"
    image     = "${var.registry}/reports:${var.image_tag}"
    essential = true
  }])
}

resource "aws_ecs_service" "reports" {
  name            = "reports"
  cluster         = "prod"
  task_definition = aws_ecs_task_definition.reports.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets = var.private_subnet_ids
  }
}

variable "registry" { type = string }
variable "image_tag" { type = string }
variable "execution_role_arn" { type = string }
variable "private_subnet_ids" { type = list(string) }
