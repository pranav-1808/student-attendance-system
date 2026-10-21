from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import apply_pagination
from modules.timetable.models import Timetable
from modules.timetable.schemas import TimetableCreate, TimetableUpdate


async def create_timetable(timetable: TimetableCreate, db: AsyncSession):
    """Create a timetable entry and save it to the database."""
    new_timetable = Timetable(
        teacher_id=timetable.teacher_id,
        class_id=timetable.class_id,
        subject=timetable.subject,
        day=timetable.day,
        period=timetable.period,
    )

    db.add(new_timetable)
    await db.commit()
    await db.refresh(new_timetable)
    return new_timetable


async def get_timetables(
    filters: dict,
    db: AsyncSession,
    page: int,
    page_size: int,
):
    """Retrieve timetable entries matching filters and pagination."""
    query = select(Timetable)

    for field, value in filters.items():
        if field == "subject":
            query = query.where(Timetable.subject.ilike(f"%{value}%"))
        elif hasattr(Timetable, field):
            query = query.where(getattr(Timetable, field) == value)

    query = apply_pagination(query, page, page_size)
    result = await db.execute(query)
    return result.scalars().all()


async def get_timetable(timetable_id: int, db: AsyncSession):
    """Retrieve a timetable entry by ID, or return None if not found."""
    result = await db.execute(select(Timetable).where(Timetable.id == timetable_id))
    return result.scalar_one_or_none()


async def update_timetable(
    timetable: Timetable, updated_timetable: TimetableUpdate, db: AsyncSession
):
    """Update a timetable entry and save the changes to the database."""
    timetable.teacher_id = updated_timetable.teacher_id
    timetable.class_id = updated_timetable.class_id
    timetable.subject = updated_timetable.subject
    timetable.day = updated_timetable.day
    timetable.period = updated_timetable.period

    await db.commit()
    await db.refresh(timetable)
    return timetable


async def delete_timetable(timetable: Timetable, db: AsyncSession):
    """Delete a timetable entry and return the deleted object."""
    await db.delete(timetable)
    await db.commit()
    return timetable


async def get_timetables_by_class(class_id: int, db: AsyncSession):
    """Retrieve all timetable entries associated with a specific class."""
    result = await db.execute(select(Timetable).where(Timetable.class_id == class_id))
    return result.scalars().all()
