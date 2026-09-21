from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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