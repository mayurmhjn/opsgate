resource "aws_db_instance" "main" {
  identifier        = "orders"
  engine            = "postgres"
  # Changed in this PR: was db.r6g.large
  instance_class    = "db.r6g.2xlarge"
  allocated_storage = 500
  multi_az          = true
}
