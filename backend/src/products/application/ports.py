"""Ports (interfaces) for repositories and units of work in the products context."""

from typing import Protocol, Optional, List, Any

from ..domain.entities import Product


class ProductRepository(Protocol):
    def list(self, *, filters: dict, limit: int, offset: int) -> tuple[List[Product], int]:
        ...

    def get_by_id(self, product_id: int) -> Optional[Product]:
        ...

    def create(self, product: Product) -> int:
        ...

    def update(self, product: Product) -> None:
        ...

    def delete(self, product_id: int, *, soft: bool = True) -> None:
        ...


class UnitOfWork(Protocol):
    products: ProductRepository

    def __enter__(self) -> "UnitOfWork":
        ...

    def __exit__(self, exc_type, exc, tb) -> None:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...





