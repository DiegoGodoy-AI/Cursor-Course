"""Session and engine configuration for SQLAlchemy 2.0 style."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.database import get_database_url


def _to_sqlalchemy_url(db_path: str) -> str:
    if db_path.startswith("sqlite://"):
        return db_path
    return f"sqlite:///{db_path}"


engine = create_engine(_to_sqlalchemy_url(get_database_url()), future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


