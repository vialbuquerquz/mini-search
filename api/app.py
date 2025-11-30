from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Conexão com o Elasticsearch
client = Elasticsearch(
    hosts=[os.getenv("ELASTIC_HOST")],
    basic_auth=(os.getenv("ELASTIC_USER"), os.getenv("ELASTIC_PASSWORD")),
    verify_certs=False
)


@app.route("/delete-index", methods=["DELETE"])
def delete_document():
    """
    Remove um documento do Elasticsearch baseado no nome do arquivo.
    Exemplo:
        DELETE /delete?filename=nome-do-arquivo.txt
    """

    filename = request.args.get("filename")

    if not filename:
        return jsonify({
            "status": "error",
            "message": "Parâmetro 'filename' é obrigatório."
        }), 400

    # Verifica se índice existe
    if not client.indices.exists(index=filename):
        return jsonify({
            "status": "error",
            "message": f"O índice '{filename}' não existe no Elasticsearch."
        }), 404

    # Realiza remoção do index
    try:
        client.indices.delete(index=filename)

        return jsonify({
            "status": "success",
            "message": f"Documento '{filename}' removido com sucesso."
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao remover índice: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
