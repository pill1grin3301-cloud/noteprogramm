from pydantic import BaseModel, ConfigDict


class Category(BaseModel):
    id: str
    name: str
    model_config = ConfigDict(from_attributes=True)


class CreateOrChangeCategory(BaseModel):
    name: str