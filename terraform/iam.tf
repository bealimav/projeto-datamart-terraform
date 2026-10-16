# ============================================================
# IAM - ROLE PARA A LAMBDA
# ============================================================

# Role que a Lambda vai "vestir" para acessar a AWS
resource "aws_iam_role" "lambda_role" {
  name = "${var.projeto}-lambda-role-${var.ambiente}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Name = "${var.projeto}-lambda-role"
  }
}

# Política gerenciada pela AWS: permite escrita de logs no CloudWatch
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Política inline: permite que a Lambda leia e escreva no nosso bucket
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "${var.projeto}-lambda-s3-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.datalake.arn,
        "${aws_s3_bucket.datalake.arn}/*"
      ]
    }]
  })
}