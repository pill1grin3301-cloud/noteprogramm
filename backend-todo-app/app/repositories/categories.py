from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categories import CategoryORM



class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db   

    def get_category_by_name(self, name: str) -> CategoryORM | None:
        """Возвращает категорию по имени"""
        return self.db.query(CategoryORM).filter(CategoryORM.name == name).first()

    def exists_by_name(self, name: str) -> bool:
        """Проверяет, существует ли категория с таким именем"""
        return self.db.query(CategoryORM).filter(CategoryORM.name == name).first() is not None


    def get_all(self) -> list[CategoryORM]:
        """Возвращает список всех категорий"""
        return self.db.scalars(select(CategoryORM)).all()
    

    def get_by_id(self, cat_id: str) -> CategoryORM | None:
        """Возвращает категорию по айди, если не найдено - None"""
        return self.db.get(CategoryORM, cat_id)
    

    def create(self, name: str) -> CategoryORM:
        """Создает новую категорию"""
        new_cat_orm = CategoryORM(name=name)
        self.db.add(new_cat_orm)
        return new_cat_orm
    

    def delete(self, CatORM) -> None:
        """Удаляет категорию"""
        self.db.delete(CatORM)
        