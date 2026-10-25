resource "aws_instance" "ci_runner" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.large"
}
