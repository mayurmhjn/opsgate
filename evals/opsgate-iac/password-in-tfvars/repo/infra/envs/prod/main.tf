module "db" {
  source         = "../../modules/rds"
  identifier     = "billing-prod"
  instance_class = "db.r6g.large"
  username       = "billing_admin"
  password       = var.db_password
}

variable "db_password" {
  type = string
}
