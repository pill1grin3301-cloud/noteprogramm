from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey



class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class CategoryORM(Base):
    __tablename__ = 'categories'
    name: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserORM"] = relationship(back_populates="categories")


class TaskORM(Base):
    __tablename__ = 'tasks'
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserORM"] = relationship(back_populates="tasks")


class UserORM(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    tasks: Mapped[list["TaskORM"]] = relationship(
        "TaskORM",                # какая модель с другой стороны
        back_populates="user",      # имя поля в TaskORM
        cascade="all, delete-orphan" # при удалении пользователя удалить и его задачи
    )
    categories: Mapped[list["CategoryORM"]] = relationship(
        "CategoryORM",
        back_populates="user",
        cascade="all, delete-orphan"
    )