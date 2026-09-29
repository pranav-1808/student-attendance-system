from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_unique_email
from modules.student.models import Student
from modules.student.schemas import StudentCreate , StudentUpdate
from common.constants import HTTP_NOT_FOUND, HTTP_BAD_REQUEST
from modules.student.services import get_student


class StudentCreateValidation:

    def __init__(self,student: StudentCreate, db: AsyncSession):
        self.student = student
        self.db = db

    async def validate(self):
        existing_student = await validate_unique_email(
            Student,
            self.student.email,
            self.db
        )

        if existing_student is not None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Email already registered"
            )

class StudentUpdateValidation:

    def __init__(self , student: StudentUpdate, student_id: int, db: AsyncSession):
        self.student = student
        self.student_id = student_id
        self.db = db

    async def validate(self):
        if self.student.email is None:
            return

        existing_student = await validate_unique_email(
            Student,
            self.student.email,
            self.db,
            self.student_id
        )

        if existing_student is not None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Email already registed to another student"
            )

async def validate_student_exists(
    student_id : int,
    db : AsyncSession
):
    student = await get_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=HTTP_NOT_FOUND,
            detail="Student not found"
        )

    return student