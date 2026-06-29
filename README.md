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

O projeto foi estruturado para demonstrar uma solucao completa, indo alem da
execucao tecnica do modelo. A entrega parte do problema de negocio, organiza um
fluxo reproduzivel de dados e apresenta uma POC capaz de apoiar analistas na
exploracao de avaliacoes textuais.

A solucao atende ao desafio em quatro dimensoes principais:

- **Negocio:** traduz o processo manual da editora em uma hipotese mensuravel
  de reducao de tempo, custo e esforco analitico.
- **Dados e NLP:** prepara avaliacoes e metadados, cria documentos textuais e
  utiliza busca semantica para recuperar evidencias relevantes.
- **Base de conhecimento:** usa Chroma como repositorio vetorial local,
  permitindo consultas por contexto e nao apenas por palavras-chave.
- **Produto analitico:** disponibiliza scripts reproduziveis, resumo executivo
  local e interface Streamlit para demonstrar a solucao durante a apresentacao.

Essa organizacao permite discutir tanto as decisoes tecnicas quanto o impacto
esperado para o time de negocio, conforme solicitado no enunciado.

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

Para execucao local e reprodutivel, mantenha no `.env`:

```text
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
LOCAL_EMBEDDING_OFFLINE=true
```

Nesse modo, os embeddings sao calculados localmente. O modelo precisa estar no
cache local para uso offline, reduzindo dependencias externas durante a
avaliacao da POC.

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
Git. Ele serve como artefato de apoio para apresentacao e validacao da analise.

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
artefatos locais ficam fora do GitHub via `.gitignore`.
