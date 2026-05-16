from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine

from app.api.routers.routers import task_router, category_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    print('app start')
    yield
    print('app finished')


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)

from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=settings.cors_allow_methods,
)