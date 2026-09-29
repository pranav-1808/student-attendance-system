from contextlib import asynccontextmanager

from fastapi import FastAPI

from common.routes import router

from db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Student Attendance System"}