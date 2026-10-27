resource "aws_s3_bucket" "logs" {
  bucket = "acme-access-logs-prod"
}

resource "aws_s3_bucket_policy" "audit" {
  bucket = "acme-audit"
  policy = file("${path.module}/audit-policy.json")
}
