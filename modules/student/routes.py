from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import PaginationParams, get_pagination_params
from db.session import get_db
from modules.student.schemas import (
    StudentCreate,
    StudentFilters,
    StudentResponse,
    StudentUpdate,
)
from modules.student.services import (
    create_student,
    delete_student,
    get_students,
    update_student,
)
from modules.student.validation import (
    validate_create_student,
    validate_student_exists,
    validate_student_update_request,
)

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse)
async def create_student_route(
    student: StudentCreate, db: AsyncSession = Depends(get_db)
):
    """Create a student after validating the request."""
    await validate_create_student(student, db)
    return await create_student(student, db)


@router.get("/", response_model=list[StudentResponse])
async def get_students_route(
    filters: StudentFilters = Depends(),
    pagination: PaginationParams = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve students matching the supplied filters and pagination."""
    student_filters = filters.model_dump(exclude_none=True)

    return await get_students(
        filters=student_filters,
        db=db,
        pagination=pagination,
    )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_route(student_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a student by ID after validating their existence."""
    return await validate_student_exists(student_id, db)


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_route(
    student_id: int, updated_student: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a student after validating the requested changes."""
    student = await validate_student_update_request(student_id, updated_student, db)
    return await update_student(student, updated_student, db)


@router.delete("/{student_id}", response_model=StudentResponse)
async def delete_student_route(student_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a student after validating their existence."""
    student = await validate_student_exists(student_id, db)
    return await delete_student(student, db)
