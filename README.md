# 🏗️ DataMart Analytics - Projeto 2: Pipeline com Terraform

Pipeline de Engenharia de Dados na AWS, **100% definido como código** via Terraform. Mesma arquitetura do Projeto 1, mas reproduzível com um único comando.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Terraform](https://img.shields.io/badge/Terraform-1.5+-purple)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![CI/CD](https://img.shields.io/badge/CI--CD-GitHub_Actions-black)
![Terraform Validate](https://github.com/bealimav/projeto-datamart-terraform/actions/workflows/terraform.yml/badge.svg)

---

## 🎯 Problema de Negócio

A DataMart tinha um pipeline funcionando (Projeto 1), mas o processo de recriar o ambiente manualmente levava horas e era suscetível a erros humanos.

**Solução:** migrar toda a infraestrutura para **Infrastructure as Code (IaC)** usando Terraform.

---

## 🏗️ Arquitetura

```text
[Script Python] → [S3 raw/] → [Lambda] → [S3 trusted/]
                                              ↓
[Athena] ← [S3 refined/] ← [Python ETL Local]
```

---

## 🚀 CI/CD (Integração Contínua)

Este projeto conta com uma esteira automatizada de **GitHub Actions** (`.github/workflows/terraform.yml`). A cada `git push`, o robô na nuvem:
1. Instala o Terraform.
2. Roda o `terraform init` para baixar os providers.
3. Roda o `terraform validate` para garantir que não há erros de sintaxe no código HCL.
Isso evita que alterações de infraestrutura quebradas cheguem à branch principal.

---

## 🛠️ Tecnologias Utilizadas

- **Terraform** — Infrastructure as Code.
- **AWS Provider** (~> 5.0) — Integração com AWS.
- **Archive Provider** — Empacotamento automático da Lambda.
- **GitHub Actions** — Automação de validação de infraestrutura.
- **Amazon S3, Lambda e IAM** — Recursos provisionados.
- **Python + Boto3 + Pandas** — Pipeline local de ETL.

---

## 📁 Estrutura

```text
projeto-datamart-terraform/
├── .github/workflows/
│   └── terraform.yml        # CI/CD de validação de infraestrutura
├── lambda/
│   └── valida.py            # Código da Lambda
├── scripts/
│   ├── gerador.py           # Gera dados sintéticos
│   └── etl_local.py         # Transforma trusted → refined
├── terraform/
│   ├── main.tf              # Provider AWS
│   ├── variables.tf         # Variáveis
│   ├── s3.tf                # Bucket + camadas
│   ├── iam.tf               # Role + policies
│   ├── lambda.tf            # Função + trigger S3
│   └── outputs.tf           # Outputs
└── README.md
```

---

## 🚀 Como Reproduzir

### 1. Criar infraestrutura
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 2. Popular e testar o pipeline
```bash
py scripts/gerador.py
py scripts/etl_local.py
```

### 3. Destruir tudo (evitar custos)
```bash
cd terraform
terraform destroy
```

---

## 📚 Aprendizados

- Infrastructure as Code com Terraform.
- Ciclo `init` → `plan` → `apply` → `destroy`.
- `force_destroy` em buckets S3 para destruição limpa.
- Implementação de **CI/CD** para validação de infraestrutura.
- FinOps via lifecycle policies no S3.

---

## 👩‍💻 Autora
Beatriz Lima — Estagiária de Engenharia de Dados
