# A3Data - Analise de Avaliacoes de Livros com Modelos de Linguagem

Projeto desenvolvido para o desafio tecnico de Cientista de Dados Sr. com foco
em processamento de linguagem natural e modelos de linguagem.

## Objetivo do Projeto

Construir uma prova de conceito para ajudar uma editora a explorar avaliacoes
de livros e metadados de forma mais rapida, estruturada e orientada por
evidencias.

A versao inicial utiliza LangChain para:

- carregar e preparar os dados de avaliacoes;
- transformar avaliacoes em documentos pesquisaveis;
- criar representacoes vetoriais e uma base local de busca semantica;
- responder perguntas de negocio com evidencias recuperadas;
- apoiar a construcao da apresentacao executiva final.

## Pergunta Central da Versao Inicial

Uma solucao RAG com LangChain consegue reduzir o tempo necessario para analisar
avaliacoes de livros, substituindo parte do fluxo manual de 3 dias por uma
exploracao guiada e baseada em evidencias?

## Primeiro Marco

Criar um fluxo RAG executado pelo terminal:

```text
pergunta de negocio -> busca semantica nas avaliacoes -> evidencias citadas -> resposta executiva
```

## Dados Esperados

Coloque os arquivos do desafio em `data/raw/`:

- `Books_rating.csv`
- `books_data.csv`

## Configuracao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Depois, edite o arquivo `.env` com a chave do provedor de modelo.

Para criar a base vetorial sem custo de API, mantenha:

```text
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LOCAL_EMBEDDING_OFFLINE=true
```

Nesse modo, os embeddings sao calculados localmente no computador. O modelo e
baixado uma vez na primeira execucao. Depois disso, a variavel
`LOCAL_EMBEDDING_OFFLINE=true` faz a consulta usar apenas o cache local.

O script de consulta retorna evidencias recuperadas da base vetorial local. Ele
nao chama um modelo externo de linguagem, evitando custo de API durante a
validacao inicial.

## Execucao Passo a Passo

```powershell
python scripts/01_verificar_ambiente.py
python scripts/02_preparar_dados.py --max-linhas 1000
python scripts/03_criar_base_vetorial.py
python scripts/04_perguntar.py "<pergunta de negocio>" --nota-min 4
python scripts/04_perguntar.py "<pergunta de negocio>" --nota-max 2
```

## Interface Streamlit

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502 --server.fileWatcherType none
```

A interface permite informar uma pergunta de negocio, aplicar filtros por nota
e visualizar as evidencias recuperadas da base vetorial local.

## Estrutura do Projeto

```text
app.py                    interface Streamlit para consulta visual
data/raw/                 bases originais
data/processed/           bases tratadas para analise e RAG
reports/                  materiais produzidos para analise
scripts/                  comandos executaveis passo a passo
src/a3_book_insights/     pacote Python reutilizavel
vectorstore/              base vetorial local com Chroma
```

## Observacoes

O projeto possui duas formas de execucao: pelos scripts numerados, para mostrar
cada etapa do processamento, e pela interface Streamlit, para consultar as
evidencias de forma visual.
