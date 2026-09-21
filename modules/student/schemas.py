from pydantic import BaseModel, ConfigDict ,EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr

class StudentUpdate(BaseModel):
    name : str
    email : EmailStr