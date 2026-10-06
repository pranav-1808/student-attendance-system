from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.teacher.schemas import (
    TeacherCreate,
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
    await validate_create_teacher(teacher, db)

    return await create_teacher(teacher, db)


@router.get("/", response_model=list[TeacherResponse])
async def get_teachers_route(db: AsyncSession = Depends(get_db)):
    return await get_teachers(db)


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher_route(teacher_id: int, db: AsyncSession = Depends(get_db)):
    return await validate_teacher_exists(teacher_id, db)


@router.put("/{teacher_id}", response_model=TeacherResponse)
async def put_teacher_route(
    teacher_id: int, updated_teacher: TeacherUpdate, db: AsyncSession = Depends(get_db)
):
    teacher = await validate_update_teacher(teacher_id, updated_teacher, db)

    return await update_teacher(teacher, updated_teacher, db)


@router.delete("/{teacher_id}", response_model=TeacherResponse)
async def delete_teacher_route(teacher_id: int, db: AsyncSession = Depends(get_db)):
    teacher = await validate_teacher_exists(teacher_id, db)

    return await delete_teacher(teacher, db)
