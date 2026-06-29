# Resumo dos Arquivos do Projeto

Este documento resume a funcao de cada arquivo e pasta principal do projeto.

## Arquivos da Raiz

### `README.md`

Documento principal do projeto. Apresenta o objetivo, o contexto de negocio, a
arquitetura, os comandos de execucao, a interface Streamlit e as metricas de
qualidade.

### `PLANO_PROJETO.md`

Documento de planejamento. Descreve desafio, hipotese, escopo implementado,
entregaveis, metricas, impacto esperado e roadmap.

### `RESUMO_ARQUIVOS.md`

Guia de leitura do repositorio. Explica a funcao de cada arquivo para facilitar
manutencao, revisao tecnica e apresentacao.

### `requirements.txt`

Lista as bibliotecas Python necessarias para executar o projeto, incluindo
manipulacao de dados, LangChain, Chroma, embeddings locais e Streamlit.

### `.env.example`

Modelo do arquivo de configuracao local. Indica variaveis de ambiente para
execucao com embeddings locais ou, opcionalmente, provedor externo.

### `.gitignore`

Define arquivos e pastas que nao devem ser versionados, como `.env`, ambiente
virtual, dados locais, base vetorial, logs e materiais internos.

### `app.py`

Interface Streamlit da POC. Possui uma visao executiva com metricas, impacto
operacional e distribuicao de notas, alem de uma area de consulta semantica com
filtros por nota.

## Documentacao

### `docs/ALINHAMENTO_DESAFIO.md`

Mapeia os requisitos do desafio para os componentes implementados no projeto.
Serve como checklist de aderencia da entrega.

## Pastas de Dados e Saida

### `data/raw/`

Pasta destinada aos arquivos originais do desafio: `Books_rating.csv` e
`books_data.csv`. Os arquivos sao locais e nao sao enviados ao GitHub.

### `data/processed/`

Pasta destinada aos dados tratados pelo projeto. O script de preparacao salva
nesta pasta a base pronta para analise e busca semantica.

### `reports/`

Pasta local para materiais produzidos durante a analise, como resumo executivo,
metricas e insumos de apresentacao. O conteudo desta pasta fica fora do GitHub.

### `vectorstore/`

Pasta destinada a armazenar a base vetorial local criada com Chroma. Essa base
permite recuperar avaliacoes semanticamente parecidas com uma pergunta de
negocio.

## Scripts de Execucao

### `scripts/01_verificar_ambiente.py`

Verifica se o ambiente minimo esta pronto. Confere arquivos de dados,
configuracao de embeddings e dependencias necessarias para execucao local.

### `scripts/02_preparar_dados.py`

Carrega os arquivos originais, identifica colunas relevantes, remove avaliacoes
sem texto, junta metadados dos livros e salva uma base tratada.

### `scripts/03_criar_base_vetorial.py`

Carrega a base tratada, transforma avaliacoes em documentos LangChain e cria a
base vetorial local com Chroma.

### `scripts/04_perguntar.py`

Executa perguntas de negocio pelo terminal. Consulta a base vetorial, recupera
evidencias semanticamente proximas e permite filtrar por nota minima ou maxima.

### `scripts/05_gerar_resumo_executivo.py`

Gera um resumo executivo local em `reports/`, contendo EDA, distribuicao de
notas, autores/categorias frequentes, metricas de qualidade e impacto financeiro
estimado.

## Pacote Python

### `src/a3_book_insights/__init__.py`

Marca a pasta `a3_book_insights` como pacote Python reutilizavel.

### `src/a3_book_insights/config.py`

Centraliza caminhos importantes do projeto, como dados brutos, dados tratados,
base vetorial e pasta de relatorios locais.

### `src/a3_book_insights/data_loader.py`

Contem funcoes para carregar os dados originais, preparar as avaliacoes e
converter cada avaliacao em documento pesquisavel pelo LangChain.

### `src/a3_book_insights/business_metrics.py`

Centraliza calculos de metricas de negocio, analise exploratoria e impacto
operacional estimado com base no enunciado.

### `src/a3_book_insights/retrieval.py`

Centraliza a logica de recuperacao de evidencias, filtros por nota e resumo de
texto usada pelo terminal e pelo Streamlit.

### `src/a3_book_insights/prompts.py`

Define a instrucao usada em uma evolucao com LLM para gerar respostas
executivas a partir das evidencias recuperadas.

### `src/a3_book_insights/rag_chain.py`

Monta componentes do fluxo RAG: embeddings locais ou externos, base Chroma,
recuperador e cadeia opcional com modelo de linguagem.
