resource "aws_instance" "app" {
  count         = 6
  ami           = "ami-0abcdef1234567890"
  instance_type = "m5.2xlarge"
  root_block_device {
    volume_type = "gp2"
    volume_size = 200
  }
}

resource "aws_db_instance" "prod" {
  identifier     = "app-prod"
  engine         = "postgres"
  instance_class = "db.r5.2xlarge"
  multi_az       = true
  allocated_storage = 1000
}

resource "aws_cloudwatch_log_group" "app" {
  name = "/app/prod"
}
