from __future__ import annotations

from pathlib import Path

import pandas as pd
from langchain_core.documents import Document


def _first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized = {col.lower().strip(): col for col in df.columns}
    for candidate in candidates:
        found = normalized.get(candidate.lower().strip())
        if found:
            return found
    return None


def _clean_metadata_value(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "<na>"} else text


def load_raw_data(
    ratings_path: Path,
    books_path: Path,
    max_rows: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # A base de avaliacoes e grande; na primeira versao lemos apenas a amostra definida.
    ratings = pd.read_csv(ratings_path, low_memory=False, nrows=max_rows)
    books = pd.read_csv(books_path, low_memory=False)
    return ratings, books


def prepare_reviews(
    ratings: pd.DataFrame,
    books: pd.DataFrame,
    max_rows: int = 50000,
) -> pd.DataFrame:
    review_text_col = _first_existing_column(
        ratings,
        ["review/text", "review_text", "text", "review", "summary"],
    )
    score_col = _first_existing_column(ratings, ["review/score", "score", "rating"])
    title_col = _first_existing_column(ratings, ["title", "book_title"])
    user_col = _first_existing_column(ratings, ["user_id", "user/id", "user"])
    book_id_col = _first_existing_column(ratings, ["Id", "book_id", "asin"])

    if review_text_col is None:
        raise ValueError("Nao foi possivel encontrar uma coluna de texto de avaliacao na base de ratings.")

    prepared = pd.DataFrame(
        {
            "review_text": ratings[review_text_col].fillna("").astype(str),
            "score": ratings[score_col] if score_col else pd.NA,
            "title": ratings[title_col] if title_col else pd.NA,
            "user_id": ratings[user_col] if user_col else pd.NA,
            "book_id": ratings[book_id_col] if book_id_col else pd.NA,
        }
    )

    if "Title" in books.columns and title_col:
        metadata_cols = [col for col in ["Title", "authors", "categories", "publisher"] if col in books.columns]
        if metadata_cols:
            book_metadata = books[metadata_cols].drop_duplicates(subset=["Title"])
            prepared = prepared.merge(
                book_metadata,
                left_on="title",
                right_on="Title",
                how="left",
            )

    prepared = prepared[prepared["review_text"].str.strip().ne("")]
    prepared = prepared.head(max_rows).reset_index(drop=True)
    return prepared


def reviews_to_documents(df: pd.DataFrame) -> list[Document]:
    documents: list[Document] = []
    for idx, row in df.iterrows():
        metadata = {
            "row_id": int(idx),
            "title": _clean_metadata_value(row.get("title", "")),
            "score": _clean_metadata_value(row.get("score", "")),
            "user_id": _clean_metadata_value(row.get("user_id", "")),
            "author": _clean_metadata_value(row.get("authors", "")),
            "category": _clean_metadata_value(row.get("categories", "")),
        }
        documents.append(Document(page_content=str(row["review_text"]), metadata=metadata))
    return documents
