from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.constants import HTTP_BAD_REQUEST, HTTP_NOT_FOUND

from modules.attendance.models import Attendance
from modules.timetable.validation import validate_timetable_exists
from modules.attendance.services import get_attendance




async def validate_timetable_class(
    timetable_id: int,
    class_id: int,
    db: AsyncSession
):
    timetable = await validate_timetable_exists(
        timetable_id,
        db
    )

    if timetable.class_id != class_id:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Timetable does not belong to this class"
        )

    return timetable


async def validate_attendance(
    student_id: int,
    timetable_id: int,
    attendance_date: date,
    db: AsyncSession
):
    result = await db.execute(
        select(Attendance).where(
            Attendance.student_id == student_id,
            Attendance.timetable_id == timetable_id,
            Attendance.date == attendance_date
        )
    )

    return result.scalar_one_or_none()

async def validate_attendance_exists(
    attendance_id: int,
    db: AsyncSession
):
    attendance = await get_attendance(
        attendance_id,
        db
    )

    if attendance is None:
        raise HTTPException(
            status_code=HTTP_NOT_FOUND,
            detail="Attendance not found"
        )

    return attendance