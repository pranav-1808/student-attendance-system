from fastapi import APIRouter

from modules.attendance.routes import router as attendance_router
from modules.classroom.routes import router as classroom_router
from modules.student.routes import router as student_router
from modules.teacher.routes import router as teacher_router
from modules.timetable.routes import router as timetable_router

router = APIRouter()

router.include_router(student_router)
router.include_router(teacher_router)
router.include_router(timetable_router)
router.include_router(attendance_router)
router.include_router(classroom_router)
