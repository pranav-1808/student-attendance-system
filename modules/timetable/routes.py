from fastapi import APIRouter, Depends
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
    update_timetable,
    delete_timetable,
    get_timetables_by_class
)

from modules.timetable.validation import TimetableCreateValidation , validate_timetable_exists, TimetableUpdateValidation


router = APIRouter(
    prefix="/timetables",
    tags=["Timetable"]
)


@router.post("/", response_model=TimetableResponse)
async def create_timetable_route(
    timetable: TimetableCreate,
    db: AsyncSession = Depends(get_db)
):
    await TimetableCreateValidation(
        timetable,
        db
    ).validate()

    return await create_timetable(
        timetable,
        db
    )


@router.get("/", response_model=list[TimetableResponse])
async def get_timetables_route(
    db: AsyncSession = Depends(get_db)
):
    return await get_timetables(db)

@router.get(
    "/class/{class_id}",
    response_model=list[TimetableResponse]
)
async def get_timetables_by_class_route(
    class_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_timetables_by_class(
        class_id,
        db
    )


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable_route(
    timetable_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await validate_timetable_exists(
        timetable_id,
        db
    )


@router.put("/{timetable_id}", response_model=TimetableResponse)
async def update_timetable_route(
    timetable_id: int,
    updated_timetable: TimetableUpdate,
    db: AsyncSession = Depends(get_db)
):
    timetable = await validate_timetable_exists(
        timetable_id,
        db
    )

    await TimetableUpdateValidation(
        updated_timetable,
        timetable_id,
        db
    ).validate()

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
    timetable = await validate_timetable_exists(
        timetable_id,
        db
    )

    return await delete_timetable(
        timetable,
        db
    )
