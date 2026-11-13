from fastapi_filters import FilterSet
from fastapi_filters.ext.sqlalchemy import apply_filters
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.pagination import PaginationParams, apply_pagination
from modules.classroom.models import Class, class_students
from modules.classroom.schemas import ClassCreate, ClassUpdate
from modules.student.models import Student


async def create_class(classroom: ClassCreate, db: AsyncSession):
    """Create a new class and save it to the database"""
    new_class = Class(name=classroom.name)
    db.add(new_class)
    await db.commit()
    await db.refresh(new_class)
    return new_class


async def get_classes(
    db: AsyncSession,
    query_filters: FilterSet,
    pagination: PaginationParams,
):
    """Retrieve classrooms matching filters and pagination."""
    query = select(Class)
    query = apply_filters(query, query_filters.filter_values)
    query = query.order_by(Class.id)
    query = apply_pagination(query, pagination)
    result = await db.execute(query)
    return result.scalars().all()


async def get_class(class_id: int, db: AsyncSession):
    """Retrieve a class by its ID, Return None if does not exists"""
    result = await db.execute(select(Class).where(Class.id == class_id))
    return result.scalar_one_or_none()


async def update_class(classroom: Class, updated_class: ClassUpdate, db: AsyncSession):
    """Update the class name and save it to the databasse"""
    classroom.name = updated_class.name

    await db.commit()
    await db.refresh(classroom)
    return classroom


async def delete_class(classroom: Class, db: AsyncSession):
    """Delete the class from databsase and return the deleted object"""
    await db.delete(classroom)
    await db.commit()
    return classroom


async def add_student_to_class(classroom: Class, student: Student, db: AsyncSession):
    """Associate a student with a class in the database."""
    await db.execute(
        class_students.insert().values(
            class_id=classroom.id,
            student_id=student.id,
        )
    )
    await db.commit()
    return classroom


async def get_class_students(classroom: Class, db: AsyncSession):
    """Retrieve all students associated with the specified class."""
    result = await db.execute(
        select(Student)
        .join(class_students)
        .where(class_students.c.class_id == classroom.id)
    )

    return result.scalars().all()


async def remove_student_from_class(
    classroom: Class, student: Student, db: AsyncSession
):
    """Remove a student from the associated class."""
    await db.execute(
        class_students.delete().where(
            class_students.c.class_id == classroom.id,
            class_students.c.student_id == student.id,
        )
    )

    await db.commit()
    return student
