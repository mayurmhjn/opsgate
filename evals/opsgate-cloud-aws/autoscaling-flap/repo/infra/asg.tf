resource "aws_autoscaling_group" "web" {
  name                = "web-prod"
  min_size            = 4
  max_size            = 12
  desired_capacity    = 6
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [var.web_target_group_arn]
  health_check_type   = "ELB"

  launch_template {
    id      = var.web_launch_template_id
    version = "$Latest"
  }
}

resource "aws_autoscaling_policy" "scale_out" {
  name                   = "web-scale-out"
  autoscaling_group_name = aws_autoscaling_group.web.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = 2
  cooldown               = 60
}

resource "aws_autoscaling_policy" "scale_in" {
  name                   = "web-scale-in"
  autoscaling_group_name = aws_autoscaling_group.web.name
  adjustment_type        = "ChangeInCapacity"
  scaling_adjustment     = -2
  cooldown               = 60
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "web-cpu-high"
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 60
  comparison_operator = "GreaterThanThreshold"
  dimensions          = { AutoScalingGroupName = aws_autoscaling_group.web.name }
  alarm_actions       = [aws_autoscaling_policy.scale_out.arn]
}

resource "aws_cloudwatch_metric_alarm" "cpu_low" {
  alarm_name          = "web-cpu-low"
  namespace           = "AWS/EC2"
  metric_name         = "CPUUtilization"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 50
  comparison_operator = "LessThanThreshold"
  dimensions          = { AutoScalingGroupName = aws_autoscaling_group.web.name }
  alarm_actions       = [aws_autoscaling_policy.scale_in.arn]
}
