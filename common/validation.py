from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.constants import DAYS_OF_WEEK


async def validate_unique_email(
    model, email: str, db: AsyncSession, record_id: int | None = None
):
    result = await db.execute(select(model).where(model.email == email))

    record = result.scalar_one_or_none()

    if record is None:
        return None

    if record_id is not None and record.id == record_id:
        return None

    return record


def validate_day(day: str):
    day = day.capitalize()

    if day not in DAYS_OF_WEEK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid day",
        )

    return day
