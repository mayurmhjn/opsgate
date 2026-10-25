resource "aws_instance" "app" {
  count         = 4
  ami           = "ami-0abcdef1234567890"
  instance_type = "m5.xlarge"
  root_block_device {
    volume_type = "gp2"
    volume_size = 200
  }
}

resource "aws_db_instance" "dev" {
  identifier     = "app-dev"
  engine         = "postgres"
  instance_class = "db.m5.xlarge"
  multi_az       = true
  allocated_storage = 300
}

resource "aws_cloudwatch_log_group" "app" {
  name = "/app/dev"
}
