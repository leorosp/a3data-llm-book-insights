"""Gera um resumo executivo local com EDA, metricas e impacto estimado."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

import pandas as pd

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.business_metrics import (
    calcular_impacto_operacional,
    distribuicao_notas,
    formatar_moeda,
    gerar_metricas_base,
    principais_autores,
    principais_categorias,
)
from a3_book_insights.config import EXECUTIVE_SUMMARY_FILE, PROCESSED_REVIEWS_FILE


def _percentual(valor: float) -> str:
    return f"{valor:.1%}".replace(".", ",")


def _numero(valor: int | float) -> str:
    if isinstance(valor, float):
        return f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{valor:,}".replace(",", ".")


def _tabela_markdown(linhas: list[tuple[str, int]]) -> str:
    if not linhas:
        return "Sem dados disponiveis.\n"

    conteudo = ["| Item | Quantidade |", "| --- | ---: |"]
    conteudo.extend(f"| {item} | {quantidade} |" for item, quantidade in linhas)
    return "\n".join(conteudo) + "\n"


def gerar_markdown(df: pd.DataFrame, dias_com_solucao: float) -> str:
    metricas = gerar_metricas_base(df)
    impacto = calcular_impacto_operacional(dias_com_solucao=dias_com_solucao)
    dist = distribuicao_notas(df)

    distribuicao_md = ["| Nota | Quantidade | Percentual |", "| ---: | ---: | ---: |"]
    for _, linha in dist.iterrows():
        distribuicao_md.append(
            f"| {linha['nota']} | {int(linha['quantidade'])} | {_percentual(float(linha['percentual']))} |"
        )

    return f"""# Resumo Executivo da Analise

Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M")}

## Contexto

A editora realiza a exploracao de avaliacoes de livros de forma manual. O
processo informado no desafio leva cerca de 3 dias e envolve 5 analistas. A POC
propoe uma busca semantica com base vetorial local para reduzir o tempo de
triagem, recuperar evidencias e apoiar decisoes sobre autores, categorias e
usuarios relevantes.

## Resumo da Base Tratada

- Avaliacoes analisadas: {_numero(metricas["total_avaliacoes"])}
- Livros unicos: {_numero(metricas["livros_unicos"])}
- Usuarios unicos: {_numero(metricas["usuarios_unicos"])}
- Nota media: {_numero(metricas["nota_media"])}
- Avaliacoes baixas: {_percentual(metricas["percentual_baixas"])}
- Avaliacoes altas: {_percentual(metricas["percentual_altas"])}
- Palavras medias por avaliacao: {_numero(metricas["palavras_medias_por_avaliacao"])}

## Distribuicao de Notas

{chr(10).join(distribuicao_md)}

## Autores Mais Frequentes

{_tabela_markdown(principais_autores(df, top_n=10))}

## Categorias Mais Frequentes

{_tabela_markdown(principais_categorias(df, top_n=10))}

## Estimativa de Impacto Operacional

- Custo mensal estimado do time: {formatar_moeda(impacto["custo_mensal_time"])}
- Custo diario estimado do time: {formatar_moeda(impacto["custo_diario_time"])}
- Custo estimado do processo manual por ciclo: {formatar_moeda(impacto["custo_processo_manual"])}
- Custo estimado com a POC por ciclo: {formatar_moeda(impacto["custo_processo_com_solucao"])}
- Economia estimada por ciclo: {formatar_moeda(impacto["economia_por_ciclo"])}
- Reducao estimada: {_percentual(impacto["reducao_percentual"])}
- Horas liberadas por ciclo: {_numero(impacto["horas_liberadas_por_ciclo"])}

## Metricas Recomendadas Para Avaliar a Qualidade

- Cobertura: quantidade de evidencias recuperadas por pergunta de negocio.
- Fidelidade: aderencia entre resposta e evidencias textuais recuperadas.
- Utilidade: capacidade de apoiar decisoes sobre autores, generos ou usuarios.
- Acionabilidade: clareza da proxima acao sugerida para o negocio.
- Tempo de analise: comparacao entre o processo manual e o fluxo com a POC.

## Proximas Evolucoes

- Ampliar a base processada para alem da amostra inicial.
- Criar um conjunto fixo de perguntas de avaliacao manual.
- Adicionar sumarizacao com LLM quando houver orcamento ou cota disponivel.
- Enriquecer filtros por autor, categoria e periodo de publicacao.
- Medir tempo real de resposta e satisfacao dos analistas em uso assistido.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera resumo executivo local para apoio a apresentacao.")
    parser.add_argument(
        "--dias-com-solucao",
        type=float,
        default=0.5,
        help="Estimativa de dias necessarios para analise usando a POC.",
    )
    parser.add_argument(
        "--saida",
        default=str(EXECUTIVE_SUMMARY_FILE),
        help="Arquivo de saida do resumo executivo.",
    )
    args = parser.parse_args()

    if not PROCESSED_REVIEWS_FILE.exists():
        raise FileNotFoundError("Execute scripts/02_preparar_dados.py antes de gerar o resumo.")

    df = pd.read_csv(PROCESSED_REVIEWS_FILE, low_memory=False)
    markdown = gerar_markdown(df, dias_com_solucao=args.dias_com_solucao)

    output_path = EXECUTIVE_SUMMARY_FILE.parent / EXECUTIVE_SUMMARY_FILE.name
    if args.saida:
        from pathlib import Path

        output_path = Path(args.saida)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Resumo executivo gerado em {output_path}")


if __name__ == "__main__":
    main()
