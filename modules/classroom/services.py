from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.classroom.models import Class, ClassStudents
from modules.classroom.schemas import ClassCreate, ClassUpdate
from modules.student.models import Student


async def create_class(classroom: ClassCreate, db: AsyncSession):
    new_class = Class(name=classroom.name)

    db.add(new_class)

    await db.commit()
    await db.refresh(new_class)

    return new_class


async def get_classes(filters: dict, db: AsyncSession):
    query = select(Class)

    for field, value in filters.items():
        if hasattr(Class, field):
            query = query.where(getattr(Class, field) == value)

    result = await db.execute(query)

    return result.scalars().all()


async def get_class(class_id: int, db: AsyncSession):
    result = await db.execute(select(Class).where(Class.id == class_id))

    return result.scalar_one_or_none()


async def update_class(classroom: Class, updated_class: ClassUpdate, db: AsyncSession):
    classroom.name = updated_class.name

    await db.commit()
    await db.refresh(classroom)

    return classroom


async def delete_class(classroom: Class, db: AsyncSession):
    await db.delete(classroom)
    await db.commit()

    return classroom


async def add_student_to_class(classroom: Class, student: Student, db: AsyncSession):
    new_relationship = ClassStudents(class_id=classroom.id, student_id=student.id)

    db.add(new_relationship)

    await db.commit()

    return classroom


async def get_class_students(classroom: Class, db: AsyncSession):
    result = await db.execute(
        select(Student)
        .join(ClassStudents)
        .where(ClassStudents.class_id == classroom.id)
    )

    return result.scalars().all()


async def remove_student_from_class(
    classroom: Class, student: Student, db: AsyncSession
):
    result = await db.execute(
        select(ClassStudents).where(
            ClassStudents.class_id == classroom.id,
            ClassStudents.student_id == student.id,
        )
    )

    relationship = result.scalar_one_or_none()

    if relationship is not None:
        await db.delete(relationship)
        await db.commit()

    return student
