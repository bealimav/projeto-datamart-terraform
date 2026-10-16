# ============================================================
# LAMBDA - VALIDAÇÃO DE INGESTÃO
# ============================================================

# Empacota o código Python em um arquivo ZIP automaticamente
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/valida.py"
  output_path = "${path.module}/build/valida.zip"
}

# Função Lambda
resource "aws_lambda_function" "valida_ingestao" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.projeto}-valida-ingestao-${var.ambiente}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "valida.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 256
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  tags = {
    Name = "${var.projeto}-valida-ingestao"
  }
}

# Log group com retenção curta (FinOps)
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.valida_ingestao.function_name}"
  retention_in_days = 1
}

# Permissão para o S3 invocar a Lambda
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.valida_ingestao.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.datalake.arn
}

# Trigger: quando um arquivo chega em raw/, invoca a Lambda
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.datalake.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.valida_ingestao.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_s3]
}