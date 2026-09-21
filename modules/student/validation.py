from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.student.models import Student


async def validate_student_email(
    email: str,
    db: AsyncSession,
    student_id: int | None = None
):
    return await validate_unique_email(
        Student,
        email,
        db,
        student_id
    )