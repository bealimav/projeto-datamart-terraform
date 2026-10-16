#Substituir serviço do Glue que está indisponível na minha conta da AWS

import boto3
import pandas as pd
import json
import io
from datetime import datetime

s3 = boto3.client('s3')


def descobrir_bucket():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if 'datamart-datalake' in bucket['Name']:
            return bucket['Name']
    raise Exception("Bucket datamart-datalake não encontrado")


def ler_arquivos_trusted(bucket):
    print(f"📂 Lendo arquivos de s3://{bucket}/trusted/")
    
    response = s3.list_objects_v2(Bucket=bucket, Prefix='trusted/')
    
    if 'Contents' not in response:
        print("⚠️ Nenhum arquivo encontrado em trusted/")
        return None
    
    dfs = []
    for obj in response['Contents']:
        key = obj['Key']
        if not key.endswith('.json'):
            continue
        
        print(f"   📥 {key}")
        data = s3.get_object(Bucket=bucket, Key=key)
        conteudo = json.loads(data['Body'].read().decode('utf-8'))
        df = pd.DataFrame(conteudo)
        dfs.append(df)
    
    if not dfs:
        print("⚠️ Nenhum JSON válido encontrado")
        return None
    
    df_final = pd.concat(dfs, ignore_index=True)
    print(f"✅ {len(df_final)} vendas lidas de {len(dfs)} arquivo(s)")
    return df_final


def transformar(df):
    print("\n🔧 Aplicando transformações...")
    
    # Renomeia colunas com prefixo _ (inválidas no Athena)
    df = df.rename(columns={'_ingestao_ts': 'ingestao_ts'})
    
    df['valor_total'] = df['quantidade'] * df['preco_unitario']
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['quantidade'] = df['quantidade'].astype('int64')
    df['preco_unitario'] = df['preco_unitario'].astype('float64')
    df['valor_total'] = df['valor_total'].astype('float64')
    
    antes = len(df)
    df = df.drop_duplicates(subset=['id_venda'], keep='last')
    depois = len(df)
    print(f"   🧹 Duplicatas removidas: {antes - depois}")
    
    df = df.dropna(subset=['id_venda', 'produto', 'valor_total', 'data_venda'])
    df['processado_em'] = datetime.utcnow().isoformat()
    
    print(f"✅ {len(df)} vendas após transformações")
    return df

def gerar_estatisticas(df):
    print("\n📊 ESTATÍSTICAS DO NEGÓCIO")
    print("=" * 50)
    print(f"💰 Faturamento total: R$ {df['valor_total'].sum():,.2f}")
    print(f"📦 Total de vendas: {len(df):,}")
    print(f"🎯 Ticket médio: R$ {df['valor_total'].mean():,.2f}")
    print()
    
    print("📍 Faturamento por Região:")
    por_regiao = df.groupby('regiao')['valor_total'].sum().sort_values(ascending=False)
    for regiao, valor in por_regiao.items():
        print(f"   {regiao}: R$ {valor:,.2f}")
    print()
    
    print("🏆 Top 5 Produtos (por quantidade):")
    top_produtos = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False).head(5)
    for produto, qtd in top_produtos.items():
        print(f"   {produto}: {qtd} unidades")
    print()
    
    print("📢 Vendas por Canal:")
    por_canal = df.groupby('canal_venda')['valor_total'].sum().sort_values(ascending=False)
    for canal, valor in por_canal.items():
        print(f"   {canal}: R$ {valor:,.2f}")
    print("=" * 50)


def salvar_parquet(df, bucket):
    print("\n💾 Salvando em Parquet...")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    key = f"refined/vendas/vendas_{timestamp}.parquet"
    
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)
    
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=buffer.getvalue(),
        ContentType='application/octet-stream'
    )
    
    tamanho_kb = buffer.tell() / 1024
    print(f"✅ Salvo em s3://{bucket}/{key}")
    print(f"📦 Tamanho: {tamanho_kb:.2f} KB")


def main():
    print("=" * 50)
    print("🚀 ETL LOCAL - DATAMART ANALYTICS")
    print("=" * 50)
    print()
    
    bucket = descobrir_bucket()
    print(f"🪣 Bucket: {bucket}\n")
    
    df = ler_arquivos_trusted(bucket)
    if df is None:
        return
    
    df_transformado = transformar(df)
    gerar_estatisticas(df_transformado)
    salvar_parquet(df_transformado, bucket)
    
    print("\n🎉 Pipeline concluído com sucesso!")


if __name__ == "__main__":
    main()