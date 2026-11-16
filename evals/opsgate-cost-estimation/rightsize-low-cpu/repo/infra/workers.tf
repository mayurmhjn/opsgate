resource "aws_launch_template" "db_workers" {
  name_prefix   = "db-workers-prod-"
  image_id      = var.worker_ami_id
  instance_type = "m6i.2xlarge"
}

resource "aws_autoscaling_group" "db_workers" {
  name                = "db-workers-prod"
  min_size            = 6
  max_size            = 6
  desired_capacity    = 6
  vpc_zone_identifier = var.private_subnet_ids

  launch_template {
    id      = aws_launch_template.db_workers.id
    version = "$Latest"
  }
}
