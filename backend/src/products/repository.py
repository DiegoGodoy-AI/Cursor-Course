from typing import List
from datetime import datetime

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from .models import Product
from .database import DATABASE_PATH


class Base(DeclarativeBase):
    pass


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    category: Mapped[str | None]
    description: Mapped[str | None]
    is_active: Mapped[int]
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]


# Use the same SQLite database file used elsewhere in the app
engine = create_engine(f"sqlite:///{DATABASE_PATH}", future=True)


def find_products_by_category(
    category: str,
    *,
    limit: int = 50,
    offset: int = 0,
    include_inactive: bool = False,
) -> List[Product]:
    """Return products filtered by category using SQLAlchemy, with pagination.

    Converts ORM rows to existing Pydantic `Product` models.
    """
    if not category or not category.strip():
        return []

    with Session(engine) as session:
        stmt = select(ProductORM).where(ProductORM.category == category)
        if not include_inactive:
            stmt = stmt.where(ProductORM.is_active == 1)

        stmt = stmt.order_by(ProductORM.id).limit(limit).offset(offset)
        rows = session.execute(stmt).scalars().all()

        return [
            Product(
                id=row.id,
                name=row.name,
                price=row.price,
                stock=row.stock,
                category=row.category or "",
                description=row.description,
                is_active=bool(row.is_active),
                created_at=row.created_at,
                updated_at=row.updated_at,
            )
            for row in rows
        ]


