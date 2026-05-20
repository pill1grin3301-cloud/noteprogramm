from fastapi import APIRouter, Depends
from fastapi import status

from app.api.dependencies import get_cat_service, get_task_service
from app.schemas.categories import Category, CreateOrChangeCategory
from app.schemas.tasks import TaskCreate, TaskSchema, TaskUpdate
from app.services.categories import CategoryService
from app.services.task import TaskService


task_router = APIRouter(prefix='/tasks')


@task_router.get('')
async def read_all_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()


@task_router.post('', status_code=status.HTTP_201_CREATED)
async def createe_task(payload: TaskCreate, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@task_router.patch('/{task_id}')
async def update_task(task_id: str, payload: TaskUpdate, task_service: TaskService = Depends(get_task_service)) -> TaskSchema:
    return task_service.update_task(task_id=task_id, task_update=payload)


@task_router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    return task_service.delete_task(task_id=task_id)




category_router = APIRouter(prefix='/categories')

@category_router.get('')
async def read_all_categories(cat_service: CategoryService = Depends(get_cat_service)) -> list[Category]:
    return cat_service.list_categories()


@category_router.post('', status_code=status.HTTP_201_CREATED)
async def create_new_category(payload: CreateOrChangeCategory, cat_service: CategoryService = Depends(get_cat_service)) -> Category:
    return cat_service.create_category(payload)


@category_router.patch('/{category_id}')
async def update_cate(category_id: str, payload: CreateOrChangeCategory, cat_service: CategoryService = Depends(get_cat_service)) -> Category:
    return cat_service.update_category(category_id, payload)


@category_router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_category(category_id, cat_service: CategoryService = Depends(get_cat_service)) -> None:
    return cat_service.delete_category(category_id)