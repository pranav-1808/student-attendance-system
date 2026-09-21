from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from modules.teacher.models import Teacher
from modules.teacher.schemas import TeacherCreate, TeacherUpdate

async def create_teacher(
    teacher: TeacherCreate,
    db:AsyncSession
):
    new_teacher = Teacher(
        name=teacher.name,
        email=teacher.email
    )

    db.add(new_teacher)
    await db.commit()
    await db.refresh(new_teacher)

    return new_teacher

async def get_teachers(
    db:AsyncSession
):
    result = await db.execute(
        select(Teacher)
    )

    teachers = result.scalars().all()

    return teachers

async def get_teacher(
    teacher_id: int,
    db:AsyncSession
):
    result = await db.execute(
        select(Teacher).where(Teacher.id == teacher_id)
    )

    teacher= result.scalar_one_or_none()

    return teacher

async def update_teacher(
    teacher: Teacher,
    updated_teacher: TeacherUpdate,
    db:AsyncSession
):
    teacher.name = updated_teacher.name
    teacher.email = updated_teacher.email

    await db.commit()
    await db.refresh(teacher)
    return teacher

async def delete_teacher(
    teacher: Teacher,
    db:AsyncSession
):
    await db.delete(teacher)
    await db.commit()
    return teacher