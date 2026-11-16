terraform {
  required_version = "~> 1.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_db_instance" "app" {
  identifier          = "app-prod"
  engine              = "postgres"
  instance_class      = "db.t4g.medium"
  allocated_storage   = 20
  username            = "app"
  password            = var.db_password
  skip_final_snapshot = false
}
