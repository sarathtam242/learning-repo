
output "application_bucket_name" {
  description = "Name of the Terraform-managed application bucket"
  value       = aws_s3_bucket.application.bucket
}

output "application_bucket_arn" {
  description = "ARN of the application bucket"
  value       = aws_s3_bucket.application.arn
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}
