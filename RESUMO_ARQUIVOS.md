# Resumo dos Arquivos do Projeto

Este documento resume a funcao de cada arquivo e pasta principal do projeto.

## Arquivos da Raiz

### `README.md`

Documento principal do projeto. Apresenta o objetivo, a pergunta central, os
dados esperados, a configuracao do ambiente, os comandos de execucao e a
estrutura geral da solucao.

### `PLANO_PROJETO.md`

Documento de planejamento. Descreve o desafio, o escopo da versao inicial, a
arquitetura proposta, o roteiro de desenvolvimento e os criterios de sucesso.

### `requirements.txt`

Lista as bibliotecas Python necessarias para executar o projeto, incluindo
pacotes para manipulacao de dados, variaveis de ambiente, LangChain, Chroma e
integracao com modelos de linguagem.

### `.env.example`

Modelo do arquivo de configuracao local. Indica quais variaveis de ambiente
devem ser preenchidas para executar o projeto, como a chave do provedor de
modelo e os nomes dos modelos utilizados.

### `.gitignore`

Define arquivos e pastas que nao devem ser versionados no repositorio, como
ambiente virtual, arquivos de cache, base vetorial, dados locais e arquivo
`.env`.

### `app.py`

Interface Streamlit do projeto. Permite consultar a base vetorial local por uma
pergunta de negocio, aplicar filtros por nota e visualizar as evidencias
recuperadas em tela.

## Pastas de Dados e Saida

### `data/raw/`

Pasta destinada aos arquivos originais do desafio. Nesta pasta devem ser
colocados os arquivos `Books_rating.csv` e `books_data.csv`.

### `data/raw/.gitkeep`

Arquivo vazio usado para manter a pasta `data/raw/` no repositorio mesmo antes
da inclusao dos dados originais.

### `data/processed/`

Pasta destinada aos dados tratados pelo projeto. O script de preparacao salva
nesta pasta a base pronta para analise e busca semantica.

### `data/processed/.gitkeep`

Arquivo vazio usado para manter a pasta `data/processed/` no repositorio.

### `reports/`

Pasta reservada para materiais produzidos durante a analise, como tabelas,
resumos, metricas e insumos para a apresentacao executiva.

### `reports/.gitkeep`

Arquivo vazio usado para manter a pasta `reports/` no repositorio.

### `vectorstore/`

Pasta destinada a armazenar a base vetorial local criada com Chroma. Essa base
permite recuperar avaliacoes semanticamente parecidas com uma pergunta de
negocio.

### `vectorstore/.gitkeep`

Arquivo vazio usado para manter a pasta `vectorstore/` no repositorio.

## Scripts de Execucao

### `scripts/01_verificar_ambiente.py`

Verifica se o ambiente esta configurado corretamente. O script confere a
existencia da chave do provedor de modelo e dos arquivos de dados esperados.

### `scripts/02_preparar_dados.py`

Carrega os arquivos originais, identifica as colunas relevantes, remove
avaliacoes sem texto e salva uma base tratada em `data/processed/`.

### `scripts/03_criar_base_vetorial.py`

Carrega a base tratada, transforma as avaliacoes em documentos e cria a base
vetorial local com Chroma.

### `scripts/04_perguntar.py`

Executa perguntas de negocio pelo terminal. O script consulta a base vetorial
local, recupera evidencias semanticamente proximas e exibe os trechos que podem
sustentar a analise. Tambem permite filtrar evidencias por nota minima ou
maxima, facilitando comparacoes entre avaliacoes positivas e negativas.

## Pacote Python

### `src/a3_book_insights/__init__.py`

Marca a pasta `a3_book_insights` como um pacote Python reutilizavel dentro do
projeto.

### `src/a3_book_insights/config.py`

Centraliza caminhos importantes do projeto, como pastas de dados, arquivos de
entrada, arquivo tratado e diretorio da base vetorial.

### `src/a3_book_insights/data_loader.py`

Contem funcoes para carregar os dados originais, preparar as avaliacoes e
converter cada avaliacao em documento pesquisavel pelo LangChain.

### `src/a3_book_insights/prompts.py`

Define a instrucao usada pelo fluxo RAG. A instrucao orienta o modelo a
responder com foco em negocio, usando apenas as evidencias recuperadas.

### `src/a3_book_insights/rag_chain.py`

Monta os componentes principais do fluxo RAG: representacoes vetoriais, modelo
de linguagem, base Chroma, recuperador de evidencias e cadeia de perguntas e
respostas.
