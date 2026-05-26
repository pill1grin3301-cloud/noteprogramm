# pydantic-settings
# python-dotenv

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings():
    DATABASE_URL: str
    cors_allowed_origins: list[str]
    cors_allow_methods: list[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:admin@note_db:5432/note"),
        cors_allowed_origins = ['http://localhost:3000'],
        cors_allow_methods = ['*']

    )

settings = get_settings()