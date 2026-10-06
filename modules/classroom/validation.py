from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.classroom.models import Class, ClassStudents
from modules.classroom.services import get_class
from modules.student.models import Student
from modules.student.validation import validate_student_exists


async def validate_class_name(name: str, db: AsyncSession, class_id: int | None = None):
    result = await db.execute(select(Class).where(Class.name == name))

    existing_class = result.scalar_one_or_none()

    if existing_class is None or existing_class.id == class_id:
        return

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Class name already exists"
    )


async def get_student_class_relationship(
    classroom: Class, student: Student, db: AsyncSession
):
    result = await db.execute(
        select(ClassStudents).where(
            ClassStudents.class_id == classroom.id,
            ClassStudents.student_id == student.id,
        )
    )

    return result.scalar_one_or_none()


async def validate_class_exists(class_id: int, db: AsyncSession):
    classroom = await get_class(class_id, db)

    if classroom is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )

    return classroom


async def validate_remove_student(class_id: int, student_id: int, db: AsyncSession):
    classroom = await validate_class_exists(class_id, db)

    student = await validate_student_exists(student_id, db)

    relationship = await get_student_class_relationship(classroom, student, db)

    if relationship is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not in this class",
        )

    return classroom, student


async def validate_add_student(class_id: int, student_id: int, db: AsyncSession):
    classroom = await validate_class_exists(class_id, db)

    student = await validate_student_exists(student_id, db)

    relationship = await get_student_class_relationship(classroom, student, db)

    if relationship is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already in the class",
        )

    return classroom, student
