"""Generic pagination helpers (framework-agnostic)."""

from dataclasses import dataclass
from typing import Generic, List, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int





