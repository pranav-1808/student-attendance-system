from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.attendance.models import Attendance
from modules.student.models import Student
from modules.timetable.models import Timetable


async def validate_student_exists(
    student_id: int,
    db: AsyncSession
):
    result = await db.execute(
        select(Student).where(
            Student.id == student_id
        )
    )

    return result.scalar_one_or_none()


async def validate_timetable_exists(
    timetable_id: int,
    db: AsyncSession
):
    result = await db.execute(
        select(Timetable).where(
            Timetable.id == timetable_id
        )
    )

    return result.scalar_one_or_none()


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