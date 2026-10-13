from pydantic import BaseModel, ConfigDict, Field


class TimetableCreate(BaseModel):
    teacher_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    subject: str
    day: str
    period: int = Field(gt=0)


class TimetableUpdate(BaseModel):
    teacher_id: int = Field(gt=0)
    class_id: int = Field(gt=0)
    subject: str
    day: str
    period: int = Field(gt=0)


class TimetableFilters(BaseModel):
    teacher_id: int | None = Field(default=None, gt=0)
    class_id: int | None = Field(default=None, gt=0)
    period: int | None = Field(default=None, gt=0)
    day: str | None = None
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=100)
    subject: str | None = Field(default=None, min_length=1, max_length=100)


class TimetableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    class_id: int
    subject: str
    day: str
    period: int
