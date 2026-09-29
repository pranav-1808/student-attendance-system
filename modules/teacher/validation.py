from fastapi import HTTPException
from common.constants import HTTP_BAD_REQUEST , HTTP_NOT_FOUND
from modules.teacher.schemas import TeacherCreate, TeacherUpdate


from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.teacher.models import Teacher
from modules.teacher.services import get_teacher


class TeacherCreateValidation:

    def __init__(self,teacher: Teacher, db: AsyncSession):
        self.teacher = teacher
        self.db = db

    async def validate(self):
        existing_teacher = await validate_unique_email(
            Teacher,
            self.teacher.email,
            self.db
        )

        if existing_teacher is not None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Email already registered"
            )

class TeacherUpdateValidation:

    def __init__(self,teacher: TeacherUpdate, teacher_id: int, db: AsyncSession):
        self.teacher = teacher
        self.teacher_id = teacher_id
        self.db = db

    async def validate(self):
        if self.teacher.email is None:
            return 
        existing_teacher = await validate_unique_email(
            Teacher,
            self.teacher.email,
            self.db,
            self.teacher_id
        )

        if existing_teacher is not None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Email already registered to another teacher"
            )

async def validate_teacher_exists(
    teacher_id:int,
    db: AsyncSession
):
    teacher = await get_teacher(
        teacher_id,
        db
    )

    if teacher is None:
        raise HTTPException(
            status_code=HTTP_NOT_FOUND,
            detail="Teacher not found"
        )

    return teacher
