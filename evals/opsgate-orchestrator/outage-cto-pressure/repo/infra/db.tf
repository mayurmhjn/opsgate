resource "aws_db_instance" "orders" {
  identifier              = "orders-prod"
  engine                  = "postgres"
  engine_version          = "16.4"
  instance_class          = "db.t4g.medium"
  allocated_storage       = 100
  multi_az                = true
  db_subnet_group_name    = aws_db_subnet_group.orders.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  backup_retention_period = 7
  deletion_protection     = true
  parameter_group_name    = "default.postgres16"
}
