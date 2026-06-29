from __future__ import annotations

from collections import Counter
from typing import Any

import pandas as pd

ANALISTAS_PROCESSO_MANUAL = 5
SALARIO_MENSAL_ANALISTA = 5000.0
DIAS_UTEIS_MES = 22
DIAS_PROCESSO_MANUAL = 3.0
DIAS_PROCESSO_COM_SOLUCAO = 0.5
HORAS_DIA = 8


def formatar_moeda(valor: float) -> str:
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def _serie_numerica(df: pd.DataFrame, coluna: str) -> pd.Series:
    if coluna not in df.columns:
        return pd.Series(dtype="float64")
    return pd.to_numeric(df[coluna], errors="coerce")


def _contar_textos(series: pd.Series, top_n: int) -> list[tuple[str, int]]:
    contador: Counter[str] = Counter()
    for valor in series.dropna().astype(str):
        texto = valor.strip()
        if not texto or texto.lower() == "nan":
            continue
        texto = texto.strip("[]").replace("'", "").replace('"', "")
        partes = [parte.strip() for parte in texto.split(",") if parte.strip()]
        contador.update(partes or [texto])
    return contador.most_common(top_n)


def gerar_metricas_base(df: pd.DataFrame) -> dict[str, Any]:
    notas = _serie_numerica(df, "score")
    textos = df["review_text"].fillna("").astype(str) if "review_text" in df.columns else pd.Series(dtype="object")

    total = int(len(df))
    notas_validas = notas.dropna()
    avaliacoes_baixas = int((notas <= 2).sum())
    avaliacoes_altas = int((notas >= 4).sum())

    return {
        "total_avaliacoes": total,
        "livros_unicos": int(df["title"].nunique(dropna=True)) if "title" in df.columns else 0,
        "usuarios_unicos": int(df["user_id"].nunique(dropna=True)) if "user_id" in df.columns else 0,
        "nota_media": float(notas_validas.mean()) if not notas_validas.empty else 0.0,
        "avaliacoes_baixas": avaliacoes_baixas,
        "avaliacoes_altas": avaliacoes_altas,
        "percentual_baixas": avaliacoes_baixas / total if total else 0.0,
        "percentual_altas": avaliacoes_altas / total if total else 0.0,
        "palavras_medias_por_avaliacao": float(textos.str.split().str.len().mean()) if total else 0.0,
    }


def distribuicao_notas(df: pd.DataFrame) -> pd.DataFrame:
    notas = _serie_numerica(df, "score").dropna()
    if notas.empty:
        return pd.DataFrame(columns=["nota", "quantidade", "percentual"])

    distribuicao = notas.round(1).value_counts().sort_index().rename_axis("nota").reset_index(name="quantidade")
    distribuicao["percentual"] = distribuicao["quantidade"] / distribuicao["quantidade"].sum()
    return distribuicao


def principais_autores(df: pd.DataFrame, top_n: int = 10) -> list[tuple[str, int]]:
    if "authors" not in df.columns:
        return []
    return _contar_textos(df["authors"], top_n)


def principais_categorias(df: pd.DataFrame, top_n: int = 10) -> list[tuple[str, int]]:
    if "categories" not in df.columns:
        return []
    return _contar_textos(df["categories"], top_n)


def calcular_impacto_operacional(dias_com_solucao: float = DIAS_PROCESSO_COM_SOLUCAO) -> dict[str, float]:
    custo_mensal_time = ANALISTAS_PROCESSO_MANUAL * SALARIO_MENSAL_ANALISTA
    custo_diario_time = custo_mensal_time / DIAS_UTEIS_MES
    custo_processo_manual = custo_diario_time * DIAS_PROCESSO_MANUAL
    custo_processo_com_solucao = custo_diario_time * dias_com_solucao
    economia_por_ciclo = custo_processo_manual - custo_processo_com_solucao
    reducao_percentual = economia_por_ciclo / custo_processo_manual if custo_processo_manual else 0.0
    horas_liberadas = max(DIAS_PROCESSO_MANUAL - dias_com_solucao, 0) * HORAS_DIA * ANALISTAS_PROCESSO_MANUAL

    return {
        "analistas": float(ANALISTAS_PROCESSO_MANUAL),
        "salario_mensal_por_analista": SALARIO_MENSAL_ANALISTA,
        "custo_mensal_time": custo_mensal_time,
        "custo_diario_time": custo_diario_time,
        "dias_processo_manual": DIAS_PROCESSO_MANUAL,
        "dias_com_solucao": dias_com_solucao,
        "custo_processo_manual": custo_processo_manual,
        "custo_processo_com_solucao": custo_processo_com_solucao,
        "economia_por_ciclo": economia_por_ciclo,
        "reducao_percentual": reducao_percentual,
        "horas_liberadas_por_ciclo": horas_liberadas,
    }
