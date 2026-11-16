resource "aws_sns_topic" "pager" {
  name = "oncall-pager"
}

resource "aws_cloudwatch_metric_alarm" "api_cpu_high" {
  alarm_name          = "api-cpu-high"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  dimensions          = { ClusterName = "prod", ServiceName = "api" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 70
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "worker_cpu_high" {
  alarm_name          = "worker-cpu-high"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  dimensions          = { ClusterName = "prod", ServiceName = "worker" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 70
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "search_cpu_high" {
  alarm_name          = "search-cpu-high"
  namespace           = "AWS/ECS"
  metric_name         = "CPUUtilization"
  dimensions          = { ClusterName = "prod", ServiceName = "search" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 70
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "api_memory_high" {
  alarm_name          = "api-memory-high"
  namespace           = "AWS/ECS"
  metric_name         = "MemoryUtilization"
  dimensions          = { ClusterName = "prod", ServiceName = "api" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 75
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "reports_disk_high" {
  alarm_name          = "reports-disk-high"
  namespace           = "CWAgent"
  metric_name         = "disk_used_percent"
  dimensions          = { InstanceId = "i-0a1b2c3d4e5f60718", path = "/", device = "nvme0n1p1", fstype = "xfs" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "batch_disk_high" {
  alarm_name          = "batch-disk-high"
  namespace           = "CWAgent"
  metric_name         = "disk_used_percent"
  dimensions          = { InstanceId = "i-0f1e2d3c4b5a69788", path = "/", device = "nvme0n1p1", fstype = "xfs" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 80
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "orders_db_cpu_high" {
  alarm_name          = "orders-db-cpu-high"
  namespace           = "AWS/RDS"
  metric_name         = "CPUUtilization"
  dimensions          = { DBInstanceIdentifier = "orders-prod" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 60
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "orders_db_connections_high" {
  alarm_name          = "orders-db-connections-high"
  namespace           = "AWS/RDS"
  metric_name         = "DatabaseConnections"
  dimensions          = { DBInstanceIdentifier = "orders-prod" }
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 200
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}

resource "aws_cloudwatch_metric_alarm" "api_5xx" {
  alarm_name          = "api-5xx"
  namespace           = "AWS/ApplicationELB"
  metric_name         = "HTTPCode_Target_5XX_Count"
  dimensions          = { LoadBalancer = "app/api-prod/50dc6c495c0c9188" }
  statistic           = "Sum"
  period              = 300
  evaluation_periods  = 3
  threshold           = 500
  comparison_operator = "GreaterThanThreshold"
  alarm_actions       = [aws_sns_topic.pager.arn]
}
