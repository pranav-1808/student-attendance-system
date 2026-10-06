from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.teacher.models import Teacher
from modules.teacher.schemas import TeacherCreate, TeacherUpdate
from modules.teacher.services import get_teacher


async def validate_create_teacher(
    teacher: TeacherCreate,
    db: AsyncSession,
):
    existing_teacher = await validate_unique_email(
        Teacher,
        teacher.email,
        db,
    )

    if existing_teacher is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )


async def validate_update_teacher(
    teacher_id: int,
    teacher: TeacherUpdate,
    db: AsyncSession,
):
    existing_teacher = await validate_teacher_exists(teacher_id, db)

    if teacher.email is None:
        return existing_teacher

    existing_email = await validate_unique_email(
        Teacher,
        teacher.email,
        db,
        teacher_id,
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered to another teacher",
        )

    return existing_teacher


async def validate_teacher_exists(teacher_id: int, db: AsyncSession):
    teacher = await get_teacher(teacher_id, db)

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
        )

    return teacher
