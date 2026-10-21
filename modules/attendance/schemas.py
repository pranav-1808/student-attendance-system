from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field


class AttendanceCreate(BaseModel):
    """Define the fields required to create an attendance record."""

    student_id: int = Field(gt=0)
    timetable_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    date: Date
    status: bool


class AttendanceUpdate(BaseModel):
    """Define the fields used to update an existing attendance record."""

    student_id: int = Field(gt=0)
    timetable_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    date: Date
    status: bool


class AttendanceFilters(BaseModel):
    """Define filtering and pagination options for attendance queries."""

    student_id: int | None = Field(default=None, gt=0)
    timetable_id: int | None = Field(default=None, gt=0)
    class_id: int | None = Field(default=None, gt=0)
    status: bool | None = None
    date: Date | None = None
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=100)


class AttendanceResponse(BaseModel):
    """Define the attendance data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    timetable_id: int
    date: Date
    status: bool
