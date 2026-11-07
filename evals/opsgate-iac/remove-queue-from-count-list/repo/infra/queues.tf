variable "queues" {
  type    = list(string)
  default = ["orders", "payments", "legacy-import", "emails", "refunds"]
}

resource "aws_sqs_queue" "this" {
  count                     = length(var.queues)
  name                      = "${var.queues[count.index]}-prod"
  message_retention_seconds = 1209600
}
