from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from src.extract_text import extract_text
from src.create_index import create_index
from src.search import search_semantic
from src.embedding import generate_embedding

load_dotenv()

# Conexão com o ElasticSearch
try:
    client = Elasticsearch(
        hosts=[os.getenv("ELASTIC_HOST")],
        basic_auth=(os.getenv("ELASTIC_USER"), os.getenv("ELASTIC_PASSWORD")),
        verify_certs=False
    )

    if not client.ping():
        raise Exception("Não foi possível conectar ao Elasticsearch")

except Exception as e:
    raise Exception(f"Erro ao conectar ao Elasticsearch: {e}")

# Função principal


def process_document(filename):

    print(f"\n📄 Processando: {filename}")
    text_extract = extract_text(filename)
    print(f"📊 Texto extraído com sucesso: {len(text_extract)} caracteres.")

    # Nome do índice baseado no arquivo
    index_name = os.path.splitext(filename)[0].lower()

    # Cria índice do doc
    create_index(client, index_name)

    # Gera embedding e indexa
    document_embedding = generate_embedding(text_extract)

    response = client.index(
        index=index_name,
        document={
            "content": text_extract,
            "filename": filename,
            "embedding": document_embedding
        }
    )
    print(f"📝 Id do documento indexado: {response['_id']}")


print("🚀 INICIANDO INDEXAÇÃO DE DOCUMENTOS")
docs_folder = "docs"
if os.path.exists(docs_folder):
    for filename in os.listdir(docs_folder):
        if filename.endswith(('.pdf', '.txt', '.docx')):
            process_document(filename)
else:
    print("❌ Pasta 'docs' não encontrada")
    exit(1)

print("\n" + "="*50)
print("🎯 SISTEMA DE BUSCA - ELASTICSEARCH COMPLETO")
print("="*50)

# Interface interativa
while True:
    query = input("\n🔍 Buscar em TODA a base (ou 'sair'): ").strip()

    if query.lower() in ["sair", "exit", "quit"]:
        print("👋 Encerrando...")
        break

    if not query:
        print("⚠️  Digite algo para buscar")
        continue

    print(f"\n🎯 Buscando: '{query}'")
    print("⏳ Aguarde...")

    results = search_semantic(client, query)

    if not results:
        print("\n❌ Nenhum resultado encontrado na base completa")
    else:
        print(
            f"\n📊 RESUMO: {len(results)} documento(s) correspondentes com a busca encontrados.")

        for i, hit in enumerate(results, 1):
            score = hit["_score"]

            # Converter script_score para intervalo 0–1
            normalized_score = (score - 1) / 1
            percentual = round(normalized_score * 100, 2)

            filename = hit["_source"]["filename"]
            index_source = hit["_index_source"]

            content = hit["_source"]["content"]

            print(f"\n{i}. 🏷️  {filename}")
            print(f"   📂 Índice Elastic: {index_source}")
            print(f"   ⭐ Similaridade com o termo buscado: {percentual}%")
