"""Consulta a base vetorial local e retorna evidencias recuperadas."""

from __future__ import annotations

import argparse
import sys

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import VECTORSTORE_DIR
from a3_book_insights.rag_chain import load_vectorstore
from a3_book_insights.retrieval import buscar_evidencias, limpar_valor_metadata, resumir_texto


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
    resultados = buscar_evidencias(
        vectorstore=vectorstore,
        pergunta=args.pergunta,
        nota_min=args.nota_min,
        nota_max=args.nota_max,
        top_k=args.top_k,
        fetch_k=args.fetch_k,
    )

    # Exibe as evidencias que podem sustentar a analise de negocio.
    print("\nEVIDENCIAS RECUPERADAS\n")
    if args.nota_min is not None or args.nota_max is not None:
        print(f"Filtro de nota: minimo={args.nota_min} | maximo={args.nota_max}\n")

    if not resultados:
        print("Nenhuma evidencia encontrada com os filtros informados.")
        raise SystemExit(0)

    for posicao, evidencia in enumerate(resultados, start=1):
        doc = evidencia.documento
        metadata = doc.metadata
        titulo = limpar_valor_metadata(metadata.get("title"), padrao="Titulo nao informado")
        usuario = limpar_valor_metadata(metadata.get("user_id"), padrao="Usuario nao informado")
        print(
            f"{posicao}. titulo={titulo} | nota={evidencia.nota:g} "
            f"| usuario={usuario} | distancia={evidencia.distancia:.4f}"
        )
        print(f"   trecho={resumir_texto(doc.page_content)}\n")


if __name__ == "__main__":
    main()
