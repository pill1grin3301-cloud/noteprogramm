
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.tasks import TaskORM


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def exists_by_title(self, title: str) -> bool:
        """Проверяет, существует ли категория с таким именем"""
        return self.db.query(TaskORM).filter(TaskORM.title == title).first() is not None

    def get_all(self) -> list[TaskORM]:
        """Возвращает все задачи"""
        return self.db.scalars(select(TaskORM)).all()
    
    def get_by_id(self, task_id: str) -> TaskORM:
        """Возвращает задачу по айди"""
        return self.db.get(TaskORM, task_id)
    
    def create(self, title: str) -> TaskORM:
        """Создает новую задачу"""
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task
    
    def delete(self, TaskORM) -> None:
        """Удаляет задачу"""
        self.db.delete(TaskORM)
        