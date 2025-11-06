"""SQLAlchemy-based Unit of Work for products."""

from typing import Optional

from sqlalchemy.orm import Session

from ..application.ports import UnitOfWork
from .db.session import SessionLocal
from .repositories.product_repository_sqlalchemy import SQLAlchemyProductRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self._session: Optional[Session] = None
        self.products = None  # type: ignore[assignment]

    def __enter__(self) -> "SQLAlchemyUnitOfWork":
        self._session = SessionLocal()
        self.products = SQLAlchemyProductRepository(self._session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc:
                self.rollback()
            else:
                self.commit()
        finally:
            if self._session is not None:
                self._session.close()
                self._session = None

    def commit(self) -> None:
        if self._session is not None:
            self._session.commit()

    def rollback(self) -> None:
        if self._session is not None:
            self._session.rollback()


