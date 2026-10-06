from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.student.models import Student
from modules.student.schemas import StudentCreate, StudentUpdate
from modules.student.services import get_student


async def validate_create_student(
    student: StudentCreate,
    db: AsyncSession,
):
    existing_student = await validate_unique_email(
        Student,
        student.email,
        db,
    )

    if existing_student is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )


async def validate_update_student(
    student: Student,
    updated_student: StudentUpdate,
    db: AsyncSession,
):
    if updated_student.email is None:
        return student

    existing_email = await validate_unique_email(
        Student,
        updated_student.email,
        db,
        student.id,
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered to another student",
        )

    return student


async def validate_student_exists(student_id: int, db: AsyncSession):
    student = await get_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    return student
