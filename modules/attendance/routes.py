from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from modules.attendance.schemas import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)

from modules.attendance.services import (
    create_attendance,
    get_attendances,
    update_attendance,
    delete_attendance
)

from modules.attendance.validation import (
    validate_attendance,
    validate_timetable_class,
    validate_attendance_exists
)

from modules.student.validation import validate_student_exists
from common.constants import HTTP_BAD_REQUEST


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post(
    "/",
    response_model=AttendanceResponse
)
async def create_attendance_route(
    attendance: AttendanceCreate,
    db: AsyncSession = Depends(get_db)
):
    await validate_student_exists(
        attendance.student_id,
        db
    )

    await validate_timetable_class(
        attendance.timetable_id,
        attendance.class_id,
        db
    )

    existing = await validate_attendance(
        attendance.student_id,
        attendance.timetable_id,
        attendance.date,
        db
    )

    if existing is not None:
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Attendance already exists for this class"
        )

    return await create_attendance(
        attendance,
        db
    )


@router.get(
    "/",
    response_model=list[AttendanceResponse]
)
async def get_attendances_route(
    db: AsyncSession = Depends(get_db)
):
    return await get_attendances(db)


@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
async def get_attendance_route(
    attendance_id: int,
    db: AsyncSession = Depends(get_db)
):
    attendance = await validate_attendance_exists(
        attendance_id,
        db
    )

    return attendance


@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
async def update_attendance_route(
    attendance_id: int,
    updated_attendance: AttendanceUpdate,
    db: AsyncSession = Depends(get_db)
):
    attendance = await validate_attendance_exists(
        attendance_id,
        db
    )

    await validate_student_exists(
        updated_attendance.student_id,
        db
    )

    await validate_timetable_class(
        updated_attendance.timetable_id,
        updated_attendance.class_id,
        db
    )

    existing = await validate_attendance(
        updated_attendance.student_id,
        updated_attendance.timetable_id,
        updated_attendance.date,
        db
    )

    if (
        existing is not None
        and existing.id != attendance_id
    ):
        raise HTTPException(
            status_code=HTTP_BAD_REQUEST,
            detail="Attendance already exists for this class"
        )

    return await update_attendance(
        attendance,
        updated_attendance,
        db
    )


@router.delete(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
async def delete_attendance_route(
    attendance_id: int,
    db: AsyncSession = Depends(get_db)
):
    attendance = await validate_attendance_exists(
        attendance_id,
        db
    )

    return await delete_attendance(
        attendance,
        db
    )