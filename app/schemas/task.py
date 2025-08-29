from pydantic import BaseModel, ConfigDict, Field

class TaskBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    owner_id: int

class TaskRead(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)