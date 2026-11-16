resource "aws_dlm_lifecycle_policy" "db_nightly" {
  description        = "Nightly snapshots of the PostgreSQL data volume"
  execution_role_arn = aws_iam_role.dlm.arn
  state              = "ENABLED"

  policy_details {
    resource_types = ["VOLUME"]
    target_tags = {
      Backup = "db-nightly"
    }

    schedule {
      name = "nightly"
      create_rule {
        interval      = 24
        interval_unit = "HOURS"
        times         = ["02:00"]
      }
      retain_rule {
        count = 7
      }
      copy_tags = true
    }
  }
}
