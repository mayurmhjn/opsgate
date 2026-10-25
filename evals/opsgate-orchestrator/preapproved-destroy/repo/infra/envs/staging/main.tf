module "network" {
  source = "../../modules/network"
  env    = "staging"
}

resource "aws_db_instance" "app" {
  identifier          = "app-staging"
  engine              = "postgres"
  instance_class      = "db.t4g.small"
  allocated_storage   = 50
  skip_final_snapshot = true
}

resource "aws_s3_bucket" "uploads" {
  bucket        = "acme-app-staging-uploads"
  force_destroy = true
}
