from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import apply_pagination, PaginationParams
from modules.student.models import Student
from modules.student.schemas import StudentCreate, StudentUpdate


async def create_student(student: StudentCreate, db: AsyncSession):
    """Create a student and save the record to the database."""
    new_student = Student(**student.model_dump())

    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student


async def get_students(
    filters: dict,
    db: AsyncSession,
    pagination: PaginationParams,
):
    """Retrieve students matching the supplied filters and pagination."""
    query = select(Student)

    for field, value in filters.items():
        if field == "name":
            query = query.where(Student.name.ilike(f"%{value}%"))
        elif hasattr(Student, field):
            query = query.where(getattr(Student, field) == value)

    query = apply_pagination(query, pagination)
    result = await db.execute(query)
    return result.scalars().all()


async def get_student(student_id: int, db: AsyncSession):
    """Retrieve a student by ID, or return None if not found."""
    result = await db.execute(select(Student).where(Student.id == student_id))
    return result.scalar_one_or_none()


async def update_student(
    student: Student, updated_student: StudentUpdate, db: AsyncSession
):
    """Update a student's fields and save the changes to the database."""
    updated_data = updated_student.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)
    return student


async def delete_student(student: Student, db: AsyncSession):
    """Delete a student from the database and return the deleted object."""
    await db.delete(student)
    await db.commit()
    return student
