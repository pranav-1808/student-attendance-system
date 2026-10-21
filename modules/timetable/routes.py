from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import get_pagination_params
from db.session import get_db
from modules.timetable.schemas import (
    TimetableCreate,
    TimetableFilters,
    TimetableResponse,
    TimetableUpdate,
)
from modules.timetable.services import (
    create_timetable,
    delete_timetable,
    get_timetables,
    get_timetables_by_class,
    update_timetable,
)
from modules.timetable.validation import (
    validate_create_timetable,
    validate_timetable_exists,
    validate_update_timetable,
)

router = APIRouter(prefix="/timetables", tags=["Timetable"])


@router.post("/", response_model=TimetableResponse)
async def create_timetable_route(
    timetable: TimetableCreate, db: AsyncSession = Depends(get_db)
):
    """Create a timetable entry after validating the request."""
    await validate_create_timetable(timetable, db)
    return await create_timetable(timetable, db)


@router.get("/", response_model=list[TimetableResponse])
async def get_timetables_route(
    filters: TimetableFilters = Depends(),
    pagination: tuple[int, int] = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve timetable entries matching filters and pagination."""
    page, page_size = pagination

    timetable_filters = filters.model_dump(exclude_none=True)
    timetable_filters.pop("page", None)
    timetable_filters.pop("page_size", None)

    return await get_timetables(
        filters=timetable_filters,
        db=db,
        page=page,
        page_size=page_size,
    )


@router.get("/class/{class_id}", response_model=list[TimetableResponse])
async def get_timetables_by_class_route(
    class_id: int, db: AsyncSession = Depends(get_db)
):
    """Retrieve timetable entries associated with a specific class."""
    return await get_timetables_by_class(class_id, db)


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable_route(timetable_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a timetable entry by ID after validating its existence."""
    return await validate_timetable_exists(timetable_id, db)


@router.put("/{timetable_id}", response_model=TimetableResponse)
async def update_timetable_route(
    timetable_id: int,
    updated_timetable: TimetableUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update a timetable entry after validating the requested changes."""
    timetable = await validate_update_timetable(timetable_id, updated_timetable, db)
    return await update_timetable(timetable, updated_timetable, db)


@router.delete("/{timetable_id}", response_model=TimetableResponse)
async def delete_timetable_route(timetable_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a timetable entry after validating its existence."""
    timetable = await validate_timetable_exists(timetable_id, db)
    return await delete_timetable(timetable, db)
