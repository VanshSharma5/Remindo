from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: conint(gt=0, lt=10)
    scheduled_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    profession: str

class UserResponse(BaseModel):
    id: int
    email: str
    profession: str

    class Config:
        from_attributes = True