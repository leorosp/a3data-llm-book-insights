"""Verifica se o ambiente minimo do projeto esta pronto para execucao."""

from __future__ import annotations

import os
import sys
from importlib.util import find_spec

from dotenv import load_dotenv

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import BOOKS_FILE, RATINGS_FILE


def main() -> None:
    # Carrega as variaveis configuradas no arquivo .env.
    load_dotenv()
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower().strip()

    # Cada item representa uma dependencia obrigatoria para continuar o fluxo local.
    verificacoes_obrigatorias = {
        "arquivo_de_avaliacoes": RATINGS_FILE.exists(),
        "arquivo_de_livros": BOOKS_FILE.exists(),
        "provedor_de_embeddings_configurado": embedding_provider in {"local", "openai"},
    }

    if embedding_provider == "local":
        verificacoes_obrigatorias["sentence_transformers_instalado"] = find_spec("sentence_transformers") is not None
        verificacoes_informativas = {"chave_openai": "DISPENSADA"}
    else:
        verificacoes_obrigatorias["chave_openai"] = bool(os.getenv("OPENAI_API_KEY"))
        verificacoes_informativas = {}

    # Exibe um diagnostico simples para facilitar a validacao pelo terminal.
    for nome, ok in verificacoes_obrigatorias.items():
        status = "OK" if ok else "AUSENTE"
        print(f"{status}: {nome}")

    for nome, status in verificacoes_informativas.items():
        print(f"{status}: {nome}")

    # Retorna erro quando algum requisito ainda nao esta pronto.
    if not all(verificacoes_obrigatorias.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
