from fastapi import APIRouter, Depends
from fastapi import status

from app.api.dependencies import get_auth_service, get_cat_service, get_current_user, get_task_service
from app.models import UserORM
from app.schemas.categories import Category, CreateOrChangeCategory
from app.schemas.tasks import TaskCreate, TaskSchema, TaskUpdate
from app.schemas.users import Token, UserCreate
from app.services.auth import AuthService
from app.services.categories import CategoryService
from app.services.task import TaskService


task_router = APIRouter(prefix='/tasks', tags=['tasks'])


@task_router.get('')
async def read_all_tasks(
    task_service: TaskService = Depends(get_task_service),
    current_user: UserORM = Depends(get_current_user)
) -> list[TaskSchema]:
    return task_service.list_tasks(current_user)


@task_router.post('', status_code=status.HTTP_201_CREATED)
async def createe_task(
    payload: TaskCreate, 
    task_service: TaskService = Depends(get_task_service),
    current_user: UserORM = Depends(get_current_user)
) -> TaskSchema:
    return task_service.create_task(task_create=payload, current_user=current_user)


@task_router.patch('')
async def update_task(
    title: str, 
    payload: TaskUpdate, 
    task_service: TaskService = Depends(get_task_service),
    current_user: UserORM = Depends(get_current_user)
) -> TaskSchema:
    return task_service.update_task(task_old_title=title, task_update=payload, current_user=current_user)


@task_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def del_task(
    title: str, 
    task_service: TaskService = Depends(get_task_service),
    current_user: UserORM = Depends(get_current_user)
) -> None:
    return task_service.delete_task(task_title=title, current_user=current_user)




category_router = APIRouter(prefix='/categories', tags=['categories'])

@category_router.get('')
async def read_all_categories(
    cat_service: CategoryService = Depends(get_cat_service), 
    current_user: UserORM = Depends(get_current_user)
) -> list[Category]:
    return cat_service.list_categories(current_user=current_user)


@category_router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_category(
    payload: CreateOrChangeCategory, 
    cat_service: CategoryService = Depends(get_cat_service),
    current_user: UserORM = Depends(get_current_user)
) -> Category:
    return cat_service.create_category(payload, current_user=current_user)


@category_router.patch('')
async def update_cate(
    category_name: str, 
    payload: CreateOrChangeCategory, 
    cat_service: CategoryService = Depends(get_cat_service),
    current_user: UserORM = Depends(get_current_user)
) -> Category:
    return cat_service.update_category(cat_name=category_name, cat_update=payload, current_user=current_user)


@category_router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def del_category(
    category_name: str, 
    cat_service: CategoryService = Depends(get_cat_service),
    current_user: UserORM = Depends(get_current_user)
) -> None:
    return cat_service.delete_category(cat_name=category_name, current_user=current_user)



auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=Token)
def register(data: UserCreate, auth = Depends(get_auth_service)):
    user = auth.register(data)
    token = auth.login(data.username, data.password)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.post("/login", response_model=Token)
def login(username: str, password: str, auth = Depends(get_auth_service)):
    token = auth.login(username, password)
    return {"access_token": token, "token_type": "bearer"}

@auth_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete(current_user: UserORM = Depends(get_current_user), auth = Depends(get_auth_service)):
    auth.delete_user(current_user.id)