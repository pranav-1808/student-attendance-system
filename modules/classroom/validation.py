from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.constants import HTTP_BAD_REQUEST, HTTP_NOT_FOUND
from modules.classroom.models import Class, ClassStudents
from modules.student.models import Student
from modules.classroom.services import get_class

async def validate_class_name(
    name:str,
    db: AsyncSession,
    class_id: int | None = None
):
    result = await db.execute(
        select(Class).where(
            Class.name == name
        )
    )

    existing_class = result.scalar_one_or_none()

    if existing_class is None or existing_class.id == class_id:
        return

    raise HTTPException(
        status_code=HTTP_BAD_REQUEST,
        detail="Class name already exists"
    )

async def get_student_class_relationship(
    classroom: Class,
    student: Student,
    db: AsyncSession
):
    result = await db.execute(
        select(ClassStudents).where(
            ClassStudents.class_id == classroom.id,
            ClassStudents.student_id == student.id
        )
    )

    return result.scalar_one_or_none()

async def validate_class_exists(
    class_id: int,
    db: AsyncSession
):
    classroom = await get_class(
        class_id,
        db
    )

    if classroom is None:
        raise HTTPException(
            status_code=HTTP_NOT_FOUND,
            detail="Class not found"
        )

    return classroom