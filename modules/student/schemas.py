from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class StudentFilters(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    page: int = Field(default=1, gt=0)
    page_size: int = Field(default=10, gt=0, le=100)
