from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from common.constants import DAYS_OF_WEEK, HTTP_BAD_REQUEST


async def validate_unique_email(
    model,
    email: str,
    db: AsyncSession,
    record_id: int | None = None
):
    result = await db.execute(
        select(model).where(model.email == email)
    )

    record = result.scalar_one_or_none()

    if record is None:
        return None

    if record_id is not None and record.id == record_id:
        return None

    return record

def validate_day(day: str):
    if day not in DAYS_OF_WEEK:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Invalid day"
        )