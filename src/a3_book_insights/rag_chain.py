from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from a3_book_insights.prompts import RAG_PROMPT


def load_project_env() -> None:
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)


class LocalSentenceTransformerEmbeddings(Embeddings):
    """Adaptador local para gerar embeddings sem chamadas de API."""

    def __init__(self, model_name: str, local_files_only: bool = True) -> None:
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name, local_files_only=local_files_only)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower().strip() in {"1", "true", "sim", "yes"}


def build_embeddings() -> OpenAIEmbeddings | LocalSentenceTransformerEmbeddings:
    load_project_env()
    provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower().strip()

    if provider == "local":
        model = os.getenv(
            "LOCAL_EMBEDDING_MODEL",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        )
        local_files_only = _env_flag("LOCAL_EMBEDDING_OFFLINE", default=True)
        return LocalSentenceTransformerEmbeddings(model_name=model, local_files_only=local_files_only)

    model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    return OpenAIEmbeddings(model=model)


def build_llm() -> ChatOpenAI:
    load_project_env()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return ChatOpenAI(model=model, temperature=0)


def load_vectorstore(persist_dir: Path) -> Chroma:
    return Chroma(
        collection_name="book_reviews",
        embedding_function=build_embeddings(),
        persist_directory=str(persist_dir),
    )


def build_rag_chain(persist_dir: Path):
    vectorstore = load_vectorstore(persist_dir)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})
    document_chain = create_stuff_documents_chain(build_llm(), RAG_PROMPT)
    return create_retrieval_chain(retriever, document_chain)
