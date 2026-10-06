from fastapi import FastAPI

from common.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def home():
    return {"message": "Student Attendance System"}
