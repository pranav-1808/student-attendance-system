from pydantic import BaseModel , EmailStr , ConfigDict


class TeacherCreate(BaseModel):
    name: str
    email : EmailStr

class TeacherUpdate(BaseModel):
    name : str
    email : EmailStr

class TeacherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    name : str
    email : EmailStr

