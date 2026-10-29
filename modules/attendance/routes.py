from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import PaginationParams, get_pagination_params
from db.session import get_db
from modules.attendance.schemas import (
    AttendanceCreate,
    AttendanceFilters,
    AttendanceResponse,
    AttendanceUpdate,
)
from modules.attendance.services import (
    create_attendance,
    delete_attendance,
    get_attendances,
    update_attendance,
)
from modules.attendance.validation import (
    validate_attendance_exists,
    validate_create_attendance,
    validate_update_attendance,
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse)
async def create_attendance_route(
    attendance: AttendanceCreate, db: AsyncSession = Depends(get_db)
):
    """Create an attendance record after validating the request."""
    await validate_create_attendance(attendance, db)
    return await create_attendance(attendance, db)


@router.get("/", response_model=list[AttendanceResponse])
async def get_attendances_route(
    filters: AttendanceFilters = Depends(),
    pagination: PaginationParams = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve attendance records matching filters and pagination."""
    attendance_filters = filters.model_dump(exclude_none=True)

    return await get_attendances(
        filters=attendance_filters,
        db=db,
        pagination=pagination,
    )


@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance_route(attendance_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve an attendance record by ID after validating its existence."""
    return await validate_attendance_exists(attendance_id, db)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance_route(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an attendance record after validating the requested changes."""
    attendance = await validate_update_attendance(attendance_id, updated_attendance, db)
    return await update_attendance(attendance, updated_attendance, db)


@router.delete("/{attendance_id}", response_model=AttendanceResponse)
async def delete_attendance_route(
    attendance_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete an attendance record after validating its existence."""
    attendance = await validate_attendance_exists(attendance_id, db)
    return await delete_attendance(attendance, db)
