"""SQLAlchemy implementation of ProductRepository port."""

from typing import List, Optional, Tuple

from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session

from ...application.ports import ProductRepository
from ...domain.entities import Product
from ..db.models import ProductORM
from ...domain.value_objects import Money


def _to_domain(row: ProductORM) -> Product:
    return Product(
        id=row.id,
        name=row.name,
        price_amount=f"{row.price:.2f}",
        stock_units=row.stock,
        category=row.category or "",
        description=row.description,
        is_active=bool(row.is_active),
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


class SQLAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, *, filters: dict, limit: int, offset: int) -> Tuple[List[Product], int]:
        stmt = select(ProductORM)
        conditions = [ProductORM.is_active == 1]

        category = filters.get("category")
        if category:
            conditions.append(ProductORM.category == category)

        min_price = filters.get("min_price")
        if min_price:
            conditions.append(ProductORM.price >= float(Money(min_price).value))

        max_price = filters.get("max_price")
        if max_price:
            conditions.append(ProductORM.price <= float(Money(max_price).value))

        search = filters.get("search")
        if search:
            conditions.append(ProductORM.name.ilike(f"%{search}%"))

        if conditions:
            stmt = stmt.where(and_(*conditions))

        total = self.session.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        stmt = stmt.order_by(ProductORM.id).limit(limit).offset(offset)
        rows = self.session.execute(stmt).scalars().all()
        return [_to_domain(r) for r in rows], int(total)

    def get_by_id(self, product_id: int) -> Optional[Product]:
        row = self.session.get(ProductORM, product_id)
        return None if row is None else _to_domain(row)

    def create(self, product: Product) -> int:
        row = ProductORM(
            name=product.name,
            price=float(Money(product.price_amount).value),
            stock=product.stock_units,
            category=product.category,
            description=product.description,
            is_active=1 if product.is_active else 0,
        )
        self.session.add(row)
        self.session.flush()
        return int(row.id)

    def update(self, product: Product) -> None:
        row = self.session.get(ProductORM, product.id)
        if row is None:
            raise ValueError("Product not found")
        row.name = product.name
        row.price = float(Money(product.price_amount).value)
        row.stock = product.stock_units
        row.category = product.category
        row.description = product.description
        row.is_active = 1 if product.is_active else 0

    def delete(self, product_id: int, *, soft: bool = True) -> None:
        row = self.session.get(ProductORM, product_id)
        if row is None:
            return
        if soft:
            row.is_active = 0
        else:
            self.session.delete(row)



