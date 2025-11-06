"""Delete product use case."""

from ..ports import UnitOfWork


def delete_product(uow: UnitOfWork, *, product_id: int, soft: bool = True) -> None:
    uow.products.delete(product_id, soft=soft)
    uow.commit()





