from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from modules.student.schemas import StudentCreate, StudentResponse , StudentUpdate
from modules.student.services import create_student , get_students , get_student , update_student ,delete_student
from modules.student.validation import validate_student_email


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse)
async def create_student_route(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_student = await validate_student_email(
        student.email,
        db
    )

    if existing_student is not None:
        raise HTTPException(
            status_code=404,
            detail="Email already registerd"
        )
    return await create_student(student,db)

@router.get("/", response_model=list[StudentResponse])
async def get_students_route(
    db:AsyncSession = Depends(get_db)
):
    return await get_students(db)

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_route(
    student_id:int,
    db:AsyncSession = Depends(get_db)
):
    student = await get_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )

    return student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student_route(
    student_id:int,
    updated_student:StudentUpdate,
    db:AsyncSession = Depends(get_db)
):
    student = await get_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student = await validate_student_email(
        updated_student.email,
        db,
        student_id
    )

    if existing_student is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered to another student"
        )

    return await update_student(
        student,
        updated_student,
        db
    )

@router.delete("/{student_id}", response_model=StudentResponse)
async def delete_student_route(
    student_id: int,
    db:AsyncSession = Depends (get_db)
):
    student = await delete_student(student_id, db)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    return student