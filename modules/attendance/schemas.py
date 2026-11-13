from datetime import date as Date

from fastapi_filters import FilterField, FilterSet
from fastapi_filters.operators import FilterOperator
from pydantic import BaseModel, ConfigDict, Field, model_validator


class AttendanceCreate(BaseModel):
    """Define the fields required to create an attendance record."""

    student_id: int = Field(gt=0)
    timetable_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    date: Date
    status: bool


class AttendanceUpdate(BaseModel):
    """Define the fields that can be updated on an attendance record."""

    student_id: int | None = Field(default=None, gt=0)
    timetable_id: int | None = Field(default=None, gt=0)
    date: Date | None = None
    status: bool | None = None

    @model_validator(mode="after")
    def reject_null_values(self):
        """Reject explicit null values while allowing omitted fields."""
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class AttendanceFilters(FilterSet):
    """Define supported filters for querying attendance records."""

    student_id: FilterField[int] = FilterField(
        operators=[
            FilterOperator.eq,
            FilterOperator.ne,
            FilterOperator.in_,
        ],
        default_op=FilterOperator.eq,
    )

    timetable_id: FilterField[int] = FilterField(
        operators=[
            FilterOperator.eq,
            FilterOperator.ne,
            FilterOperator.in_,
        ],
        default_op=FilterOperator.eq,
    )

    class_id: FilterField[int] = FilterField(
        operators=[
            FilterOperator.eq,
            FilterOperator.ne,
            FilterOperator.in_,
        ],
        default_op=FilterOperator.eq,
    )

    status: FilterField[bool] = FilterField(
        operators=[FilterOperator.eq],
        default_op=FilterOperator.eq,
    )

    date: FilterField[Date] = FilterField(
        operators=[
            FilterOperator.eq,
            FilterOperator.gt,
            FilterOperator.ge,
            FilterOperator.lt,
            FilterOperator.le,
        ],
        default_op=FilterOperator.eq,
    )


class AttendanceResponse(BaseModel):
    """Define the attendance data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    timetable_id: int
    date: Date
    status: bool
