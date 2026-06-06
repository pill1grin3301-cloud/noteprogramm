from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=42)
    password: str = Field(min_length=3)

class UserResponse(BaseModel):
    id: int
    username: str = Field(max_length=42)
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"