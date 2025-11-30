# 🔍 Mini Search - Sistema de Busca

Um sistema avançado de recuperação de informações que implementa técnicas de PLN para integrar buscas lexical (BM25) e semântica através de embeddings vetoriais. A solução recupera documentos indexados no ElasticSearch mediante consultas por termos específicos, apresentando os resultados classificados por score de relevância calculado a partir da similaridade de cosseno, comparado com a consulta original.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Fluxo de execução](#-fluxo-de-execucao)
- [Estrutura do projeto](#-extrutura-do-projeto)


## 🎯 Visão Geral

O Mini Search é um sistema de busca que utiliza técnicas modernas de processamento de linguagem natural para oferecer duas formas de busca:

- **Busca Lexical(BM25)**: Busca tradicional por palavras-chave localizando resultados com correspondência literal
- **Busca Semântica**: Busca por similaridade de significado usando embeddings, calculados pelo cosseno de similaridade.
- **Busca Híbrida**: Combinação de lexical e semântica,

Essa combinação permite encontrar tanto informações exatas quanto conceitualmente relacionadas, melhorando o poder de busca em documentos extensos.

## ✨ Funcionalidades

### 🔤 Busca Lexical
- Busca tradicional por palavras-chave exatas
- Suporte a operadores de busca do Elasticsearch
- Ordenação por relevância

### 🧠 Busca Semântica
- Busca por similaridade de significado
- Usa modelos de embeddings multilíngues
- Encontra documentos semanticamente relacionados
- Score baseado em similaridade de cosseno

###⚡ Busca Híbrida
- Combina BM25 (lexical) + embeddings (semântica).
- Parametrização para dar prioridade ao que contém o termo exato.
- Filtragem automática de resultados relevântes, com score mínimo de 30%


### 📄 Processamento de Documentos
- Suporte a múltiplos formatos: PDF, TXT, DOCX
- Extração automática de texto
- Indexação eficiente no Elasticsearch
- Geração automática de embeddings

### 🎯 Interface
- Interface de linha de comando intuitiva
- Exibição de trechos relevantes
- Score de relevância
- Destaque de resultados

## 🛠️ Tecnologias

### Backend
- **Python 3.8+** - Linguagem principal
- **Elasticsearch 8.x** - Motor de busca e indexação
- **Sentence Transformers** - Modelo de embedding all-MiniLM-L6-v2 de 384 dimensões
- **pdfplumber** - Extração de texto de PDFs
- **python-docx** - Extração de texto de DOCX
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Modelos de IA
- **all-MiniLM-L6-v2** - Modelo de embeddings multilíngue
- **384 dimensões** - Tamanho dos vetores de embedding

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Elasticsearch 8.x

### 🐳 Docker Compose para Mini Search

Configuração completa do Elasticsearch e Kibana para o projeto Mini Search usando Docker Compose.

#### 🚀 Como Usar

 1. Inicie os serviços
Na raíz do projeto, execute para a criação do conteiner do ElasticSearch e Kibana.
```bash
docker-compose up -d
```

2. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/mini-search.git
cd mini-search
```

3. Criação do ambiente virtual(opcional, mas recomendado)

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ⚡ Fluxo de Trabalho

1. Preparação dos Documentos
- Coloque os documentos na pasta `docs/`
- Formatos suportados: **PDF**, **TXT**, **DOCX**

2. Indexação Automática
- O sistema detecta automaticamente novos documentos
- Extrai o texto e gera embeddings
- Indexa os dados no **Elasticsearch**

3. Busca
- Digite os termos de busca
- Visualize os resultados com trechos relevantes

### Estrutura do Projeto

- `mini-search/`
  - `main.py`: Aplicação principal
  - `docker-compose.yml`: Docker Compose para ambiente de desenvolvimento local
  - `requirements.txt`: Dependências do Python
  - `.env`: Variáveis de ambiente
  - `docs/`: Diretório onde são armazenados os arquivos que serão utilizados para busca
    - `historico-aluno.pdf`: Exemplo de documento
  - `src/`
    - `__init__.py`
    - `extract_text.py`: Funções associadas a extração de textos de documentos em PDF, TXT ou DOCX
    - `embedding.py`: Funções de vetorização de palavras extraídas
    - `search.py`: Funções de busca por textos dentro do ElasticSearch
    - `create_index.py`: Criação e gerenciamento de índices.

