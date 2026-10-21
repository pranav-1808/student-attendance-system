from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import get_pagination_params
from db.session import get_db
from modules.teacher.schemas import (
    TeacherCreate,
    TeacherFilters,
    TeacherResponse,
    TeacherUpdate,
)
from modules.teacher.services import (
    create_teacher,
    delete_teacher,
    get_teachers,
    update_teacher,
)
from modules.teacher.validation import (
    validate_create_teacher,
    validate_teacher_exists,
    validate_update_teacher,
)

router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/", response_model=TeacherResponse)
async def create_teacher_route(
    teacher: TeacherCreate, db: AsyncSession = Depends(get_db)
):
    """Create a teacher after validating the request."""
    await validate_create_teacher(teacher, db)
    return await create_teacher(teacher, db)


@router.get("/", response_model=list[TeacherResponse])
async def get_teachers_route(
    filters: TeacherFilters = Depends(),
    pagination: tuple[int, int] = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve teachers matching the supplied filters and pagination."""
    page, page_size = pagination

    teacher_filters = filters.model_dump(exclude_none=True)
    teacher_filters.pop("page", None)
    teacher_filters.pop("page_size", None)

    return await get_teachers(
        filters=teacher_filters,
        db=db,
        page=page,
        page_size=page_size,
    )


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_route(teacher_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a teacher by ID after validating their existence."""
    return await validate_teacher_exists(teacher_id, db)


@router.put("/{teacher_id}", response_model=TeacherResponse)
async def put_teacher_route(
    teacher_id: int, updated_teacher: TeacherUpdate, db: AsyncSession = Depends(get_db)
):
    """Update a teacher after validating the requested changes."""
    teacher = await validate_update_teacher(teacher_id, updated_teacher, db)
    return await update_teacher(teacher, updated_teacher, db)


@router.delete("/{teacher_id}", response_model=TeacherResponse)
async def delete_teacher_route(teacher_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a teacher after validating their existence."""
    teacher = await validate_teacher_exists(teacher_id, db)
    return await delete_teacher(teacher, db)
