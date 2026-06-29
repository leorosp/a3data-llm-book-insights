from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
VECTORSTORE_DIR = ROOT_DIR / "vectorstore"

RATINGS_FILE = DATA_RAW_DIR / "Books_rating.csv"
BOOKS_FILE = DATA_RAW_DIR / "books_data.csv"
PROCESSED_REVIEWS_FILE = DATA_PROCESSED_DIR / "avaliacoes_preparadas.csv"
