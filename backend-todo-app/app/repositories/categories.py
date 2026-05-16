from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categories import CategoryORM



class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_by_id(self, cat_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, cat_id)
    
    def create(self, name: str) -> CategoryORM:
        new_cat_orm = CategoryORM(name=name)
        self.db.add(new_cat_orm)
        return new_cat_orm
    
    def delete(self, CatORM) -> None:
        self.db.delete(CatORM)
        