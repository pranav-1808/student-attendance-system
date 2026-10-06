from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.student.schemas import StudentCreate, StudentResponse, StudentUpdate
from modules.student.services import (
    create_student,
    delete_student,
    get_students,
    update_student,
)
from modules.student.validation import (
    validate_create_student,
    validate_student_exists,
    validate_update_student,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse)
async def create_student_route(
    student: StudentCreate, db: AsyncSession = Depends(get_db)
):
    await validate_create_student(student, db)

    return await create_student(student, db)


@router.get("/", response_model=list[StudentResponse])
async def get_students_route(db: AsyncSession = Depends(get_db)):
    return await get_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_route(student_id: int, db: AsyncSession = Depends(get_db)):
    return await validate_student_exists(student_id, db)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_route(
    student_id: int, updated_student: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    student = await validate_student_exists(student_id, db)

    await validate_update_student(student, updated_student, db)

    return await update_student(student, updated_student, db)


@router.delete("/{student_id}", response_model=StudentResponse)
async def delete_student_route(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await validate_student_exists(student_id, db)

    return await delete_student(student, db)
