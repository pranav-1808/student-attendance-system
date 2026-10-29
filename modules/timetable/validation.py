from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_day
from modules.classroom.validation import validate_class_exists
from modules.teacher.validation import validate_teacher_exists
from modules.timetable.models import Timetable
from modules.timetable.schemas import TimetableCreate, TimetableUpdate
from modules.timetable.services import get_timetable


async def validate_timetable(teacher_id: int, day: str, period: int, db: AsyncSession):
    """Check whether a teacher already has a timetable entry for a given period."""
    result = await db.execute(
        select(Timetable).where(
            Timetable.teacher_id == teacher_id,
            Timetable.day == day,
            Timetable.period == period,
        )
    )

    return result.scalar_one_or_none()


async def validate_create_timetable(timetable: TimetableCreate, db: AsyncSession):
    """Validate a new timetable entry and prevent teacher scheduling conflicts."""
    timetable.day = validate_day(timetable.day)

    await validate_teacher_exists(timetable.teacher_id, db)

    await validate_class_exists(timetable.class_id, db)

    existing_timetable = await validate_timetable(
        timetable.teacher_id,
        timetable.day,
        timetable.period,
        db,
    )

    if existing_timetable is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher already has a class at this period",
        )


async def validate_update_timetable(
    timetable_id: int,
    timetable: TimetableUpdate,
    db: AsyncSession,
):
    """Validate timetable updates and prevent scheduling conflicts."""
    existing_timetable = await validate_timetable_exists(timetable_id, db)

    timetable.day = validate_day(timetable.day)

    await validate_teacher_exists(timetable.teacher_id, db)

    await validate_class_exists(timetable.class_id, db)

    conflicting_timetable = await validate_timetable(
        timetable.teacher_id,
        timetable.day,
        timetable.period,
        db,
    )

    if conflicting_timetable is not None and conflicting_timetable.id != timetable_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Teacher already has a class at this period",
        )

    return existing_timetable


async def validate_timetable_exists(timetable_id: int, db: AsyncSession):
    """Retrieve a timetable entry by ID or raise a 404 error if not found."""
    timetable = await get_timetable(timetable_id, db)

    if timetable is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found"
        )

    return timetable
