provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "reports" {
  bucket = "acme-reports-prod"
}

resource "aws_s3_bucket_ownership_controls" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "reports" {
  bucket     = aws_s3_bucket.reports.id
  acl        = "public-read"
  depends_on = [aws_s3_bucket_ownership_controls.reports]
}
