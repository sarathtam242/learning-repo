
variable "aws_region" {
  description = "AWS region for Project 2"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project identifier used for naming and tagging"
  type        = string
  default     = "enminto-p2-drift"
}
