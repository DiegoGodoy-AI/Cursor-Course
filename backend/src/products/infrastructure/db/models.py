"""ORM models for the products context."""

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Numeric


class Base(DeclarativeBase):
    pass


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]  # kept as float to match existing legacy schema
    stock: Mapped[int]
    category: Mapped[str | None]
    description: Mapped[str | None]
    is_active: Mapped[int]
    created_at: Mapped[datetime | None]
    updated_at: Mapped[datetime | None]


