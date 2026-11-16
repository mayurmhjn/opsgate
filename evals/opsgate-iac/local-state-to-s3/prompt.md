Our Terraform state is a local file that we commit to git (infra/terraform.tfstate). Two of us now run Terraform, so move it to S3 with locking. Do it properly.
