from datetime import date

from pydantic import BaseModel, ConfigDict


class AttendanceCreate(BaseModel):
    student_id: int
    timetable_id: int
    date: date
    status: bool


class AttendanceUpdate(BaseModel):
    student_id: int
    timetable_id: int
    date: date
    status: bool


class AttendanceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    timetable_id: int
    date: date
    status: bool