resource "aws_db_instance" "orders" {
  identifier                  = "orders-prod"
  engine                      = "postgres"
  engine_version              = "17"
  instance_class              = "db.r6g.large"
  allocated_storage           = 200
  storage_type                = "gp3"
  db_name                     = "orders"
  username                    = "orders_admin"
  manage_master_user_password = true
  multi_az                    = true
  backup_retention_period     = 14
  deletion_protection         = true
  storage_encrypted           = true
}

resource "aws_cloudwatch_metric_alarm" "orders_free_storage_low" {
  alarm_name          = "orders-free-storage-low"
  alarm_description   = "Orders DB free storage below 20 GiB. Runbook: TODO"
  namespace           = "AWS/RDS"
  metric_name         = "FreeStorageSpace"
  dimensions          = { DBInstanceIdentifier = aws_db_instance.orders.identifier }
  statistic           = "Minimum"
  period              = 300
  evaluation_periods  = 1
  threshold           = 21474836480
  comparison_operator = "LessThanThreshold"
  alarm_actions       = [var.pager_topic_arn]
}

variable "pager_topic_arn" { type = string }
