from __future__ import annotations

from dataclasses import dataclass
from math import isnan
from typing import Any

from langchain_core.documents import Document


@dataclass(frozen=True)
class Evidencia:
    documento: Document
    distancia: float
    nota: float | None


def converter_nota(valor: object) -> float | None:
    try:
        nota = float(valor)
    except (TypeError, ValueError):
        return None
    return None if isnan(nota) else nota


def passa_filtro_nota(nota: float | None, nota_min: float | None, nota_max: float | None) -> bool:
    if nota is None:
        return False
    if nota_min is not None and nota < nota_min:
        return False
    if nota_max is not None and nota > nota_max:
        return False
    return True


def resumir_texto(texto: str, limite: int = 500) -> str:
    texto_limpo = " ".join(texto.split())
    if len(texto_limpo) <= limite:
        return texto_limpo
    return f"{texto_limpo[:limite].rstrip()}..."


def limpar_valor_metadata(valor: object, padrao: str = "Nao informado") -> str:
    if valor is None:
        return padrao
    texto = str(valor).strip()
    if not texto or texto.lower() in {"nan", "none", "<na>"}:
        return padrao
    return texto


def buscar_evidencias(
    vectorstore: Any,
    pergunta: str,
    nota_min: float | None = None,
    nota_max: float | None = None,
    top_k: int = 5,
    fetch_k: int = 50,
) -> list[Evidencia]:
    candidatos = vectorstore.similarity_search_with_score(pergunta, k=max(fetch_k, top_k))

    evidencias: list[Evidencia] = []
    for documento, distancia in candidatos:
        nota = converter_nota(documento.metadata.get("score"))
        if passa_filtro_nota(nota, nota_min, nota_max):
            evidencias.append(Evidencia(documento=documento, distancia=float(distancia), nota=nota))
        if len(evidencias) >= top_k:
            break

    return evidencias
