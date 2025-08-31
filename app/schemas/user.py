from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from schemas.task import TaskRead

class UserBase(BaseModel):
    id: int
    email: str

class UserRead(UserBase):
    tasks: Optional[List[TaskRead]] = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6)
