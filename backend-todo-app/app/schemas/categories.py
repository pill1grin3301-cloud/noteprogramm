from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    class Config:
        from_attributes = True


class CreateOrChangeCategory(BaseModel):
    name: str