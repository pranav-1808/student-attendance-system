from datetime import date as Date

from pydantic import BaseModel, ConfigDict, Field


class AttendanceCreate(BaseModel):
    student_id: int = Field(gt=0)
    timetable_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    date: Date
    status: bool


class AttendanceUpdate(BaseModel):
    student_id: int = Field(gt=0)
    timetable_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    date: Date
    status: bool


class AttendanceFilters(BaseModel):
    student_id: int | None = Field(default=None, gt=0)
    timetable_id: int | None = Field(default=None, gt=0)
    class_id: int | None = Field(default=None, gt=0)
    status: bool | None = None
    date: Date | None = None
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=100)


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    timetable_id: int
    date: Date
    status: bool
