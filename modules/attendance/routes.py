from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.attendance.schemas import (
    AttendanceCreate,
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
    await validate_create_attendance(attendance, db)

    return await create_attendance(attendance, db)


@router.get("/", response_model=list[AttendanceResponse])
async def get_attendances_route(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    filters = dict(request.query_params)

    for field in ["student_id", "timetable_id", "class_id"]:
        if field in filters:
            try:
                filters[field] = int(filters[field])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be an integer",
                )

    if "status" in filters:
        if filters["status"].lower() == "true":
            filters["status"] = True
        elif filters["status"].lower() == "false":
            filters["status"] = False
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="status must be true or false",
            )

    if "date" in filters:
        try:
            filters["date"] = date.fromisoformat(filters["date"])
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date must be in YYYY-MM-DD format",
            )

    return await get_attendances(filters, db)


@router.get("/{attendance_id}", response_model=AttendanceResponse)
async def get_attendance_route(attendance_id: int, db: AsyncSession = Depends(get_db)):
    attendance = await validate_attendance_exists(attendance_id, db)

    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance_route(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: AsyncSession = Depends(get_db),
):
    attendance = await validate_update_attendance(attendance_id, updated_attendance, db)

    return await update_attendance(attendance, updated_attendance, db)


@router.delete("/{attendance_id}", response_model=AttendanceResponse)
async def delete_attendance_route(
    attendance_id: int, db: AsyncSession = Depends(get_db)
):
    attendance = await validate_attendance_exists(attendance_id, db)

    return await delete_attendance(attendance, db)
