from sqlalchemy.orm import Session

from app.models.categories import CategoryORM
from app.repositories.categories import CategoryRepository
from app.schemas.categories import Category, CreateOrChangeCategory


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.cat_repository = CategoryRepository(db=db)

    def list_categories(self) -> list[Category]:
        categories_orm = self.cat_repository.get_all()
        return [Category.model_validate(cat) for cat in categories_orm]
    
    def create_category(self, cat_create: CreateOrChangeCategory) -> Category:
        new_cat_orm = self.cat_repository.create(cat_create.name)
        self.db.commit()
        return Category.model_validate(new_cat_orm)
    
    def update_category(self, cat_id: str, cat_update: CreateOrChangeCategory) -> Category:
        cat_for_update = self.cat_repository.get_by_id(cat_id=cat_id)
        cat_for_update.name = cat_update.name
        self.db.commit()
        return Category.model_validate(cat_for_update)
    
    def delete_category(self, cat_id: str) -> None:
        cat_for_del = self.db.get(CategoryORM, cat_id)
        self.cat_repository.delete(cat_for_del)
        self.db.commit()
