from pydantic import BaseModel

class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None