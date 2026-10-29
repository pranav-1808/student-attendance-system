from fastapi_filters import FilterField, FilterSet
from fastapi_filters.operators import FilterOperator
from pydantic import BaseModel, ConfigDict, Field


class ClassCreate(BaseModel):
    """Validate the data required to create a class"""

    name: str = Field(min_length=1, max_length=100)


class ClassUpdate(BaseModel):
    """Validate the data required to update a class"""

    name: str = Field(min_length=1, max_length=100)


class ClassQueryFilters(FilterSet):
    """Define supported filters for querying classes."""

    id: FilterField[int]
    name: FilterField[str] = FilterField(
        operators=[
            FilterOperator.eq,
            FilterOperator.ne,
            FilterOperator.like,
            FilterOperator.ilike,
        ],
        default_op=FilterOperator.ilike,
    )


class ClassResponse(BaseModel):
    """Define the class data retrieved by the API"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
