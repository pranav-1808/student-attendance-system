from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TeacherCreate(BaseModel):
    """Define the fields required to create a teacher."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class TeacherUpdate(BaseModel):
    """Define the optional fields that can be updated for a teacher."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class TeacherFilters(BaseModel):
    """Define the filters and pagination options for retrieving teachers."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class TeacherResponse(BaseModel):
    """Define the teacher data returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
