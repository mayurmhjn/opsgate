data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "orders" {
  bucket = "acme-orders-incoming"
}

resource "aws_dynamodb_table" "orders" {
  name         = "orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

resource "aws_iam_role" "order_sync" {
  name = "order-sync-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_lambda_function" "order_sync" {
  function_name = "order-sync"
  role          = aws_iam_role.order_sync.arn
  runtime       = "python3.12"
  handler       = "app.handler"
  filename      = "build/order_sync.zip"
}
