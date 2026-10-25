provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app" {
  ami                    = "ami-0abcdef1234567890"
  instance_type          = "t3.large"
  subnet_id              = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.app.id]
  key_name               = "deploy-key"
  associate_public_ip_address = true
}

resource "aws_security_group" "app" {
  name   = "app"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "main" {
  identifier              = "app-db"
  engine                  = "mysql"
  instance_class          = "db.m5.large"
  allocated_storage       = 200
  multi_az                = false
  storage_encrypted       = false
  backup_retention_period = 0
  publicly_accessible     = false
  username                = "admin"
  password                = var.db_password
}
