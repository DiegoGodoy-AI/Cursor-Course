"""Domain-specific error types for the products bounded context."""


class DomainError(Exception):
    """Base error for domain rule violations."""


class InvalidProductName(DomainError):
    pass


class InvalidPrice(DomainError):
    pass


class InvalidStock(DomainError):
    pass





