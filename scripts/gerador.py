import boto3
import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('pt_BR')
s3 = boto3.client('s3')

# Descobre o bucket automaticamente
def descobrir_bucket():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if 'datamart-datalake' in bucket['Name']:
            return bucket['Name']
    raise Exception("Bucket datamart-datalake não encontrado")

def gerar_venda():
    return {
        "id_venda": random.randint(1000, 9999),
        "produto": random.choice(['Notebook', 'Mouse', 'Teclado', 'Monitor', 'Headset']),
        "quantidade": random.randint(1, 5),
        "preco_unitario": round(random.uniform(50.0, 5000.0), 2),
        "data_venda": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
        "regiao": random.choice(['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']),
        "canal_venda": random.choice(['site', 'app', 'parceiro'])
    }

def upload_vendas(quantidade=100):
    bucket = descobrir_bucket()
    vendas = [gerar_venda() for _ in range(quantidade)]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    key = f"raw/vendas_{timestamp}.json"
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(vendas, ensure_ascii=False),
        ContentType='application/json'
    )
    print(f"✅ {quantidade} vendas enviadas para s3://{bucket}/{key}")

if __name__ == "__main__":
    upload_vendas(100)