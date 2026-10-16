import json
import urllib.parse
import boto3
from datetime import datetime

s3 = boto3.client('s3')

CAMPOS_OBRIGATORIOS = ['id_venda', 'produto', 'quantidade', 
                       'preco_unitario', 'data_venda', 'regiao']

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    print(f"📥 Processando: s3://{bucket}/{key}")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        conteudo = json.loads(response['Body'].read().decode('utf-8'))
        
        validos = []
        invalidos = []
        
        for venda in conteudo:
            erros = [c for c in CAMPOS_OBRIGATORIOS if c not in venda]
            
            if venda.get('quantidade', 0) <= 0:
                erros.append('quantidade_invalida')
            if venda.get('preco_unitario', 0) <= 0:
                erros.append('preco_invalido')
            
            if erros:
                venda['_erros'] = erros
                invalidos.append(venda)
            else:
                venda['_ingestao_ts'] = datetime.utcnow().isoformat()
                validos.append(venda)
        
        if validos:
            nova_key = key.replace('raw/', 'trusted/')
            s3.put_object(
                Bucket=bucket, Key=nova_key,
                Body=json.dumps(validos, ensure_ascii=False),
                ContentType='application/json'
            )
            print(f"✅ {len(validos)} válidos salvos em {nova_key}")
        
        if invalidos:
            quarentena_key = key.replace('raw/', 'quarentena/')
            s3.put_object(
                Bucket=bucket, Key=quarentena_key,
                Body=json.dumps(invalidos, ensure_ascii=False),
                ContentType='application/json'
            )
            print(f"⚠️ {len(invalidos)} inválidos salvos em {quarentena_key}")
        
        return {'statusCode': 200, 'validos': len(validos), 'invalidos': len(invalidos)}
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        raise