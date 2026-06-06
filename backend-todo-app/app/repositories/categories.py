from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import CategoryORM



class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db   


    def get_category_by_name(self, name: str, user_id: str) -> CategoryORM | None:
        """Возвращает категорию по имени и пользователю"""
        return self.db.query(CategoryORM).filter(
            CategoryORM.name == name, 
            CategoryORM.user_id == user_id
        ).first()


    def exists_by_name(self, name: str, user_id: str) -> bool:
        """Проверяет, существует ли категория с таким именем и пользователь"""
        return self.db.query(CategoryORM).filter(
            CategoryORM.name == name, 
            CategoryORM.user_id == user_id
        ).first() is not None


    def get_all(self, user_id: str) -> list[CategoryORM]:
        """Возвращает список всех категорий пользователя"""
        return self.db.query(CategoryORM).filter(CategoryORM.user_id == user_id).all()
    

    def get_by_id(self, cat_id: str, user_id: str) -> CategoryORM | None:
        """Возвращает категорию пользователя по айди, если не найдено - None"""
        return self.db.query(CategoryORM).filter(
            CategoryORM.id == cat_id, 
            CategoryORM.user_id == user_id
        ).first()
    

    def create(self, name: str, user_id: str) -> CategoryORM:
        """Создает новую категорию"""
        new_cat_orm = CategoryORM(name=name, user_id=user_id)
        self.db.add(new_cat_orm)
        return new_cat_orm
    

    def delete(self, cat: CategoryORM) -> None:
        """Удаляет категорию"""
        self.db.delete(cat)
        