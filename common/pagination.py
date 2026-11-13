"""Shared pagination utilities for list endpoints."""

from dataclasses import dataclass

from fastapi import Query
from sqlalchemy.sql import Select


@dataclass(frozen=True)
class PaginationParams:
    """Store validated pagination parameters."""

    page: int = 1
    page_size: int = 10


def get_pagination_params(
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=10, gt=0, le=100),
) -> PaginationParams:
    """Validate and return pagination parameters."""
    return PaginationParams(page=page, page_size=page_size)


def apply_pagination(
    query: Select,
    pagination: PaginationParams,
) -> Select:
    """Apply pagination to a SQLAlchemy SELECT query."""
    offset = (pagination.page - 1) * pagination.page_size
    return query.offset(offset).limit(pagination.page_size)
