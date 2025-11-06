"""Domain entities for products.

Keep this layer free of framework and persistence concerns.
"""

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Optional

from .value_objects import Money, Stock
from .errors import InvalidProductName


@dataclass
class Product:
    """Aggregate root representing a product in the catalog."""
    id: Optional[int]
    name: str
    price_amount: str  # use Decimal as string at boundaries; VO handles validation
    stock_units: int
    category: str
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def create(
        *,
        name: str,
        price_amount: str,
        stock_units: int,
        category: str,
        description: Optional[str] = None,
    ) -> "Product":
        normalized_name = (name or "").strip()
        if not normalized_name:
            raise InvalidProductName("Product name is required")

        # Validate value objects
        Money(price_amount)
        Stock(stock_units)

        return Product(
            id=None,
            name=normalized_name,
            price_amount=price_amount,
            stock_units=stock_units,
            category=category,
            description=description,
            is_active=True,
        )

    def with_updates(
        self,
        *,
        name: Optional[str] = None,
        price_amount: Optional[str] = None,
        stock_units: Optional[int] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> "Product":
        new_name = self.name if name is None else name.strip()
        if new_name == "":
            raise InvalidProductName("Product name cannot be empty")

        if price_amount is not None:
            Money(price_amount)
        if stock_units is not None:
            Stock(stock_units)

        return replace(
            self,
            name=new_name,
            price_amount=self.price_amount if price_amount is None else price_amount,
            stock_units=self.stock_units if stock_units is None else stock_units,
            category=self.category if category is None else category,
            description=self.description if description is None else description,
            is_active=self.is_active if is_active is None else is_active,
        )


