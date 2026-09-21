from sqlalchemy.ext.asyncio import AsyncSession

from modules.timetable.models import Timetable


async def validate_timetable(
    teacher_id: int,
    day: str,
    period: int,
    db: AsyncSession
):
    from sqlalchemy import select

    result = await db.execute(
        select(Timetable).where(
            Timetable.teacher_id == teacher_id,
            Timetable.day == day,
            Timetable.period == period
        )
    )

    return result.scalar_one_or_none()