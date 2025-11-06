"""Value objects for the product domain (money, stock, identifiers)."""

from decimal import Decimal, InvalidOperation


class Money:
    """Represents a monetary amount with two decimal places precision."""

    def __init__(self, amount: str):
        try:
            value = Decimal(amount)
        except (InvalidOperation, TypeError):
            raise ValueError("Invalid money amount")

        quantized = value.quantize(Decimal("0.01"))
        if quantized < Decimal("0.00"):
            raise ValueError("Money amount cannot be negative")
        self._value = quantized

    @property
    def value(self) -> Decimal:
        return self._value

    def __str__(self) -> str:
        return f"{self._value:.2f}"


class Stock:
    """Represents stock units; ensures non-negative integers."""

    def __init__(self, units: int):
        if not isinstance(units, int) or units < 0:
            raise ValueError("Stock units must be a non-negative integer")
        self._units = units

    @property
    def units(self) -> int:
        return self._units





