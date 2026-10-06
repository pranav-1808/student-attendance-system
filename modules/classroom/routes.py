from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.classroom.schemas import ClassCreate, ClassResponse, ClassUpdate
from modules.classroom.services import (
    add_student_to_class,
    create_class,
    delete_class,
    get_class_students,
    get_classes,
    remove_student_from_class,
    update_class,
)
from modules.classroom.validation import (
    validate_add_student,
    validate_class_exists,
    validate_class_name,
    validate_remove_student,
)
from modules.student.schemas import StudentResponse

router = APIRouter(prefix="/classes", tags=["Classroom"])


@router.post("/", response_model=ClassResponse)
async def create_class_route(
    classroom: ClassCreate, db: AsyncSession = Depends(get_db)
):
    await validate_class_name(classroom.name, db)

    return await create_class(classroom, db)


@router.get("/", response_model=list[ClassResponse])
async def get_classes_route(request: Request, db: AsyncSession = Depends(get_db)):
    filters = dict(request.query_params)

    return await get_classes(filters, db)


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class_route(class_id: int, db: AsyncSession = Depends(get_db)):
    classroom = await validate_class_exists(class_id, db)

    return classroom


@router.put("/{class_id}", response_model=ClassResponse)
async def update_class_route(
    class_id: int, updated_class: ClassUpdate, db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(class_id, db)

    await validate_class_name(updated_class.name, db, class_id)

    return await update_class(classroom, updated_class, db)


@router.delete("/{class_id}", response_model=ClassResponse)
async def delete_class_route(class_id: int, db: AsyncSession = Depends(get_db)):
    classroom = await validate_class_exists(class_id, db)

    return await delete_class(classroom, db)


@router.post("/{class_id}/students/{student_id}")
async def add_student_route(
    class_id: int, student_id: int, db: AsyncSession = Depends(get_db)
):
    classroom, student = await validate_add_student(class_id, student_id, db)
    return await add_student_to_class(classroom, student, db)


@router.get("/{class_id}/students")
async def get_class_students_route(class_id: int, db: AsyncSession = Depends(get_db)):
    classroom = await validate_class_exists(class_id, db)

    return await get_class_students(classroom, db)


@router.delete("/{class_id}/students/{student_id}", response_model=StudentResponse)
async def remove_student_route(
    class_id: int, student_id: int, db: AsyncSession = Depends(get_db)
):
    classroom, student = await validate_remove_student(class_id, student_id, db)

    return await remove_student_from_class(classroom, student, db)
