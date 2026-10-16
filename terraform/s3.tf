# ============================================================
# BUCKET S3 - DATA LAKE DATAMART
# ============================================================

resource "aws_s3_bucket" "datalake" {
  bucket        = "${var.projeto}-datalake-${data.aws_caller_identity.current.account_id}"
  force_destroy = true   # ← Linha adicionada aqui

  tags = {
    Name = "${var.projeto}-datalake"
  }
}

# Bloqueia qualquer acesso público (segurança)
resource "aws_s3_bucket_public_access_block" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Criptografia no lado do servidor (AES256)
resource "aws_s3_bucket_server_side_encryption_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Criação das "pastas" (camadas do Data Lake)
resource "aws_s3_object" "pastas" {
  for_each = toset(["raw/", "trusted/", "refined/", "quarentena/", "athena-results/"])

  bucket = aws_s3_bucket.datalake.id
  key    = each.value
}

# Lifecycle: expira arquivos de quarentena após 30 dias
resource "aws_s3_bucket_lifecycle_configuration" "datalake" {
  bucket = aws_s3_bucket.datalake.id

  rule {
    id     = "expirar-quarentena"
    status = "Enabled"

    filter {
      prefix = "quarentena/"
    }

    expiration {
      days = 30
    }
  }

  rule {
    id     = "expirar-athena-results"
    status = "Enabled"

    filter {
      prefix = "athena-results/"
    }

    expiration {
      days = 7
    }
  }
}