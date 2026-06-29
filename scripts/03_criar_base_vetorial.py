"""Cria a base vetorial local a partir da base tratada de avaliacoes."""

from __future__ import annotations

import sys

import pandas as pd
from dotenv import load_dotenv
from langchain_chroma import Chroma
from chromadb import PersistentClient

# Permite importar o pacote local sem instalar o projeto como biblioteca.
sys.path.append("src")

from a3_book_insights.config import PROCESSED_REVIEWS_FILE, VECTORSTORE_DIR
from a3_book_insights.data_loader import reviews_to_documents
from a3_book_insights.rag_chain import build_embeddings


def main() -> None:
    # Carrega o provedor e os modelos configurados no arquivo .env.
    load_dotenv()

    # Esta etapa depende da base gerada pelo script de preparacao dos dados.
    if not PROCESSED_REVIEWS_FILE.exists():
        raise FileNotFoundError("Execute scripts/02_preparar_dados.py primeiro.")

    # Le a base tratada e transforma cada avaliacao em um Document do LangChain.
    df = pd.read_csv(PROCESSED_REVIEWS_FILE, low_memory=False)
    documents = reviews_to_documents(df)

    # Cria embeddings e persiste os vetores localmente no Chroma.
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    client = PersistentClient(path=str(VECTORSTORE_DIR))
    collection_name = "book_reviews"
    try:
        client.delete_collection(collection_name)
    except ValueError:
        pass

    Chroma.from_documents(
        documents=documents,
        embedding=build_embeddings(),
        collection_name=collection_name,
        persist_directory=str(VECTORSTORE_DIR),
    )
    print(f"Base vetorial criada com {len(documents):,} documentos em {VECTORSTORE_DIR}")


if __name__ == "__main__":
    main()
