"""Create product use case."""

from ..ports import UnitOfWork
from ...domain.entities import Product


def create_product(
    uow: UnitOfWork,
    *,
    name: str,
    price_amount: str,
    stock_units: int,
    category: str,
    description: str | None = None,
) -> int:
    product = Product.create(
        name=name,
        price_amount=price_amount,
        stock_units=stock_units,
        category=category,
        description=description,
    )
    new_id = uow.products.create(product)
    uow.commit()
    return new_id





