from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StudentCreate(BaseModel):
    """Validate the data required to create a student"""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class StudentResponse(BaseModel):
    """Define the Student data retrieved by API"""

    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr


class StudentUpdate(BaseModel):
    """Validate the data required to update a student"""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class StudentFilters(BaseModel):
    """Define pagination and filtering for student"""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
