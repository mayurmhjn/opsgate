resource "aws_db_parameter_group" "orders" {
  name   = "orders-pg17"
  family = "postgres17"

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }
}

resource "aws_db_instance" "orders" {
  identifier                  = "orders-prod"
  engine                      = "postgres"
  engine_version              = "17"
  instance_class              = "db.t4g.medium"
  allocated_storage           = 100
  db_name                     = "orders"
  username                    = "orders_admin"
  manage_master_user_password = true
  parameter_group_name        = aws_db_parameter_group.orders.name
  multi_az                    = true
  backup_retention_period     = 14
  deletion_protection         = true
  storage_encrypted           = true
  db_subnet_group_name        = "orders-private"
  vpc_security_group_ids      = [var.db_security_group_id]
}

variable "db_security_group_id" {
  type = string
}
