from elasticsearch import Elasticsearch
from src.embedding import generate_embedding


def search_semantic(client: Elasticsearch, query: str):
    """
    Executa uma busca semântica no Elasticsearch.

    - Realiza busca em todos os índices do cluster.
    - Gera o embedding da consulta.
    - Utiliza similaridade de cosseno para avaliar relevância.
    - Ordena resultados (no caso de busca em múltiplos índices).

    Params:
        client (Elasticsearch): Conexão com o ElasticSearch.
        query (str): Texto da busca semântica.
        index_name (str | None): Índice de busca.

    Returns:
        list[dict] | dict: Resultados da busca.  
                           - Se índice único → dict do Elasticsearch  
                           - Se múltiplos índices → lista com todos os hits ordenados
    """
    query_embedding = generate_embedding(query)

    body = {
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding')",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    }

    try:
        indices = client.indices.get(index="*")
        user_indices = [
            idx for idx in indices.keys() if not idx.startswith('.')]

        print(
            f"🔍 Buscando em {len(user_indices)} índices: {', '.join(user_indices)}")

        if not user_indices:
            print("❌ Nenhum índice de usuário encontrado")
            return []

    except Exception as e:
        print(f"❌ Erro ao listar índices: {e}")
        return []

    all_results = []

    for idx in user_indices:
        try:
            print(f"   📂 Buscando em: {idx}")

            response = client.search(index=idx, body=body)

            for hit in response["hits"]["hits"]:
                hit["_index_source"] = idx
                all_results.append(hit)

        except Exception as e:
            print(f"   ⚠️  Erro no índice {idx}: {e}")

    all_results.sort(key=lambda x: x["_score"], reverse=True)

    print(f"✅ Busca concluída: {len(all_results)} resultado(s) encontrado(s)")
    return all_results


def search_documents(client: Elasticsearch, index_name: str, query: str):
    """
    Executa uma busca textual tradicional (full-text search) em um índice Elasticsearch.

    - Utiliza a query 'match' para procurar termos dentro do campo 'content'.
    - Não utiliza embeddings nem similaridade semântica.
    - Retorna documentos cujo texto contém ou se relaciona lexicalmente ao termo buscado.

    Parâmetros:
        client (Elasticsearch): Conexão com o ElasticSearch.
        query (str): Texto da busca semântica.
        index_name (str | None): Índice de busca.

    Retorna:
        dict: Resultado da busca textual no Elasticsearch.
    """
    body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    return client.search(index=index_name, body=body)


def find_relevant_preview(content: str, query: str, fragment_size: int = 200):
    """
    Extrai um trecho relevante do conteúdo com base nos termos da query.

    - Converte conteúdo e query para minúsculas para busca case-insensitive.
    - Percorre as palavras da query.
    - Quando encontra uma palavra relevante, retorna um fragmento do texto
      ao redor dessa palavra, limitado por `fragment_size`.
    - Retorna somente trechos com tamanho razoável para uso como preview.

    Params:
        content (str): Texto completo de onde o trecho será extraído.
        query (str): Termos usados para localizar a parte relevante.
        fragment_size (int): Tamanho máximo do trecho retornado (default: 200).

    Returns:
        str | None: Trecho relevante do conteúdo ou None se nada for encontrado.
    """
    content_lower = content.lower()
    query_lower = query.lower()

    # Procura por palavras da query no conteúdo
    for word in query_lower.split():
        pos = content_lower.find(word)
        if pos != -1:
            start = max(0, pos - fragment_size // 2)
            end = min(len(content), start + fragment_size)
            preview = content[start:end].strip()
            if len(preview) > 50:
                return preview + "..."

    # Fallback: primeiros caracteres
    return content[:fragment_size].strip() + "..."
