# Temporary exports for developers, deleted weekly.

resource "aws_s3_bucket" "tmp_exports" {
  bucket = "acme-dev-tmp-exports"
}
