from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import CategoryORM
from app.models import UserORM
from app.repositories.categories import CategoryRepository
from app.schemas.categories import Category, CreateOrChangeCategory


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.cat_repository = CategoryRepository(db=db)


    def list_categories(self, current_user: UserORM) -> list[Category]:
        categories_orm = self.cat_repository.get_all(current_user.id)
        return [Category.model_validate(cat) for cat in categories_orm]
    

    def create_category(self, cat_create: CreateOrChangeCategory, current_user: UserORM) -> Category:
        if self.cat_repository.exists_by_name(name=cat_create.name, user_id=current_user.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category with this name already exists"
            )
        new_cat_orm = self.cat_repository.create(cat_create.name, user_id=current_user.id)
        self.db.commit()
        return Category.model_validate(new_cat_orm)
    

    def update_category(self, cat_name: str, cat_update: CreateOrChangeCategory, current_user: UserORM) -> Category:
        cat_for_update = self.cat_repository.get_category_by_name(cat_name, user_id=current_user.id)
        if not cat_for_update:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {cat_name} not found"
            )   
        if cat_name == cat_update.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"This category already names {cat_update.name}"
            )      
            
        cat_for_update.name = cat_update.name
        self.db.commit()
        return Category.model_validate(cat_for_update)
    
    
    def delete_category(self, cat_name: str, current_user: UserORM) -> None:
        cat_for_del = self.cat_repository.get_category_by_name(name=cat_name, user_id=current_user.id)
        if not cat_for_del:           
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category {cat_name} not found"
            )
        self.cat_repository.delete(cat_for_del)
        self.db.commit()
