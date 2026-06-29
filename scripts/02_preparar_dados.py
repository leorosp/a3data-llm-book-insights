"""Prepara uma base tratada de avaliacoes para analise e busca semantica."""

from __future__ import annotations

import argparse
import sys

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import BOOKS_FILE, PROCESSED_REVIEWS_FILE, RATINGS_FILE
from a3_book_insights.data_loader import load_raw_data, prepare_reviews


def main() -> None:
    # O limite padrao mantem a primeira execucao leve e rapida para validacao.
    parser = argparse.ArgumentParser(description="Prepara os dados brutos do desafio.")
    parser.add_argument("--max-linhas", type=int, default=50000)
    args = parser.parse_args()

    # Le os dois CSVs originais: avaliacoes e metadados dos livros.
    ratings, books = load_raw_data(RATINGS_FILE, BOOKS_FILE, max_rows=args.max_linhas)

    # Seleciona colunas relevantes, remove textos vazios e junta metadados.
    prepared = prepare_reviews(ratings, books, max_rows=args.max_linhas)

    # Salva a base intermediaria usada pelas proximas etapas do projeto.
    PROCESSED_REVIEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_csv(PROCESSED_REVIEWS_FILE, index=False)
    print(f"Arquivo gerado com {len(prepared):,} linhas em {PROCESSED_REVIEWS_FILE}")


if __name__ == "__main__":
    main()
