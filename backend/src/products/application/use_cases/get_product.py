"""Get single product use case."""

from typing import Optional

from ..ports import UnitOfWork
from ...domain.entities import Product


def get_product(uow: UnitOfWork, *, product_id: int) -> Optional[Product]:
    return uow.products.get_by_id(product_id)





