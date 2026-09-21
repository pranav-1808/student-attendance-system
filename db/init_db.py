from db.base import Base
from db.session import engine

from modules.student.models import Student
from modules.teacher.models import Teacher
from modules.attendance.models import Attendance
from modules.timetable.models import Timetable


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)