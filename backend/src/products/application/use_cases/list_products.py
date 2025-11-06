"""List products use case."""

from ..dto import ListProductsFilters, Page
from ..ports import UnitOfWork


def list_products(uow: UnitOfWork, *, filters: ListProductsFilters, limit: int, offset: int) -> Page:
    filter_dict = {
        "category": filters.category,
        "min_price": filters.min_price,
        "max_price": filters.max_price,
        "search": filters.search,
    }
    items, total = uow.products.list(filters=filter_dict, limit=limit, offset=offset)
    return Page(items=items, total=total, limit=limit, offset=offset)





