

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import UserORM
from app.repositories.task import TaskRepository
from app.schemas.tasks import TaskSchema, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db=db)


    def list_tasks(self, current_user: UserORM) -> list[TaskSchema]:
        tasks_orm = self.task_repository.get_all(current_user.id)
        return [TaskSchema.model_validate(task) for task in tasks_orm]


    def create_task(self, task_create: TaskCreate, current_user: UserORM) -> TaskSchema:
        task = self.task_repository.create(title=task_create.title, user_id=current_user.id)
        self.db.commit()
        return TaskSchema.model_validate(task)


    def update_task(self, task_old_title: str, task_update: TaskUpdate, current_user: UserORM) -> TaskSchema:
        task_for_update = self.task_repository.get_by_name(title=task_old_title, user_id=current_user.id)

        if not task_for_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with title {task_old_title} not found"
            )
        
        if task_old_title == task_update.title:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This task already names {task_update.title}"
            )

        if task_update.title != None:
            task_for_update.title = task_update.title

        if task_update.completed != None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return TaskSchema.model_validate(task_for_update)


    def delete_task(self, task_title: str, current_user: UserORM) -> None:
        task_for_delete = self.task_repository.get_by_name(title=task_title, user_id=current_user.id)

        if not task_for_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with title {task_title} not found"
            )

        self.task_repository.delete(task_for_delete)
        self.db.commit()
        