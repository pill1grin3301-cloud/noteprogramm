from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import UserORM
from app.services.auth import AuthService
from app.services.categories import CategoryService
from app.services.task import TaskService

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)

def get_cat_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserORM:
    auth_service = AuthService(db)
    return auth_service.get_current_user(credentials.credentials)

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)