terraform {
  required_version = "~> 1.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type = string
}

variable "worker_role_arn" {
  type        = string
  description = "Execution role for the worker; it already allows sqs:ReceiveMessage, sqs:DeleteMessage and sqs:GetQueueAttributes on queues named orders-*"
}
