from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.teacher.models import Teacher
from modules.teacher.schemas import TeacherCreate, TeacherUpdate


async def create_teacher(teacher: TeacherCreate, db: AsyncSession):
    new_teacher = Teacher(**teacher.model_dump())

    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)

    return new_teacher


async def get_teachers(filters: dict, db: AsyncSession):
    filters = filters.copy()

    page = filters.pop("page", 1)
    page_size = filters.pop("page_size", 10)

    query = select(Teacher)

    for field, value in filters.items():
        if field == "name":
            query = query.where(Teacher.name.ilike(f"%{value}%"))
        elif hasattr(Teacher, field):
            query = query.where(getattr(Teacher, field) == value)

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all()


async def get_teacher(teacher_id: int, db: AsyncSession):
    result = await db.execute(select(Teacher).where(Teacher.id == teacher_id))

    teacher = result.scalar_one_or_none()

    return teacher


async def update_teacher(
    teacher: Teacher, updated_teacher: TeacherUpdate, db: AsyncSession
):
    updated_data = updated_teacher.model_dump(exclude_unset=True)

    for field, value in updated_data.items():
        setattr(teacher, field, value)

    await db.commit()
    await db.refresh(teacher)
    return teacher


async def delete_teacher(teacher: Teacher, db: AsyncSession):
    await db.delete(teacher)
    await db.commit()
    return teacher
