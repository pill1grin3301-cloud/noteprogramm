from fastapi import HTTPException, status
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
        if self.cat_repository.exists_by_name(name=cat_create.name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists"
            )
        new_cat_orm = self.cat_repository.create(cat_create.name)
        self.db.commit()
        return Category.model_validate(new_cat_orm)
    

    def update_category(self, cat_id: str, cat_update: CreateOrChangeCategory) -> Category:
        cat_for_update = self.cat_repository.get_by_id(cat_id=cat_id)
        if not cat_for_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with {cat_id} not found"
            )   
        existing_category = self.cat_repository.get_category_by_name(name=cat_update.name)
        if existing_category and existing_category.id != cat_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This category already names {cat_update.name}"
            )      
            
        cat_for_update.name = cat_update.name
        self.db.commit()
        return Category.model_validate(cat_for_update)
    
    
    def delete_category(self, cat_id: str) -> None:
        cat_for_del = self.db.get(CategoryORM, cat_id)
        if not cat_for_del:           
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with {cat_id} not found"
            )
        self.cat_repository.delete(cat_for_del)
        self.db.commit()
