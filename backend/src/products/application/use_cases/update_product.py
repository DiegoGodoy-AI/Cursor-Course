"""Update product use case."""

from ..ports import UnitOfWork


def update_product(
    uow: UnitOfWork,
    *,
    product_id: int,
    name: str | None = None,
    price_amount: str | None = None,
    stock_units: int | None = None,
    category: str | None = None,
    description: str | None = None,
    is_active: bool | None = None,
) -> None:
    existing = uow.products.get_by_id(product_id)
    if existing is None:
        raise ValueError("Product not found")

    updated = existing.with_updates(
        name=name,
        price_amount=price_amount,
        stock_units=stock_units,
        category=category,
        description=description,
        is_active=is_active,
    )
    uow.products.update(updated)
    uow.commit()





