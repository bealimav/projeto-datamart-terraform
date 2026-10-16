# 🏗️ DataMart Analytics - Projeto 2: Pipeline com Terraform

Pipeline de Engenharia de Dados na AWS, **100% definido como código** via Terraform. Mesma arquitetura do Projeto 1, mas reproduzível com um único comando.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![Terraform](https://img.shields.io/badge/Terraform-1.5+-purple)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Status](https://img.shields.io/badge/Status-Completo-green)

## 🎯 Problema de Negócio

A DataMart tinha um pipeline funcionando (Projeto 1), mas o processo de recriar o ambiente manualmente levava horas e era suscetível a erros humanos.

**Solução:** migrar toda a infraestrutura para **Infrastructure as Code (IaC)** usando Terraform.

## 🏗️ Arquitetura

```text
[Script Python] → [S3 raw/] → [Lambda] → [S3 trusted/]
                                              ↓
[Athena] ← [S3 refined/] ← [Python ETL Local]
```

## 🛠️ Tecnologias

- **Terraform** — Infrastructure as Code
- **AWS Provider** (~> 5.0) — Integração com AWS
- **Archive Provider** — Empacotamento automático da Lambda
- **Amazon S3** — Data Lake em camadas (raw/trusted/refined/quarentena)
- **AWS Lambda** (Python 3.12) — Validação orientada a eventos
- **AWS IAM** — Roles e políticas
- **CloudWatch** — Logs com retenção de 1 dia
- **Python + Boto3 + Pandas** — Pipeline local de ETL

## 📁 Estrutura

```text
projeto-datamart-terraform/
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
│   ├── outputs.tf           # Outputs
│   └── terraform.tfvars     # Valores das variáveis
├── .gitignore
└── README.md
```

## 🚀 Como Reproduzir

### Pré-requisitos

- Terraform >= 1.5.0
- AWS CLI configurado
- Python 3.10+ com `py -m pip install boto3 faker pandas pyarrow`

### Criar infraestrutura

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### Popular e testar o pipeline

```bash
py scripts/gerador.py
py scripts/etl_local.py
```

### Destruir tudo (evitar custos)

```bash
cd terraform
terraform destroy
```

## 🎯 Vantagens sobre o Projeto 1

| Aspecto | Projeto 1 (Manual) | Projeto 2 (Terraform) |
|---------|:---:|:---:|
| Tempo para recriar ambiente | ~2 horas | **~1 minuto** |
| Versionamento de infra | ❌ | ✅ |
| Reproduzível | ❌ | ✅ |
| Erro humano | Alto | Baixo |
| CI/CD ready | ❌ | ✅ |
| Custo se esquecer algo | Alto | Baixo (destroy limpa tudo) |

## 📚 Aprendizados

- Infrastructure as Code com Terraform
- Providers, resources, variables, outputs
- `data sources` (aws_caller_identity, archive_file)
- Referência entre recursos (bucket → lambda → trigger)
- Ciclo `init` → `plan` → `apply` → `destroy`
- FinOps via lifecycle policies no S3
- `force_destroy` em buckets S3 para destruição limpa

## 💡 Nota sobre FinOps

> Este projeto foi desenvolvido aplicando o princípio de *Infrastructure as Code*. Toda a infraestrutura AWS pode ser recriada ou destruída com apenas um comando (`terraform apply` / `terraform destroy`). Nenhum recurso permanece na nuvem após a destruição, mantendo o custo em $0.

## 👩‍💻 Autora

Beatriz Lima — Estudante de Engenharia de Dados