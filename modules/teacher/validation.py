from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.teacher.models import Teacher


async def validate_teacher_email(
    email: str,
    db: AsyncSession,
    teacher_id: int | None = None
):
    return await validate_unique_email(
        Teacher,
        email,
        db,
        teacher_id
    )