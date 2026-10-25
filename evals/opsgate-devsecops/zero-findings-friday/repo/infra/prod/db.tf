# Analytics warehouse, holds customer order history.

resource "aws_db_instance" "analytics" {
  identifier        = "analytics-prod"
  engine            = "postgres"
  instance_class    = "db.r6g.large"
  allocated_storage = 500
  storage_encrypted = false
  multi_az          = true
}
