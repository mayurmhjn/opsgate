resource "aws_lambda_function" "orders_api" {
  function_name = "orders-api"
  runtime       = "nodejs22.x"
  handler       = "handler.handler"
  filename      = "build/orders-api.zip"
  role          = var.lambda_role_arn
  timeout       = 10
  memory_size   = 512

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [var.lambda_security_group_id]
  }

  environment {
    variables = {
      DB_HOST = aws_db_instance.orders.address
      DB_USER = "orders_app"
    }
  }
}

variable "lambda_role_arn" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "lambda_security_group_id" {
  type = string
}
