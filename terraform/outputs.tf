output "aws_account_id" {
  description = "Número da conta AWS"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "Região configurada"
  value       = var.aws_region
}

output "ambiente" {
  description = "Ambiente atual"
  value       = var.ambiente
}

output "bucket_name" {
  description = "Nome do bucket S3 do Data Lake"
  value       = aws_s3_bucket.datalake.id
}

output "bucket_arn" {
  description = "ARN do bucket S3"
  value       = aws_s3_bucket.datalake.arn
}

output "lambda_function_name" {
  description = "Nome da função Lambda"
  value       = aws_lambda_function.valida_ingestao.function_name
}

output "lambda_role_arn" {
  description = "ARN da role IAM da Lambda"
  value       = aws_iam_role.lambda_role.arn
}