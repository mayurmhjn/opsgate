resource "aws_ecs_service" "api" {
  name                      = "api"
  cluster                   = aws_ecs_cluster.main.id
  task_definition           = aws_ecs_task_definition.api.arn
  desired_count             = 2
  launch_type               = "FARGATE"
  health_check_grace_period = 60

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = [aws_security_group.api.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
}
