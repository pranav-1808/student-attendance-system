from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.teacher.schemas import(
    TeacherCreate,
    TeacherUpdate,
    TeacherResponse,
)
from modules.teacher.services import(
    create_teacher,
    get_teachers,
    get_teacher,
    update_teacher,
    delete_teacher,
)
from modules.teacher.validation import validate_teacher_email

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

@router.post("/", response_model= TeacherResponse)
async def create_teacher_route(
    teacher: TeacherCreate,
    db:AsyncSession = Depends(get_db)
):
    existing_teacher = await validate_teacher_email(
        teacher.email,
        db
    )

    if existing_teacher is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return await create_teacher(teacher,db)

@router.get("/", response_model= list[TeacherResponse])
async def get_teachers_route(
    db: AsyncSession = Depends(get_db)
):
    return await get_teachers(db)

@router.get("/{teacher_id}",response_model=TeacherResponse)
async def get_teacher_route(
    teacher_id:int,
    db:AsyncSession = Depends(get_db)
):
    teacher = await get_teacher(teacher_id,db)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher

@router.put("/{teacher_id}", response_model=TeacherResponse)
async def put_teacher_route(
    teacher_id: int,
    updated_teacher: TeacherUpdate,
    db: AsyncSession = Depends(get_db)
):
    teacher = await get_teacher(
        teacher_id,
        db
    )

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    existing_teacher = await validate_teacher_email(
        updated_teacher.email,
        db,
        teacher_id
    )

    if existing_teacher is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered to another teacher"
        )

    return await update_teacher(
        teacher,
        updated_teacher,
        db
    )

@router.delete("/{teacher_id}",response_model=TeacherResponse)
async def delete_teacher_route(
    teacher_id:int,
    db:AsyncSession = Depends(get_db)
):
    teacher = await get_teacher(teacher_id,db)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )
    return await delete_teacher(
        teacher,
        db
    )