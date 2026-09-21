from pydantic import BaseModel, ConfigDict


class TimetableCreate(BaseModel):
    teacher_id: int
    subject: str
    day: str
    period: int


class TimetableUpdate(BaseModel):
    teacher_id: int
    subject: str
    day: str
    period: int


class TimetableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    subject: str
    day: str
    period: int