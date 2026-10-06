from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.attendance.models import Attendance
from modules.attendance.schemas import AttendanceCreate, AttendanceUpdate
from modules.attendance.services import get_attendance
from modules.student.validation import validate_student_exists
from modules.timetable.validation import validate_timetable_exists


async def validate_timetable_class(timetable_id: int, class_id: int, db: AsyncSession):
    timetable = await validate_timetable_exists(timetable_id, db)

    if timetable.class_id != class_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Timetable does not belong to this class",
        )

    return timetable


async def validate_attendance(
    student_id: int, timetable_id: int, attendance_date: date, db: AsyncSession
):
    result = await db.execute(
        select(Attendance).where(
            Attendance.student_id == student_id,
            Attendance.timetable_id == timetable_id,
            Attendance.date == attendance_date,
        )
    )

    return result.scalar_one_or_none()


async def validate_attendance_exists(attendance_id: int, db: AsyncSession):
    attendance = await get_attendance(attendance_id, db)

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Attendance not found"
        )

    return attendance


async def validate_create_attendance(attendance: AttendanceCreate, db: AsyncSession):
    await validate_student_exists(attendance.student_id, db)

    await validate_timetable_class(attendance.timetable_id, attendance.class_id, db)

    existing = await validate_attendance(
        attendance.student_id, attendance.timetable_id, attendance.date, db
    )

    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already exists for this class",
        )


async def validate_update_attendance(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: AsyncSession,
):
    existing_attendance = await validate_attendance_exists(attendance_id, db)

    await validate_student_exists(updated_attendance.student_id, db)

    await validate_timetable_class(
        updated_attendance.timetable_id,
        updated_attendance.class_id,
        db,
    )

    existing = await validate_attendance(
        updated_attendance.student_id,
        updated_attendance.timetable_id,
        updated_attendance.date,
        db,
    )

    if existing is not None and existing.id != attendance_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already exists for this class",
        )

    return existing_attendance
