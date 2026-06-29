# Plano do Projeto

## Desafio

A editora explora avaliacoes de livros manualmente. O processo atual leva cerca
de 3 dias e envolve 5 analistas. O desafio e propor uma solucao que acelere a
exploracao, extraia insights acionaveis e conecte o trabalho tecnico ao impacto
de negocio.

## Escopo da Versao Inicial

A primeira versao sera uma solucao RAG com LangChain para analise de
avaliacoes de livros.

Ele deve apoiar analises como:

- identificacao de reclamacoes em avaliacoes com baixa nota;
- priorizacao de autores ou categorias que merecem atencao editorial;
- localizacao de usuarios com avaliacoes detalhadas;
- comparacao entre fatores de satisfacao positiva e negativa;
- recuperacao das evidencias que sustentam cada resposta.

## Arquitetura

```text
bases CSV
  -> preparacao dos dados
  -> documentos de avaliacoes
  -> representacoes vetoriais
  -> base vetorial Chroma
  -> recuperador de evidencias
  -> instrucao LangChain
  -> resposta com citacoes
```

## Roteiro

### Etapa 1 - Fundacao do projeto

- Criar a estrutura do repositorio.
- Definir dependencias e variaveis de ambiente.
- Adicionar plano do projeto e README.

### Etapa 2 - Preparacao dos dados

- Carregar notas, avaliacoes e metadados de livros.
- Unir as duas bases.
- Normalizar colunas relevantes.
- Criar uma base tratada para iteracao rapida.

### Etapa 3 - RAG com LangChain

- Converter avaliacoes em objetos `Document` do LangChain.
- Gerar representacoes vetoriais.
- Persistir uma base vetorial local com Chroma.
- Criar recuperador de evidencias e cadeia de perguntas e respostas.

### Etapa 4 - Avaliacao

- Medir quantidade de evidencias recuperadas.
- Medir completude das fontes.
- Criar um pequeno conjunto de perguntas para avaliacao manual.
- Avaliar utilidade, fidelidade e acionabilidade.

### Etapa 5 - Narrativa de negocio

- Estimar reducao do custo manual.
- Resumir insights por autor, categoria e usuario.
- Preparar uma apresentacao de 30 minutos.

### Etapa 6 - Aplicacao opcional

- Adicionar uma interface em Streamlit depois que a prova de conceito no
  terminal estiver funcionando.

## Criterios de Sucesso

- O projeto pode ser executado a partir das instrucoes do README.
- As respostas incluem evidencias da base de avaliacoes.
- A solucao conecta claramente resultados de processamento de linguagem natural
  e modelos de linguagem a decisoes de negocio.
- A narrativa final e clara para um publico nao tecnico.
