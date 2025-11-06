"""Application-level DTOs for inputs and outputs of product use cases."""

from dataclasses import dataclass
from typing import List

from ..domain.entities import Product


@dataclass
class ListProductsFilters:
    category: str | None = None
    min_price: str | None = None  # decimal as string at boundary
    max_price: str | None = None
    search: str | None = None


@dataclass
class Page:
    items: List[Product]
    total: int
    limit: int
    offset: int





