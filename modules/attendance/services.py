from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import PaginationParams, apply_pagination
from modules.attendance.models import Attendance
from modules.attendance.schemas import AttendanceCreate, AttendanceUpdate


async def create_attendance(attendance: AttendanceCreate, db: AsyncSession):
    """Create an attendance record and save it to the database."""
    new_attendance = Attendance(
        student_id=attendance.student_id,
        timetable_id=attendance.timetable_id,
        date=attendance.date,
        status=attendance.status,
    )

    db.add(new_attendance)

    await db.commit()
    await db.refresh(new_attendance)

    return new_attendance


async def get_attendances(
    filters: dict,
    db: AsyncSession,
    pagination: PaginationParams,
):
    """Retrieve attendance records matching filters and pagination."""
    query = select(Attendance)

    for field, value in filters.items():
        if hasattr(Attendance, field):
            query = query.where(getattr(Attendance, field) == value)

    query = apply_pagination(query, pagination)

    result = await db.execute(query)
    return result.scalars().all()


async def get_attendance(attendance_id: int, db: AsyncSession):
    """Retrieve an attendance record by ID, or return None if not found."""
    result = await db.execute(select(Attendance).where(Attendance.id == attendance_id))

    return result.scalar_one_or_none()


async def update_attendance(
    attendance: Attendance,
    updated_attendance: AttendanceUpdate,
    db: AsyncSession,
):
    """Update only the supplied attendance fields and save changes."""
    update_data = updated_attendance.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(attendance, field, value)

    await db.commit()
    await db.refresh(attendance)

    return attendance


async def delete_attendance(attendance: Attendance, db: AsyncSession):
    """Delete an attendance record and return the deleted object."""
    await db.delete(attendance)

    await db.commit()

    return attendance
