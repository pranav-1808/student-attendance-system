from fastapi import Query
from sqlalchemy.sql import Select


def get_pagination_params(
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
) -> tuple[int, int]:
    return page, page_size


def apply_pagination(
    query: Select,
    page: int,
    page_size: int,
) -> Select:
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size)


def extract_pagination(filters: dict) -> tuple[dict, int, int]:
    """Extract pagination values and return the remaining filters"""
    filters = filters.copy()
    page = filters.pop("page", 1)
    page_size = filters.pop("page_size", 10)
    return filters, page, page_size
