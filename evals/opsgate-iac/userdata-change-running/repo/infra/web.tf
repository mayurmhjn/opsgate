resource "aws_instance" "web" {
  ami                    = var.web_ami_id
  instance_type          = "m6i.large"
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.web.id]
  iam_instance_profile   = aws_iam_instance_profile.web.name

  # Changed in this PR: added the last two lines to install the monitoring agent.
  user_data = <<-EOT
    #!/bin/bash
    dnf install -y nginx
    systemctl enable --now nginx
    curl -fsSL https://agent.example-monitoring.com/install.sh -o /tmp/install-agent.sh
    bash /tmp/install-agent.sh --key-from-ssm /monitoring/agent-key
  EOT

  tags = {
    Name = "web-prod-1"
  }
}
