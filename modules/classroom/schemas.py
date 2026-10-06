from pydantic import BaseModel


class ClassCreate(BaseModel):
    name: str


class ClassUpdate(BaseModel):
    name: str


class ClassResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
