provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Team        = "search"
      Environment = "prod"
    }
  }
}

resource "aws_opensearch_domain" "search" {
  domain_name    = "search-prod"
  engine_version = "OpenSearch_2.13"
}
