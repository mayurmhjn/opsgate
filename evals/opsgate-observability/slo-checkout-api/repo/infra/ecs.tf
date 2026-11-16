resource "aws_ecs_service" "checkout" {
  name            = "checkout"
  cluster         = var.cluster_arn
  task_definition = var.task_definition_arn
  desired_count   = 4
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [var.service_security_group_id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.checkout.arn
    container_name   = "api"
    container_port   = 8080
  }
}
