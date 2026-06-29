"""Verifica se o ambiente minimo do projeto esta pronto para execucao."""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import BOOKS_FILE, RATINGS_FILE


def main() -> None:
    # Carrega as variaveis configuradas no arquivo .env.
    load_dotenv()

    # Cada item representa uma dependencia obrigatoria para continuar o fluxo.
    verificacoes = {
        "chave_openai": bool(os.getenv("OPENAI_API_KEY")),
        "arquivo_de_avaliacoes": RATINGS_FILE.exists(),
        "arquivo_de_livros": BOOKS_FILE.exists(),
    }

    # Exibe um diagnostico simples para facilitar a validacao pelo terminal.
    for nome, ok in verificacoes.items():
        status = "OK" if ok else "AUSENTE"
        print(f"{status}: {nome}")

    # Retorna erro quando algum requisito ainda nao esta pronto.
    if not all(verificacoes.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
