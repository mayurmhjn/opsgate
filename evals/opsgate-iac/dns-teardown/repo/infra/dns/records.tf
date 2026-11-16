# Managed by the platform team in a separate root module and state.

resource "aws_route53_record" "promo" {
  zone_id = var.acme_example_zone_id
  name    = "promo.acme-example.com"
  type    = "CNAME"
  ttl     = 300
  records = ["promo.acme-example.com.s3-website-eu-west-1.amazonaws.com"]
}

resource "aws_route53_record" "www" {
  zone_id = var.acme_example_zone_id
  name    = "www.acme-example.com"
  type    = "CNAME"
  ttl     = 300
  records = ["d111111abcdef8.cloudfront.net"]
}
