from pydantic import BaseModel, ConfigDict, EmailStr


class TeacherCreate(BaseModel):
    name: str
    email: EmailStr


class TeacherUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
