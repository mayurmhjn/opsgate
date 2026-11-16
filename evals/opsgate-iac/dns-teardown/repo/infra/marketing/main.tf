resource "aws_s3_bucket" "promo" {
  bucket        = "promo.acme-example.com"
  force_destroy = true
}

resource "aws_s3_bucket_website_configuration" "promo" {
  bucket = aws_s3_bucket.promo.id

  index_document {
    suffix = "index.html"
  }
}
