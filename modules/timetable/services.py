from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.timetable.models import Timetable
from modules.timetable.schemas import (
    TimetableCreate,
    TimetableUpdate
)


async def create_timetable(
    timetable: TimetableCreate,
    db: AsyncSession
):
    new_timetable = Timetable(
        teacher_id=timetable.teacher_id,
        subject=timetable.subject,
        day=timetable.day,
        period=timetable.period
    )

    db.add(new_timetable)
    await db.commit()
    await db.refresh(new_timetable)

    return new_timetable


async def get_timetables(
    db: AsyncSession
):
    result = await db.execute(
        select(Timetable)
    )

    return result.scalars().all()


async def get_timetable(
    timetable_id: int,
    db: AsyncSession
):
    result = await db.execute(
        select(Timetable).where(
            Timetable.id == timetable_id
        )
    )

    return result.scalar_one_or_none()


async def update_timetable(
    timetable: Timetable,
    updated_timetable: TimetableUpdate,
    db: AsyncSession
):
    timetable.teacher_id = updated_timetable.teacher_id
    timetable.subject = updated_timetable.subject
    timetable.day = updated_timetable.day
    timetable.period = updated_timetable.period

    await db.commit()
    await db.refresh(timetable)

    return timetable


async def delete_timetable(
    timetable: Timetable,
    db: AsyncSession
):
    await db.delete(timetable)
    await db.commit()

    return timetable