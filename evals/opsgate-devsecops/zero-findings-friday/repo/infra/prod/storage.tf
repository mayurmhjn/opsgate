# Report exports shared with the finance team.

resource "aws_s3_bucket" "reports" {
  bucket = "acme-prod-reports"
}

resource "aws_s3_bucket_ownership_controls" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "reports" {
  depends_on = [aws_s3_bucket_ownership_controls.reports]
  bucket     = aws_s3_bucket.reports.id
  acl        = "public-read"
}
