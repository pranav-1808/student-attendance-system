from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.student.models import Student
from modules.student.schemas import StudentCreate , StudentUpdate


async def create_student(
    student: StudentCreate,
    db: AsyncSession
):
    new_student = Student(
        name=student.name,
        email=student.email
    )

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    return new_student


async def get_students(db:AsyncSession):
    result = await db.execute(
        select(Student)
    )

    students = result.scalars().all()

    return students

async def get_student(
    student_id: int,
    db:AsyncSession
):
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    return student

async def update_student(
    student: Student,
    updated_student: StudentUpdate,
    db: AsyncSession
):
    student.name = updated_student.name
    student.email = updated_student.email

    await db.commit()
    await db.refresh(student)

    return student

async def delete_student(
    student_id: int,
    db:AsyncSession
):
    student = await get_student(student_id, db)

    if student is None:
        return None
    
    await db.delete(student)
    await db.commit()

    return student