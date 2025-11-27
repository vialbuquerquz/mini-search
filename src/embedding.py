from sentence_transformers import SentenceTransformer

# Carrega o modelo uma vez (fica em memória)
print("🔄 Carregando modelo de embeddings...")
model = SentenceTransformer(
    'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
print("✅ Modelo de embeddings carregado!")


def generate_embedding(text: str):
    """
    Gera o embedding de um texto usando o modelo MiniLM.
    - Divide textos maiores que 4000 caracteres em chunks de 2000.
    - Gera embeddings para cada chunk e retorna a média deles.
    - Para textos menores, retorna o embedding direto.

    Params:
        text (str): Texto a ser convertido.

    Returns:
        list[float]: Vetor de embedding.
    """
    if len(text) > 4000:
        chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
        embeddings = [model.encode(chunk) for chunk in chunks]
        import numpy as np
        return np.mean(embeddings, axis=0).tolist()
    else:
        return model.encode(text).tolist()
