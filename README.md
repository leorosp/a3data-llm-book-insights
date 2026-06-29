# A3Data - Analise Semantica de Avaliacoes de Livros

Projeto desenvolvido para o desafio tecnico de Cientista de Dados com foco em
NLP, busca semantica, base de conhecimento e impacto de negocio.

## Resumo Executivo

A editora do desafio realiza a exploracao de avaliacoes de livros de forma
manual. O processo informado leva cerca de 3 dias, envolve 5 analistas e tem
custo operacional relevante.

A proposta deste projeto e uma POC que combina:

- preparacao de dados textuais e metadados de livros;
- analise exploratoria da base tratada;
- busca semantica com LangChain e Chroma;
- recuperacao de evidencias textuais por pergunta de negocio;
- estimativa de reducao de custo e tempo do processo manual;
- interface Streamlit para exploracao visual.

## Objetivo

Reduzir o tempo de triagem e exploracao das avaliacoes, permitindo que analistas
encontrem rapidamente evidencias sobre autores, categorias, livros e usuarios
com opinioes relevantes.

## Alinhamento com o Desafio

O projeto cobre os principais pontos solicitados:

- apresentacao do problema e planejamento em `PLANO_PROJETO.md`;
- processo tecnico reproduzivel por scripts numerados;
- analise exploratoria e metricas pelo script `05_gerar_resumo_executivo.py`;
- proposta de sumarizacao e RAG com LangChain;
- uso de base de conhecimento local com Chroma;
- metricas para avaliar qualidade do resultado;
- estimativa de impacto financeiro e operacional;
- POC opcional em Streamlit.

## Arquitetura da Solucao

```text
CSVs originais
  -> preparacao e limpeza
  -> base tratada de avaliacoes
  -> analise exploratoria e metricas
  -> documentos LangChain
  -> embeddings locais
  -> Chroma vectorstore
  -> busca semantica por pergunta de negocio
  -> evidencias para analise executiva
```

## Dados Esperados

Os arquivos originais do desafio devem ser colocados em `data/raw/`:

- `Books_rating.csv`
- `books_data.csv`

Esses arquivos nao sao versionados no GitHub por tamanho e governanca de dados.

## Configuracao do Ambiente

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Para execucao sem custo de API, mantenha no `.env`:

```text
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LOCAL_EMBEDDING_OFFLINE=true
```

Nesse modo, os embeddings sao calculados localmente. O modelo precisa estar no
cache local para uso offline.

## Execucao Passo a Passo

```powershell
python scripts/01_verificar_ambiente.py
python scripts/02_preparar_dados.py --max-linhas 1000
python scripts/03_criar_base_vetorial.py
python scripts/04_perguntar.py "<pergunta de negocio>" --nota-min 4
python scripts/04_perguntar.py "<pergunta de negocio>" --nota-max 2
python scripts/05_gerar_resumo_executivo.py
```

O arquivo gerado pelo script `05` fica em `reports/`, pasta local ignorada pelo
Git. Ele serve como insumo para apresentacao, sem expor anotacoes privadas no
repositorio.

## Interface Streamlit

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502 --server.fileWatcherType none
```

A interface possui uma visao executiva com metricas, impacto operacional e
distribuicao de notas, alem de uma area de consulta semantica com filtros por
nota.

## Metricas de Qualidade

As metricas recomendadas para avaliar a solucao sao:

- cobertura de evidencias recuperadas por pergunta;
- fidelidade entre evidencia textual e conclusao;
- utilidade para decisao de negocio;
- acionabilidade da proxima etapa sugerida;
- reducao de tempo em relacao ao processo manual;
- economia estimada por ciclo de analise.

## Estrutura do Projeto

```text
app.py                    interface Streamlit da POC
data/raw/                 bases originais locais
data/processed/           base tratada local
docs/                     documentos de alinhamento da entrega
reports/                  saidas locais para apresentacao e analise
scripts/                  scripts numerados de execucao
src/a3_book_insights/     pacote Python reutilizavel
vectorstore/              base vetorial local com Chroma
```

## Governanca da Entrega

O repositorio contem codigo, documentacao e estrutura de pastas. Arquivos
sensiveis, dados brutos, dados tratados, base vetorial, logs, ambiente virtual e
anotacoes internas ficam fora do GitHub via `.gitignore`.
