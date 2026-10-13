from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.student.models import Student
from modules.student.schemas import StudentCreate, StudentUpdate


async def create_student(student: StudentCreate, db: AsyncSession):
    new_student = Student(**student.model_dump())

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)

    return new_student


async def get_students(filters: dict, db: AsyncSession):
    filters = filters.copy()

    page = filters.pop("page", 1)
    page_size = filters.pop("page_size", 10)

    query = select(Student)

    for field, value in filters.items():
        if field == "name":
            query = query.where(Student.name.ilike(f"%{value}%"))
        elif hasattr(Student, field):
            query = query.where(getattr(Student, field) == value)

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all()


async def get_student(student_id: int, db: AsyncSession):
    result = await db.execute(select(Student).where(Student.id == student_id))

    student = result.scalar_one_or_none()

    return student


async def update_student(
    student: Student, updated_student: StudentUpdate, db: AsyncSession
):
    updated_data = updated_student.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return student


async def delete_student(student: Student, db: AsyncSession):

    await db.delete(student)
    await db.commit()

    return student
