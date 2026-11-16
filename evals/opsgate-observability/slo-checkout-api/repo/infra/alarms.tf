resource "aws_sns_topic" "oncall_pager" {
  name = "oncall-pager"
}

resource "aws_cloudwatch_metric_alarm" "checkout_cpu_high" {
  alarm_name          = "checkout-cpu-high"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  dimensions          = { ClusterName = var.cluster_name, ServiceName = aws_ecs_service.checkout.name }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.oncall_pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "checkout_memory_high" {
  alarm_name          = "checkout-memory-high"
  namespace           = "AWS/ECS"
  metric_name         = "MemoryUtilization"
  dimensions          = { ClusterName = var.cluster_name, ServiceName = aws_ecs_service.checkout.name }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.oncall_pager.arn]
}
