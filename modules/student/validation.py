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
    """Validate that a new student's email is not already registered."""
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
    """Validate email uniqueness when updating an existing student."""
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
    """Retrieve a student by ID or raise a 404 error if not found."""
    student = await get_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )

    return student


async def validate_student_update_request(
    student_id: int,
    updated_student: StudentUpdate,
    db: AsyncSession,
):
    """Validate a student update request and return the existing student."""
    student = await validate_student_exists(student_id, db)
    await validate_update_student(student, updated_student, db)
    return student
