"""Consulta a base vetorial local e retorna evidencias recuperadas."""

from __future__ import annotations

import argparse
import sys

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import VECTORSTORE_DIR
from a3_book_insights.rag_chain import load_vectorstore


def _converter_nota(valor: object) -> float | None:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return None


def _passa_filtro_nota(nota: float | None, nota_min: float | None, nota_max: float | None) -> bool:
    if nota is None:
        return False
    if nota_min is not None and nota < nota_min:
        return False
    if nota_max is not None and nota > nota_max:
        return False
    return True


def _resumir_texto(texto: str, limite: int = 500) -> str:
    texto_limpo = " ".join(texto.split())
    if len(texto_limpo) <= limite:
        return texto_limpo
    return f"{texto_limpo[:limite].rstrip()}..."


def main() -> None:
    # A pergunta de negocio e recebida pelo terminal para facilitar testes.
    parser = argparse.ArgumentParser(description="Consulta evidencias na base vetorial local.")
    parser.add_argument("pergunta", help="Pergunta de negocio para consultar o corpus de avaliacoes")
    parser.add_argument("--top-k", type=int, default=5, help="Quantidade de evidencias recuperadas")
    parser.add_argument("--nota-min", type=float, default=None, help="Nota minima das avaliacoes retornadas")
    parser.add_argument("--nota-max", type=float, default=None, help="Nota maxima das avaliacoes retornadas")
    parser.add_argument(
        "--fetch-k",
        type=int,
        default=50,
        help="Quantidade de candidatos buscados antes do filtro por nota",
    )
    args = parser.parse_args()

    # Carrega a base vetorial criada anteriormente e usa embeddings locais para buscar.
    vectorstore = load_vectorstore(VECTORSTORE_DIR)
    fetch_k = max(args.fetch_k, args.top_k)
    candidatos = vectorstore.similarity_search_with_score(args.pergunta, k=fetch_k)

    # Filtra as evidencias por nota, quando os limites forem informados.
    resultados = []
    for doc, score in candidatos:
        nota = _converter_nota(doc.metadata.get("score"))
        if _passa_filtro_nota(nota, args.nota_min, args.nota_max):
            resultados.append((doc, score, nota))
        if len(resultados) >= args.top_k:
            break

    # Exibe as evidencias que podem sustentar a analise de negocio.
    print("\nEVIDENCIAS RECUPERADAS\n")
    if args.nota_min is not None or args.nota_max is not None:
        print(f"Filtro de nota: minimo={args.nota_min} | maximo={args.nota_max}\n")

    if not resultados:
        print("Nenhuma evidencia encontrada com os filtros informados.")
        raise SystemExit(0)

    for posicao, (doc, score, nota) in enumerate(resultados, start=1):
        metadata = doc.metadata
        print(
            f"{posicao}. titulo={metadata.get('title')} | nota={nota:g} "
            f"| usuario={metadata.get('user_id')} | distancia={score:.4f}"
        )
        print(f"   trecho={_resumir_texto(doc.page_content)}\n")


if __name__ == "__main__":
    main()
