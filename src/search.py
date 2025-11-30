from elasticsearch import Elasticsearch
from src.embedding import generate_embedding


def search_semantic(client: Elasticsearch, query_text: str, total_results: int = 5):
    """
    Busca híbrida (BM25 + Embedding) em todos os índices de usuário.
    - Retorna apenas resultados acima do limite mínimo de relevância.
    """

    query_embedding = generate_embedding(query_text)

    # Acessa todos os índices disponíveis
    try:
        all_indices = client.indices.get(index="*")
    except Exception as err:
        raise Exception(f"Erro ao listar índices: {err}")

    # Remove os filtros do sistema
    user_indices = [name for name in all_indices.keys()
                    if not name.startswith(".")]

    if not user_indices:
        print("❌ Não há índices de usuário para buscar.")
        return []

    indices_csv = ",".join(user_indices)

    # Monta payload de consulta léxica, semântica e
    search_payload = {
        "size": total_results,
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "content": {
                                "query": query_text,
                                "boost": 3
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "content": {
                                "query": query_text,
                                "boost": 5
                            }
                        }
                    },
                    {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {"query_vector": query_embedding}
                            }
                        }
                    }
                ],
                "minimum_should_match": 1
            }
        }
    }

    # Realiza a consulta e filtra pela relevância
    try:
        response = client.search(index=indices_csv, body=search_payload)
    except Exception as err:
        raise Exception(f"Erro ao executar busca: {err}")

    hits = response.get("hits", {}).get("hits", [])
    score_min = 1.30
    filtered_hits = [result for result in hits if result.get(
        "_score", 0) >= score_min]
    for hit in filtered_hits:
        hit["_index_source"] = hit.get("_index", "")

    return filtered_hits
