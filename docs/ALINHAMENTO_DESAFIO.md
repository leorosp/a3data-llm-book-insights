# Matriz de Aderencia ao Desafio

Este documento conecta os requisitos do desafio tecnico aos componentes
implementados no projeto. A leitura foi organizada para evidenciar nao apenas
o que foi desenvolvido, mas tambem a razao de cada decisao.

## Leitura do Problema

A editora possui um processo manual para explorar avaliacoes de livros. Segundo
o enunciado, essa atividade leva cerca de 3 dias, envolve 5 analistas e consome
tempo que poderia ser realocado para analises mais estrategicas.

A proposta da POC e reduzir o esforco de triagem textual por meio de uma base
vetorial consultavel por perguntas de negocio. Em vez de navegar manualmente por
milhares de avaliacoes, o analista consegue recuperar evidencias relevantes,
comparar recortes de notas e priorizar investigacoes.

## Aderencia aos Requisitos

| Dimensao avaliada | Evidencia no projeto | Valor para a avaliacao |
| --- | --- | --- |
| Contexto de negocio | `README.md` e `PLANO_PROJETO.md` apresentam o problema, a hipotese e o impacto esperado. | Mostra entendimento do desafio alem da implementacao tecnica. |
| Planejamento | `PLANO_PROJETO.md` descreve escopo, entregaveis, criterios de sucesso e roadmap. | Demonstra organizacao e capacidade de evoluir a solucao. |
| Processo tecnico | Scripts numerados executam verificacao, preparacao, vetorizacao, consulta e resumo executivo. | Facilita reproducibilidade e explicacao durante a entrevista. |
| Analise exploratoria | `scripts/05_gerar_resumo_executivo.py` calcula volume, notas, autores, categorias e distribuicao da amostra. | Sustenta a narrativa com metricas iniciais da base. |
| NLP e busca semantica | `retrieval.py`, `rag_chain.py` e Chroma recuperam evidencias por similaridade semantica. | Mostra aplicacao pratica de NLP em dados textuais. |
| Base de conhecimento | `scripts/03_criar_base_vetorial.py` persiste uma base vetorial local. | Atende a proposta de uso de conhecimento consultavel. |
| Metricas de qualidade | `README.md`, `PLANO_PROJETO.md` e `business_metrics.py` definem cobertura, fidelidade, utilidade e impacto. | Permite avaliar qualidade e valor da solucao. |
| Impacto financeiro | `business_metrics.py` estima custo do processo manual, economia e horas liberadas. | Conecta a POC aos numeros fornecidos no enunciado. |
| Produto demonstravel | `app.py` entrega uma interface Streamlit com visao executiva e consulta semantica. | Facilita demonstracao para publico tecnico e de negocio. |
| Governanca | `.gitignore` remove dados, chaves, logs, base vetorial e relatorios locais do repositorio. | Mostra cuidado com seguranca, tamanho do repo e separacao entre entrega e insumos locais. |

## Decisoes de Escopo

- A POC usa embeddings locais para reduzir custo e dependencia de API.
- A versao atual prioriza recuperacao de evidencias, deixando sumarizacao com
  LLM como evolucao quando houver cota ou orcamento disponivel.
- Dados brutos, base tratada, base vetorial e relatorios gerados ficam fora do
  GitHub por governanca e tamanho.
- A interface Streamlit foi incluida como demonstracao executiva, nao como
  produto final de producao.

## Pontos Fortes Para Apresentacao

- A solucao nasce de uma dor clara de negocio: reduzir tempo de analise manual.
- O codigo esta separado em camadas simples: dados, metricas, recuperacao e
  interface.
- As evidencias recuperadas mantem rastreabilidade com titulo, nota, usuario e
  trecho textual.
- O impacto e estimado com base nos numeros do proprio desafio.
- O roadmap mostra consciencia de evolucao, avaliacao e uso real pelos
  analistas.

## Proximos Passos Recomendados

- Expandir o processamento para uma amostra maior ou para a base completa.
- Criar um conjunto fixo de perguntas de avaliacao manual.
- Medir tempo real de uso com analistas.
- Adicionar filtros por autor, categoria, editora e periodo.
- Incorporar sumarizacao com LLM quando houver cota disponivel.
