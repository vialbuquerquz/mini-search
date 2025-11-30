import pdfplumber
from docx import Document
import os

def extract_text(filename: str) -> str:
    """
    Extração de texto de arquivos nos formatos: TXT, PDF ou DOCX.

    Args:
        filepath (str): O caminho completo para o arquivo a ser processado.
    Returns:
        str: O conteúdo textual extraído do arquivo.
    """
    filepath = os.path.join("docs", filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    ext = filepath.lower().split(".")[-1]

    # Processamento para .txt e .md
    if ext in ["txt", "md"]:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            return file.read()

    # Processamento para .pdf
    elif ext == "pdf":
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # Processamento para .docx
    elif ext == "docx":
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        raise ValueError(f"Extensão não suportada: .{ext}")
