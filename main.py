from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.init_db import init_db
from modules.student.routes import router as student_router
from modules.teacher.routes import router as teacher_router
from modules.timetable.routes import router as timetable_router
from modules.attendance.routes import router as attendance_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(timetable_router)
app.include_router(attendance_router)


@app.get("/")
async def home():
    return {"message": "Student Attendance System"}