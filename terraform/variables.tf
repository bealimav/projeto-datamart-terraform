variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "ambiente" {
  description = "Nome do ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "projeto" {
  description = "Nome do projeto (prefixo dos recursos)"
  type        = string
  default     = "datamart"
}