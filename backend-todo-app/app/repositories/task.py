
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import TaskORM


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def exists_by_title(self, title: str, user_id: str) -> bool:
        """Проверяет, существует ли задача с таким именем у пользователя"""
        return self.db.query(TaskORM).filter(
            TaskORM.title == title, 
            TaskORM.user_id == user_id
        ).first() is not None


    def get_all(self, user_id: str) -> list[TaskORM]:
        """Возвращает все задачи пользователя"""
        return self.db.query(TaskORM).filter(TaskORM.user_id == user_id).all()
    

    def get_by_id(self, task_id: str, user_id: str) -> TaskORM:
        """Возвращает задачу пользователя по айди"""
        return self.db.query(TaskORM).filter(
            TaskORM.id == task_id, 
            TaskORM.user_id == user_id
        ).first()
    
    
    def get_by_name(self, title: str, user_id: str) -> TaskORM:
        """Возвращает задачу пользователя по имени"""
        return self.db.query(TaskORM).filter(
            TaskORM.user_id == user_id, 
            TaskORM.title == title
        ).first()
    

    def create(self, title: str, user_id: str) -> TaskORM:
        """Создает новую задачу"""
        new_task = TaskORM(title=title, completed=False, user_id=user_id)
        self.db.add(new_task)
        return new_task
    
    def delete(self, TaskORM) -> None:
        """Удаляет задачу"""
        self.db.delete(TaskORM)
        