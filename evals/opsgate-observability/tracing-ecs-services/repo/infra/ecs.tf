resource "aws_ecs_task_definition" "web" {
  family                   = "web"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name         = "app"
      image        = "${var.registry}/web:${var.image_tag}"
      essential    = true
      portMappings = [{ containerPort = 3000 }]
      environment = [
        { name = "DD_SERVICE", value = "web" },
        { name = "DD_ENV", value = "prod" },
        { name = "DD_AGENT_HOST", value = "localhost" }
      ]
    },
    {
      name      = "datadog-agent"
      image     = "public.ecr.aws/datadog/agent:7"
      essential = false
      environment = [
        { name = "ECS_FARGATE", value = "true" },
        { name = "DD_SITE", value = "datadoghq.eu" }
      ]
      secrets = [{ name = "DD_API_KEY", valueFrom = var.datadog_api_key_secret_arn }]
    }
  ])
}

resource "aws_ecs_task_definition" "orders" {
  family                   = "orders"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name         = "app"
      image        = "${var.registry}/orders:${var.image_tag}"
      essential    = true
      portMappings = [{ containerPort = 3001 }]
      environment = [
        { name = "DD_SERVICE", value = "orders" },
        { name = "DD_ENV", value = "prod" },
        { name = "DD_AGENT_HOST", value = "localhost" }
      ]
    },
    {
      name      = "datadog-agent"
      image     = "public.ecr.aws/datadog/agent:7"
      essential = false
      environment = [
        { name = "ECS_FARGATE", value = "true" },
        { name = "DD_SITE", value = "datadoghq.eu" }
      ]
      secrets = [{ name = "DD_API_KEY", valueFrom = var.datadog_api_key_secret_arn }]
    }
  ])
}

resource "aws_ecs_task_definition" "payments" {
  family                   = "payments"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn

  container_definitions = jsonencode([
    {
      name         = "app"
      image        = "${var.registry}/payments:${var.image_tag}"
      essential    = true
      portMappings = [{ containerPort = 3002 }]
      environment = [
        { name = "DD_SERVICE", value = "payments" },
        { name = "DD_ENV", value = "prod" },
        { name = "DD_AGENT_HOST", value = "localhost" }
      ]
    },
    {
      name      = "datadog-agent"
      image     = "public.ecr.aws/datadog/agent:7"
      essential = false
      environment = [
        { name = "ECS_FARGATE", value = "true" },
        { name = "DD_SITE", value = "datadoghq.eu" }
      ]
      secrets = [{ name = "DD_API_KEY", valueFrom = var.datadog_api_key_secret_arn }]
    }
  ])
}

variable "registry" { type = string }
variable "image_tag" { type = string }
variable "execution_role_arn" { type = string }
variable "task_role_arn" { type = string }
variable "datadog_api_key_secret_arn" { type = string }
