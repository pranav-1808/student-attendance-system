from pydantic import BaseModel, ConfigDict, Field


class ClassCreate(BaseModel):
    name: str = Field(min_lenght=1, max_length=100)


class ClassUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ClassFliters(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=100)


class ClassResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
