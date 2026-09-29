from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.validation import validate_day
from common.constants import HTTP_BAD_REQUEST, HTTP_NOT_FOUND

from modules.timetable.schemas import (
    TimetableCreate,
    TimetableUpdate
)

from modules.timetable.models import Timetable
from modules.timetable.services import get_timetable
from modules.teacher.validation import validate_teacher_exists
from modules.classroom.validation import validate_class_exists


async def validate_timetable(
    teacher_id: int,
    day: str,
    period: int,
    db: AsyncSession
):
    result = await db.execute(
        select(Timetable).where(
            Timetable.teacher_id == teacher_id,
            Timetable.day == day,
            Timetable.period == period
        )
    )

    return result.scalar_one_or_none()





class TimetableCreateValidation:

    def __init__(
        self,
        timetable: TimetableCreate,
        db: AsyncSession
    ):
        self.timetable = timetable
        self.db = db

    async def validate(self):

        validate_day(
            self.timetable.day
        )

        await validate_teacher_exists(
            self.timetable.teacher_id,
            self.db
        )

        await validate_class_exists(
            self.timetable.class_id,
            self.db
        )

        existing_timetable = await validate_timetable(
            self.timetable.teacher_id,
            self.timetable.day,
            self.timetable.period,
            self.db
        )

        if existing_timetable is not None:
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Teacher already has a class at this period"
            )


class TimetableUpdateValidation:

    def __init__(
        self,
        timetable: TimetableUpdate,
        timetable_id: int,
        db: AsyncSession
    ):
        self.timetable = timetable
        self.timetable_id = timetable_id
        self.db = db

    async def validate(self):

        validate_day(
            self.timetable.day
        )

        await validate_teacher_exists(
            self.timetable.teacher_id,
            self.db
        )

        await validate_class_exists(
            self.timetable.class_id,
            self.db
        )

        existing_timetable = await validate_timetable(
            self.timetable.teacher_id,
            self.timetable.day,
            self.timetable.period,
            self.db
        )

        if (
            existing_timetable is not None
            and existing_timetable.id != self.timetable_id
        ):
            raise HTTPException(
                status_code=HTTP_BAD_REQUEST,
                detail="Teacher already has a class at this period"
            )


async def validate_timetable_exists(
    timetable_id: int,
    db: AsyncSession
):
    timetable = await get_timetable(
        timetable_id,
        db
    )

    if timetable is None:
        raise HTTPException(
            status_code=HTTP_NOT_FOUND,
            detail="Timetable entry not found"
        )

    return timetable