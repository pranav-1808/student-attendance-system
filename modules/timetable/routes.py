from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from modules.timetable.schemas import (
    TimetableCreate,
    TimetableUpdate,
    TimetableResponse
)

from modules.timetable.services import (
    create_timetable,
    get_timetables,
    get_timetable,
    update_timetable,
    delete_timetable
)

from modules.timetable.validation import validate_timetable


router = APIRouter(
    prefix="/timetables",
    tags=["Timetable"]
)


@router.post("/", response_model=TimetableResponse)
async def create_timetable_route(
    timetable: TimetableCreate,
    db: AsyncSession = Depends(get_db)
):
    existing = await validate_timetable(
        timetable.teacher_id,
        timetable.day,
        timetable.period,
        db
    )

    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="Teacher already has a class at this period"
        )

    return await create_timetable(
        timetable,
        db
    )


@router.get("/", response_model=list[TimetableResponse])
async def get_timetables_route(
    db: AsyncSession = Depends(get_db)
):
    return await get_timetables(db)


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable_route(
    timetable_id: int,
    db: AsyncSession = Depends(get_db)
):
    timetable = await get_timetable(
        timetable_id,
        db
    )

    if timetable is None:
        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    return timetable


@router.put("/{timetable_id}", response_model=TimetableResponse)
async def update_timetable_route(
    timetable_id: int,
    updated_timetable: TimetableUpdate,
    db: AsyncSession = Depends(get_db)
):
    timetable = await get_timetable(
        timetable_id,
        db
    )

    if timetable is None:
        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    existing = await validate_timetable(
        updated_timetable.teacher_id,
        updated_timetable.day,
        updated_timetable.period,
        db
    )

    if existing is not None and existing.id != timetable_id:
        raise HTTPException(
            status_code=400,
            detail="Teacher already has a class at this period"
        )

    return await update_timetable(
        timetable,
        updated_timetable,
        db
    )


@router.delete("/{timetable_id}", response_model=TimetableResponse)
async def delete_timetable_route(
    timetable_id: int,
    db: AsyncSession = Depends(get_db)
):
    timetable = await get_timetable(
        timetable_id,
        db
    )

    if timetable is None:
        raise HTTPException(
            status_code=404,
            detail="Timetable entry not found"
        )

    return await delete_timetable(
        timetable,
        db
    )