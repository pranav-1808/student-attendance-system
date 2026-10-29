from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import PaginationParams, get_pagination_params
from db.session import get_db
from modules.classroom.schemas import (
    ClassCreate,
    ClassQueryFilters,
    ClassResponse,
    ClassUpdate,
)
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
    validate_update_class,
)
from modules.student.schemas import StudentResponse

router = APIRouter(prefix="/classes", tags=["Classroom"])


@router.post("/", response_model=ClassResponse)
async def create_class_route(
    classroom: ClassCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new classroom after validating its name."""
    await validate_class_name(classroom.name, db)
    return await create_class(classroom, db)


@router.get("/", response_model=list[ClassResponse])
async def get_classes_route(
    filters: ClassQueryFilters = Depends(),
    pagination: PaginationParams = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve classrooms matching the supplied filters and pagination."""

    return await get_classes(
        db=db,
        query_filters=filters,
        pagination=pagination,
    )


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class_route(class_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a classroom by its ID after validating its existence."""
    return await validate_class_exists(class_id, db)


@router.put("/{class_id}", response_model=ClassResponse)
async def update_class_route(
    class_id: int, updated_class: ClassUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a classroom after validating the requested changes."""
    classroom = await validate_update_class(class_id, updated_class.name, db)
    return await update_class(classroom, updated_class, db)


@router.delete("/{class_id}", response_model=ClassResponse)
async def delete_class_route(class_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a classroom after validating its existence."""
    classroom = await validate_class_exists(class_id, db)
    return await delete_class(classroom, db)


@router.post("/{class_id}/students/{student_id}")
async def add_student_route(
    class_id: int, student_id: int, db: AsyncSession = Depends(get_db)
):
    """Add a student to a classroom after validating the request."""
    classroom, student = await validate_add_student(class_id, student_id, db)
    return await add_student_to_class(classroom, student, db)


@router.get("/{class_id}/students")
async def get_class_students_route(class_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve all students associated with a classroom."""
    classroom = await validate_class_exists(class_id, db)
    return await get_class_students(classroom, db)


@router.delete("/{class_id}/students/{student_id}", response_model=StudentResponse)
async def remove_student_route(
    class_id: int, student_id: int, db: AsyncSession = Depends(get_db)
):
    """Remove a student from a classroom after validating the request."""
    classroom, student = await validate_remove_student(class_id, student_id, db)
    return await remove_student_from_class(classroom, student, db)
