from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from modules.classroom.schemas import (
    ClassCreate,
    ClassResponse,
    ClassUpdate
)

from modules.classroom.services import (
    create_class,
    get_classes,
    update_class,
    delete_class,
    add_student_to_class,
    get_class_students,
    remove_student_from_class
)

from modules.classroom.validation import (
    validate_class_name,
    validate_class_exists,
    get_student_class_relationship
)

from common.constants import HTTP_BAD_REQUEST

from modules.student.validation import validate_student_exists
from modules.student.schemas import StudentResponse


router = APIRouter(
    prefix="/classes",
    tags=["Classroom"]
)


@router.post("/", response_model=ClassResponse)
async def create_class_route(
    classroom: ClassCreate,
    db: AsyncSession = Depends(get_db)
):
    await validate_class_name(
        classroom.name,
        db
    )

    return await create_class(
        classroom,
        db
    )


@router.get("/", response_model=list[ClassResponse])
async def get_classes_route(
    db: AsyncSession = Depends(get_db)
):
    return await get_classes(db)


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class_route(
    class_id: int,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )

    return classroom


@router.put("/{class_id}", response_model=ClassResponse)
async def update_class_route(
    class_id: int,
    updated_class: ClassUpdate,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )


    await validate_class_name(
        updated_class.name,
        db,
        class_id
    )

    return await update_class(
        classroom,
        updated_class,
        db
    )


@router.delete("/{class_id}", response_model=ClassResponse)
async def delete_class_route(
    class_id: int,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )

    return await delete_class(
        classroom,
        db
    )


@router.post("/{class_id}/students/{student_id}")
async def add_student_route(
    class_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )

    student = await validate_student_exists(
        student_id,
        db
    )

    relationship = await get_student_class_relationship(
        classroom,
        student,
        db
    )

    if relationship is not None:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Student is already in this class"
        )

    return await add_student_to_class(
        classroom,
        student,
        db
    )


@router.get("/{class_id}/students")
async def get_class_students_route(
    class_id: int,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )

    return await get_class_students(
        classroom,
        db
    )


@router.delete("/{class_id}/students/{student_id}",response_model=StudentResponse)
async def remove_student_route(
    class_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db)
):
    classroom = await validate_class_exists(
        class_id,
        db
    )

    student = await validate_student_exists(
        student_id,
        db
    )

    relationship = await get_student_class_relationship(
        classroom,
        student,
        db
    )

    if relationship is None:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Student is not in this class"
        )

    return await remove_student_from_class(
        classroom,
        student,
        db
    )