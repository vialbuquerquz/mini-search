import os
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import BadRequestError


def create_index(client, index_name):
    """
    Exclui um índice existente (se houver) e cria um novo 
    com o mapeamento para campos de texto e vetores densos (embeddings).

    Args: 
        client(obj): Conexão com o ElasticSearch.
        index_name(str): Índice do arquivo que será criado.
    """

    # Remove índice existente se houver
    if client.indices.exists(index=index_name):
        print(f"🔄 Índice existente. Atualizando...")
        client.indices.delete(index=index_name)

    # Cria novo índice com mapeamento correto
    client.indices.create(
        index=index_name,
        body={
            "mappings": {
                "properties": {
                    "filename": {"type": "text"},
                    "content": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }
    )
    print(f"✅ Índice criado: {index_name}")
