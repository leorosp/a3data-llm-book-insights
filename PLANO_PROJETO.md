# Plano do Projeto

## Desafio

A editora explora avaliacoes de livros manualmente. O processo atual leva cerca
de 3 dias e envolve 5 analistas. O objetivo e criar uma solucao que acelere a
exploracao, extraia insights acionaveis e conecte o trabalho tecnico a impacto
operacional e financeiro.

## Hipotese Principal

Uma POC com busca semantica, base vetorial e filtros de negocio pode reduzir a
triagem manual de avaliacoes, permitindo que os analistas encontrem evidencias
relevantes em minutos, nao em dias.

## Escopo Implementado

- Preparacao dos dados de avaliacoes e metadados de livros.
- Conversao de avaliacoes em documentos pesquisaveis.
- Criacao de base vetorial local com Chroma.
- Consulta semantica por pergunta de negocio.
- Filtros por nota para comparar avaliacoes positivas e negativas.
- Analise exploratoria da base tratada.
- Estimativa de impacto operacional com base nos dados do desafio.
- Interface Streamlit para demonstracao da POC.

## Arquitetura

```text
bases CSV
  -> preparacao dos dados
  -> base tratada
  -> analise exploratoria
  -> documentos LangChain
  -> embeddings locais
  -> Chroma vectorstore
  -> recuperador de evidencias
  -> terminal e Streamlit
```

## Entregaveis do Projeto

### Codigo no GitHub

Repositorio com scripts, pacote Python, interface Streamlit, documentacao e
estrutura reproduzivel.

### POC da Solucao

Aplicacao Streamlit e script de consulta semantica que permitem explorar a base
por perguntas de negocio e recuperar evidencias textuais.

### Insumos Para Apresentacao

O script `05_gerar_resumo_executivo.py` gera localmente um resumo com EDA,
metricas e impacto estimado. O arquivo gerado fica em `reports/` e nao e
versionado.

## Metricas de Avaliacao

- Cobertura: evidencias recuperadas por pergunta.
- Fidelidade: aderencia entre evidencia e conclusao.
- Utilidade: apoio a decisoes sobre autores, categorias, livros ou usuarios.
- Acionabilidade: clareza da proxima investigacao sugerida.
- Tempo: comparacao entre fluxo manual e POC.
- Impacto: economia estimada por ciclo de analise.

## Impacto Esperado

Com base no enunciado, o processo manual envolve 5 analistas com salario mensal
de R$ 5.000,00. Considerando 22 dias uteis, o custo diario aproximado do time e
de R$ 1.136,36. Um ciclo manual de 3 dias custa cerca de R$ 3.409,09.

Se a POC reduzir a triagem para 0,5 dia, o custo estimado por ciclo cai para
cerca de R$ 568,18, liberando aproximadamente 100 horas de trabalho por ciclo.

## Roadmap

### Curto Prazo

- Ampliar o volume processado alem da amostra inicial.
- Criar perguntas padrao para avaliacao manual da qualidade.
- Registrar tempo real de execucao das consultas.

### Medio Prazo

- Adicionar filtros por autor, categoria, editora e periodo.
- Criar sumarizacao com LLM quando houver cota ou orcamento disponivel.
- Gerar rankings de oportunidades por autor ou categoria.

### Longo Prazo

- Integrar a solucao ao fluxo dos analistas.
- Monitorar satisfacao do usuario e tempo economizado.
- Criar avaliacao periodica de fidelidade e utilidade das respostas.

## Criterios de Sucesso

- O projeto pode ser executado a partir das instrucoes do README.
- A POC recupera evidencias textuais rastreaveis.
- A solucao apresenta impacto de negocio mensuravel.
- A narrativa final e clara para publico tecnico e nao tecnico.
