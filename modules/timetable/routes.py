from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.timetable.schemas import (
    TimetableCreate,
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
    await validate_create_timetable(timetable, db)

    return await create_timetable(timetable, db)


@router.get("/", response_model=list[TimetableResponse])
async def get_timetables_route(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    filters = dict(request.query_params)

    for field in ["teacher_id", "class_id", "period"]:
        if field in filters:
            try:
                filters[field] = int(filters[field])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field} must be an integer",
                )

    return await get_timetables(filters, db)


@router.get("/class/{class_id}", response_model=list[TimetableResponse])
async def get_timetables_by_class_route(
    class_id: int, db: AsyncSession = Depends(get_db)
):
    return await get_timetables_by_class(class_id, db)


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable_route(timetable_id: int, db: AsyncSession = Depends(get_db)):
    return await validate_timetable_exists(timetable_id, db)


@router.put("/{timetable_id}", response_model=TimetableResponse)
async def update_timetable_route(
    timetable_id: int,
    updated_timetable: TimetableUpdate,
    db: AsyncSession = Depends(get_db),
):
    timetable = await validate_update_timetable(timetable_id, updated_timetable, db)

    return await update_timetable(timetable, updated_timetable, db)


@router.delete("/{timetable_id}", response_model=TimetableResponse)
async def delete_timetable_route(timetable_id: int, db: AsyncSession = Depends(get_db)):
    timetable = await validate_timetable_exists(timetable_id, db)

    return await delete_timetable(timetable, db)
